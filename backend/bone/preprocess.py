from pathlib import Path
import numpy as np
import torch
from PIL import Image
import pydicom
from torchvision import transforms

from backend.core.logging import get_logger

logger = get_logger(__name__)

# -----------------------------
# Locked constants
# -----------------------------
IMG_SIZE = 224
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])


def load_dicom(path: Path) -> Image.Image:
    ds = pydicom.dcmread(path)
    pixels = ds.pixel_array.astype(np.float32)

    if hasattr(ds, "RescaleSlope"):
        pixels *= float(ds.RescaleSlope)
    if hasattr(ds, "RescaleIntercept"):
        pixels += float(ds.RescaleIntercept)

    # Percentile clipping (bone-safe)
    p1, p99 = np.percentile(pixels, (1, 99))
    pixels = np.clip(pixels, p1, p99)
    pixels = (pixels - p1) / (p99 - p1 + 1e-6)
    pixels = (pixels * 255.0).astype(np.uint8)

    return Image.fromarray(pixels).convert("RGB")


def load_png(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")


def preprocess_bone_image(image_path: Path) -> torch.Tensor:
    """
    Preprocess bone X-ray image.

    Input:
      DICOM or PNG

    Output:
      Tensor shape: (3, 224, 224)
    """

    if image_path.suffix.lower() == ".dcm":
        logger.info("Bone preprocessing: DICOM input")
        img = load_dicom(image_path)

    elif image_path.suffix.lower() == ".png":
        logger.info("Bone preprocessing: PNG input")
        img = load_png(image_path)

    else:
        raise ValueError(f"Unsupported bone format: {image_path}")

    tensor = _transform(img)
    logger.info(f"Bone tensor shape: {tuple(tensor.shape)}")
    return tensor
