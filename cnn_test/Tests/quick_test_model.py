"""
Quick model testing script without visualization dependencies
Provides essential performance metrics and confidence analysis
"""

import torch
import torch.nn.functional as F
import pandas as pd
import numpy as np
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from pathlib import Path
import argparse
from tqdm import tqdm

# Import your modules
from data.dataset import CarbonCreditDatasetAdvanced
from models.efficientnet import EfficientNetClassifier
from config import DATA_CONFIG, MODEL_CONFIG
import warnings
warnings.filterwarnings('ignore')

def load_model(model_path, device):
    """Load the trained model"""
    print(f"Loading model from: {model_path}")
    
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
            print(f"✅ Loaded model with validation accuracy: {val_acc}")
        else:
            model.load_state_dict(checkpoint)
            print("✅ Loaded model state dict")
            
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None
    
    model.to(device)
    model.eval()
    return model

def calibrate_model_confidence(model, val_loader, device):
    """Find temperature scaling parameter to improve confidence calibration"""
    model.eval()
    
    all_logits = []
    all_labels = []
    
    print("🌡️ Calibrating model confidence...")
    
    with torch.no_grad():
        for images, labels in tqdm(val_loader, desc="Collecting validation data"):
            images, labels = images.to(device), labels.to(device)
            logits = model(images)
            all_logits.append(logits.cpu())
            all_labels.append(labels.cpu())
    
    all_logits = torch.cat(all_logits, 0)
    all_labels = torch.cat(all_labels, 0)
    
    # Find optimal temperature using simple grid search
    best_temperature = 1.0
    best_loss = float('inf')
    
    for temp in np.arange(0.5, 3.0, 0.1):
        scaled_logits = all_logits / temp
        loss = F.cross_entropy(scaled_logits, all_labels)
        
        if loss < best_loss:
            best_loss = loss
            best_temperature = temp
    
    print(f"🌡️ Optimal temperature: {best_temperature:.2f}")
    return best_temperature

class CalibratedModel:
    """Wrapper for temperature-scaled model"""
    def __init__(self, model, temperature=1.0):
        self.model = model
        self.temperature = temperature
    
    def __call__(self, x):
        logits = self.model(x)
        return logits / self.temperature
    
    def eval(self):
        self.model.eval()
    
    def to(self, device):
        self.model.to(device)
        return self

# Optimal threshold from test_model_performance.py results
OPTIMAL_THRESHOLD = 0.2031

def test_model_quick(model, test_loader, device, threshold=OPTIMAL_THRESHOLD):
    """Quick model testing with optimal threshold and confidence analysis"""
    all_predictions = []
    all_labels = []
    all_confidences = []
    all_eligible_probs = []
    
    print(f"\n🔍 Running model predictions with threshold: {threshold:.4f}")
    
    with torch.no_grad():
        for images, labels in tqdm(test_loader, desc="Testing"):
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            probabilities = F.softmax(outputs, dim=1)
            
            # Use optimal threshold instead of max probability
            eligible_probs = probabilities[:, 1]  # Get eligible class probabilities
            predictions = (eligible_probs > threshold).long()
            
            # Calculate confidence based on the predicted class
            confidence_scores = torch.where(
                predictions == 1,
                eligible_probs,  # If predicted eligible, use eligible probability
                1 - eligible_probs  # If predicted ineligible, use ineligible probability
            )
            
            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_confidences.extend(confidence_scores.cpu().numpy())
            all_eligible_probs.extend(eligible_probs.cpu().numpy())
    
    predictions = np.array(all_predictions)
    labels = np.array(all_labels)
    confidences = np.array(all_confidences)
    
    # Calculate basic metrics
    accuracy = np.mean(predictions == labels)
    mean_confidence = np.mean(confidences)
    
    # Confidence analysis
    low_conf_mask = confidences < 0.7
    low_conf_ratio = np.mean(low_conf_mask)
    
    very_low_conf_mask = confidences < 0.6
    very_low_conf_ratio = np.mean(very_low_conf_mask)
    
    print(f"\n📊 QUICK RESULTS SUMMARY")
    print("="*50)
    print(f"Total test samples: {len(predictions)}")
    print(f"Overall accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Mean confidence: {mean_confidence:.4f}")
    print(f"Low confidence (<0.7): {low_conf_ratio:.3f} ({low_conf_ratio*100:.1f}%)")
    print(f"Very low confidence (<0.6): {very_low_conf_ratio:.3f} ({very_low_conf_ratio*100:.1f}%)")
    
    # Show some examples of low confidence predictions
    if np.any(low_conf_mask):
        print(f"\n⚠️ Examples of low confidence predictions:")
        low_conf_indices = np.where(low_conf_mask)[0][:5]  # Show first 5
        for i, idx in enumerate(low_conf_indices):
            actual = 'eligible' if labels[idx] == 1 else 'ineligible'
            predicted = 'eligible' if predictions[idx] == 1 else 'ineligible'
            correct = "✅" if predictions[idx] == labels[idx] else "❌"
            print(f"   {i+1}. Confidence: {confidences[idx]:.3f}, "
                  f"Predicted: {predicted}, Actual: {actual} {correct}")
    
    return accuracy, mean_confidence, low_conf_ratio

