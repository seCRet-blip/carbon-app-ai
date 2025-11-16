# Carbon Credit Eligibility Classifier

A deep learning project for classifying land use images as eligible or ineligible for carbon credits using state-of-the-art CNN architectures.

## Project Structure

```
cnn_test/
├── models/                    # Model architectures
│   ├── __init__.py
│   ├── efficientnet.py      # EfficientNet-B3 classifier
│   ├── resnet.py            # ResNet-50 classifier
│   └── ensemble.py          # Ensemble model
├── data/                     # Data loading and transforms
│   ├── __init__.py
│   ├── dataset.py           # Dataset classes
│   └── transforms.py        # Data augmentation
├── training/                 # Training utilities
│   ├── __init__.py
│   ├── trainer.py           # Main training loop
│   ├── losses.py            # Custom loss functions
│   └── utils.py             # Training utilities
├── config.py                # Configuration settings
├── main.py                  # Main entry point
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Features

- **Multiple Model Architectures**: EfficientNet-B3, ResNet-50, and ensemble models
- **Advanced Data Augmentation**: Albumentations support with fallback to PyTorch transforms
- **Class Imbalance Handling**: Focal Loss, weighted sampling, and class weights
- **Multi-GPU Support**: Automatic DataParallel for multiple GPUs
- **Regularization Techniques**: Dropout, weight decay, and early stopping
- **Comprehensive Metrics**: Accuracy, F1-score, AUC-ROC, confusion matrix

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your data is organized as:
```
carbon_dataset/
├── train.csv
├── val.csv
└── test.csv
```

## Usage

### Basic Training
```bash
python main.py --model efficientnet
```

### Advanced Training Options
```bash
# Use ResNet-50
python main.py --model resnet

# Use ensemble model
python main.py --model both --ensemble

# Enable mixup augmentation
python main.py --model efficientnet --mixup

# Run dataset diagnosis only
python main.py --diagnose
```

### Programmatic Usage
```python
from training import train_advanced_model

# Train EfficientNet model
model = train_advanced_model(
    model_type='efficientnet',
    use_mixup=True,
    use_ensemble=False
)
```

## Model Architectures

### EfficientNet-B3
- Pretrained on ImageNet
- Custom classification head with dropout and batch normalization
- Optimized for efficiency and accuracy

### ResNet-50
- Pretrained on ImageNet
- Modified final layers for binary classification
- Robust feature extraction

### Ensemble Model
- Combines multiple architectures
- Average prediction across models
- Higher accuracy through model diversity

## Training Features

### Class Imbalance Solutions
- **Focal Loss**: Focuses learning on hard examples
- **Weighted Sampling**: Balances classes during training
- **Class Weights**: Adjusts loss function for imbalanced data

### Regularization
- **Dropout**: Prevents overfitting in dense layers
- **Weight Decay**: L2 regularization in optimizer
- **Early Stopping**: Stops training when validation performance plateaus

### Data Augmentation
- **Albumentations**: Advanced augmentation library (optional)
- **PyTorch Transforms**: Fallback augmentation
- **Mixup**: Mixes training samples for better generalization

## Configuration

Modify `config.py` to adjust:
- Model hyperparameters
- Training settings
- Data paths
- Augmentation parameters

## Troubleshooting

### Common Issues

1. **Class Imbalance**: Run `python main.py --diagnose` to check data distribution
2. **Out of Memory**: Reduce batch size in `config.py`
3. **Poor Performance**: Try different models or enable ensemble mode
4. **Overfitting**: Increase weight decay or reduce learning rate

### Performance Tips

1. Use multiple GPUs if available
2. Enable albumentations for better augmentation
3. Try ensemble models for higher accuracy
4. Adjust focal loss parameters for your specific class imbalance

## Results Interpretation

The training outputs several metrics:
- **Accuracy**: Overall classification accuracy
- **F1-Score**: Harmonic mean of precision and recall (important for imbalanced data)
- **AUC-ROC**: Area under the ROC curve (measures discrimination ability)
- **Confusion Matrix**: Detailed breakdown of predictions

For imbalanced datasets, focus on F1-score and AUC rather than just accuracy.

## License

This project is for educational and research purposes.
