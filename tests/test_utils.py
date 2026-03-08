import pytest
from unittest.mock import patch
from edl.utils import check_ffmpeg, format_size, safe_filename, get_default_download_dir


class TestCheckFfmpeg:
    def test_both_present(self):
        with patch("shutil.which", return_value="/usr/bin/ffmpeg"):
            assert check_ffmpeg() is True

    def test_ffmpeg_missing(self):
        def which(b):
            return None if b == "ffmpeg" else "/usr/bin/ffprobe"
        with patch("shutil.which", side_effect=which):
            assert check_ffmpeg() is False

    def test_ffprobe_missing(self):
        def which(b):
            return "/usr/bin/ffmpeg" if b == "ffmpeg" else None
        with patch("shutil.which", side_effect=which):
            assert check_ffmpeg() is False

    def test_both_missing(self):
        with patch("shutil.which", return_value=None):
            assert check_ffmpeg() is False


class TestFormatSize:
    def test_bytes(self):
        assert format_size(512) == "512.0 B"

    def test_kilobytes(self):
        assert format_size(1024) == "1.0 KB"

    def test_megabytes(self):
        assert format_size(1024 ** 2) == "1.0 MB"

    def test_gigabytes(self):
        assert format_size(1024 ** 3) == "1.0 GB"

    def test_terabytes(self):
        assert format_size(1024 ** 4) == "1.0 TB"

    def test_zero(self):
        assert format_size(0) == "0.0 B"


class TestSafeFilename:
    def test_strips_invalid_chars(self):
        assert safe_filename('hello<world>') == "hello_world_"

    def test_strips_leading_dots(self):
        assert safe_filename("...file") == "file"

    def test_strips_trailing_spaces(self):
        assert safe_filename("file   ") == "file"

    def test_clean_name_unchanged(self):
        assert safe_filename("my video 1080p") == "my video 1080p"


class TestDefaultDownloadDir:
    def test_returns_path(self, tmp_path, monkeypatch):
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        result = get_default_download_dir()
        assert result.exists()

    def test_creates_dir(self, tmp_path, monkeypatch):
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
        result = get_default_download_dir()
        assert result.name == "Downloads"