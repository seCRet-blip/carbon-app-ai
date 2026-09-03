# Carbon App AI

A computer vision pipeline that classifies New Zealand aerial imagery as **eligible** or **ineligible** for carbon credits under the NZ Emissions Trading Scheme.

Landowners and assessors currently rely on slow, manual GIS review to decide whether a parcel can enter the forestry ETS. This project automates a first-pass screening: it downloads LINZ aerial tiles across all 18 regions, labels them against official land-use layers, and trains a CNN to predict eligibility from a 128×128 image.

Built as an end-to-end ML system — data collection, GIS labelling, imbalanced-class training, evaluation, and inference — not just a notebook model.

---

## Results

Tested on a held-out set of **3,368 tiles** covering every NZ region (never seen during training):

| Metric | Score |
| --- | --- |
| Overall accuracy | **86.8%** |
| ROC-AUC | **0.917** |
| Eligible recall | **76.3%** |
| Ineligible F1 | **91.8%** |

The eligible class is the minority (~1:5 in the test set, far more extreme in the raw data). The training setup uses weighted sampling, mixup, and a custom classification head so the model does not collapse to “always ineligible”.

---

## What it does

1. **Collect** — Download zoom-15 aerial tiles from [LINZ Basemaps](https://basemaps.linz.govt.nz/) for all New Zealand regions, with parallel downloads and on-the-fly JPEG compression.
2. **Label** — Overlay each tile on LCDB / LUCAS land-use shapefiles with GeoPandas and mark it eligible or ineligible from official forest cover.
3. **Train** — Fine-tune EfficientNet-B3 or ResNet-50 (or an ensemble of both) on 128×128 RGB tiles, with Albumentations, mixup, class weights, and early stopping.
4. **Predict** — Run a single image or a folder through the trained model and return class, confidence, and a calibrated threshold.

---

## Stack

- **Models:** PyTorch, torchvision EfficientNet-B3 / ResNet-50, custom ensemble
- **Training:** Focal loss option, weighted random sampling, mixup, AdamW, early stopping
- **Data:** LINZ WMTS aerial tiles, LCDB & LUCAS GIS layers, GeoPandas / Shapely
- **Eval:** Accuracy, precision, recall, F1, ROC-AUC, confusion matrix, per-image confidence

---

## Project layout

```
carbon-app-ai/
├── README.md
└── CNN_model/
    ├── main.py                 # Training entry point
    ├── config.py               # Hyperparameters and data paths
    ├── models/                 # EfficientNet, ResNet, ensemble
    ├── data/                   # Dataset + augmentation
    ├── training/               # Trainer, losses, samplers
    ├── GetData/                # Tile download + GIS labelling
    ├── Tests/                  # Single-image and batch evaluation
    ├── docs/                   # Validation, risk, and compliance notes
    └── requirements.txt
```

Datasets, trained weights, and API keys stay local and are gitignored.

---

## Setup

You do not need the full dataset or a LINZ key to read the code. The steps below are for running training or inference locally.

### 1. Clone and install

```bash
git clone https://github.com/seCRet-blip/carbon-app-ai.git
cd carbon-app-ai/CNN_model
python -m venv .venv
```

**Windows (PowerShell)**

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux**

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

A GPU is recommended for training. CPU works for single-image inference.

### 2. API key (data download only)

Copy the example env file and add a [LINZ Basemaps](https://basemaps.linz.govt.nz/) API key:

```bash
cp .env.example .env
```

Then set `LINZ_API_KEY` in `.env`. This is only required if you want to fetch aerial tiles yourself.

### 3. Data (optional)

Aerial tiles and GIS layers are large and are not in this repo.

- Place LINZ tiles under `CNN_model/nz_data/<region>/`
- Place LCDB / LUCAS shapefiles under `CNN_model/raw_data/`
- Build labelled CSVs:

```bash
python GetData/createData.py
```

Expected CSVs (already configured in `config.py`):

```
carbon_dataset/
├── all_region_train.csv
├── all_region_val.csv
└── all_region_test.csv
```

### 4. Train

From `CNN_model/`:

```bash
# Diagnose class balance first
python main.py --diagnose

# EfficientNet with mixup, all NZ regions
python main.py --model efficientnet --mixup --multi-region

# ResNet-50
python main.py --model resnet --mixup --multi-region

# Ensemble
python main.py --model both --ensemble --mixup --multi-region
```

Hyperparameters live in `config.py` (batch size, learning rate, image size, loss weights).

### 5. Inference

```bash
python Tests/test_single_image.py --model TrainedModels/All_nz_regions_model.pth --image path/to/tile.jpg
python Tests/test_single_image.py --model TrainedModels/All_nz_regions_model.pth --folder path/to/tiles/
```

---

## Notes

This is a screening tool, not a legal determination of ETS eligibility. Low-confidence predictions should be reviewed by a person. Extra write-ups on validation, risk, and compliance are in `CNN_model/docs/`.
