# CNN training pipeline

Training, data collection, and inference code for this **proof-of-concept** carbon credit eligibility classifier.

**Start here for the project overview and setup:** [root README](../README.md)

```
CNN_model/
├── models/          # EfficientNet, ResNet-50, ensemble
├── data/            # Dataset classes and augmentation
├── training/        # Trainer, losses, samplers
├── GetData/         # LINZ tile download and GIS labelling
├── Tests/           # Single-image and batch evaluation
├── docs/            # Validation, risk, and compliance notes
├── config.py
├── main.py
└── requirements.txt
```

Quick commands (from this folder):

```bash
pip install -r requirements.txt
python main.py --diagnose
python main.py --model efficientnet --mixup --multi-region
python Tests/test_single_image.py --model TrainedModels/All_nz_regions_model.pth --image path/to/tile.jpg
```
