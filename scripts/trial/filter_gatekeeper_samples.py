import os
import numpy as np
from PIL import Image

# ================= CONFIG =================
DATASETS = {
    "brain": {
        "path": "data/gatekeeper/organamnist",
        "min_ratio": 0.10,
    },
    "chest": {
        "path": "data/gatekeeper/pneumoniamnist",
        "min_ratio": 0.07,
    },
    "bone": {
        "path": "data/gatekeeper/fracturemnist3d",
        "min_ratio": 0.05,
    },
}

LOG_PATH = "docs/gatekeeper_filter_log.txt"
# =========================================

os.makedirs("docs", exist_ok=True)

def nonzero_ratio(img_array):
    return np.count_nonzero(img_array) / img_array.size

log_lines = []
log_lines.append("GATEKEEPER SAMPLE FILTERING LOG\n")

for name, cfg in DATASETS.items():
    input_dir = cfg["path"]
    threshold = cfg["min_ratio"]

    kept = []
    discarded = []

    log_lines.append(f"\n=== {name.upper()} ===")
    log_lines.append(f"Path: {input_dir}")
    log_lines.append(f"Threshold (nonzero ratio): {threshold}\n")

    for fname in sorted(os.listdir(input_dir)):
        if not fname.lower().endswith(".png"):
            continue

        file_path = os.path.join(input_dir, fname)

        img = Image.open(file_path).convert("L")
        arr = np.array(img)

        ratio = nonzero_ratio(arr)

        if ratio >= threshold:
            kept.append((fname, ratio))
        else:
            os.remove(file_path)
            discarded.append((fname, ratio))

    # ---------- Console Summary ----------
    print(f"\n✅ {name.upper()} filtering complete")
    print(f"Kept: {len(kept)} | Discarded: {len(discarded)}")

    # ---------- Log ----------
    log_lines.append(f"Kept samples: {len(kept)}")
    log_lines.append(f"Discarded samples: {len(discarded)}\n")

    log_lines.append("Examples kept:")
    for f, r in kept[:5]:
        log_lines.append(f"  {f} | nonzero ratio = {r:.4f}")

    log_lines.append("\nExamples discarded:")
    for f, r in discarded[:5]:
        log_lines.append(f"  {f} | nonzero ratio = {r:.4f}")

    log_lines.append("\n")

# ================= WRITE LOG =================
with open(LOG_PATH, "w") as f:
    f.write("\n".join(log_lines))

print("\n📄 Full filtering log written to:", LOG_PATH)
