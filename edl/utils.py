import shutil
from pathlib import Path
from typing import Optional
from edl.colors import error, info


def check_ffmpeg() -> bool:
    """Return True if ffmpeg and ffprobe are on PATH."""
    missing = [b for b in ("ffmpeg", "ffprobe") if not shutil.which(b)]
    if missing:
        error(f"missing required binaries: {', '.join(missing)}")
        info("install ffmpeg:")
        info("  ubuntu/debian : sudo apt install ffmpeg")
        info("  macos         : brew install ffmpeg")
        info("  windows       : https://ffmpeg.org/download.html")
        return False
    return True


def get_default_download_dir() -> Path:
    """Return ~/Downloads, creating it if necessary."""
    d = Path.home() / "Downloads"
    d.mkdir(parents=True, exist_ok=True)
    return d


def format_size(num_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num_bytes < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"


def safe_filename(name: str) -> str:
    for ch in r'<>:"/\\|?*':
        name = name.replace(ch, "_")
    return name.strip(" .")
