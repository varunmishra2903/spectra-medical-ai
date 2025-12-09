\# SPECTRA Architecture



\## Overview

SPECTRA = System for Precision Extraction, Classification, Triage \& Radiomics Analysis.



Three main zones:



1\. \*\*Zone 1 – Gatekeeper (Triage \& Routing)\*\*

&nbsp;  - Input standardization \& anonymization

&nbsp;  - Gatekeeper model (MobileNetV2)

&nbsp;  - Mismatch error handling



2\. \*\*Zone 2 – Specialist Models (Model Zoo)\*\*

&nbsp;  - Brain: 3D U-Net on BraTS (tumor segmentation)

&nbsp;  - Chest: DenseNet121 on RSNA (pneumonia classification)

&nbsp;  - Bone: U-Net++ on MURA/FracAtlas (fracture detection)

&nbsp;  - Each returns raw outputs (mask/probability/bbox)



3\. \*\*Zone 3 – Unified Reporting (JSON → UI → PDF)\*\*

&nbsp;  - Backend converts results to a \*\*standard JSON\*\*

&nbsp;  - Frontend renders overlays \& quantitative metrics

&nbsp;  - PDF generator builds the final AI diagnostic report



\## Technologies

\- \*\*Backend\*\*: Python, FastAPI, PyTorch, MONAI

\- \*\*Frontend\*\*: React, Electron, Cornerstone.js (for DICOM view)

\- \*\*Packaging\*\*: PyInstaller (api.exe), electron-builder (desktop installer)



\## Core API



\### POST /analyze

\*\*Query params:\*\*

\- `mode`: "brain" | "chest" | "bone"



\*\*Body:\*\*

\- `file`: uploaded image (DICOM/PNG/JPG)



\*\*Success Response (simplified):\*\*

```json

{

&nbsp; "status": "success",

&nbsp; "modality": "MRI\_BRAIN",

&nbsp; "ai\_finding": "POSITIVE",

&nbsp; "confidence\_score": 0.94,

&nbsp; "visual\_overlay": "mask\_overlay\_layer\_1.png",

&nbsp; "quantitative\_metrics": \[

&nbsp;   {"label": "Tumor Volume", "value": "24.5", "unit": "cm3"}

&nbsp; ],

&nbsp; "interpretability": "Explainability\_heatmap.png"

}



