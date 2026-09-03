"""
NZ Carbon Credits - Multi-Region Data Labeling Script
Automatically labels aerial images from multiple NZ regions using government forest data
"""

import os
import math
import geopandas as gpd
import pandas as pd
from pathlib import Path
from shapely.geometry import Point
from sklearn.model_selection import train_test_split

class MultiRegionCarbonLabeler:
    def __init__(self, base_data_dir, output_dir, regions=None):
        """
        Initialize the labeler for multiple regions
        
        Args:
            base_data_dir: Path to nz_data folder containing region subdirectories
            output_dir: Where to save the labeled dataset
            regions: List of region names, or None for all regions
        """
        self.base_data_dir = Path(base_data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'raw_data').mkdir(exist_ok=True)
        
        # Get available regions
        available_regions = [d.name for d in self.base_data_dir.iterdir() if d.is_dir()]
        
        if regions is None:
            self.regions = available_regions
        else:
            self.regions = [r for r in regions if r in available_regions]
            missing = set(regions) - set(available_regions)
            if missing:
                print(f"Warning: Regions not found: {missing}")
        
        print(f"Processing regions: {', '.join(self.regions)}")
        
    def tile_to_latlon(self, x, y, zoom):
        """Convert WMTS tile coordinates to lat/lon (center of tile)"""
        n = 2.0 ** zoom
        lon = x / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
        lat = math.degrees(lat_rad)
        return (lat, lon)
    
    def extract_coordinates_from_filename(self, image_path):
        """
        Extract coordinates from tile filenames
        Format: region_15_29234_40123.jpg → zoom=15, x=29234, y=40123
        """
        filename = Path(image_path).stem
        parts = filename.split('_')
        
        if len(parts) >= 4:
            try:
                region = parts[0]  # Extract region name
                zoom = int(parts[-3])
                tile_x = int(parts[-2])
                tile_y = int(parts[-1])
                lat, lon = self.tile_to_latlon(tile_x, tile_y, zoom)
                return (lat, lon, region)
            except ValueError:
                return None
        return None
    
    def scan_all_regions(self):
        """Scan all images from all regions and extract their coordinates"""
        print("Scanning images from all regions...")
        
        all_image_data = []
        region_counts = {}
        
        for region in self.regions:
            region_dir = self.base_data_dir / region
            if not region_dir.exists():
                print(f"  Warning: {region} directory not found")
                continue
                
            print(f"  Processing {region}...")
            
            # Get all images in this region
            image_files = list(region_dir.glob('*.jpg')) + \
                         list(region_dir.glob('*.jpeg')) + \
                         list(region_dir.glob('*.png'))
            
            region_count = 0
            for img_path in image_files:
                coords = self.extract_coordinates_from_filename(img_path)
                if coords:
                    lat, lon, detected_region = coords
                    all_image_data.append({
                        'filename': img_path.name,
                        'path': str(img_path),
                        'lat': lat,
                        'lon': lon,
                        'region': region,  # Use folder name as primary region
                        'detected_region': detected_region,  # Region from filename
                        'geometry': Point(lon, lat)
                    })
                    region_count += 1
            
            region_counts[region] = region_count
            print(f"    Found {region_count} images with coordinates")
        
        # Summary
        total_images = sum(region_counts.values())
        print(f"\n📊 Region Summary:")
        for region, count in sorted(region_counts.items()):
            print(f"  {region}: {count:,} images")
        print(f"  TOTAL: {total_images:,} images")
        
        if not all_image_data:
            print("ERROR: No coordinates extracted from filenames!")
            print("Expected format: region_zoom_x_y.jpg")
            return None
        
        # Create GeoDataFrame with WGS84 (EPSG:4326)
        gdf = gpd.GeoDataFrame(all_image_data, crs="EPSG:4326")
        
        # Transform to NZGD 2000 (EPSG:2193) to match government data
        gdf = gdf.to_crs("EPSG:2193")
        
        print(f"✓ Extracted coordinates from {len(gdf):,} images")
        print(f"✓ Transformed to EPSG:2193 for spatial matching")
        return gdf
    
    def load_lucas_data(self):
        """Load LUCAS land use data"""
        lucas_path = Path('./raw_data/lucas_land_use.shp')
        
        if not lucas_path.exists():
            print(f"LUCAS data not found at: {lucas_path}")
            return None
        
        print("Loading LUCAS data...")
        gdf = gpd.read_file(lucas_path)
        print(f"  Loaded {len(gdf)} LUCAS polygons")
        return gdf
    
    def load_lcdb_data(self):
        """Load LCDB land cover data"""
        lcdb_path = Path('./raw_data/lcdb.shp')
        
        if not lcdb_path.exists():
            print(f"LCDB data not found at: {lcdb_path}")
            return None
        
        print("Loading LCDB data...")
        gdf = gpd.read_file(lcdb_path)
        print(f"  Loaded {len(gdf)} LCDB polygons")
        return gdf
    
    def label_with_lucas(self, image_gdf, lucas_gdf):
        """Label images using LUCAS data"""
        if lucas_gdf is None:
            return None
        
        print("Labeling with LUCAS...")
        
        # Both should now be in EPSG:2193
        print(f"  Image GDF CRS: {image_gdf.crs}")
        print(f"  LUCAS GDF CRS: {lucas_gdf.crs}")
        
        # Ensure same CRS
        if image_gdf.crs != lucas_gdf.crs:
            lucas_gdf = lucas_gdf.to_crs(image_gdf.crs)
        
        # Spatial join
        joined = gpd.sjoin(image_gdf, lucas_gdf, how='left', predicate='within')
        
        # Look for forest establishment after 1989 for ETS eligibility
        # LUCAS uses START_YYYY columns for establishment years
        if 'START_2020' in joined.columns:
            # Use most recent forest establishment year
            joined['lucas_label'] = joined['START_2020'].apply(
                lambda x: True if pd.notna(x) and x > 1989 else False if pd.notna(x) else None
            )
        elif 'START_2016' in joined.columns:
            joined['lucas_label'] = joined['START_2016'].apply(
                lambda x: True if pd.notna(x) and x > 1989 else False if pd.notna(x) else None
            )
        else:
            # No establishment year data available
            joined['lucas_label'] = None
        
        matched = joined['lucas_label'].notna().sum()
        eligible = joined['lucas_label'].sum() if matched > 0 else 0
        print(f"  Spatially matched: {matched:,} images")
        print(f"  Eligible for carbon credits: {eligible:,} images")
        
        # Show breakdown by region
        if 'region' in joined.columns:
            region_breakdown = joined.groupby('region')['lucas_label'].agg(['count', 'sum']).fillna(0)
            print("  By region:")
            for region, stats in region_breakdown.iterrows():
                print(f"    {region}: {int(stats['sum'])}/{int(stats['count'])} eligible")
        
        return joined['lucas_label']
    
    def label_with_lcdb(self, image_gdf, lcdb_gdf):
        """Label images using LCDB data"""
        if lcdb_gdf is None:
            return None
        
        print("Labeling with LCDB...")
        
        # Both should now be in EPSG:2193
        print(f"  Image GDF CRS: {image_gdf.crs}")
        print(f"  LCDB GDF CRS: {lcdb_gdf.crs}")
        
        if image_gdf.crs != lcdb_gdf.crs:
            lcdb_gdf = lcdb_gdf.to_crs(image_gdf.crs)
        
        joined = gpd.sjoin(image_gdf, lcdb_gdf, how='left', predicate='within')
        
        # Check for forest that's eligible for ETS (post-1989 forest)
        forest_classes = ['Exotic Forest', 'Forest - Harvested', 'Indigenous Forest']
        
        if 'Name_2018' in joined.columns:
            # Current forest coverage (2018)
            is_forest_now = joined['Name_2018'].isin(forest_classes)
            
            # Check if it wasn't forest in 1996 (closest to 1989)
            if 'Name_1996' in joined.columns:
                was_not_forest_1996 = ~joined['Name_1996'].isin(forest_classes)
                # Eligible if it's forest now but wasn't forest in 1996
                joined['lcdb_label'] = is_forest_now & was_not_forest_1996
            else:
                # Fallback: assume all current forest might be eligible
                joined['lcdb_label'] = is_forest_now
        else:
            joined['lcdb_label'] = None
        
        matched = joined['lcdb_label'].notna().sum()
        eligible = joined['lcdb_label'].sum() if matched > 0 else 0
        print(f"  Spatially matched: {matched} images")
        print(f"  Eligible for carbon credits: {eligible} images")
        return joined['lcdb_label']
    
    def combine_labels(self, image_gdf, lucas_labels, lcdb_labels):
        """Combine labels from multiple sources using voting"""
        print("\nCombining labels...")
        
        image_gdf['lucas'] = lucas_labels
        image_gdf['lcdb'] = lcdb_labels
        
        def vote(row):
            votes = []
            if pd.notna(row['lucas']):
                votes.append(row['lucas'])
            if pd.notna(row['lcdb']):
                votes.append(row['lcdb'])
            
            if not votes:
                return 'uncertain', 0.0
            
            true_count = sum(votes)
            total = len(votes)
            
            if true_count > total / 2:
                return 'eligible', true_count / total
            elif true_count < total / 2:
                return 'ineligible', (total - true_count) / total
            else:
                return 'uncertain', 0.5
        
        image_gdf[['label', 'confidence']] = image_gdf.apply(
            vote, axis=1, result_type='expand'
        )
        
        return image_gdf
    
    def save_labels(self, labeled_gdf):
        """Save labels to CSV"""
        output = labeled_gdf[['filename', 'path', 'region', 'lat', 'lon', 'label', 'confidence']].copy()
        output_path = self.output_dir / 'labels.csv'
        output.to_csv(output_path, index=False)
        
        print("\n" + "="*60)
        print("LABELING COMPLETE")
        print("="*60)
        print(f"Total images: {len(output)}")
        print(f"Eligible: {len(output[output['label']=='eligible'])} ({len(output[output['label']=='eligible'])/len(output)*100:.1f}%)")
        print(f"Ineligible: {len(output[output['label']=='ineligible'])} ({len(output[output['label']=='ineligible'])/len(output)*100:.1f}%)")
        print(f"Uncertain: {len(output[output['label']=='uncertain'])} ({len(output[output['label']=='uncertain'])/len(output)*100:.1f}%)")
        print(f"\nAverage confidence: {output['confidence'].mean():.2f}")
        print(f"\nSaved to: {output_path}")
        
        return output_path
    
    def create_train_val_test_splits(self, labeled_gdf):
        """Create train/val/test splits"""
        print("\nCreating train/val/test splits...")
        
        # Use high confidence samples
        high_conf = labeled_gdf[labeled_gdf['confidence'] > 0.5].copy()
        
        # Remove uncertain labels
        high_conf = high_conf[high_conf['label'] != 'uncertain']
        
        if len(high_conf) == 0:
            print("ERROR: No high-confidence labels to split!")
            return
        
        # Train/temp split
        train_df, temp_df = train_test_split(
            high_conf,
            train_size=0.7,
            stratify=high_conf['label'],
            random_state=42
        )
        
        # Val/test split
        val_df, test_df = train_test_split(
            temp_df,
            train_size=0.5,
            stratify=temp_df['label'],
            random_state=42
        )
        
        # Save with region information
        train_df[['filename', 'path', 'region', 'label']].to_csv(self.output_dir / 'all_region_train.csv', index=False)
        val_df[['filename', 'path', 'region', 'label']].to_csv(self.output_dir / 'all_region_val.csv', index=False)
        test_df[['filename', 'path', 'region', 'label']].to_csv(self.output_dir / 'all_region_test.csv', index=False)
        
        print(f"  Train: {len(train_df)} images")
        print(f"  Val: {len(val_df)} images")
        print(f"  Test: {len(test_df)} images")
    
    def run(self):
        """Main execution"""
        print("="*60)
        print("NZ CARBON CREDITS - AUTO LABELING")
        print("="*60)
        
        # Step 1: Scan images
        image_gdf = self.scan_all_regions()
        if image_gdf is None:
            return False
        
        # Step 2: Load government data
        lucas_gdf = self.load_lucas_data()
        lcdb_gdf = self.load_lcdb_data()
        
        if lucas_gdf is None and lcdb_gdf is None:
            print("\nERROR: No government data found!")
            print("Download LUCAS or LCDB data to: " + str(self.output_dir / 'raw_data'))
            return False
        
        # Step 3: Label images
        lucas_labels = self.label_with_lucas(image_gdf, lucas_gdf)
        lcdb_labels = self.label_with_lcdb(image_gdf, lcdb_gdf)
        
        # Step 4: Combine labels
        labeled_gdf = self.combine_labels(image_gdf, lucas_labels, lcdb_labels)

                # --- BALANCE DATASET ---
        # Only keep high-confidence eligible samples and randomly undersample ineligible
        eligible_df = labeled_gdf[(labeled_gdf['label'] == 'eligible') & (labeled_gdf['confidence'] > 0.5)]
        ineligible_df = labeled_gdf[(labeled_gdf['label'] == 'ineligible') & (labeled_gdf['confidence'] > 0.5)]

        # Set desired ratio (e.g., 1 eligible : 5 ineligible)
        target_ratio = 5
        n_eligible = len(eligible_df)
        n_ineligible = min(len(ineligible_df), n_eligible * target_ratio)
        ineligible_df = ineligible_df.sample(n=n_ineligible, random_state=42)

        balanced_gdf = pd.concat([eligible_df, ineligible_df]).sample(frac=1, random_state=42)

        print(f"\nBalanced dataset: {len(eligible_df)} eligible, {len(ineligible_df)} ineligible (ratio 1:{target_ratio})")

        # Step 5: Save results
        self.save_labels(balanced_gdf)
        self.create_train_val_test_splits(balanced_gdf)
        
        print("\n✓ Ready for model training!")
        return True


