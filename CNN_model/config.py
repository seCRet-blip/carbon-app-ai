"""
Configuration settings for the CNN training pipeline
"""
CLASS_WEIGHTS = {
    0: 1.0,          # ineligible
    1: 121.5         # eligible (inverse of ratio)
}

# Focal Loss parameters for handling imbalance
FOCAL_LOSS_ALPHA = 0.25
FOCAL_LOSS_GAMMA = 2.0

TARGET_RATIO = 10  # aim for 1:10 instead of 1:121
# Model Configuration
MODEL_CONFIG = {
    'num_classes': 2,
    'pretrained': True,
    'dropout_rates': [0.4, 0.3, 0.2],  # Different dropout rates for layers
}

# Class Imbalance Configuration
CLASS_IMBALANCE_CONFIG = {
    'use_class_weights': True,
    'class_weights': [1.0, 5.0],  # [ineligible, eligible] - based on your ratio
    'use_balanced_sampling': True,
    'use_focal_loss': False,
}

# Training Configuration
TRAINING_CONFIG = {
    'num_epochs': 100,         # More epochs for imbalanced data
    'batch_size': 32,
    'learning_rate': 0.0001,   # Higher learning rate
    'weight_decay': 5e-4,      # Reduced weight decay
    'patience': 15,            # More patience for early stopping
    'num_workers': 4,
    'use_balanced_metrics': True,  # Focus on F1 score instead of accuracy
}

# Data Configuration
DATA_CONFIG = {
    'train_csv': 'carbon_dataset/all_region_train.csv',
    'val_csv': 'carbon_dataset/all_region_val.csv',
    'test_csv': 'carbon_dataset/all_region_test.csv',
    'image_size': 128,
    'use_albumentations': True,
}

# Multi-Region Data Configuration
MULTI_REGION_DATA_CONFIG = {
    'train_csv': 'carbon_dataset/all_region_train.csv',
    'val_csv': 'carbon_dataset/all_region_val.csv',
    'test_csv': 'carbon_dataset/all_region_test.csv',
    'image_size': 128,
    'use_albumentations': True,
}

# Augmentation Configuration
AUGMENTATION_CONFIG = {
    'use_mixup': True,
    'mixup_alpha': 0.4,        # Stronger mixing for imbalanced data
    'horizontal_flip_prob': 0.8,
    'vertical_flip_prob': 0.3, # Add vertical flip for minority class
    'rotation_limit': 30,      # More aggressive rotation
    'brightness_contrast_prob': 0.9,
    'noise_blur_prob': 0.5,
    'oversample_minority': True, # Oversample eligible class
}

# Enhanced augmentation for multi-region
MULTI_REGION_AUGMENTATION_CONFIG = {
    'use_mixup': True,
    'mixup_alpha': 0.4,  # Stronger mixing for region blending
    'horizontal_flip_prob': 0.7,
    'rotation_limit': 25,  # More rotation for geographic variety
    'brightness_contrast_prob': 0.9,
    'noise_blur_prob': 0.5,
}

# Loss Configuration
LOSS_CONFIG = {
    'focal_loss_alpha': 0.25,  # Weight for minority class (eligible)
    'focal_loss_gamma': 2.0,   # Higher gamma for harder examples
    'label_smoothing': 0.0,    # Add label smoothing
}

# Enhanced loss for multi-region
MULTI_REGION_LOSS_CONFIG = {
    'focal_loss_alpha': 0.25,  # Weight for minority class
    'focal_loss_gamma': 2.0,   # Even higher gamma for severe imbalance
    'label_smoothing': 0.15,   # More label smoothing for multi-region
}

# Paths
PATHS = {
    'model_save_path': 'improved_All_nz_regions_model.pth',
    'multi_region_model_save_path': 'improved_All_nz_regions_model.pth',
    'data_root': 'carbon_dataset/',
}
