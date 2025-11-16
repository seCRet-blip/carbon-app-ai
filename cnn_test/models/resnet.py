"""
ResNet-based classifier for carbon credit eligibility
"""

import torch
import torch.nn as nn
from torchvision import models

class ResNetClassifier(nn.Module):
    """ResNet-50 with custom head"""
    
    def __init__(self, num_classes=2, pretrained=True):
        super(ResNetClassifier, self).__init__()
        
        # Load pretrained ResNet-50
        self.backbone = models.resnet50(pretrained=pretrained)
        
        # Replace final layer
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.4),
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x):
        return self.backbone(x)
