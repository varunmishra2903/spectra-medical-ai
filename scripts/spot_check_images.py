import os
import random
from PIL import Image

IMAGE_ROOTS = [
    r"C:\Users\delta\Datasets\SPECTRA\rsna",
    r"C:\Users\delta\Datasets\SPECTRA\mura",
    r"spectra-medical-ai\data\gatekeeper",
]

NUM_SAMPLES = 10

image_files = []

for root_path in IMAGE_ROOTS:
    if not os.path.exists(root_path):
        continue
    for root, _, files in os.walk(root_path):
        for f in files:
            if f.lower().endswith((".png", ".jpg", ".jpeg")):
                image_files.append(os.path.join(root, f))

if len(image_files) == 0:
    raise RuntimeError("No image files found")

samples = random.sample(image_files, min(NUM_SAMPLES, len(image_files)))

print(f"Spot-checking {len(samples)} images...\n")

for path in samples:
    try:
        with Image.open(path) as img:
            img.verify()
        print(f"OK  | {os.path.basename(path)}")
    except Exception as e:
        print(f"BAD | {os.path.basename(path)} | {e}")