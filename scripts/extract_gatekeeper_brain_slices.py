import os
import numpy as np
import nibabel as nib
from PIL import Image
from pathlib import Path
import csv
from tqdm import tqdm

# =========================
# CONFIG (EDIT CAREFULLY)
# =========================

RAW_BRA_TS_DIR = r"C:\Users\delta\Datasets\SPECTRA\brats"
OUTPUT_DIR = r"C:\Users\delta\Datasets\SPECTRA\data_for_gatekeeper\brain"

# Choose EXACTLY ONE modality per run
MODALITY = "flair"     # allowed: "flair" or "t1ce"

# Slice extraction rules
NUM_SLICES = 40        # choose between 30–40
DISCARD_PERCENT = 0.10 # top & bottom 10%

# Resize target
TARGET_SIZE = 224

# Quality thresholds
MIN_NONZERO_RATIO = 0.05  # ≥ 5% non‑zero pixels

# =========================
# UTILITY FUNCTIONS
# =========================

def percentile_normalize(slice_2d: np.ndarray) -> np.ndarray | None:
    p1, p99 = np.percentile(slice_2d, (1, 99))
    if p99 - p1 < 1e-5:
        return None
    slice_2d = np.clip(slice_2d, p1, p99)
    slice_2d = 255 * (slice_2d - p1) / (p99 - p1)
    return slice_2d.astype(np.uint8)


def resize_with_padding(img: Image.Image, target: int) -> Image.Image:
    w, h = img.size
    scale = target / max(w, h)
    new_w, new_h = int(w * scale), int(h * scale)
    img = img.resize((new_w, new_h), Image.BILINEAR)

    canvas = Image.new("L", (target, target), 0)
    paste_x = (target - new_w) // 2
    paste_y = (target - new_h) // 2
    canvas.paste(img, (paste_x, paste_y))
    return canvas


def passes_quality_checks(slice_uint8: np.ndarray) -> bool:
    nonzero_ratio = np.count_nonzero(slice_uint8) / slice_uint8.size
    return nonzero_ratio >= MIN_NONZERO_RATIO


# =========================
# MAIN EXTRACTION LOGIC
# =========================

def extract_slices():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    log_path = Path(OUTPUT_DIR) / "extraction_log.csv"
    with open(log_path, "w", newline="") as log_file:
        logger = csv.writer(log_file)
        logger.writerow(["patient_id", "slice_index", "status", "reason"])

        patients = sorted(os.listdir(RAW_BRA_TS_DIR))

        for patient in tqdm(patients, desc="Processing patients"):
            patient_dir = os.path.join(RAW_BRA_TS_DIR, patient)
            if not os.path.isdir(patient_dir):
                continue

            modality_file = None
            for f in os.listdir(patient_dir):
                if f.lower().endswith(f"_{MODALITY}.nii.gz"):
                    modality_file = os.path.join(patient_dir, f)
                    break

            if modality_file is None:
                logger.writerow([patient, "", "SKIP", "missing_modality"])
                continue

            try:
                volume = nib.load(modality_file).get_fdata()
            except Exception:
                logger.writerow([patient, "", "SKIP", "load_error"])
                continue

            total_slices = volume.shape[2]
            discard = int(total_slices * DISCARD_PERCENT)
            valid_slices = list(range(discard, total_slices - discard))

            if len(valid_slices) < NUM_SLICES:
                logger.writerow([patient, "", "SKIP", "insufficient_slices"])
                continue

            mid = len(valid_slices) // 2
            half = NUM_SLICES // 2
            selected = valid_slices[mid - half : mid + half]

            for idx in tqdm(
                selected,
                desc=f"Slices ({patient})",
                leave=False
            ):
                raw_slice = volume[:, :, idx]

                norm_slice = percentile_normalize(raw_slice)
                if norm_slice is None:
                    logger.writerow([patient, idx, "DROP", "low_intensity_range"])
                    continue

                if not passes_quality_checks(norm_slice):
                    logger.writerow([patient, idx, "DROP", "low_nonzero_ratio"])
                    continue

                img = Image.fromarray(norm_slice)
                img = resize_with_padding(img, TARGET_SIZE)

                filename = f"brats_{patient}_slice{idx:03d}.png"
                img.save(os.path.join(OUTPUT_DIR, filename))

                logger.writerow([patient, idx, "KEEP", "ok"])

    print("✅ Extraction complete")
    print(f"📄 Log saved to {log_path}")


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    extract_slices()
