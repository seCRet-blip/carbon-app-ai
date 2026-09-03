"""
EfficientNet-based classifier for carbon credit eligibility
"""

import torch
import torch.nn as nn
from torchvision import models

class EfficientNetClassifier(nn.Module):
    """EfficientNet-B3 with custom head"""
    
    def __init__(self, num_classes=2, pretrained=True):
        super(EfficientNetClassifier, self).__init__()
        
        # Load pretrained EfficientNet-B3
        self.backbone = models.efficientnet_b3(pretrained=pretrained)
        
        # Get the number of features from the classifier
        in_features = self.backbone.classifier[1].in_features
        
        # Replace final layer with custom head
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(0.4),
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Dropout(0.2),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        return self.backbone(x)
