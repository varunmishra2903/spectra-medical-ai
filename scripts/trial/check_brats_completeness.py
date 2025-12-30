import os

BRATS_ROOT = r"C:\Users\delta\Datasets\SPECTRA\brats"

required_suffixes = [
    "_t1.nii.gz",
    "_t1ce.nii.gz",
    "_t2.nii.gz",
    "_flair.nii.gz",
    "_seg.nii.gz",
]

missing = []

for case in os.listdir(BRATS_ROOT):
    case_dir = os.path.join(BRATS_ROOT, case)
    if not os.path.isdir(case_dir):
        continue

    files = os.listdir(case_dir)
    for suf in required_suffixes:
        if not any(f.endswith(suf) for f in files):
            missing.append((case, suf))

if missing:
    print("❌ Missing files detected:")
    for m in missing:
        print(m)
else:
    print("✅ All BraTS cases are complete")