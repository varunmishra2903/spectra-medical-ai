import os
import shutil
import numpy as np
from PIL import Image

# ================= CONFIG =================
INPUT_DIR = "data/gatekeeper/fracturemnist3d"
MIN_NONZERO_RATIO = 0.05  # 5% minimum anatomical signal
LOG_PATH = "docs/dataset_preprocessing/gatekeeper_bone_filter_log.txt"
# =========================================

os.makedirs("docs", exist_ok=True)

kept = []
discarded = []

def nonzero_ratio(img_array):
    return np.count_nonzero(img_array) / img_array.size

for fname in sorted(os.listdir(INPUT_DIR)):
    if not fname.lower().endswith(".png"):
        continue

    file_path = os.path.join(INPUT_DIR, fname)

    img = Image.open(file_path).convert("L")
    arr = np.array(img)

    ratio = nonzero_ratio(arr)

    if ratio >= MIN_NONZERO_RATIO:
        kept.append((fname, ratio))
    else:
        os.remove(file_path)  # ❗ remove low-signal image
        discarded.append((fname, ratio))

# ================= REPORT =================
print("✅ Gatekeeper Bone Filtering Complete\n")

print(f"Kept samples: {len(kept)}")
print(f"Discarded samples: {len(discarded)}\n")

print("Examples kept:")
for f, r in kept[:5]:
    print(f"  {f}  | nonzero ratio = {r:.3f}")

print("\nExamples discarded:")
for f, r in discarded[:5]:
    print(f"  {f}  | nonzero ratio = {r:.3f}")

# ================= LOG =================
with open(LOG_PATH, "w") as f:
    f.write("GATEKEEPER BONE FILTER LOG\n")
    f.write(f"Threshold (nonzero ratio): {MIN_NONZERO_RATIO}\n\n")

    f.write("KEPT FILES:\n")
    for name, r in kept:
        f.write(f"{name}, {r:.4f}\n")

    f.write("\nDISCARDED FILES:\n")
    for name, r in discarded:
        f.write(f"{name}, {r:.4f}\n")
