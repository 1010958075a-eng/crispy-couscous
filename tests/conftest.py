import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

for p in (PROJECT_ROOT, SRC_PATH):
    sp = str(p)
    if sp not in sys.path:
        sys.path.insert(0, sp)
