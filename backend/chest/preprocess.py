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


# -----------------------------
# Utility functions
# -----------------------------
def apply_lung_window(pixel_array: np.ndarray,
                      center: int = -600,
                      width: int = 1500) -> np.ndarray:
    """
    Apply lung window to DICOM pixel array.
    """
    low = center - width // 2
    high = center + width // 2
    windowed = np.clip(pixel_array, low, high)
    windowed = (windowed - low) / (high - low)
    windowed = (windowed * 255.0).astype(np.uint8)
    return windowed


def load_dicom(path: Path) -> Image.Image:
    ds = pydicom.dcmread(path)
    pixels = ds.pixel_array.astype(np.float32)

    if hasattr(ds, "RescaleSlope"):
        pixels *= float(ds.RescaleSlope)
    if hasattr(ds, "RescaleIntercept"):
        pixels += float(ds.RescaleIntercept)

    windowed = apply_lung_window(pixels)
    return Image.fromarray(windowed).convert("RGB")


def load_png(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")


# -----------------------------
# Main entry
# -----------------------------
def preprocess_chest_image(image_path: Path) -> torch.Tensor:
    """
    Preprocess a chest image for model inference.

    Input:
      DICOM (.dcm) or PNG (.png)

    Output:
      Tensor shape: (3, 224, 224)
    """

    if image_path.suffix.lower() == ".dcm":
        logger.info("Chest preprocessing: DICOM input")
        img = load_dicom(image_path)

    elif image_path.suffix.lower() == ".png":
        logger.info("Chest preprocessing: PNG input")
        img = load_png(image_path)

    else:
        raise ValueError(f"Unsupported chest format: {image_path}")

    tensor = _transform(img)
    logger.info(f"Chest tensor shape: {tuple(tensor.shape)}")

    return tensor
