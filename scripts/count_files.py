import os

def countfiles(root):
    total = 0
    for _, _, files in os.walk(root):
        total += len([f for f in files if not f.startswith(".")])
    return total

BASE = r"C:\Users\delta\DATASETS\SPECTRA"  # ← CHANGE THIS

for ds in ["brats", "rsna", "mura"]:
    path = os.path.join(BASE, ds)
    if os.path.exists(path):
        print(ds, ":", countfiles(path))
    else:
        print(ds, ": PATH NOT FOUND ->", path)