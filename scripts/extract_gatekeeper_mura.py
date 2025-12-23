import os
import numpy as np
from PIL import Image
from pathlib import Path
from tqdm import tqdm

# ================= CONFIG =================
RAW_MURA_DIR = r"C:\Users\delta\Datasets\SPECTRA\mura\train"
OUTPUT_DIR = r"C:\Users\delta\Datasets\SPECTRA\processed_data\mura"
TARGET_SIZE = 224
MIN_NONZERO_RATIO = 0.05

# Preferred body parts (folder name hints)
PREFERRED_PARTS = ["forearm", "humerus", "femur", "tibia"]
# =========================================

def percentile_normalize(img):
    img = img.astype(np.float32)
    p1, p99 = np.percentile(img, (1, 99))
    if p99 - p1 < 1e-5:
        return None
    img = np.clip(img, p1, p99)
    img = 255 * (img - p1) / (p99 - p1)
    return img.astype(np.uint8)

def resize_pad(img):
    h, w = img.shape
    scale = TARGET_SIZE / max(h, w)
    nh, nw = int(h * scale), int(w * scale)
    img = Image.fromarray(img).resize((nw, nh), Image.BILINEAR)
    canvas = Image.new("L", (TARGET_SIZE, TARGET_SIZE), 0)
    canvas.paste(img, ((TARGET_SIZE - nw)//2, (TARGET_SIZE - nh)//2))
    return canvas

def passes_quality(img):
    return (np.count_nonzero(img) / img.size) >= MIN_NONZERO_RATIO

def is_preferred_study(path):
    p = path.lower()
    return any(part in p for part in PREFERRED_PARTS)

def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    files = []
    for root, _, filenames in os.walk(RAW_MURA_DIR):
        if not is_preferred_study(root):
            continue
        for f in filenames:
            if f.lower().endswith((".png", ".jpg", ".jpeg")):
                files.append(os.path.join(root, f))

    print(f"Found {len(files)} candidate MURA images")

    kept = 0
    for idx, path in tqdm(enumerate(files), total=len(files), desc="MURA"):
        try:
            img = Image.open(path).convert("L")
            img = np.array(img)

            img = percentile_normalize(img)
            if img is None or not passes_quality(img):
                continue

            img = resize_pad(img)
            img.save(f"{OUTPUT_DIR}/mura_{idx:06d}.png")
            kept += 1

        except Exception:
            continue

    print(f"✅ MURA done | kept: {kept}")

if __name__ == "__main__":
    main()