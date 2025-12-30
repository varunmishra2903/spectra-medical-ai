import torch
import numpy as np
from scipy.ndimage import label

from backend.core.logging import get_logger

logger = get_logger(__name__)

# -----------------------------
# 9.1 Brain aggregation
# -----------------------------
def postprocess_brain_logits(
    logits: torch.Tensor,
    min_voxels: int = 500
):
    """
    logits: (1, 3, D, H, W)
    returns: cleaned_mask, confidence
    """

    probs = torch.softmax(logits, dim=1)
    pred = torch.argmax(probs, dim=1)[0]  # (D, H, W)

    cleaned = torch.zeros_like(pred)
    confidence = 0.0

    for cls in [1, 2]:  # tumor classes only
        mask = (pred == cls).cpu().numpy()
        labeled, num = label(mask)

        for i in range(1, num + 1):
            region = (labeled == i)
            if region.sum() >= min_voxels:
                cleaned[region] = cls
                confidence = max(
                    confidence,
                    probs[0, cls][region].mean().item()
                )

    logger.info(f"Brain postprocess confidence: {confidence:.3f}")
    return cleaned, confidence


# -----------------------------
# 9.2 Chest aggregation
# -----------------------------
def postprocess_chest_probs(mean_probs: torch.Tensor):
    """
    mean_probs: (2,)
    returns: probs, confidence
    """
    confidence = mean_probs.max().item()
    logger.info(f"Chest postprocess confidence: {confidence:.3f}")
    return mean_probs, confidence


# -----------------------------
# 9.3 Bone aggregation
# -----------------------------
def postprocess_bone_probs(probs: torch.Tensor):
    """
    probs: (2,) or (1, 2)
    returns: probs, confidence
    """
    if probs.ndim == 2:
        probs = probs.squeeze(0)

    confidence = probs.max().item()
    logger.info(f"Bone postprocess confidence: {confidence:.3f}")
    return probs, confidence

