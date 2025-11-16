import os
import math
import requests
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from PIL import Image
import io

# ==============================
# CONFIG
# ==============================
API_KEY = os.getenv("LINZ_API_KEY", "")
OUTPUT_ROOT = "nz_data"
ZOOM = 15

# Compression settings
COMPRESS_IMAGES = True
JPEG_QUALITY = 60  # Lower = smaller files (60 is good quality/size balance)
RESIZE_FACTOR = 0.5  # 0.5 = half size (128x128) - 4x smaller!

# Performance settings
MAX_WORKERS = 10
TIMEOUT = 30
CHUNK_SIZE = 8192

# ==============================
# NEW ZEALAND REGIONS
# ==============================
# Major regions with their bounding boxes (min_lon, min_lat, max_lon, max_lat)
NZ_REGIONS = {
    # North Island - North
    "northland": (173.0, -36.2, 174.8, -34.4),
    "auckland": (174.4, -37.2, 175.2, -36.6),
    "waikato": (174.6, -38.4, 176.0, -37.0),
    "bay_of_plenty": (176.0, -38.3, 177.5, -37.2),
    
    # North Island - Central
    "gisborne": (177.5, -38.8, 178.6, -37.8),
    "hawkes_bay": (176.2, -40.2, 177.3, -38.8),
    "taranaki": (173.5, -39.8, 174.9, -38.6),
    "manawatu_whanganui": (174.5, -40.6, 176.5, -38.8),
    "wellington": (174.6, -41.6, 175.6, -40.8),
    
    # South Island - North
    "tasman": (172.4, -41.9, 173.3, -40.5),
    "nelson": (173.0, -41.5, 173.4, -41.0),
    "marlborough": (173.3, -42.2, 174.5, -40.9),
    
    # South Island - Central
    "west_coast": (169.0, -43.8, 171.8, -41.7),
    "canterbury": (170.0, -44.5, 173.2, -42.5),
    "christchurch": (172.4, -43.7, 172.8, -43.4),  # City detail
    
    # South Island - South
    "otago": (168.5, -46.0, 170.8, -44.0),
    "queenstown": (168.5, -45.2, 169.0, -44.8),  # Tourist area detail
    "southland": (166.0, -46.8, 169.5, -45.5),
    
    # Optional: Entire NZ (WARNING: HUGE - ~500k+ tiles)
    # "full_nz": (166.0, -47.5, 179.0, -34.0),
}

os.makedirs(OUTPUT_ROOT, exist_ok=True)

