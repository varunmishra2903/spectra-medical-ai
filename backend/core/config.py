from pathlib import Path
from backend.core.paths import REPO_ROOT

# ------------------
# Model paths
# ------------------
MODELS_DIR = REPO_ROOT / "models"

GATEKEEPER_MODEL = MODELS_DIR / "gatekeeper.pth"
BRAIN_MODEL = MODELS_DIR / "brain_unet.pth"
CHEST_MODEL = MODELS_DIR / "chest_model.pth"
BONE_MODEL = MODELS_DIR / "bone_model.pth"

# ------------------
# Thresholds
# ------------------
GATEKEEPER_CONFIDENCE_THRESHOLD = 0.65

# ------------------
# Runtime behavior
# ------------------
MAX_UPLOAD_MB = 500
TEMP_FILE_SUFFIX = ".tmp"

# ------------------
# Versioning
# ------------------
BACKEND_VERSION = "0.1.0"
