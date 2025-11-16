"""
Training utilities for data sampling and augmentation
"""

import numpy as np
import torch
from collections import Counter
from torch.utils.data import WeightedRandomSampler

def create_balanced_sampler(dataset):
    """Create weighted sampler for severe class imbalance (1:121 ratio)"""
    labels = [dataset[i][1].item() for i in range(len(dataset))]
    class_counts = Counter(labels)
    
    # Calculate the actual ratio
    ratio = class_counts[0] / class_counts[1] if class_counts[1] > 0 else 1
    print(f"Dataset class distribution - Ineligible: {class_counts[0]}, Eligible: {class_counts[1]}")
    print(f"Class imbalance ratio: 1:{ratio:.1f}")
    
    # For severe imbalance, use inverse frequency weighting
    total_samples = len(labels)
    weights = {
        0: 1.0,  # Normal weight for majority class
        1: ratio * 0.8  # Strong boost for minority class, but not full inverse
    }
    
    sample_weights = [weights[label] for label in labels]
    
    print(f"Sampling weights - Ineligible: {weights[0]:.2f}, Eligible: {weights[1]:.2f}")
    print(f"This will oversample eligible class by {weights[1]:.1f}x")
    
    return WeightedRandomSampler(
        weights=sample_weights,
        num_samples=len(sample_weights),
        replacement=True
    )


def calculate_class_weights(dataset):
    """Calculate class weights for severe imbalance loss function"""
    labels = [dataset[i][1].item() for i in range(len(dataset))]
    class_counts = Counter(labels)
    
    # Calculate weights for severe imbalance (1:121 ratio)
    ratio = class_counts[0] / class_counts[1] if class_counts[1] > 0 else 1
    
    weights = {
        0: 1.0,  # Base weight for majority class (ineligible)
        1: min(ratio * 0.5, 50.0)  # Cap the weight to prevent extreme values
    }
    
    print(f"Loss function class weights - Ineligible: {weights[0]:.2f}, Eligible: {weights[1]:.2f}")
    
    return torch.tensor([weights[0], weights[1]], dtype=torch.float32)


def mixup_data(x, y, alpha=0.2):
    """Mixup augmentation for better generalization"""
    if alpha > 0:
        lam = np.random.beta(alpha, alpha)
    else:
        lam = 1
    
    batch_size = x.size()[0]
    index = torch.randperm(batch_size).to(x.device)
    
    mixed_x = lam * x + (1 - lam) * x[index, :]
    y_a, y_b = y, y[index]
    return mixed_x, y_a, y_b, lam


def mixup_criterion(criterion, pred, y_a, y_b, lam):
    """Loss function for mixup"""
    return lam * criterion(pred, y_a) + (1 - lam) * criterion(pred, y_b)
