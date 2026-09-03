"""
Single image testing script for carbon eligibility classification
Test individual images and see prediction + confidence
"""

import torch
import torch.nn.functional as F
import cv2
import numpy as np
from PIL import Image
import argparse
import os
from pathlib import Path

# Import your modules
from models.efficientnet import EfficientNetClassifier
from config import MODEL_CONFIG



# Use the optimal threshold from test results
OPTIMAL_THRESHOLD = 0.2031

def load_model(model_path, device):
    """Load the trained model"""
    print(f"🔧 Loading model from: {model_path}")
    
    # Initialize model architecture
    model = EfficientNetClassifier(
        num_classes=MODEL_CONFIG['num_classes'],
        pretrained=False
    )
    
    # Load trained weights
    try:
        checkpoint = torch.load(model_path, map_location=device)
        
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
            val_acc = checkpoint.get('val_accuracy', 'Unknown')
            print(f"✅ Model loaded successfully (Val Accuracy: {val_acc})")
        else:
            model.load_state_dict(checkpoint)
            print("✅ Model loaded successfully")
            
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None
    
    model.to(device)
    model.eval()
    return model

def preprocess_image(image_path, image_size=128):
    """Preprocess image for model input"""
    try:
        # Load image
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize to model input size
        image = cv2.resize(image, (image_size, image_size))
        
        # Convert to tensor and normalize
        image = image.astype(np.float32) / 255.0
        
        # Apply ImageNet normalization
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        image = (image - mean) / std
        
        # Convert to PyTorch tensor and add batch dimension
        image_tensor = torch.from_numpy(image.transpose(2, 0, 1)).float().unsqueeze(0)
        
        return image_tensor
        
    except Exception as e:
        print(f"❌ Error preprocessing image: {e}")
        return None

def predict_image(model, image_path, device, threshold=OPTIMAL_THRESHOLD):
    """Predict carbon eligibility for a single image"""
    # Preprocess image
    image_tensor = preprocess_image(image_path)
    if image_tensor is None:
        return None, None, None
    
    image_tensor = image_tensor.to(device)
    
    # Make prediction
    model.eval()
    with torch.no_grad():
        # Get raw model output
        outputs = model(image_tensor)
        probabilities = F.softmax(outputs, dim=1)
        
        # Get probabilities for each class
        ineligible_prob = probabilities[0, 0].item()
        eligible_prob = probabilities[0, 1].item()
        
        # Make prediction based on threshold
        predicted_class = 1 if eligible_prob > threshold else 0
        
        # Calculate confidence (probability of predicted class)
        confidence = eligible_prob if predicted_class == 1 else ineligible_prob
        
        return predicted_class, confidence, eligible_prob

def format_prediction_output(image_path, predicted_class, confidence, eligible_prob, threshold):
    """Format and display prediction results"""
    class_name = "🟢 ELIGIBLE" if predicted_class == 1 else "🔴 INELIGIBLE"
    
    print("=" * 60)
    print(f"📁 Image: {Path(image_path).name}")
    print(f"🎯 Prediction: {class_name}")
    print(f"🎲 Confidence: {confidence:.4f} ({confidence*100:.2f}%)")
    print(f"📊 Eligible Probability: {eligible_prob:.4f} ({eligible_prob*100:.2f}%)")
    print(f"📊 Ineligible Probability: {1-eligible_prob:.4f} ({(1-eligible_prob)*100:.2f}%)")
    print(f"⚖️  Threshold Used: {threshold:.4f}")
    
    # Add confidence level interpretation
    if confidence >= 0.95:
        conf_level = "Very High ✅"
        conf_color = "🟢"
    elif confidence >= 0.85:
        conf_level = "High ✅"
        conf_color = "🟡"
    elif confidence >= 0.70:
        conf_level = "Medium ⚠️"
        conf_color = "🟠"
    else:
        conf_level = "Low ⚠️"
        conf_color = "🔴"
    
    print(f"📈 Confidence Level: {conf_color} {conf_level}")
    
    # Add interpretation
    if predicted_class == 1:
        if eligible_prob > 0.8:
            print("💡 Interpretation: Strong eligible candidate")
        elif eligible_prob > 0.5:
            print("💡 Interpretation: Likely eligible, review recommended")
        else:
            print("💡 Interpretation: Borderline case, manual review needed")
    else:
        if eligible_prob < 0.2:
            print("💡 Interpretation: Clearly not eligible")
        elif eligible_prob < 0.4:
            print("💡 Interpretation: Likely not eligible")
        else:
            print("💡 Interpretation: Borderline case, manual review needed")
    
    print("=" * 60)

