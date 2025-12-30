from pathlib import Path
import numpy as np
from PIL import Image
import torch
from torchvision import transforms

from backend.core.logging import get_logger
from backend.image.slicing import get_axial_slice

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
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
])


def _to_rgb(pil_img: Image.Image) -> Image.Image:
    if pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")
    return pil_img


def preprocess_slice(slice_2d: np.ndarray) -> torch.Tensor:
    """
    Preprocess a single axial slice into a gatekeeper tensor.
    """
    # Normalize to 0–255 safely
    slice_2d = slice_2d.astype(np.float32)
    slice_2d -= slice_2d.min()
    if slice_2d.max() > 0:
        slice_2d /= slice_2d.max()
    slice_2d *= 255.0

    slice_2d = slice_2d.astype(np.uint8)

    pil = Image.fromarray(slice_2d)
    pil = _to_rgb(pil)

    tensor = _transform(pil)
    return tensor


def select_middle_slices(volume: np.ndarray, k: int = 3):
    """
    Deterministically select middle ±k axial slices.
    """
    z = volume.shape[2]
    center = z // 2
    indices = list(range(center - k, center + k + 1))

    valid = [i for i in indices if 0 <= i < z]
    logger.info(f"Selected slices: {valid}")
    return valid


def preprocess_volume(volume: np.ndarray) -> torch.Tensor:
    """
    Full gatekeeper preprocessing for a volume.
    Returns tensor of shape (N, 3, 224, 224)
    """
    tensors = []
    indices = select_middle_slices(volume)

    for idx in indices:
        slice_ = get_axial_slice(volume, idx)
        tensor = preprocess_slice(slice_)
        tensors.append(tensor)

    batch = torch.stack(tensors, dim=0)
    logger.info(f"Gatekeeper batch shape: {batch.shape}")
    return batch