# ==============================
# SESSION WITH CONNECTION POOLING
# ==============================
def create_session():
    """Create a requests session with retry logic and connection pooling."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=MAX_WORKERS,
        pool_maxsize=MAX_WORKERS * 2
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# ==============================
# HELPERS
# ==============================
def latlon_to_tile(lat, lon, zoom):
    """Convert lat/lon to WMTS tile numbers."""
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return xtile, ytile


def compress_image(image_data, quality=75, resize_factor=1.0):
    """Compress and optionally resize image."""
    try:
        img = Image.open(io.BytesIO(image_data))
        
        # Resize if needed
        if resize_factor != 1.0:
            new_size = (int(img.width * resize_factor), int(img.height * resize_factor))
            img = img.resize(new_size, Image.LANCZOS)
        
        # Compress
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        return output.getvalue()
    except Exception as e:
        # If compression fails, return original
        return image_data


def download_tile(session, z, x, y, save_path):
    """Download a single tile with optional compression."""
    url = f"https://basemaps.linz.govt.nz/v1/tiles/aerial/EPSG:3857/{z}/{x}/{y}.jpg?api={API_KEY}"
    
    try:
        response = session.get(url, stream=True, timeout=TIMEOUT)
        if response.status_code == 200:
            # Download image data
            image_data = b''.join(response.iter_content(CHUNK_SIZE))
            
            # Compress if enabled
            if COMPRESS_IMAGES:
                image_data = compress_image(image_data, JPEG_QUALITY, RESIZE_FACTOR)
            
            # Save
            with open(save_path, "wb") as f:
                f.write(image_data)
            
            return True, None, len(image_data)
        elif response.status_code in (403, 404):
            return False, "not_found", 0
        else:
            return False, f"HTTP_{response.status_code}", 0
    except Exception as e:
        return False, str(e), 0


def download_tile_wrapper(args):
    """Wrapper for parallel execution."""
    session, z, x, y, save_path = args
    
    # Skip if already exists
    if os.path.exists(save_path):
        size = os.path.getsize(save_path)
        return "skipped", x, y, None, size
    
    success, error, size = download_tile(session, z, x, y, save_path)
    
    if success:
        return "success", x, y, None, size
    else:
        return "failed", x, y, error, 0


def download_region(region_name, bbox):
    """Download all tiles for a single region."""
    print(f"\n{'='*60}")
    print(f"📍 REGION: {region_name.upper()}")
    print(f"{'='*60}")
    
    region_dir = os.path.join(OUTPUT_ROOT, region_name)
    os.makedirs(region_dir, exist_ok=True)
    
    min_lon, min_lat, max_lon, max_lat = bbox
    
    # Get tile coordinates
    x_min_tile, y_max_tile = latlon_to_tile(min_lat, min_lon, ZOOM)
    x_max_tile, y_min_tile = latlon_to_tile(max_lat, max_lon, ZOOM)
    
    min_x = min(x_min_tile, x_max_tile)
    max_x = max(x_min_tile, x_max_tile)
    min_y = min(y_min_tile, y_max_tile)
    max_y = max(y_min_tile, y_max_tile)
    
    total_tiles = (max_x - min_x + 1) * (max_y - min_y + 1)
    
    print(f"   Tiles: {total_tiles:,}")
    print(f"   X range: {min_x} to {max_x}")
    print(f"   Y range: {min_y} to {max_y}")
    print(f"   Compression: {'ON' if COMPRESS_IMAGES else 'OFF'} (quality={JPEG_QUALITY})")
    
    # Generate all tile coordinates
    tile_tasks = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            filename = f"{region_name}_{ZOOM}_{x}_{y}.jpg"
            save_path = os.path.join(region_dir, filename)
            tile_tasks.append((ZOOM, x, y, save_path))
    
    # Download with parallel workers
    downloaded = 0
    skipped = 0
    failed = 0
    failed_tiles = []
    total_bytes = 0
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        sessions = [create_session() for _ in range(MAX_WORKERS)]
        
        futures = []
        for i, (z, x, y, save_path) in enumerate(tile_tasks):
            session = sessions[i % MAX_WORKERS]
            future = executor.submit(download_tile_wrapper, (session, z, x, y, save_path))
            futures.append(future)
        
        with tqdm(total=total_tiles, desc=f"{region_name}") as pbar:
            for future in as_completed(futures):
                status, x, y, error, size = future.result()
                
                if status == "success":
                    downloaded += 1
                    total_bytes += size
                elif status == "skipped":
                    skipped += 1
                    total_bytes += size
                elif status == "failed":
                    failed += 1
                    failed_tiles.append((x, y, error))
                
                pbar.update(1)
    
    elapsed = time.time() - start_time
    
    # Save failed tiles log
    if failed_tiles:
        with open(os.path.join(region_dir, "failed.log"), "w") as log:
            for x, y, error in failed_tiles:
                log.write(f"{x},{y},{error}\n")
    
    # Report
    print(f"\n   ✅ Downloaded: {downloaded:,}")
    print(f"   ⏭️  Skipped: {skipped:,}")
    print(f"   ❌ Failed: {failed:,}")
    print(f"   ⏱️  Time: {elapsed/60:.1f} minutes")
    print(f"   💾 Size: {total_bytes/1024**2:.1f} MB ({total_bytes/1024**3:.2f} GB)")
    if downloaded > 0:
        print(f"   📊 Avg tile size: {total_bytes/total_tiles/1024:.1f} KB")
        print(f"   🚀 Speed: {total_tiles/elapsed:.1f} tiles/sec")
    
    return {
        'region': region_name,
        'downloaded': downloaded,
        'skipped': skipped,
        'failed': failed,
        'time': elapsed,
        'bytes': total_bytes
    }


# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    print("🇳🇿 NEW ZEALAND AERIAL IMAGERY DOWNLOADER")
    print("=" * 60)
    print(f"Zoom level: {ZOOM}")
    print(f"Regions: {len(NZ_REGIONS)}")
    print(f"Compression: {'Enabled' if COMPRESS_IMAGES else 'Disabled'}")
    if COMPRESS_IMAGES:
        print(f"  Quality: {JPEG_QUALITY}%")
        print(f"  Resize: {RESIZE_FACTOR}x")
    print(f"Workers: {MAX_WORKERS}")
    print()
    
    # Estimate total tiles
    total_estimate = 0
    for region, bbox in NZ_REGIONS.items():
        min_lon, min_lat, max_lon, max_lat = bbox
        x1, y1 = latlon_to_tile(min_lat, min_lon, ZOOM)
        x2, y2 = latlon_to_tile(max_lat, max_lon, ZOOM)
        tiles = (abs(x2-x1)+1) * (abs(y2-y1)+1)
        total_estimate += tiles
    
    print(f"📊 Estimated total tiles: {total_estimate:,}")
    
    # Better size estimation
    avg_tile_kb = 50  # Uncompressed average
    if COMPRESS_IMAGES:
        # More accurate compression estimation
        quality_factor = JPEG_QUALITY / 100
        resize_factor = RESIZE_FACTOR ** 2  # Area reduction
        avg_tile_kb = avg_tile_kb * quality_factor * resize_factor * 0.7
    
    estimated_gb = total_estimate * avg_tile_kb / 1024 / 1024
    print(f"   Estimated size: {estimated_gb:.1f} GB")
    if COMPRESS_IMAGES:
        print(f"   (Quality: {JPEG_QUALITY}%, Size: {int(256*RESIZE_FACTOR)}x{int(256*RESIZE_FACTOR)}px)")
    print()
    
    input("Press Enter to start downloading...")
    
    # Download all regions
    results = []
    overall_start = time.time()
    
    for region_name, bbox in NZ_REGIONS.items():
        result = download_region(region_name, bbox)
        results.append(result)
    
    overall_elapsed = time.time() - overall_start
    
    # Final summary
    print(f"\n{'='*60}")
    print("🎉 ALL REGIONS COMPLETE")
    print(f"{'='*60}")
    
    total_downloaded = sum(r['downloaded'] for r in results)
    total_skipped = sum(r['skipped'] for r in results)
    total_failed = sum(r['failed'] for r in results)
    total_bytes = sum(r['bytes'] for r in results)
    
    print(f"Total tiles downloaded: {total_downloaded:,}")
    print(f"Total tiles skipped: {total_skipped:,}")
    print(f"Total tiles failed: {total_failed:,}")
    print(f"Total time: {overall_elapsed/3600:.2f} hours")
    print(f"Total size: {total_bytes/1024**3:.2f} GB")
    print(f"\nData saved to: {OUTPUT_ROOT}/")
    
    # Per-region summary
    print(f"\n{'Region':<25} {'Tiles':<10} {'Size (MB)':<12} {'Time (min)':<12}")
    print("-" * 60)
    for r in results:
        print(f"{r['region']:<25} {r['downloaded']:<10,} {r['bytes']/1024**2:<12.1f} {r['time']/60:<12.1f}")