import shutil
import tempfile
from pathlib import Path

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def safe_copy(src: Path, dst: Path):
    ensure_dir(dst.parent)
    shutil.copy2(src, dst)


def atomic_write(path: Path, data: bytes):
    ensure_dir(path.parent)

    with tempfile.NamedTemporaryFile(delete=False, dir=path.parent) as tmp:
        tmp.write(data)
        tmp.flush()
        temp_path = Path(tmp.name)

    temp_path.replace(path)

