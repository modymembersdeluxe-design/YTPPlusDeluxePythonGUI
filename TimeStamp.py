from __future__ import annotations

from datetime import datetime
from pathlib import Path


def make_output_path(input_path: str, suffix: str = "_ytp_deluxe", ext: str | None = None) -> str:
    src = Path(input_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_ext = ext if ext else src.suffix or ".mp4"
    return str(src.with_name(f"{src.stem}{suffix}_{timestamp}{final_ext}"))
