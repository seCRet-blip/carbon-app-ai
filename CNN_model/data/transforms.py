"""
Data transforms for training and validation
"""

import cv2
import numpy as np
from torchvision import transforms

def get_train_transforms():
    """Get training transforms with augmentation"""
    return transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((128, 128)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(0.3, 0.3, 0.3, 0.1),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

def get_val_transforms():
    """Get validation transforms without augmentation"""
    return transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

def get_albumentations_transforms():
    """Get advanced albumentations transforms"""
    try:
        import albumentations as A
        from albumentations.pytorch import ToTensorV2
        
        train_transform = A.Compose([
            A.Resize(128, 128),
            A.HorizontalFlip(p=0.5),
            A.RandomRotate90(p=0.5),
            A.OneOf([
                A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=1),
                A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=1),
                A.RandomGamma(gamma_limit=(80, 120), p=1),
            ], p=0.8),
            A.OneOf([
                A.GaussNoise(noise_limit=(10.0, 50.0), p=1),
                A.GaussianBlur(blur_limit=3, p=1),
                A.MotionBlur(blur_limit=3, p=1),
            ], p=0.3),
            A.Affine(
                translate_percent=0.1,  # equivalent to shift_limit
                    scale=0.9,             # equivalent to scale_limit  
                    rotate=15,             # equivalent to rotate_limit
                    p=0.7
                ),
            A.RandomCrop(height=112, width=112, p=0.3),
            A.Resize(128, 128),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2(),
        ])
        
        val_transform = A.Compose([
            A.Resize(128, 128),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2(),
        ])
        
        return train_transform, val_transform
        
    except ImportError:
        return None, None