def test_images_in_folder(model, folder_path, device, threshold=OPTIMAL_THRESHOLD, limit=10):
    """Test multiple images in a folder"""
    folder_path = Path(folder_path)
    
    # Find image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(list(folder_path.glob(f'*{ext}')))
        image_files.extend(list(folder_path.glob(f'*{ext.upper()}')))
    
    if not image_files:
        print(f"❌ No image files found in {folder_path}")
        return
    
    # Limit number of images to test
    if len(image_files) > limit:
        print(f"📊 Found {len(image_files)} images, testing first {limit}")
        image_files = image_files[:limit]
    else:
        print(f"📊 Found {len(image_files)} images, testing all")
    
    results = []
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\n🔍 Testing image {i}/{len(image_files)}")
        
        predicted_class, confidence, eligible_prob = predict_image(model, image_path, device, threshold)
        
        if predicted_class is not None:
            format_prediction_output(image_path, predicted_class, confidence, eligible_prob, threshold)
            results.append({
                'image': image_path.name,
                'prediction': 'eligible' if predicted_class == 1 else 'ineligible',
                'confidence': confidence,
                'eligible_prob': eligible_prob
            })
        else:
            print(f"❌ Failed to process {image_path.name}")
    
    # Summary
    if results:
        print(f"\n📋 SUMMARY OF {len(results)} IMAGES")
        print("=" * 60)
        eligible_count = sum(1 for r in results if r['prediction'] == 'eligible')
        avg_confidence = np.mean([r['confidence'] for r in results])
        
        print(f"🟢 Eligible: {eligible_count}/{len(results)} ({eligible_count/len(results)*100:.1f}%)")
        print(f"🔴 Ineligible: {len(results)-eligible_count}/{len(results)} ({(len(results)-eligible_count)/len(results)*100:.1f}%)")
        print(f"📈 Average Confidence: {avg_confidence:.4f} ({avg_confidence*100:.2f}%)")
        
        # High confidence predictions
        high_conf = sum(1 for r in results if r['confidence'] >= 0.8)
        print(f"✅ High Confidence (≥80%): {high_conf}/{len(results)} ({high_conf/len(results)*100:.1f}%)")

def main():
    parser = argparse.ArgumentParser(description='Test carbon eligibility model on images')
    parser.add_argument('--model', type=str, default='improved_All_nz_regions_model.pth',
                       help='Path to model file')
    parser.add_argument('--image', type=str,
                       help='Path to single image to test')
    parser.add_argument('--folder', type=str,
                       help='Path to folder containing images to test')
    parser.add_argument('--threshold', type=float, default=OPTIMAL_THRESHOLD,
                       help=f'Classification threshold (default: {OPTIMAL_THRESHOLD})')
    parser.add_argument('--limit', type=int, default=10,
                       help='Maximum number of images to test from folder (default: 10)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.image and not args.folder:
        print("❌ Please provide either --image or --folder argument")
        print("Examples:")
        print("  py test_single_image.py --image path/to/image.jpg")
        print("  py test_single_image.py --folder path/to/images/")
        return
    
    # Setup device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🖥️ Using device: {device}")
    
    # Load model
    model = load_model(args.model, device)
    if model is None:
        return
    
    print(f"🎯 Using threshold: {args.threshold:.4f}")
    print(f"💡 Threshold meaning: Images with >{args.threshold*100:.1f}% eligible probability = ELIGIBLE")
    
    # Test single image or folder
    if args.image:
        print(f"\n🔍 Testing single image: {args.image}")
        
        if not os.path.exists(args.image):
            print(f"❌ Image file not found: {args.image}")
            return
        
        predicted_class, confidence, eligible_prob = predict_image(model, args.image, device, args.threshold)
        
        if predicted_class is not None:
            format_prediction_output(args.image, predicted_class, confidence, eligible_prob, args.threshold)
        else:
            print("❌ Failed to process image")
    
    elif args.folder:
        print(f"\n🔍 Testing images in folder: {args.folder}")
        
        if not os.path.exists(args.folder):
            print(f"❌ Folder not found: {args.folder}")
            return
        
        test_images_in_folder(model, args.folder, device, args.threshold, args.limit)

if __name__ == "__main__":
    main()