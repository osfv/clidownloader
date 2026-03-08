import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock


@pytest.fixture
def tmp_config(tmp_path, monkeypatch):
    """Redirect config to a temp dir."""
    monkeypatch.setattr("edl.auth.get_config_dir", lambda: tmp_path)
    return tmp_path


@pytest.fixture
def fake_args():
    args = MagicMock()
    args.out = "./test_downloads"
    args.filename_template = "%(title)s [%(id)s].%(ext)s"
    args.playlist = False
    args.audio = None
    args.embed_art = True
    args.max_quality = 2160
    args.cookies = None
    args.cookies_from_browser = None
    args.sponsorblock = False
    args.subtitles = False
    args.username = None
    args.password = None
    return args