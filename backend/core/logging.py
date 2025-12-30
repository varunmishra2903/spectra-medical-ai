import logging
from backend.core.paths import LOG_DIR, ensure_runtime_dirs

_LOGGER_INITIALIZED = False

def setup_logging():
    global _LOGGER_INITIALIZED
    if _LOGGER_INITIALIZED:
        return

    ensure_runtime_dirs()

    log_file = LOG_DIR / "app.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ],
    )

    _LOGGER_INITIALIZED = True


def get_logger(name: str) -> logging.Logger:
    setup_logging()
    return logging.getLogger(name)

