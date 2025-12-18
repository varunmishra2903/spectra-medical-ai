# Data Sources & Licensing — SPECTRA Medical AI

This document provides the authoritative list of datasets used in the SPECTRA medical imaging system.  
All datasets are used strictly for academic, research, and educational purposes as part of the  
6th semester mini-project.

No raw medical data is stored in the repository. Only lightweight, derived samples  
(e.g., MedMNIST gatekeeper data) are included.

---

# 1. Brain Tumor Segmentation (BraTS 2021)

### Official Source
MICCAI BraTS Challenge  
https://www.med.upenn.edu/cbica/brats2021/data.html

### Usage in SPECTRA
- Used by the **Brain Imaging Pipeline**  
- Enables tumor detection, segmentation, and measurement  
- Provides multi-modal MRI scans: T1, T1CE, T2, FLAIR + segmentation mask

### License & Restrictions
- **Research Use Only**  
- Academic projects: ✔ Allowed  
- Redistribution: ❌ Not allowed  
- Commercial use: ❌ Not allowed  

### Required Citation
> Menze et al., The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS), IEEE TMI.

### Notes
- All raw `.nii.gz` files remain stored locally on each team member’s device.  
- Only processed masks and visualizations may appear in the repo.

---

# 2. RSNA Pneumonia Detection Dataset (Chest X-Ray)

### Official Source
RSNA Pneumonia Detection Challenge (Kaggle)  
https://www.kaggle.com/c/rsna-pneumonia-detection-challenge

### Usage in SPECTRA
- Used by the **Chest Imaging Pipeline**  
- Enables pneumonia classification and report score generation  
- Contains DICOM images + pneumonia bounding boxes and labels

### License & Restrictions
- Subject to Kaggle Terms of Service  
- Academic use: ✔ Allowed  
- Redistribution: ❌ Not allowed  
- Commercial use: ❌ Not allowed

### Required Citation
> RSNA Pneumonia Detection Challenge, Radiological Society of North America.

### Notes
- Raw `.dcm` images are kept locally; not included in the repository.  
- Models trained on this dataset are allowed to be shared (not the raw data).

---

# 3. MURA v1.1 — Musculoskeletal Radiographs (Bone/Fracture)

### Official Source
Stanford ML Group  
https://stanfordmlgroup.github.io/competitions/mura/

### Usage in SPECTRA
- Used by the **Bone Imaging Pipeline**  
- Supports fracture detection in regions like wrist, elbow, shoulder, etc.  
- Provides labeled X-ray studies across 7 anatomical regions

### License & Restrictions
- Research & Educational License  
- Academic use: ✔ Allowed  
- Redistribution: ❌ Not allowed  
- Commercial use: ❌ Not allowed

### Required Citation
> Rajpurkar et al., MURA: Large Dataset for Musculoskeletal Radiographs, arXiv.

### Notes
- Only predictions, heatmaps, and diagnostics can appear in GitHub — never raw images.

---

# 4. MedMNIST (Gatekeeper Data)

### Official Source
MedMNIST v2  
https://medmnist.com/

### Usage in SPECTRA
- Used by the **Gatekeeper/Categorizer**  
- Helps classify input modality into:
  - Chest (PneumoniaMNIST)
  - Organ/Abdomen (OrganAMNIST)
  - Bone (FractureMNIST3D)

### License & Restrictions
- **CC BY 4.0** — most permissive dataset used
- Academic use: ✔ Allowed  
- Redistribution: ✔ Allowed (with attribution)  
- Commercial use: ✔ Allowed (with attribution)

### Required Citation
> Yang et al., MedMNIST v2: A Large-Scale Lightweight Benchmark for Biomedical Image Classification, Nature Scientific Data.

### Notes
- Only these small derived PNG samples are inside the repo.  
- No licensing conflicts with including gatekeeper samples.

---

# Summary Table

| Dataset | Source | Academic Use | Redistribution | License |
|--------|--------|--------------|----------------|---------|
| BraTS 2021 | MICCAI | ✔ Allowed | ❌ No | Research Only |
| RSNA Pneumonia | Kaggle | ✔ Allowed | ❌ No | Kaggle Terms |
| MURA v1.1 | Stanford ML Group | ✔ Allowed | ❌ No | Research/Education |
| MedMNIST | MedMNIST.org | ✔ Allowed | ✔ Yes | CC BY 4.0 |

---

# Compliance Notes
- No raw medical datasets are uploaded to GitHub.  
- Only small, derived gatekeeper samples (MedMNIST) are included.  
- All datasets are used strictly for academic research under fair-use guidelines.  
- Every dataset used in SPECTRA requires proper citation in the final report.