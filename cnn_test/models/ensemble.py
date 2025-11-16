"""
Ensemble model combining multiple architectures
"""

import torch
import torch.nn as nn

class EnsembleModel(nn.Module):
    """Ensemble of multiple models for higher accuracy"""
    
    def __init__(self, models_list):
        super(EnsembleModel, self).__init__()
        self.models = nn.ModuleList(models_list)
    
    def forward(self, x):
        outputs = [model(x) for model in self.models]
        # Average predictions
        return torch.mean(torch.stack(outputs), dim=0)
