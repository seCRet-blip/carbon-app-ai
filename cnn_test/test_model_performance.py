"""
Comprehensive model testing script for carbon eligibility classification
Tests model performance and provides detailed metrics and confidence analysis
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
from config import DATA_CONFIG, MULTI_REGION_DATA_CONFIG, MODEL_CONFIG
import warnings
warnings.filterwarnings('ignore')

def load_model(model_path, device):
    """Load the trained model"""
    print(f"Loading model from: {model_path}")
    
    # Initialize model architecture
    model = EfficientNetClassifier(
        num_classes=MODEL_CONFIG['num_classes'],
        pretrained=False  # Don't load pretrained weights since we're loading our trained model
    )
    
    # Load trained weights
    try:
        checkpoint = torch.load(model_path, map_location=device)
        
        # Handle different checkpoint formats
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
            print(f"✅ Loaded model with validation accuracy: {checkpoint.get('val_accuracy', 'Unknown'):.4f}")
        else:
            model.load_state_dict(checkpoint)
            print("✅ Loaded model state dict directly")
            
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None
    
    model.to(device)
    model.eval()
    return model

def analyze_predictions(model, test_loader, device, class_names=['ineligible', 'eligible']):
    """Get predictions and confidence scores"""
    all_predictions = []
    all_labels = []
    all_probabilities = []
    all_confidences = []
    
    print("\n🔍 Running model predictions...")
    
    with torch.no_grad():
        for batch_idx, (images, labels) in enumerate(tqdm(test_loader, desc="Testing")):
            images, labels = images.to(device), labels.to(device)
            
            # Get model outputs
            outputs = model(images)
            probabilities = F.softmax(outputs, dim=1)
            
            # Get predictions and confidence scores
            confidence_scores, predictions = torch.max(probabilities, 1)
            
            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_probabilities.extend(probabilities.cpu().numpy())
            all_confidences.extend(confidence_scores.cpu().numpy())
    
    return np.array(all_predictions), np.array(all_labels), np.array(all_probabilities), np.array(all_confidences)

def calculate_detailed_metrics(predictions, labels, probabilities, confidences, class_names=['ineligible', 'eligible']):
    """Calculate comprehensive performance metrics"""
    print("\n📊 DETAILED PERFORMANCE ANALYSIS")
    print("="*60)
    
    # Basic accuracy
    accuracy = np.mean(predictions == labels)
    print(f"Overall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Classification report
    print("\n📈 Classification Report:")
    print(classification_report(labels, predictions, target_names=class_names, digits=4))
    
    # Confusion Matrix
    cm = confusion_matrix(labels, predictions)
    print("\n🎯 Confusion Matrix:")
    print("                Predicted")
    print("              Inelig  Elig")
    print(f"Actual Inelig    {cm[0,0]:4d}  {cm[0,1]:4d}")
    print(f"       Elig      {cm[1,0]:4d}  {cm[1,1]:4d}")
    
    # ROC AUC
    try:
        eligible_probs = probabilities[:, 1]  # Probability of being eligible
        roc_auc = roc_auc_score(labels, eligible_probs)
        print(f"\n🎯 ROC AUC Score: {roc_auc:.4f}")
    except Exception as e:
        print(f"\n❌ Could not calculate ROC AUC: {e}")
        roc_auc = None
    
    return accuracy, cm, roc_auc

def analyze_confidence_distribution(confidences, predictions, labels, class_names=['ineligible', 'eligible']):
    """Analyze confidence score distribution"""
    print("\n🎲 CONFIDENCE ANALYSIS")
    print("="*60)
    
    # Overall confidence stats
    mean_conf = np.mean(confidences)
    median_conf = np.median(confidences)
    std_conf = np.std(confidences)
    
    print(f"Mean Confidence: {mean_conf:.4f}")
    print(f"Median Confidence: {median_conf:.4f}")
    print(f"Std Confidence: {std_conf:.4f}")
    
    # Confidence by correctness
    correct_mask = predictions == labels
    incorrect_mask = ~correct_mask
    
    if np.any(correct_mask):
        correct_conf = confidences[correct_mask]
        print(f"\n✅ Correct Predictions:")
        print(f"   Mean Confidence: {np.mean(correct_conf):.4f}")
        print(f"   Count: {len(correct_conf)}")
    
    if np.any(incorrect_mask):
        incorrect_conf = confidences[incorrect_mask]
        print(f"\n❌ Incorrect Predictions:")
        print(f"   Mean Confidence: {np.mean(incorrect_conf):.4f}")
        print(f"   Count: {len(incorrect_conf)}")
    
    # Low confidence predictions (< 0.7)
    low_conf_mask = confidences < 0.7
    low_conf_count = np.sum(low_conf_mask)
    total_count = len(confidences)
    
    print(f"\n⚠️  Low Confidence Predictions (< 0.7):")
    print(f"   Count: {low_conf_count}/{total_count} ({low_conf_count/total_count*100:.1f}%)")
    
    if low_conf_count > 0:
        low_conf_accuracy = np.mean(predictions[low_conf_mask] == labels[low_conf_mask])
        print(f"   Accuracy of low confidence: {low_conf_accuracy:.4f}")
    
    # Very low confidence predictions (< 0.5)
    very_low_conf_mask = confidences < 0.5
    very_low_conf_count = np.sum(very_low_conf_mask)
    
    print(f"\n🚨 Very Low Confidence Predictions (< 0.5):")
    print(f"   Count: {very_low_conf_count}/{total_count} ({very_low_conf_count/total_count*100:.1f}%)")
    
    return {
        'mean_confidence': mean_conf,
        'median_confidence': median_conf,
        'low_confidence_ratio': low_conf_count / total_count,
        'very_low_confidence_count': very_low_conf_count
    }

def confidence_by_class(confidences, predictions, labels, class_names=['ineligible', 'eligible']):
    """Analyze confidence by predicted class"""
    print("\n🏷️  CONFIDENCE BY CLASS")
    print("="*60)
    
    for class_idx, class_name in enumerate(class_names):
        class_mask = predictions == class_idx
        if np.any(class_mask):
            class_confidences = confidences[class_mask]
            class_labels = labels[class_mask]
            class_predictions = predictions[class_mask]
            
            # Accuracy for this predicted class
            class_accuracy = np.mean(class_predictions == class_labels)
            
            print(f"\n{class_name.upper()} Predictions:")
            print(f"   Count: {np.sum(class_mask)}")
            print(f"   Mean Confidence: {np.mean(class_confidences):.4f}")
            print(f"   Min Confidence: {np.min(class_confidences):.4f}")
            print(f"   Max Confidence: {np.max(class_confidences):.4f}")
            print(f"   Accuracy: {class_accuracy:.4f}")

def print_detailed_analysis(confidences, predictions, labels, probabilities):
    """Print detailed text-based analysis without plots"""
    print("\n📈 DETAILED ANALYSIS")
    print("="*60)
    
    # Confidence distribution stats
    print(f"Confidence Distribution:")
    print(f"   Min: {np.min(confidences):.4f}")
    print(f"   Max: {np.max(confidences):.4f}")
    print(f"   Mean: {np.mean(confidences):.4f}")
    print(f"   Median: {np.median(confidences):.4f}")
    print(f"   Std: {np.std(confidences):.4f}")
    
    # Confidence buckets
    high_conf = np.sum(confidences >= 0.8)
    med_conf = np.sum((confidences >= 0.6) & (confidences < 0.8))
    low_conf = np.sum(confidences < 0.6)
    total = len(confidences)
    
    print(f"\nConfidence Buckets:")
    print(f"   High (≥0.8): {high_conf}/{total} ({high_conf/total*100:.1f}%)")
    print(f"   Medium (0.6-0.8): {med_conf}/{total} ({med_conf/total*100:.1f}%)")
    print(f"   Low (<0.6): {low_conf}/{total} ({low_conf/total*100:.1f}%)")
    
    # Correctness analysis
    correct_mask = predictions == labels
    correct_conf = confidences[correct_mask]
    incorrect_conf = confidences[~correct_mask]
    
    if len(correct_conf) > 0 and len(incorrect_conf) > 0:
        print(f"\nCorrectness vs Confidence:")
        print(f"   Correct predictions confidence: {np.mean(correct_conf):.4f} ± {np.std(correct_conf):.4f}")
        print(f"   Incorrect predictions confidence: {np.mean(incorrect_conf):.4f} ± {np.std(incorrect_conf):.4f}")
    
    # ROC AUC calculation
    if probabilities.shape[1] == 2:
        from sklearn.metrics import roc_curve, auc
        fpr, tpr, thresholds = roc_curve(labels, probabilities[:, 1])
        roc_auc = auc(fpr, tpr)
        print(f"\nROC Analysis:")
        print(f"   AUC Score: {roc_auc:.4f}")
        
        # Find optimal threshold
        optimal_idx = np.argmax(tpr - fpr)
        optimal_threshold = thresholds[optimal_idx]
        print(f"   Optimal Threshold: {optimal_threshold:.4f}")
        print(f"   TPR at optimal: {tpr[optimal_idx]:.4f}")
        print(f"   FPR at optimal: {fpr[optimal_idx]:.4f}")

def suggest_improvements(confidence_stats, accuracy, low_conf_ratio):
    """Suggest specific improvements based on test results"""
    print("\n💡 IMPROVEMENT SUGGESTIONS")
    print("="*60)
    
    suggestions = []
    
    if accuracy < 0.85:
        suggestions.append("🎯 Low overall accuracy - Consider:")
        suggestions.append("   • More training epochs")
        suggestions.append("   • Learning rate scheduling")
        suggestions.append("   • Different model architecture")
        suggestions.append("   • More training data")
    
    if confidence_stats['mean_confidence'] < 0.8:
        suggestions.append("\n🎲 Low average confidence - Consider:")
        suggestions.append("   • Temperature scaling for calibration")
        suggestions.append("   • Ensemble methods")
        suggestions.append("   • Label smoothing during training")
        suggestions.append("   • Dropout tuning")
    
    if low_conf_ratio > 0.3:
        suggestions.append("\n⚠️  Many low-confidence predictions - Consider:")
        suggestions.append("   • Test-time augmentation")
        suggestions.append("   • Model ensembling")
        suggestions.append("   • Confidence thresholding")
    
    if confidence_stats['very_low_confidence_count'] > 0:
        suggestions.append("\n🚨 Very low confidence predictions detected:")
        suggestions.append("   • Review these samples manually")
        suggestions.append("   • Consider removing ambiguous training data")
        suggestions.append("   • Implement uncertainty quantification")
    
    if not suggestions:
        suggestions.append("✅ Model performance looks good!")
        suggestions.append("   Consider fine-tuning for marginal improvements")
    
    for suggestion in suggestions:
        print(suggestion)

def main():
    parser = argparse.ArgumentParser(description='Test model performance')
    parser.add_argument('--model', type=str, default='TrainedModels/All_nz_regions_model.pth',
                       help='Path to model file')
    parser.add_argument('--dataset', type=str, default='all_region',
                       choices=['all_region', 'multi_region', 'single_region'],
                       help='Which test dataset to use')
    parser.add_argument('--batch_size', type=int, default=32,
                       help='Batch size for testing')
    parser.add_argument('--detailed', action='store_true',
                       help='Show detailed analysis')
    
    args = parser.parse_args()
    
    # Setup device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🖥️  Using device: {device}")
    
    # Load model
    model = load_model(args.model, device)
    if model is None:
        return
    
    # Setup dataset
    if args.dataset == 'all_region':
        config = DATA_CONFIG
        test_csv = 'carbon_dataset/all_region_test.csv'
    elif args.dataset == 'multi_region':
        config = MULTI_REGION_DATA_CONFIG
        test_csv = 'carbon_dataset/multi_region_test.csv'
    else:
        config = DATA_CONFIG
        test_csv = 'carbon_dataset/test.csv'
    
    print(f"📊 Testing on: {test_csv}")
    
    # Create test dataset and loader
    try:
        test_dataset = CarbonCreditDatasetAdvanced(
            csv_file=test_csv,
            use_albumentations=False  # No augmentation for testing
        )
        
        test_loader = DataLoader(
            test_dataset,
            batch_size=args.batch_size,
            shuffle=False,
            num_workers=2
        )
        
        print(f"✅ Loaded test dataset: {len(test_dataset)} samples")
        
    except Exception as e:
        print(f"❌ Error loading test dataset: {e}")
        return
    
    # Run predictions
    predictions, labels, probabilities, confidences = analyze_predictions(model, test_loader, device)
    
    # Calculate metrics
    accuracy, cm, roc_auc = calculate_detailed_metrics(predictions, labels, probabilities, confidences)
    
    # Analyze confidence
    confidence_stats = analyze_confidence_distribution(confidences, predictions, labels)
    confidence_by_class(confidences, predictions, labels)
    
    # Print detailed analysis
    print_detailed_analysis(confidences, predictions, labels, probabilities)
    
    # Provide improvement suggestions
    suggest_improvements(confidence_stats, accuracy, confidence_stats['low_confidence_ratio'])
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 SUMMARY")
    print(f"{'='*60}")
    print(f"Model: {args.model}")
    print(f"Test Dataset: {test_csv}")
    print(f"Test Samples: {len(predictions)}")
    print(f"Overall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Mean Confidence: {confidence_stats['mean_confidence']:.4f}")
    print(f"Low Confidence Ratio: {confidence_stats['low_confidence_ratio']:.3f}")
    if roc_auc:
        print(f"ROC AUC: {roc_auc:.4f}")

if __name__ == "__main__":
    main()