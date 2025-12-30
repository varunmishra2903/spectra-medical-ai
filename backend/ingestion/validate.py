from pathlib import Path
from backend.core.logging import get_logger

logger = get_logger(__name__)

MIN_FILE_SIZE_BYTES = 1024  # 1 KB (defensive minimum)

def validate_file(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError("Provided path is not a file")

    size = path.stat().st_size
    if size < MIN_FILE_SIZE_BYTES:
        raise ValueError("File too small to be a valid medical scan")

    try:
        with open(path, "rb") as f:
            f.read(16)
    except Exception as e:
        raise ValueError(f"File not readable: {e}")

    logger.info(f"File validated: {path.name} ({size} bytes)")
