# Data Manifest — SPECTRA Medical AI

This document provides a complete overview of all datasets used in the SPECTRA
project, including storage locations, formats, class definitions, known issues,
licensing, and team usage.

This file serves as the single source of truth for data handling across the team
(M1–M6).

---

## 📌 BraTS 2021 — Brain Tumor Segmentation

### Purpose
- 3D brain MRI tumor segmentation
- Volumetric analysis and radiomics feature extraction

### Local Storage (NOT in repo):&emsp; *C:\Users\delta\DATASETS\SPECTRA\brain*

### Repo Storage
- None (raw dataset excluded due to size)

### Approximate Size & Counts
- Extracted files: ~6,258
- Approx. patient volumes: ~1,200+

### Train / Validation / Test (Approx.)
- Train: ~1,200 volumes
- Validation: ~200 volumes
- Test: ~250 volumes  
*(Exact split handled during preprocessing)*

### Data Format
- `.nii.gz` (NIfTI)
- Multi-modal MRI:
  - T1
  - T1CE
  - T2
  - FLAIR
- Ground-truth segmentation masks included

### Classes
- Whole Tumor (WT)
- Tumor Core (TC)
- Enhancing Tumor (ET)

### Known Issues
- Inconsistent voxel spacing
- Orientation differences across scans
- Requires careful normalization and resampling

### Usage
- Used by **M2** for 3D U-Net training and validation
- Used in radiomics extraction pipeline

### Source & License
- Dataset: BraTS 2021
- License: Research Use Only
- Academic Use: ✔ Allowed
- Citation:
  > Menze et al., *The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS)*

---

## 📌 RSNA Pneumonia Detection — Chest X-Ray

### Purpose
- Pneumonia classification from chest X-ray images

### Local Storage (NOT in repo):&emsp; *C:\Users\delta\DATASETS\SPECTRA\rsna*


### Repo Storage
- None (raw dataset excluded due to size)

### Approximate Size & Counts
- Total files: ~29,688
- Includes images + CSV metadata

### Data Format
- `.dcm` (DICOM)
- CSV files:
  - `stage_2_train_labels.csv`
  - `stage_2_detailed_class_info.csv`

### Classes
- Pneumonia
- No Pneumonia

### Known Issues
- DICOM format requires conversion or special loaders
- Class imbalance present
- Varying image resolutions

### Usage
- Used by **M3** for CNN/DenseNet-based classification
- Supports probability scoring for reports

### Source & License
- Dataset: RSNA Pneumonia Detection
- Platform: Kaggle
- License: Kaggle Terms of Use
- Academic Use: ✔ Allowed

---

## 📌 MURA v1.1 — Bone Fracture Detection

### Purpose
- Bone fracture classification from X-ray images

### Local Storage (NOT in repo) : *C:\Users\delta\DATASETS\SPECTRA\MURA-v1.1*


### Repo Storage
- None (raw dataset excluded due to size)

### Approximate Size & Counts
- Total files: ~40,009
- Includes images and CSV metadata

### Data Format
- `.png` / `.jpg`
- CSV metadata:
  - `train_image_paths.csv`
  - `train_labeled_studies.csv`
  - `valid_image_paths.csv`
  - `valid_labeled_studies.csv`

### Classes
- Fracture
- No Fracture

### Known Issues
- Labels are study-level, not image-level
- Multiple views per study
- Requires aggregation logic

### Usage
- Used by **M3** for fracture detection models
- Supports orthopedic analysis pipeline

### Source & License
- Dataset: MURA v1.1
- License: Research & Educational Use
- Academic Use: ✔ Allowed

---

## 📌 MedMNIST — Gatekeeper Dataset

### Purpose
- Lightweight modality classification (Gatekeeper)
- Routes input images to the correct specialist model

### Local Storage
- Generated dynamically via script

### Repo Storage (Included)
spectra-medical-ai/data/gatekeeper/<br>
├── pneumoniamnist/<br>
├── organamnist/<br>
└── fracturemnist3d/


### Approximate Size
- 50 sample images per class (demo & training support)

### Data Format
- `.png`
- 2D images
- 3D datasets reduced to representative middle slices

### Classes
- Chest (PneumoniaMNIST)
- Organ / Abdomen (OrganAMNIST)
- Bone / Fracture (FractureMNIST3D)

### Known Issues
- Small sample size by design
- Intended only for routing, not diagnosis

### Usage
- Used by **M1** for Gatekeeper model training
- Enables safe modality-based routing

### Source & License
- Dataset: MedMNIST
- License: CC BY 4.0
- Academic Use: ✔ Fully Allowed

---

## 📎 Notes

- Raw datasets are stored externally due to size constraints.
- Only lightweight, derived datasets (Gatekeeper samples) are included in the repo.
- Dataset integrity was validated using QA scripts before preprocessing.


