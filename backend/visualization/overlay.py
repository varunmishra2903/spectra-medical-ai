import numpy as np
import cv2
from typing import Tuple, Optional

from backend.core.logging import get_logger

logger = get_logger(__name__)

# ============================================================
# PHASE 10.1 — BRAIN OVERLAY (MASK → CONTOURS)
# ============================================================

def overlay_brain_mask(
    image: np.ndarray,
    mask: np.ndarray,
    color: Tuple[int, int, int] = (255, 0, 0),
    thickness: int = 2
) -> np.ndarray:
    """
    Draw tumor contours on a brain MRI slice.

    Parameters
    ----------
    image : np.ndarray
        Shape (H, W) or (H, W, 3), dtype uint8
    mask : np.ndarray
        Shape (H, W), integer labels
    color : tuple
        RGB color for contour (default red)
    thickness : int
        Contour thickness

    Returns
    -------
    overlay : np.ndarray
        RGB image with contours
    """

    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    overlay = image.copy()

    # Any non-zero label = tumor
    binary = (mask > 0).astype(np.uint8) * 255

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cv2.drawContours(
        overlay,
        contours,
        contourIdx=-1,
        color=color,
        thickness=thickness
    )

    logger.info(f"Brain overlay drawn | contours={len(contours)}")
    return overlay


# ============================================================
# PHASE 10.2 — CHEST OVERLAY (HEATMAP STUB)
# ============================================================

def overlay_chest_heatmap(
    image: np.ndarray,
    heatmap: Optional[np.ndarray] = None,
    alpha: float = 0.4
) -> np.ndarray:
    """
    Overlay chest heatmap (placeholder for Grad-CAM).

    Parameters
    ----------
    image : np.ndarray
        RGB image (H, W, 3), uint8
    heatmap : np.ndarray or None
        (H, W) float heatmap, optional
    alpha : float
        Heatmap blending factor

    Returns
    -------
    overlay : np.ndarray
        RGB image
    """

    # For now: return image unchanged
    # This is intentionally a stub for future CAM logic
    logger.info("Chest overlay generated (stub)")
    return image


# ============================================================
# PHASE 10.3 — BONE OVERLAY (ATTENTION STUB)
# ============================================================

def overlay_bone_attention(
    image: np.ndarray,
    attention: Optional[np.ndarray] = None,
    alpha: float = 0.4
) -> np.ndarray:
    """
    Overlay bone attention map (placeholder).

    Parameters
    ----------
    image : np.ndarray
        RGB image (H, W, 3), uint8
    attention : np.ndarray or None
        (H, W) attention map, optional
    alpha : float
        Blending factor

    Returns
    -------
    overlay : np.ndarray
        RGB image
    """

    # For now: return image unchanged
    logger.info("Bone overlay generated (stub)")
    return image

