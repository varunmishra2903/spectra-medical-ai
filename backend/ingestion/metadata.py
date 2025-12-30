from dataclasses import dataclass
from pathlib import Path
import pydicom
import nibabel as nib

from backend.core.logging import get_logger

logger = get_logger(__name__)

@dataclass(frozen=True)
class CaseInfo:
    case_id: str
    file_path: Path
    file_type: str
    metadata: dict


def extract_metadata(path: Path, file_type: str) -> dict:
    if file_type == "dicom":
        ds = pydicom.dcmread(path, stop_before_pixels=True)

        meta = {
            "modality": getattr(ds, "Modality", None),
            "pixel_spacing": getattr(ds, "PixelSpacing", None),
            "slice_thickness": getattr(ds, "SliceThickness", None),
            "rows": getattr(ds, "Rows", None),
            "columns": getattr(ds, "Columns", None),
        }

        logger.info("DICOM metadata extracted (no pixels)")
        return meta

    if file_type == "nifti":
        img = nib.load(str(path))  # header only
        hdr = img.header

        meta = {
            "shape": img.shape,
            "voxel_spacing": hdr.get_zooms(),
            "affine": img.affine.tolist(),
        }

        logger.info("NIfTI metadata extracted (no pixels)")
        return meta

    raise ValueError(f"Unknown file type: {file_type}")
