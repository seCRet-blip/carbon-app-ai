import torch
import torch.nn.functional as F
from models.efficientnet import EfficientNetClassifier
from PIL import Image
from torchvision import transforms
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import math
import time
def test_multi_region_comprehensive():
    """
    Test the unified model on all regions with eligible and ineligible images.
    This is the user's original test script with performance improvements:
    - Torch thread tuning
    - TorchScript compilation
    - Parallel image loading + preprocessing
    - Batched inference
    """
    start_time = time.time()

    print("🧪 COMPREHENSIVE MULTI-REGION MODEL TESTING (All NZ Regions)")
    print("=" * 70)

    # -------------------------
    # Device & performance tuning
    # -------------------------
    torch.set_grad_enabled(False)          # disable autograd globally
    # Tune these based on your CPU; typical starting points: 4 or 8
    torch.set_num_threads(4)
    torch.set_num_interop_threads(1)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Simple transform for PIL images (kept same sizes/norm to preserve model input behavior)
    # Use functional-style transforms for slightly better performance per-image
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Test cases organized by region and class (exact lists preserved)
    test_cases = {
        "Christchurch": {
            "eligible": [
                ("nz_data/christchurch/christchurch_15_32097_20812.jpg", "eligible"),
                ("nz_data/christchurch/christchurch_15_32098_20813.jpg", "eligible"),
                ("nz_data/christchurch/christchurch_15_32095_20811.jpg", "eligible"),
            ],
            "ineligible": [
                ("nz_data/christchurch/christchurch_15_32097_20813.jpg", "ineligible"),
                ("nz_data/christchurch/christchurch_15_32082_20809.jpg", "ineligible"),
                ("nz_data/christchurch/christchurch_15_32078_20809.jpg", "ineligible"),
                ("nz_data/christchurch/christchurch_15_32103_20803.jpg", "ineligible"),
            ]
        },
        "Otago": {
            "eligible": [
                ("nz_data/otago/otago_15_31813_21052.jpg", "eligible"),
                ("nz_data/otago/otago_15_31729_21036.jpg", "eligible"),
                ("nz_data/otago/otago_15_31811_21085.jpg", "eligible"),
                ("nz_data/otago/otago_15_31847_20874.jpg", "eligible"),
                ("nz_data/otago/otago_15_31873_21087.jpg", "eligible"),
            ],
            "ineligible": [
                ("nz_data/otago/otago_15_31812_21079.jpg", "ineligible"),
                ("nz_data/otago/otago_15_31735_21016.jpg", "ineligible"),
                ("nz_data/otago/otago_15_31852_21093.jpg", "ineligible"),
                ("nz_data/otago/otago_15_31772_21056.jpg", "ineligible"),
            ]
        },
        "Canterbury": {
            "eligible": [
                ("nz_data/canterbury/canterbury_15_32092_20813.jpg", "eligible"),
                ("nz_data/canterbury/canterbury_15_31960_20694.jpg", "eligible"),
                ("nz_data/canterbury/canterbury_15_31885_20822.jpg", "eligible"),
                ("nz_data/canterbury/canterbury_15_32136_20844.jpg", "eligible"),
                ("nz_data/canterbury/canterbury_15_32065_20857.jpg", "eligible")
            ],
            "ineligible": [
                ("nz_data/canterbury/canterbury_15_31906_20745.jpg", "ineligible"),
                ("nz_data/canterbury/canterbury_15_31950_20740.jpg", "ineligible"),
                ("nz_data/canterbury/canterbury_15_31919_20900.jpg", "ineligible"),
                ("nz_data/canterbury/canterbury_15_32048_20845.jpg", "ineligible"),
                ("nz_data/canterbury/canterbury_15_32052_20738.jpg", "ineligible")
            ]
        },
        "Northland": {
            "eligible": [
                ("nz_data/northland/northland_15_32179_19838.jpg", "eligible"),
                ("nz_data/northland/northland_15_32270_19905.jpg", "eligible"),
                ("nz_data/northland/northland_15_32223_19884.jpg", "eligible"),
                ("nz_data/northland/northland_15_32261_19840.jpg", "eligible"),
                ("nz_data/northland/northland_15_32208_19784.jpg", "eligible")
            ],
            "ineligible": [
                ("nz_data/northland/northland_15_32205_19746.jpg", "ineligible"),
                ("nz_data/northland/northland_15_32155_19920.jpg", "ineligible"),
                ("nz_data/northland/northland_15_32241_19763.jpg", "ineligible"),
                ("nz_data/northland/northland_15_32245_19808.jpg", "ineligible"),
                ("nz_data/northland/northland_15_32274_19835.jpg", "ineligible")
            ]
        },
        "Bay_of_Plenty": {
            "eligible": [
                ("nz_data/bay_of_plenty/bay_of_plenty_15_32440_20117.jpg", "eligible"),
                ("nz_data/bay_of_plenty/bay_of_plenty_15_32413_20125.jpg", "eligible"),
                ("nz_data/bay_of_plenty/bay_of_plenty_15_32492_20108.jpg", "eligible"),
                ("nz_data/bay_of_plenty/bay_of_plenty_15_32481_20145.jpg", "eligible"),
                ("nz_data/bay_of_plenty/bay_of_plenty_15_32431_20136.jpg", "eligible")
            ],
            "ineligible": [
                ("nz_data/bay_of_plenty/bay_of_plenty_15_32431_20056.jpg", "ineligible"),
                ("nz_data/bay_of_plenty/bay_of_plenty_15_32455_20114.jpg", "ineligible"),
                ("nz_data/bay_of_plenty/bay_of_plenty_15_32403_20160.jpg", "ineligible"),
                ("nz_data/bay_of_plenty/bay_of_plenty_15_32458_20147.jpg", "ineligible"),
                ("nz_data/bay_of_plenty/bay_of_plenty_15_32474_20139.jpg", "ineligible")
            ]
        }
    }

    # -------------------------
    # Load only the single model (user requested)
    # -------------------------
    MODEL_PATH = "./TrainedModels/All_nz_regions_model.pth"
    if not Path(MODEL_PATH).exists():
        print(f"⚠️ Model file not found: {MODEL_PATH}")
        return

    print(f"\n🔬 TESTING SINGLE MODEL: {MODEL_PATH}")
    print("=" * 50)

    try:
        # map to the target device
        checkpoint = torch.load(MODEL_PATH, map_location=device)
        model = EfficientNetClassifier(num_classes=2)

        if 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)

        model = model.to(device)
        model.eval()

        # TorchScript compile for faster CPU inference (safe for typical feed-forward)
        try:
            model = torch.jit.script(model)
            # note: if scripting fails for your model, you can remove the above line.
        except Exception as e:
            # scripting can fail for some dynamic models; keep original model if so
            print(f"⚠️ TorchScript scripting failed, continuing without it: {e}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return

    # -------------------------
    # Helpers for parallel load + batched inference
    # -------------------------
    def load_and_transform(path):
        """Load image and apply transform; returns (path, tensor) or raises."""
        img = Image.open(path).convert('RGB')
        t = transform(img)
        return path, t

    # default batch size - tune this for your CPU/GPU memory
    batch_size = 8

    region_stats = {}

    # Test each region
    for region_name, region_data in test_cases.items():
        print(f"\n📍 REGION: {region_name.upper()}")
        print("-" * 30)

        region_correct = 0
        region_total = 0
        class_stats = {}

        # Test each class in this region
        for class_name, image_list in region_data.items():
            print(f"\n  🏷️ {class_name.upper()} Images:")

            class_correct = 0
            class_total = 0

            # Prepare list of paths that exist
            paths = []
            for image_path, true_label in image_list:
                if not Path(image_path).exists():
                    print(f"    ⚠️ {Path(image_path).name} not found")
                else:
                    paths.append((image_path, true_label))

            # Parallelized loading + transform
            tensors_with_meta = []  # list of tuples (image_path, true_label, tensor)
            if paths:
                with ThreadPoolExecutor(max_workers=4) as ex:
                    # submit tasks
                    futures = [ex.submit(load_and_transform, p) for p, _ in paths]
                    # collect in same order as paths
                    for idx, f in enumerate(futures):
                        try:
                            pth, tensor = f.result()
                            # keep true_label aligned with path (find it)
                            true_label = next(lbl for (pp, lbl) in paths if pp == pth)
                            tensors_with_meta.append((pth, true_label, tensor))
                        except Exception as e:
                            print(f"    ❌ Error loading {paths[idx][0]}: {e}")

            # run inference in batches, preserving print style
            for start in range(0, len(tensors_with_meta), batch_size):
                batch = tensors_with_meta[start:start + batch_size]
                if not batch:
                    continue

                # build input tensor batch
                input_batch = torch.stack([t for (_, _, t) in batch]).to(device)

                with torch.no_grad():
                    outputs = model(input_batch)
                    probs = F.softmax(outputs, dim=1)

                # iterate batch results
                for i, (img_path, true_label, _) in enumerate(batch):
                    prob = probs[i]
                    pred_class = torch.argmax(prob).item()
                    confidence = prob[pred_class].item()
                    pred_label = 'eligible' if pred_class == 1 else 'ineligible'
                    correct = (pred_label == true_label)

                    print(f"    {Path(img_path).name}")
                    print(f"      True: {true_label}, Predicted: {pred_label} ({confidence:.3f}) {'✅' if correct else '❌'}")

                    if correct:
                        class_correct += 1
                        region_correct += 1
                    class_total += 1
                    region_total += 1

            # Class summary
            if class_total > 0:
                class_accuracy = class_correct / class_total * 100
                class_stats[class_name] = (class_correct, class_total, class_accuracy)
                print(f"    📊 {class_name.title()}: {class_correct}/{class_total} ({class_accuracy:.1f}%)")

        # Region summary
        if region_total > 0:
            region_accuracy = region_correct / region_total * 100
            region_stats[region_name] = (region_correct, region_total, region_accuracy, class_stats)
            print(f"\n  📊 {region_name} Total: {region_correct}/{region_total} ({region_accuracy:.1f}%)")

    # Overall model summary
    total_correct = sum(stats[0] for stats in region_stats.values())
    total_tested = sum(stats[1] for stats in region_stats.values())

    print(f"\n📊 OVERALL RESULTS (All NZ Regions):")
    print("=" * 40)

    for region_name, (correct, total, accuracy, class_stats) in region_stats.items():
        print(f"  {region_name}: {correct}/{total} ({accuracy:.1f}%)")
        for class_name, (c_correct, c_total, c_accuracy) in class_stats.items():
            status = "✅" if c_accuracy > 80 else "⚠️" if c_accuracy > 50 else "🔴"
            print(f"    {class_name.title()}: {c_correct}/{c_total} ({c_accuracy:.1f}%) {status}")

    if total_tested > 0:
        overall_accuracy = total_correct / total_tested * 100
        print(f"\n  🎯 OVERALL: {total_correct}/{total_tested} ({overall_accuracy:.1f}%)")

        if overall_accuracy > 80:
            print(f"  ✅ EXCELLENT PERFORMANCE")
        elif overall_accuracy > 60:
            print(f"  🟡 GOOD PERFORMANCE")
        else:
            print(f"  🔴 NEEDS IMPROVEMENT")

    print(f"\n{'='*50}")
    elapsed = time.time() - start_time
    print(f"\n⏱️ Test completed in {elapsed:.2f} seconds.")


if __name__ == "__main__":
    test_multi_region_comprehensive()
