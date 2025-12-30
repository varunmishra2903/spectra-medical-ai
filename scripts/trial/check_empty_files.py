import os

BASE = r"C:\Users\delta\Datasets\SPECTRA"

empty_files = []

for root, _, files in os.walk(BASE):
    for f in files:
        path = os.path.join(root, f)
        try:
            if os.path.getsize(path) == 0:
                empty_files.append(path)
        except OSError:
            empty_files.append(path)

if empty_files:
    print("❌ Empty or unreadable files:")
    for f in empty_files:
        print(f)
else:
    print("✅ No empty files detected")