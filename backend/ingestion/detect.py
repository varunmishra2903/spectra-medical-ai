from pathlib import Path
from backend.core.logging import get_logger

logger = get_logger(__name__)

def detect_file_type(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    name = path.name.lower()

    # ---- NIfTI ----
    if name.endswith(".nii.gz"):
        logger.info("Detected NIfTI (.nii.gz)")
        return "nifti"

    if name.endswith(".nii"):
        logger.info("Detected NIfTI (.nii)")
        return "nifti"

    # ---- DICOM ----
    if name.endswith(".dcm"):
        logger.info("Detected DICOM (.dcm)")
        return "dicom"

    # ---- PNG (Gatekeeper / Preprocessed) ----
    if name.endswith(".png"):
        logger.info("Detected PNG image")
        return "png"

    raise ValueError(f"Unsupported file type: {path.name}")