def print_download_instructions():
    """Show where to download required data"""
    print("\n" + "="*60)
    print("DOWNLOAD GOVERNMENT DATA")
    print("="*60)
    
    print("\n1. LUCAS Land Use Map (RECOMMENDED)")
    print("   URL: https://data.mfe.govt.nz/")
    print("   Search: 'LUCAS NZ Land Use'")
    print("   Download: Shapefile format")
    print("   Save as: carbon_dataset/raw_data/lucas_land_use.shp")
    
    print("\n2. LCDB (Land Cover Database)")
    print("   URL: https://lris.scinfo.org.nz/")
    print("   Search: 'LCDB v5'")
    print("   Download: Shapefile format")
    print("   Save as: carbon_dataset/raw_data/lcdb.shp")
    
    print("\n" + "="*60)
    print("After downloading, run this script again")
    print("="*60)


if __name__ == "__main__":
    # Configuration for multi-region processing
    IMAGE_DIR = "./nz_data"  # Updated to use the new multi-region structure
    OUTPUT_DIR = "./carbon_dataset"  # Output location
    
    # Check if government data exists
    data_exists = (
        Path('./raw_data/lucas_land_use.shp')
    ).exists() or (
        Path('./raw_data/lcdb.shp')
    ).exists()
    
    if not data_exists:
        print_download_instructions()
        print("\nNo government data found. Please download first.")
    else:
        # Run the multi-region labeling
        labeler = MultiRegionCarbonLabeler(IMAGE_DIR, OUTPUT_DIR)
        labeler.run()