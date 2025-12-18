import os
import random
import nibabel as nib

BRATS_ROOT = r"C:\Users\delta\Datasets\SPECTRA\brats"
NUM_SAMPLES = 10

nii_files = []

for root, _, files in os.walk(BRATS_ROOT):
    for f in files:
        if f.endswith(".nii.gz"):
            nii_files.append(os.path.join(root, f))

if len(nii_files) == 0:
    raise RuntimeError("No NIfTI files found")

samples = random.sample(nii_files, min(NUM_SAMPLES, len(nii_files)))

print(f"Spot-checking {len(samples)} BraTS NIfTI files...\n")

for path in samples:
    try:
        nii = nib.load(path)
        data = nii.get_fdata()
        print(f"OK  | {os.path.basename(path)} | shape={data.shape}")
    except Exception as e:
        print(f"BAD | {os.path.basename(path)} | {e}")