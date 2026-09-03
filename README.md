# Carbon App AI

**Proof of concept** — end-to-end computer vision pipeline that screens New Zealand land for **carbon credit eligibility** from aerial imagery.

Under the NZ Emissions Trading Scheme (ETS), deciding whether a parcel qualifies for forestry credits usually means slow, manual GIS review. This POC explores whether that first pass can be automated: collect LINZ aerial tiles across all 18 regions, label them from official land-use layers, train a CNN on a heavily imbalanced dataset, and return eligible / ineligible with a confidence score.

It is intentionally scoped as a research / portfolio prototype — a full ML loop (data → label → train → eval → infer) with validation and risk notes — not a production ETS decision system.

---

## Highlights

| | |
| --- | --- |
| **Status** | Proof of concept (not production) |
| **Problem** | Manual ETS eligibility screening does not scale across NZ |
| **Approach** | CNN classifier on 128×128 LINZ aerial tiles, labelled from LCDB / LUCAS |
| **Coverage** | All 18 New Zealand regions |
| **Held-out test** | 3,368 tiles never seen in training |
| **Accuracy** | **86.8%** |
| **ROC-AUC** | **0.917** |
| **Eligible recall** | **76.3%** (minority class) |
| **Ineligible F1** | **91.8%** |

The raw eligible class is extremely rare (roughly 1:100+ before balancing). Training uses weighted sampling, mixup, class weights, and a custom head so the model does not collapse to “always ineligible”.

---

## Pipeline

1. **Collect** — Parallel download of zoom-15 aerial tiles from [LINZ Basemaps](https://basemaps.linz.govt.nz/), with compression to keep storage manageable.
2. **Label** — GeoPandas overlays each tile on LCDB / LUCAS shapefiles and marks eligible vs ineligible from official forest cover.
3. **Train** — Fine-tune EfficientNet or ResNet-50 (or an ensemble) with Albumentations, mixup, AdamW, early stopping, and imbalance-aware sampling.
4. **Infer** — Score a single tile or a folder; return class, confidence, and a calibrated decision threshold.

---

## Tech stack

- **Deep learning:** PyTorch, torchvision (EfficientNet / ResNet-50), custom ensemble
- **Training:** Mixup, weighted sampling, focal loss option, dropout, weight decay, early stopping
- **Geospatial:** LINZ WMTS tiles, LCDB & LUCAS layers, GeoPandas, Shapely
- **Evaluation:** Accuracy, precision / recall / F1, ROC-AUC, confusion matrix, confidence analysis
- **Docs:** Validation report, risk mitigation, and legal compliance notes in `CNN_model/docs/`

---

## Repo structure

```
carbon-app-ai/
├── README.md                 # You are here
├── .gitignore
└── CNN_model/
    ├── main.py               # Training entry point
    ├── config.py             # Hyperparameters and paths
    ├── models/               # EfficientNet, ResNet, ensemble
    ├── data/                 # Dataset + augmentation
    ├── training/             # Trainer, losses, samplers
    ├── GetData/              # Tile download + GIS labelling
    ├── Tests/                # Single-image and batch evaluation
    ├── docs/                 # Validation, risk, compliance
    └── requirements.txt
```

Large datasets, trained weights (`.pth`), and API keys are gitignored and stay local.

---

## Setup (optional)

You can review the code without data or an API key. The steps below are only if you want to run training or inference yourself.

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

GPU recommended for training; CPU is fine for single-image inference.

### 2. API key (tile download only)

```bash
cp .env.example .env
```

Add a [LINZ Basemaps](https://basemaps.linz.govt.nz/) key as `LINZ_API_KEY` in `.env`. Skip this unless you are downloading aerial tiles.

### 3. Data (optional)

Tiles and GIS layers are large and are not in this repo.

- Aerial tiles → `CNN_model/nz_data/<region>/`
- LCDB / LUCAS shapefiles → `CNN_model/raw_data/`
- Build labelled CSVs:

```bash
python GetData/createData.py
```

Expected layout (paths also set in `config.py`):

```
carbon_dataset/
├── all_region_train.csv
├── all_region_val.csv
└── all_region_test.csv
```

### 4. Train

From `CNN_model/`:

```bash
python main.py --diagnose
python main.py --model efficientnet --mixup --multi-region
python main.py --model resnet --mixup --multi-region
python main.py --model both --ensemble --mixup --multi-region
```

Tune batch size, learning rate, and related settings in `config.py`.

### 5. Inference

```bash
python Tests/test_single_image.py --model TrainedModels/All_nz_regions_model.pth --image path/to/tile.jpg
python Tests/test_single_image.py --model TrainedModels/All_nz_regions_model.pth --folder path/to/tiles/
```

---

## Important

This project is a **proof of concept**. Metrics above are from a held-out test set for that POC; they are not a guarantee of real-world ETS outcomes. It is a screening experiment, not a legal determination of eligibility, and is not intended for production use without further validation, review, and compliance work. Low-confidence predictions should always be checked by a person. See `CNN_model/docs/` for validation, risk, and compliance notes.
