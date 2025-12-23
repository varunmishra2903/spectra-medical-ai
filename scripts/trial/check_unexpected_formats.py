import os

BASE = r"C:\Users\delta\Datasets\SPECTRA"

EXPECTED_EXTENSIONS = {
    "brats": {".nii.gz",".tar",""},
    "rsna": {".dcm", ".txt", ".csv"},
    "mura": {".png", ".jpg", ".csv"},
    "medmnist": {".npz"},
}

for ds, allowed_exts in EXPECTED_EXTENSIONS.items():
    root = os.path.join(BASE, ds)
    print(f"\nChecking {ds.upper()}")

    unexpected = set()

    for _, _, files in os.walk(root):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if not any(f.endswith(e) for e in allowed_exts):
                unexpected.add(ext)

    if unexpected:
        print("❌ Unexpected formats found:", unexpected)
    else:
        print("✅ No unexpected formats")