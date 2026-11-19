from __future__ import annotations

from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("outputs")

def save_output(image_bytes: bytes) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"edited_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = OUTPUT_DIR / filename
    path.write_bytes(image_bytes)
    return str(path)
