import os
import numpy as np
import pydicom
from PIL import Image
from pathlib import Path
from tqdm import tqdm

# ================= CONFIG =================
RAW_RSNA_DIR = r"C:\Users\delta\Datasets\SPECTRA\rsna\stage_2_train_images"
OUTPUT_DIR = r"C:\Users\delta\Datasets\SPECTRA\data_for_gatekeeper\rsna"
TARGET_SIZE = 224
MIN_NONZERO_RATIO = 0.05

WINDOW_CENTER = -600
WINDOW_WIDTH = 1500
# =========================================

def apply_lung_window(img, center, width):
    lo = center - width // 2
    hi = center + width // 2
    return np.clip(img, lo, hi)

def percentile_normalize(img):
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

def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    files = [f for f in os.listdir(RAW_RSNA_DIR) if f.endswith(".dcm")]

    kept = 0
    for idx, fname in tqdm(enumerate(files), total=len(files), desc="RSNA"):
        path = os.path.join(RAW_RSNA_DIR, fname)

        try:
            ds = pydicom.dcmread(path)
            img = ds.pixel_array.astype(np.float32)

            if hasattr(ds, "RescaleSlope"):
                img = img * ds.RescaleSlope + ds.RescaleIntercept

            img = apply_lung_window(img, WINDOW_CENTER, WINDOW_WIDTH)
            img = percentile_normalize(img)
            if img is None:
                continue

            if np.count_nonzero(img) / img.size < MIN_NONZERO_RATIO:
                continue

            img = resize_pad(img)
            img.save(f"{OUTPUT_DIR}/rsna_{idx:06d}.png")
            kept += 1

        except Exception:
            continue

    print(f"✅ RSNA done | kept: {kept}")

if __name__ == "__main__":
    main()