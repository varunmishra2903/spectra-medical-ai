import torch
import torch.nn.functional as F
from torchvision import models

from backend.core.logging import get_logger
from backend.core.config import BONE_MODEL_PATH

logger = get_logger(__name__)

_model = None


def load_bone_model(device: torch.device):
    global _model
    if _model is not None:
        return _model

    logger.info("Loading bone model")

    model = models.resnet18(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, 2)

    state = torch.load(BONE_MODEL_PATH, map_location=device)
    model.load_state_dict(state)
    model.to(device)
    model.eval()

    _model = model
    return _model


def infer_bone(tensor: torch.Tensor, device: torch.device):
    """
    tensor: (3, 224, 224)
    """
    model = load_bone_model(device)

    with torch.no_grad():
        tensor = tensor.unsqueeze(0).to(device)
        logits = model(tensor)
        probs = F.softmax(logits, dim=1)

    confidence = probs.max().item()
    logger.info(f"Bone confidence: {confidence:.3f}")
    return probs
