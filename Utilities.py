from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Iterable


class FFmpegError(RuntimeError):
    pass


def locate_ffmpeg() -> str:
    env_path = os.environ.get("FFMPEG_PATH")
    if env_path and Path(env_path).exists():
        return env_path
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return ffmpeg
    raise FFmpegError("ffmpeg not found. Add it to PATH or set FFMPEG_PATH.")


def locate_ffprobe() -> str:
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        return ffprobe
    ffmpeg_dir = Path(locate_ffmpeg()).parent
    probe_candidate = ffmpeg_dir / "ffprobe.exe"
    if probe_candidate.exists():
        return str(probe_candidate)
    raise FFmpegError("ffprobe not found. Add it to PATH.")


def run_command(cmd: Iterable[str]) -> None:
    result = subprocess.run(list(cmd), capture_output=True, text=True)
    if result.returncode != 0:
        raise FFmpegError(f"Command failed ({result.returncode}): {' '.join(cmd)}\n{result.stderr}")


def run_ffmpeg(args: Iterable[str]) -> None:
    ffmpeg = locate_ffmpeg()
    run_command([ffmpeg, "-y", *list(args)])
