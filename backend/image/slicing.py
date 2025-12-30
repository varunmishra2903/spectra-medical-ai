import numpy as np
from backend.core.logging import get_logger

logger = get_logger(__name__)


def get_axial_slice(volume: np.ndarray, index: int) -> np.ndarray:
    """
    Extract axial slice safely.
    """
    if volume.ndim != 3:
        raise ValueError("Expected 3D volume for axial slicing")

    max_index = volume.shape[2] - 1
    if index < 0 or index > max_index:
        raise IndexError(f"Slice index out of bounds: {index}")

    slice_ = volume[:, :, index]
    logger.info(f"Axial slice extracted at index {index}")
    return slice_
