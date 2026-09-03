# CNN training pipeline

Training, data collection, and inference code for the carbon credit eligibility classifier.

The project overview, results, and setup steps are in the [root README](../README.md).

```
CNN_model/
├── models/          # EfficientNet-B3, ResNet-50, ensemble
├── data/            # Dataset classes and augmentation
├── training/        # Trainer, losses, samplers
├── GetData/         # LINZ tile download and GIS labelling
├── Tests/           # Single-image and batch evaluation
├── docs/            # Validation, risk, and compliance notes
├── config.py
├── main.py
└── requirements.txt
```

Quick commands (run from this folder):

```bash
pip install -r requirements.txt
python main.py --diagnose
python main.py --model efficientnet --mixup --multi-region
python Tests/test_single_image.py --model TrainedModels/All_nz_regions_model.pth --image path/to/tile.jpg
```
