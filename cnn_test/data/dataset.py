"""
Dataset classes for carbon credit eligibility classification
"""

import os
import cv2
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset
from .transforms import get_train_transforms, get_val_transforms, get_albumentations_transforms

class CarbonCreditDatasetAdvanced(Dataset):
    """Advanced dataset with albumentations support"""
    
    def __init__(self, csv_file, use_albumentations=True):
        self.data = pd.read_csv(csv_file)
        
        # Filter for binary classification
        self.data = self.data[self.data['label'].isin(['eligible', 'ineligible'])]
        self.data['binary_label'] = (self.data['label'] == 'eligible').astype(int)
        
        self.use_albumentations = use_albumentations
        
        if use_albumentations:
            self.train_transform, self.val_transform = get_albumentations_transforms()
            if self.train_transform is None:
                print("⚠️ Albumentations not available, falling back to PyTorch transforms")
                self.use_albumentations = False
        
        if not self.use_albumentations:
            self.train_transform = get_train_transforms()
            self.val_transform = get_val_transforms()
        
        print(f"Loaded {len(self.data)} samples")
        
        # Print class distribution
        eligible_count = len(self.data[self.data['binary_label'] == 1])
        ineligible_count = len(self.data[self.data['binary_label'] == 0])
        print(f"Class distribution - Eligible: {eligible_count}, Ineligible: {ineligible_count}")
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        img_path = self.data.iloc[idx]['path']
        
        # Load and process image
        image = cv2.imread(img_path)
        if image is None:
            print(f"Warning: Could not load image {img_path}")
            image = np.zeros((128, 128, 3), dtype=np.uint8)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        label = self.data.iloc[idx]['binary_label']
        
        # Apply transforms
        if self.use_albumentations:
            if hasattr(self, 'train_transform') and self.train_transform is not None:
                transformed = self.train_transform(image=image)
                image = transformed['image']
            else:
                transformed = self.val_transform(image=image)
                image = transformed['image']
        else:
            # Use PyTorch transforms
            image = self.train_transform(image)
        
        return image, torch.tensor(label, dtype=torch.long)


class SimpleDataset(Dataset):
    """Simple dataset with basic PyTorch transforms"""
    
    def __init__(self, csv_file, transform):
        self.data = pd.read_csv(csv_file)
        self.data = self.data[self.data['label'].isin(['eligible', 'ineligible'])]
        self.data['binary_label'] = (self.data['label'] == 'eligible').astype(int)
        self.transform = transform
        print(f"Loaded {len(self.data)} samples")
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        img_path = self.data.iloc[idx]['path']
        image = cv2.imread(img_path)
        if image is None:
            image = np.zeros((128, 128, 3), dtype=np.uint8)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        label = self.data.iloc[idx]['binary_label']
        if self.transform:
            image = self.transform(image)
        return image, torch.tensor(label, dtype=torch.long)
