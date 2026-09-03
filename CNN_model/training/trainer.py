"""
Main training loop and model training functions
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import numpy as np
from tqdm import tqdm
from sklearn.metrics import f1_score, roc_auc_score, classification_report, confusion_matrix

from models import EfficientNetClassifier, ResNetClassifier, EnsembleModel
from data import CarbonCreditDatasetAdvanced, SimpleDataset, get_train_transforms, get_val_transforms
from .utils import create_balanced_sampler, calculate_class_weights, mixup_data, mixup_criterion
from .losses import FocalLoss
from config import (
    TRAINING_CONFIG, AUGMENTATION_CONFIG, LOSS_CONFIG, PATHS, DATA_CONFIG,
    MULTI_REGION_DATA_CONFIG, MULTI_REGION_AUGMENTATION_CONFIG, MULTI_REGION_LOSS_CONFIG,
    CLASS_IMBALANCE_CONFIG
)


def train_advanced_model(model_type='efficientnet', use_mixup=True, use_ensemble=False, multi_region=False):
    """
    Train advanced model with state-of-the-art techniques
    
    Args:
        model_type: 'efficientnet', 'resnet', or 'both'
        use_mixup: Use mixup augmentation
        use_ensemble: Train ensemble of models
        multi_region: Use multi-region dataset (Otago + Christchurch)
    """
    # Select configuration based on multi-region flag
    if multi_region:
        print("🌍 MULTI-REGION CNN TRAINING (All NZ Regions)")
        print("Training on images from all regions listed in:")
        print(f"  Train CSV: {MULTI_REGION_DATA_CONFIG['train_csv']}")
        print(f"  Val CSV:   {MULTI_REGION_DATA_CONFIG['val_csv']}")
        print(f"  Test CSV:  {MULTI_REGION_DATA_CONFIG['test_csv']}")
        data_config = MULTI_REGION_DATA_CONFIG
        augmentation_config = MULTI_REGION_AUGMENTATION_CONFIG
        loss_config = MULTI_REGION_LOSS_CONFIG
        model_save_path = PATHS['multi_region_model_save_path']
    else:
        print("🚀 SINGLE REGION CNN TRAINING")
        print("Training on images from:")
        print(f"  Train CSV: {DATA_CONFIG['train_csv']}")
        print(f"  Val CSV:   {DATA_CONFIG['val_csv']}")
        print(f"  Test CSV:  {DATA_CONFIG['test_csv']}")
        data_config = DATA_CONFIG
        augmentation_config = AUGMENTATION_CONFIG
        loss_config = LOSS_CONFIG
        model_save_path = PATHS['model_save_path']
    print("="*60)
    
    # Check for multiple GPUs
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    num_gpus = torch.cuda.device_count()
    
    print(f"Available GPUs: {num_gpus}")
    if num_gpus > 1:
        for i in range(num_gpus):
            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
        print(f"✅ Using DataParallel across {num_gpus} GPUs")
    else:
        print(f"Using device: {device}")
    
    # Load datasets with advanced augmentation
    use_albumentations = True
    try:
        print("✓ Albumentations available - using advanced augmentation")
        train_dataset = CarbonCreditDatasetAdvanced(
            data_config['train_csv'], 
            use_albumentations=True
        )
        val_dataset = CarbonCreditDatasetAdvanced(
            data_config['val_csv'], 
            use_albumentations=False  # No augmentation for validation
        )
        test_dataset = CarbonCreditDatasetAdvanced(
            data_config['test_csv'], 
            use_albumentations=False
        )
    except (ImportError, Exception) as e:
        print(f"⚠️  Albumentations error: {e}")
        print("Using basic PyTorch transforms instead")
        use_albumentations = False
    
    if not use_albumentations:
        # Fallback to basic transforms
        train_transform = get_train_transforms()
        val_transform = get_val_transforms()
        
        train_dataset = SimpleDataset(data_config['train_csv'], train_transform)
        val_dataset = SimpleDataset(data_config['val_csv'], val_transform)
        test_dataset = SimpleDataset(data_config['test_csv'], val_transform)
    
    # Check data balance
    eligible_count = sum(1 for i in range(len(train_dataset)) if train_dataset[i][1].item() == 1)
    print(f"Training: Eligible={eligible_count}, Ineligible={len(train_dataset)-eligible_count}")
    
    # Data loaders with increased workers for multi-GPU
    train_sampler = None
    if CLASS_IMBALANCE_CONFIG['use_balanced_sampling']:
        train_sampler = create_balanced_sampler(train_dataset)
        print("✅ Using balanced sampling for severe class imbalance")
    else:
        print("⚠️ Using standard sampling (no balance correction)")
    
    # Increase batch size and workers for multi-GPU
    batch_size = 32 * max(1, num_gpus)  # Scale batch size with GPU count
    num_workers = 4 * max(1, num_gpus)  # More workers for parallel loading
    
    print(f"Batch size: {batch_size} (scaled for {num_gpus} GPU{'s' if num_gpus > 1 else ''})")
    print(f"Num workers: {num_workers}")
    
    if train_sampler is not None:
        train_loader = DataLoader(train_dataset, batch_size=batch_size, sampler=train_sampler, 
                                 num_workers=num_workers, pin_memory=True)
    else:
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, 
                                 num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, 
                           num_workers=num_workers, pin_memory=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, 
                            num_workers=num_workers, pin_memory=True)
    
    # Initialize model
    if use_ensemble or model_type == 'both':
        models_list = [
            EfficientNetClassifier(pretrained=True),
            ResNetClassifier(pretrained=True)
        ]
        model = EnsembleModel(models_list)
        print("Using Ensemble Model (EfficientNet + ResNet)")
    elif model_type == 'efficientnet':
        model = EfficientNetClassifier(pretrained=True)
        print("Using EfficientNet-B3")
    else:
        model = ResNetClassifier(pretrained=True)
        print("Using ResNet-50")
    
    # Wrap model with DataParallel for multi-GPU
    if num_gpus > 1:
        model = nn.DataParallel(model)
        print(f"✅ Model wrapped with DataParallel for {num_gpus} GPUs")
    
    model = model.to(device)
    
    # Loss function - Configure based on CLASS_IMBALANCE_CONFIG
    class_weights = None
    if CLASS_IMBALANCE_CONFIG['use_class_weights']:
        class_weights = torch.FloatTensor(CLASS_IMBALANCE_CONFIG['class_weights']).to(device)
        print(f"✅ Using class weights: {CLASS_IMBALANCE_CONFIG['class_weights']}")
    
    if CLASS_IMBALANCE_CONFIG['use_focal_loss']:
        criterion = FocalLoss(
            alpha=loss_config['focal_loss_alpha'], 
            gamma=loss_config['focal_loss_gamma'],
            weight=class_weights
        )
        print(f"✅ Using Focal Loss (alpha={loss_config['focal_loss_alpha']}, gamma={loss_config['focal_loss_gamma']})")
    elif class_weights is not None:
        criterion = nn.CrossEntropyLoss(weight=class_weights)
        print("✅ Using weighted CrossEntropyLoss")
    else:
        criterion = nn.CrossEntropyLoss()
        print("⚠️ Using standard CrossEntropyLoss (no imbalance handling)")
    
    # Updated optimizer settings for imbalanced data
    optimizer = optim.AdamW(model.parameters(), 
                           lr=TRAINING_CONFIG['learning_rate'], 
                           weight_decay=TRAINING_CONFIG['weight_decay'])
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, 
                                                   patience=TRAINING_CONFIG['patience']//3)
    
    # Training - Updated for imbalanced data
    num_epochs = TRAINING_CONFIG['num_epochs']
    best_f1 = 0.0
    best_acc = 0.0
    patience = TRAINING_CONFIG['patience']
    patience_counter = 0
    
    print(f"\n🎯 Training Configuration:")
    print(f"   • Use focal loss: {CLASS_IMBALANCE_CONFIG['use_focal_loss']}")
    print(f"   • Use class weights: {CLASS_IMBALANCE_CONFIG['use_class_weights']}")
    print(f"   • Use balanced sampling: {CLASS_IMBALANCE_CONFIG['use_balanced_sampling']}")
    if class_weights is not None:
        print(f"   • Class weights: {class_weights.tolist()}")
    print(f"   • Learning rate: {TRAINING_CONFIG['learning_rate']}")
    print(f"   • Epochs: {num_epochs}, Patience: {patience}")
    print("="*70)
    
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        
        pbar = tqdm(train_loader, desc=f'Epoch {epoch+1}/{num_epochs}')
        for data, target in pbar:
            data, target = data.to(device), target.to(device)
            
            # Apply mixup
            if use_mixup and np.random.random() > 0.5:
                data, target_a, target_b, lam = mixup_data(data, target, alpha=augmentation_config['mixup_alpha'])
                optimizer.zero_grad()
                outputs = model(data)
                loss = mixup_criterion(criterion, outputs, target_a, target_b, lam)
            else:
                optimizer.zero_grad()
                outputs = model(data)
                loss = criterion(outputs, target)
            
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            pbar.set_postfix({'loss': f'{loss.item():.4f}'})
        
        avg_train_loss = running_loss / len(train_loader)
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        y_true_val, y_pred_val, y_scores = [], [], []
        
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(device), target.to(device)
                outputs = model(data)
                val_loss += criterion(outputs, target).item()
                
                probs = torch.softmax(outputs, dim=1)
                _, predicted = torch.max(outputs, 1)
                
                y_true_val.extend(target.cpu().numpy())
                y_pred_val.extend(predicted.cpu().numpy())
                y_scores.extend(probs[:, 1].cpu().numpy())
        
        avg_val_loss = val_loss / len(val_loader)
        
        # Metrics - Enhanced for imbalanced data
        val_acc = np.mean(np.array(y_true_val) == np.array(y_pred_val))
        val_f1 = f1_score(y_true_val, y_pred_val, pos_label=1, zero_division=0)
        val_auc = roc_auc_score(y_true_val, y_scores) if len(np.unique(y_true_val)) > 1 else 0
        
        # Calculate class-specific metrics
        from sklearn.metrics import precision_recall_fscore_support
        precision, recall, _, _ = precision_recall_fscore_support(y_true_val, y_pred_val, pos_label=1, zero_division=0)
        eligible_precision = precision[1] if len(precision) > 1 else 0
        eligible_recall = recall[1] if len(recall) > 1 else 0
        
        print(f'\nEpoch {epoch+1}/{num_epochs}:')
        print(f'  Train Loss: {avg_train_loss:.4f}')
        print(f'  Val Loss: {avg_val_loss:.4f}')
        print(f'  Val Accuracy: {val_acc:.4f}')
        print(f'  Val F1 (Eligible): {val_f1:.4f}')
        print(f'  Val Precision (Eligible): {eligible_precision:.4f}')
        print(f'  Val Recall (Eligible): {eligible_recall:.4f}')
        print(f'  Val AUC: {val_auc:.4f}')
        
        # Use validation F1 for scheduler (more important than accuracy for imbalanced data)
        scheduler.step(val_f1)
        
        # Enhanced early stopping - focus on F1 score for minority class
        # Lower accuracy threshold since we care more about detecting eligible cases
        if val_f1 > best_f1 and val_acc > 0.3:
            best_f1 = val_f1
            best_acc = val_acc
            
            # Save model (handle DataParallel wrapper)
            if num_gpus > 1:
                torch.save(model.module.state_dict(), model_save_path)
            else:
                torch.save(model.state_dict(), model_save_path)
            
            print(f'  ✅ New best model! (Acc: {val_acc:.4f}, F1: {val_f1:.4f})')
            patience_counter = 0
        else:
            patience_counter += 1
        
        # Early stopping
        if patience_counter >= patience:
            print(f"\n⏹️  Early stopping at epoch {epoch+1}")
            break
        
        print('-' * 60)
    
    # Final evaluation
    print("\n📊 FINAL TEST EVALUATION (All NZ Regions):" if multi_region else "\n📊 FINAL TEST EVALUATION (Single Region):")
    print("="*60)
    
    # Load best model (handle DataParallel)
    if num_gpus > 1:
        model.module.load_state_dict(torch.load(model_save_path))
    else:
        model.load_state_dict(torch.load(model_save_path))
    
    model.eval()
    
    y_true, y_pred, y_scores = [], [], []
    
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            outputs = model(data)
            probs = torch.softmax(outputs, dim=1)
            _, predicted = torch.max(outputs, 1)
            
            y_true.extend(target.cpu().numpy())
            y_pred.extend(predicted.cpu().numpy())
            y_scores.extend(probs[:, 1].cpu().numpy())
    
    # Results
    test_acc = np.mean(np.array(y_true) == np.array(y_pred))
    test_f1 = f1_score(y_true, y_pred, pos_label=1, zero_division=0)
    test_auc = roc_auc_score(y_true, y_scores) if len(np.unique(y_true)) > 1 else 0
    
    print(classification_report(y_true, y_pred, target_names=['Ineligible', 'Eligible']))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_true, y_pred))
    
    print(f"\n🎯 FINAL RESULTS:")
    print(f"   Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"   Test F1 Score: {test_f1:.4f}")
    print(f"   Test AUC: {test_auc:.4f}")
    print(f"   Best Val Accuracy: {best_acc:.4f} ({best_acc*100:.2f}%)")
    print(f"   Best Val F1: {best_f1:.4f}")
    
    region_type = "Multi-Region (All NZ Regions)" if multi_region else "Single Region"
    print(f"\n✅ {region_type} model saved as '{model_save_path}'")
    
    return model
