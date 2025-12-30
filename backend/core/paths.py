from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
RUNTIME_ROOT = REPO_ROOT / "runtime"

LOG_DIR = RUNTIME_ROOT / "logs"
CASE_DIR = RUNTIME_ROOT / "cases"
TEMP_DIR = RUNTIME_ROOT / "tmp"

def ensure_runtime_dirs():
    for p in [LOG_DIR, CASE_DIR, TEMP_DIR]:
        p.mkdir(parents=True, exist_ok=True)

