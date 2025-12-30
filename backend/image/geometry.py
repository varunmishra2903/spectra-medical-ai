from backend.core.logging import get_logger

logger = get_logger(__name__)


def slice_index_to_depth(index: int, spacing_z: float) -> float:
    """
    Convert slice index to real-world depth (mm).
    """
    depth = index * spacing_z
    logger.info(f"Slice {index} -> depth {depth} mm")
    return depth
