"""
Custom loss functions for imbalanced datasets
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class FocalLoss(nn.Module):
    """Enhanced Focal Loss for severe class imbalance with class weights"""
    
    def __init__(self, alpha=0.25, gamma=2.0, weight=None):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.weight = weight
        
    def forward(self, inputs, targets):
        # Use class weights in cross entropy if provided
        ce_loss = F.cross_entropy(inputs, targets, weight=self.weight, reduction='none')
        pt = torch.exp(-ce_loss)
        
        # Apply focal loss weighting
        if isinstance(self.alpha, (float, int)):
            alpha_t = self.alpha
        else:
            alpha_t = self.alpha.gather(0, targets)
            
        focal_loss = alpha_t * (1-pt)**self.gamma * ce_loss
        return focal_loss.mean()
