# Data Sources & Licensing — SPECTRA Medical AI

This document provides the authoritative list of datasets used in the SPECTRA medical imaging system. All datasets are used strictly for academic, research, and educational purposes as part of the 6th semester mini-project.

No raw medical data is stored in the repository. Only lightweight, derived samples (e.g., MedMNIST gatekeeper data) are included.

---

# 💻 How to Download All Required Datasets

Below are the **exact terminal commands** used to download and prepare the datasets. Team members must use the **same commands** to ensure consistent folder structure.

All datasets were downloaded using **Kaggle CLI** or script-driven APIs.

Before running anything:

```bash
pip install kaggle
mkdir ~/.kaggle
# Place kaggle.json inside ~/.kaggle
chmod 600 ~/.kaggle/kaggle.json
```

---

# 1. BraTS 2021 — Brain Tumor Segmentation

### 📥 Download Command (Used by Member 6)

```bash
kaggle datasets download -d dschettler8845/brats-2021-task1
```

This will download:

```
brats-2021-task1.zip
```

### 📦 Extraction

```bash
unzip brats-2021-task1.zip -d brain
```

Then move contents into:

```
C:\Users\delta\DATASETS\SPECTRA\brain\
```

### (Large .tar extraction)

After unzipping, extract the main training tar:

```bash
tar -xvf BraTS2021_Training_Data.tar -C C:\Users\delta\DATASETS\SPECTRA\brain
```

---

# 2. RSNA Pneumonia Detection — Chest X-Ray

### 📥 Download Command

```bash
kaggle competitions download -c rsna-pneumonia-detection-challenge
```

This will download multiple zip files.

### 📦 Extraction

```bash
unzip rsna-pneumonia-detection-challenge.zip -d chest
```

Move extracted files to:

```
C:\Users\delta\DATASETS\SPECTRA\rsna\
```

---

# 3. MURA v1.1 — Bone/Fracture Dataset

### 📥 Download Command

```bash
kaggle datasets download -d radiologist/mura-v11
```

This downloads:

```
MURA-v1.1.zip
```

### 📦 Extraction

```bash
unzip MURA-v1.1.zip -d MURA
```

Move folder to:

```
C:\Users\delta\DATASETS\SPECTRA\MURA-v1.1\
```

---

# 4. MedMNIST (Gatekeeper Data)

These datasets are downloaded using the **Python script written by Member 6**.

### 📜 Script Used

```python
import medmnist
from medmnist import INFO
import os
from PIL import Image
import numpy as np

OUTPUT_DIR = "data/gatekeeper"
DATASETS = ['pneumoniamnist', 'organamnist', 'fracturemnist3d']

# (script continues...)  # Full script is inside scripts/download_medmnist.py
```

Run it with:

```bash
python scripts/download_medmnist.py
```

This generates 50 images per category into:

```
spectra-medical-ai/data/gatekeeper/
```

---

# 🔒 Licensing Summary

| Dataset        | Source            | Academic Use | Redistribution | License            |
| -------------- | ----------------- | ------------ | -------------- | ------------------ |
| BraTS 2021     | MICCAI            | ✔ Allowed    | ❌ No           | Research Only      |
| RSNA Pneumonia | Kaggle            | ✔ Allowed    | ❌ No           | Kaggle Terms       |
| MURA v1.1      | Stanford ML Group | ✔ Allowed    | ❌ No           | Research/Education |
| MedMNIST       | MedMNIST.org      | ✔ Allowed    | ✔ Yes          | CC BY 4.0          |

---

# 📝 Notes

* Team members must **download datasets exactly as shown above** to maintain identical folder structures.
* No raw imaging data should be committed to GitHub.
* Only gatekeeper sample data (MedMNIST) is allowed inside the repository.
* All datasets must be cited properly in the final report.