def main():
    parser = argparse.ArgumentParser(description='Quick model test')
    parser.add_argument('--model', type=str, default='TrainedModels/All_nz_regions_model.pth',
                       help='Path to model file')
    parser.add_argument('--calibrate', action='store_true', 
                       help='Use confidence calibration')
    
    args = parser.parse_args()
    
    # Setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🖥️ Using device: {device}")
    
    # Load model
    model = load_model(args.model, device)
    if model is None:
        return
    
    # Load test dataset
    try:
        test_dataset = CarbonCreditDatasetAdvanced(
            csv_file='carbon_dataset/all_region_test.csv',
            use_albumentations=False
        )
        
        test_loader = DataLoader(
            test_dataset,
            batch_size=32,
            shuffle=False,
            num_workers=2
        )
        
        print(f"✅ Loaded test dataset: {len(test_dataset)} samples")
        
    except Exception as e:
        print(f"❌ Error loading test dataset: {e}")
        print("Available CSV files:")
        import os
        csv_files = [f for f in os.listdir('carbon_dataset') if f.endswith('.csv')]
        for f in csv_files:
            print(f"   • {f}")
        return
    
    # Optional: Load validation dataset for calibration
    if args.calibrate:
        try:
            val_dataset = CarbonCreditDatasetAdvanced(
                csv_file='carbon_dataset/all_region_val.csv',
                use_albumentations=False
            )
            
            val_loader = DataLoader(
                val_dataset,
                batch_size=32,
                shuffle=False,
                num_workers=2
            )
            
            print(f"✅ Loaded validation dataset for calibration: {len(val_dataset)} samples")
            
            # Calibrate the model
            optimal_temp = calibrate_model_confidence(model, val_loader, device)
            model = CalibratedModel(model, optimal_temp)
            print(f"🌡️ Using calibrated model with temperature: {optimal_temp:.2f}")
            
        except Exception as e:
            print(f"⚠️ Could not load validation data for calibration: {e}")
            print("Proceeding without calibration...")
    
    # Test model with optimal threshold
    accuracy, mean_confidence, low_conf_ratio = test_model_quick(model, test_loader, device, OPTIMAL_THRESHOLD)
    
    # Provide simple recommendations
    print(f"\n💡 RECOMMENDATIONS")
    print("="*50)
    
    if accuracy < 0.80:
        print("🎯 Low accuracy detected. Consider:")
        print("   • More training epochs")
        print("   • Learning rate adjustment")
        print("   • Data augmentation")
    
    if mean_confidence < 0.75:
        print("🎲 Low confidence detected. Consider:")
        print("   • Ensemble methods")
        print("   • Test-time augmentation")
        print("   • Model calibration")
    
    if low_conf_ratio > 0.3:
        print("⚠️  Many uncertain predictions. Consider:")
        print("   • Reviewing training data quality")
        print("   • Adding confidence thresholds")
        print("   • Manual review of low-confidence cases")
    
    if accuracy > 0.85 and mean_confidence > 0.8 and low_conf_ratio < 0.2:
        print("✅ Model performance looks good!")
        print("   Consider fine-tuning for marginal improvements")

if __name__ == "__main__":
    main()