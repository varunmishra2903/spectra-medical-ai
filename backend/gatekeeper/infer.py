import torch
import torch.nn.functional as F

from backend.core.logging import get_logger
from backend.core.config import GATEKEEPER_CONFIDENCE_THRESHOLD
from backend.gatekeeper.model import load_gatekeeper_model

logger = get_logger(__name__)

LABELS = ["brain", "chest", "bone"]


def gatekeeper_infer(batch: torch.Tensor, device: torch.device) -> str:
    """
    batch: (N, 3, 224, 224)
    returns: brain | chest | bone | ambiguous
    """

    model = load_gatekeeper_model(device)

    with torch.no_grad():
        batch = batch.to(device)
        logits = model(batch)
        probs = F.softmax(logits, dim=1)

    # Aggregate across slices
    mean_probs = probs.mean(dim=0)
    confidence, pred_idx = torch.max(mean_probs, dim=0)

    confidence = confidence.item()
    pred_idx = pred_idx.item()

    logger.info(f"Gatekeeper confidence: {confidence:.3f}")

    if confidence < GATEKEEPER_CONFIDENCE_THRESHOLD:
        logger.warning("Gatekeeper result ambiguous")
        return "ambiguous"

    return LABELS[pred_idx]
