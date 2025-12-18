# Data Sources & Licensing — SPECTRA Medical AI

This document lists all datasets used in the SPECTRA project along with their
official sources, licenses, usage permissions, and citations.  
This ensures academic transparency, legal compliance, and reproducibility.

---

## 📌 BraTS 2021 — Brain Tumor Segmentation

### Official Source
- MICCAI BraTS Challenge  
- URL: https://www.med.upenn.edu/cbica/brats2021/data.html  
  (mirrors available on Kaggle)

### License & Permissions
- License: Research Use Only  
- Redistribution: ❌ Not allowed  
- Academic Use: ✔ Allowed  
- Commercial Use: ❌ Not allowed  

### Required Citation
> Menze et al., *The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS)*, IEEE Transactions on Medical Imaging.

### Notes
- Must not upload or share raw `.nii.gz` data publicly.
- Allowed in classroom, academic, and research projects.

---

## 📌 RSNA Pneumonia Detection — Chest X-Ray

### Official Source
- Kaggle RSNA Pneumonia Detection Challenge  
- URL: https://www.kaggle.com/c/rsna-pneumonia-detection-challenge

### License & Permissions
- License: Kaggle Terms of Use  
- Academic Use: ✔ Allowed  
- Redistribution: ❌ Not allowed  
- Commercial Use: ❌ Not allowed  

### Required Citation
> RSNA Pneumonia Detection Challenge (Radiological Society of North America)

### Notes
- Use requires a Kaggle account.
- Data cannot be re-hosted or uploaded to GitHub.

---

## 📌 MURA v1.1 — Bone Fracture Dataset

### Official Source
- Stanford ML Group  
- URL: https://stanfordmlgroup.github.io/competitions/mura/

### License & Permissions
- License: Research & Educational Use License  
- Academic Use: ✔ Allowed  
- Redistribution: ❌ Not allowed  
- Commercial Use: ❌ Not allowed  

### Required Citation
> Rajpurkar et al., *MURA: Large Dataset for Musculoskeletal Radiographs*, arXiv.

### Notes
- Only processed results can be shared.
- Raw images must remain local.

---

## 📌 MedMNIST — Gatekeeper Dataset

### Official Source
- MedMNIST v2  
- URL: https://medmnist.com/

### License & Permissions
- License: CC BY 4.0 (Creative Commons Attribution 4.0)  
- Academic Use: ✔ Fully Allowed  
- Redistribution: ✔ Allowed with citation  
- Commercial Use: ✔ Allowed (with attribution)

### Required Citation
> Yang et al., *MedMNIST v2: A Large-Scale Lightweight Benchmark for 2D and 3D Biomedical Image Classification*, Scientific Data.

### Notes
- This is the **only dataset** in SPECTRA allowed inside the Git repo.
- Ideal for lightweight preprocessing and demos.

---

## 📎 Compliance Summary

| Dataset | Academic Use | Commercial Use | Redistribution | License |
|--------|--------------|----------------|----------------|---------|
| BraTS 2021 | ✔ Allowed | ❌ No | ❌ No | Research Only |
| RSNA Pneumonia | ✔ Allowed | ❌ No | ❌ No | Kaggle Terms |
| MURA v1.1 | ✔ Allowed | ❌ No | ❌ No | Research/Educational |
| MedMNIST | ✔ Allowed | ✔ Yes | ✔ Yes | CC BY 4.0 |

---

## 📝 Final Notes

- No raw medical datasets are included in the repo due to licensing restrictions and size.
- Only derived, lightweight gatekeeper data (MedMNIST samples) is stored inside the project.
- All external datasets are used strictly for academic coursework (6th semester mini-project).
