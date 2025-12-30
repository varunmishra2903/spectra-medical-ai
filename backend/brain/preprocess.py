from pathlib import Path
import torch
import numpy as np
import nibabel as nib

from monai.transforms import (
    Compose,
    LoadImaged,
    EnsureChannelFirstd,
    Spacingd,
    NormalizeIntensityd,
    CenterSpatialCropd,
    SpatialPadd,
    ToTensord,
)

from backend.core.logging import get_logger

logger = get_logger(__name__)

# -----------------------------
# Locked brain preprocessing config
# -----------------------------
TARGET_SPACING = (1.0, 1.0, 1.0)
TARGET_SIZE = (128, 128, 128)

MODALITIES = ["t1", "t1ce", "t2", "flair"]


def build_brain_preprocess():
    """
    Returns MONAI preprocessing pipeline.
    This MUST match training preprocessing exactly.
    """

    transforms = Compose([
        # Load NIfTI files
        LoadImaged(keys=MODALITIES, image_only=True),

        # (D, H, W) -> (1, D, H, W)
        EnsureChannelFirstd(keys=MODALITIES),

        # Resample to 1mm³
        Spacingd(
            keys=MODALITIES,
            pixdim=TARGET_SPACING,
            mode="bilinear",
        ),

        # Z-score normalization (non-zero voxels only)
        NormalizeIntensityd(
            keys=MODALITIES,
            nonzero=True,
            channel_wise=True,
        ),

        # Center crop
        CenterSpatialCropd(
            keys=MODALITIES,
            roi_size=TARGET_SIZE,
        ),

        # Pad if volume is smaller
        SpatialPadd(
            keys=MODALITIES,
            spatial_size=TARGET_SIZE,
        ),

        # Convert to torch.Tensor
        ToTensord(keys=MODALITIES),
    ])

    return transforms


def preprocess_brain_case(case_dir: Path) -> torch.Tensor:
    """
    Preprocess a single brain case directory.

    Expected files inside case_dir:
      *_t1.nii.gz
      *_t1ce.nii.gz
      *_t2.nii.gz
      *_flair.nii.gz

    Returns:
      Tensor shape: (4, 128, 128, 128)
    """

    # Locate modality files
    data = {}
    for mod in MODALITIES:
        files = list(case_dir.glob(f"*_{mod}.nii*"))
        if len(files) != 1:
            raise FileNotFoundError(f"Expected 1 file for {mod}, found {len(files)}")
        data[mod] = str(files[0])

    logger.info(f"Brain preprocessing started for {case_dir.name}")

    transforms = build_brain_preprocess()
    out = transforms(data)

    # Stack channels: (4, 128, 128, 128)
    tensor = torch.stack([out[m] for m in MODALITIES], dim=0)

    logger.info(f"Brain tensor shape: {tuple(tensor.shape)}")

    return tensor

