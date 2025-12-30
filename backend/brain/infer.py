import torch
from monai.networks.nets import UNet

from backend.core.logging import get_logger
from backend.core.config import BRAIN_MODEL_PATH

logger = get_logger(__name__)

_model = None


def load_brain_model(device: torch.device):
    global _model
    if _model is not None:
        return _model

    logger.info("Loading brain model")

    model = UNet(
        spatial_dims=3,
        in_channels=4,
        out_channels=3,
        channels=(16, 32, 64, 128, 256),
        strides=(2, 2, 2, 2),
    )

    state = torch.load(BRAIN_MODEL_PATH, map_location=device)
    model.load_state_dict(state)
    model.to(device)
    model.eval()

    _model = model
    return _model


def infer_brain(volume: torch.Tensor, device: torch.device):
    """
    volume: (1, 4, 128, 128, 128)
    """
    model = load_brain_model(device)

    with torch.no_grad():
        volume = volume.to(device)
        logits = model(volume)

    logger.info(f"Brain logits shape: {tuple(logits.shape)}")
    return logits


