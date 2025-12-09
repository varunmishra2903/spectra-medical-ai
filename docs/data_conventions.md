\# Data Naming \& Folder Conventions



\## Top-level dataset folders

\- Brain (BraTS): `data/brain/`

\- Chest (RSNA): `data/chest/`

\- Bone (MURA / FracAtlas): `data/bone/`



\## Train/Val/Test splits

Inside each modality folder:



\- `data/brain/train/`, `data/brain/val/`, `data/brain/test/`

\- `data/chest/train/`, `data/chest/val/`, `data/chest/test/`

\- `data/bone/train/`, `data/bone/val/`, `data/bone/test/`



\## Gatekeeper dataset

Unified 2D classification set:



\- `data/gatekeeper/brain/`

\- `data/gatekeeper/chest/`

\- `data/gatekeeper/bone/`



Each folder contains ~N sample PNG/JPG images, resized to 224x224.



\## File naming

\- Brain: `<patientID>\_<studyID>\_<slice>.nii.gz` or `.png`

\- Chest: `<patientID>\_<studyID>.png`

\- Bone: `<studyID>\_<view>.png`

(Adjust as needed once M6 confirms downloads.)



