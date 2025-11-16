import torch
import torch.nn.functional as F
from models.efficientnet import EfficientNetClassifier
from PIL import Image
from torchvision import transforms
from pathlib import Path
import time
def test_multi_region_comprehensive():
    """
    Test the unified model on all regions with eligible and ineligible images
    """
    start_time = time.time() 
    print("🧪 COMPREHENSIVE MODEL TESTING (All NZ Regions - Single Model)")
    print("=" * 70)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Simple transform for PIL images
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    # Test cases for multiple regions
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

    # ✅ Load only one model
    if not Path(MODEL_PATH).exists():
        print(f"⚠️ Model file not found: {MODEL_PATH}")
        return
        
    print(f"\n🔬 TESTING SINGLE MODEL: {MODEL_PATH}")
    print("=" * 50)
    
    try:
        checkpoint = torch.load(MODEL_PATH, map_location=device)
        model = EfficientNetClassifier(num_classes=2)
        
        if 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
            
        model = model.to(device)
        model.eval()
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    region_stats = {}
    
    for region_name, region_data in test_cases.items():
        print(f"\n📍 REGION: {region_name.upper()}")
        print("-" * 30)
        
        region_correct = 0
        region_total = 0
        class_stats = {}
        
        for class_name, image_list in region_data.items():
            print(f"\n  🏷️ {class_name.upper()} Images:")
            class_correct = 0
            class_total = 0
            
            for image_path, true_label in image_list:
                if not Path(image_path).exists():
                    print(f"    ⚠️ {Path(image_path).name} not found")
                    continue
                    
                try:
                    image = Image.open(image_path).convert('RGB')
                    input_tensor = transform(image).unsqueeze(0).to(device)
                    
                    with torch.no_grad():
                        outputs = model(input_tensor)
                        probabilities = F.softmax(outputs, dim=1)[0]
                        
                        pred_class = torch.argmax(probabilities).item()
                        confidence = probabilities[pred_class].item()
                        pred_label = 'eligible' if pred_class == 1 else 'ineligible'
                        
                        correct = (pred_label == true_label)
                        
                        print(f"    {Path(image_path).name}")
                        print(f"      True: {true_label}, Predicted: {pred_label} ({confidence:.3f}) {'✅' if correct else '❌'}")
                        
                        if correct:
                            class_correct += 1
                            region_correct += 1
                        class_total += 1
                        region_total += 1
                            
                except Exception as e:
                    print(f"    ❌ Error testing {Path(image_path).name}: {e}")
            
            if class_total > 0:
                class_accuracy = class_correct / class_total * 100
                class_stats[class_name] = (class_correct, class_total, class_accuracy)
                print(f"    📊 {class_name.title()}: {class_correct}/{class_total} ({class_accuracy:.1f}%)")
        
        if region_total > 0:
            region_accuracy = region_correct / region_total * 100
            region_stats[region_name] = (region_correct, region_total, region_accuracy, class_stats)
            print(f"\n  📊 {region_name} Total: {region_correct}/{region_total} ({region_accuracy:.1f}%)")
    
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
    elapsed= time.time() - start_time
    print(f"\n⏱️ Test completed in {elapsed:.2f} seconds.")
if __name__ == "__main__":
    MODEL_PATH = "All_nz_regions_model.pth"
    test_multi_region_comprehensive()
