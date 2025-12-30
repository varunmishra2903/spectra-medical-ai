# M6 — Data Preprocessing Contribution Summary
**Author:** Priyotosh (M6 — Data Engineer)  
**Last Updated:** 19 December 2025

---

# 🎯 1. Overview
After completing the dataset validation stage (file counts, folder structure, integrity checks), I moved into the **preprocessing phase** — preparing medical imaging datasets for training.

This document explains **what I did**, **what problems I encountered**, and **how I solved them**, in a clear and team‑friendly way.

---

# 📦 2. Datasets Prepared
### ✔ BraTS 2021 (Brain MRI — For M2)
- Downloaded and extracted
- Verified `.nii.gz` integrity

### ✔ RSNA Pneumonia (Chest X-Ray — For M3)
- Downloaded and extracted
- Verified DICOM & CSV structure

### ✔ MedMNIST (Gatekeeper — For M1)
- Script-based dataset extraction
- Generated sample routing images

### ✔ **MURA v1.1 (Bone X-Ray Fracture Dataset — For M4)**
**This is the dataset I fully preprocessed using an advanced pipeline.**

---

# ⚙️ 3. What Preprocessing I Performed (Advanced Level‑2)
This was more than basic histogram equalization. I implemented a **stronger, clinically meaningful preprocessing pipeline**:

### 🔹 Center Cropping
Removes unwanted black borders and improves region focus.

### 🔹 Gaussian Blur (Noise Reduction)
Removes X-ray graininess.

### 🔹 **CLAHE (Contrast Limited Adaptive Histogram Equalization)**
Far more advanced than normal histogram equalization — improves local contrast and reveals fractures clearly.

### 🔹 Z-score Intensity Normalization
Ensures stable training across varying exposure levels.

### 🔹 Resize to 224×224
Standard input size for common CNN architectures.

### 🔹 Normalization back to uint8
Ensures PNG safe saving.

### 🔹 Safe Short Filenames
Prevents Windows MAX_PATH failures.

### 🔹 Full Metadata CSV Generation
Creates a usable training reference for M4.

---

# 🧪 4. Problems I Encountered & How I Solved Them
## ❌ Issue 1 — Script Only Processed 51 Images
**Cause:** Directory traversal broke due to hidden files and folder structure mismatch.

**Fix:** Added strict directory checks at each folder level.

---

## ❌ Issue 2 — Windows Explorer Showed ~37,312 Files Instead of 40,000+
**Cause:** Windows Explorer caching + hidden files not displayed.

**Fix:** Used Python counters to verify actual counts (source of truth).

---

## ❌ Issue 3 — About 2,700 Images Didn’t Save
**Cause:** Windows MAX_PATH limitation silently blocked long filenames.

**Fix:** Implemented short, safe filenames like:
```
mura_000001.png
mura_000002.png
```
This solved the silent write failures.

---

## ❌ Issue 4 — Some Images Were Corrupted
**Cause:** A few X-ray files could not be read by OpenCV.

**Fix:** Logged them in:
```
failed_images.txt
```
Only **4** images failed — normal for large medical datasets.

---

# 🎉 5. Final Output Summary
### ✔ **40,005 fully processed MURA images**
### ✔ **metadata.csv** generated for training usage
### ✔ **4** corrupted images logged in `failed_images.txt`
### ✔ Dataset is fully consistent, clean, and ML‑ready

Final structure:
```
processed/mura/
    images/               ← 40,005 images
    metadata.csv
    failed_images.txt
```

---

# 🚀 6. Why This Work Matters
The advanced preprocessing pipeline improves:
- Image clarity
- Contrast
- Model stability
- Fracture visibility
- Training accuracy
- Clean reproducibility

This dramatically reduces the workload for M4 and ensures a high‑quality dataset.

---

# 🧠 7. What My Teammates Should Know
- The **entire MURA pipeline is complete**: downloading → validating → preprocessing → metadata.
- I implemented **advanced enhancement techniques**, not basic histogram methods.
- M4 can now start training **immediately** with no cleanup required.
- All failures and corrections are **logged and documented**.

---

# 🏁 8. Next Steps for Me
- Support M3 & M4 with DataLoader integration
- Provide QA visualization tools
- Assist with model verification and debugging
- Maintain structured documentation in `docs/`

---

This document represents my completed contributions after dataset validation, covering full preprocessing, debugging, and delivery of clean ML-ready data.

