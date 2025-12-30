import torch
import torch.nn.functional as F
from torchvision import models

from backend.core.logging import get_logger
from backend.core.config import CHEST_MODEL_PATH

logger = get_logger(__name__)

_model = None


def load_chest_model(device: torch.device):
    global _model
    if _model is not None:
        return _model

    logger.info("Loading chest model")

    model = models.densenet121(weights=None)
    model.classifier = torch.nn.Linear(
        model.classifier.in_features, 2
    )

    state = torch.load(CHEST_MODEL_PATH, map_location=device)
    model.load_state_dict(state)
    model.to(device)
    model.eval()

    _model = model
    return _model


def infer_chest(batch: torch.Tensor, device: torch.device):
    """
    batch: (N, 3, 224, 224)
    """
    model = load_chest_model(device)

    with torch.no_grad():
        batch = batch.to(device)
        logits = model(batch)
        probs = F.softmax(logits, dim=1)

    mean_probs = probs.mean(dim=0)
    confidence = mean_probs.max().item()

    logger.info(f"Chest confidence: {confidence:.3f}")
    return mean_probs
