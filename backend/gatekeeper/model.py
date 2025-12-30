import torch
from torchvision import models
from backend.core.logging import get_logger
from backend.core.config import GATEKEEPER_MODEL

logger = get_logger(__name__)

_model = None


def load_gatekeeper_model(device: torch.device):
    global _model

    if _model is not None:
        return _model

    logger.info("Loading Gatekeeper model")

    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = torch.nn.Linear(
        model.last_channel, 3  # brain, chest, bone
    )

    state = torch.load(GATEKEEPER_MODEL, map_location=device)
    model.load_state_dict(state)

    model.to(device)
    model.eval()

    _model = model
    logger.info("Gatekeeper model loaded and ready")
    return _model
