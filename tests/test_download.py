import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from edl.download import build_ydl_opts, AUDIO_FORMATS, VIDEO_QUALITIES


class TestBuildYdlOpts:
    def test_default_video_format(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path)
        assert "bestvideo" in opts["format"]
        assert "2160" in opts["format"]

    def test_quality_1080(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path, max_quality=1080)
        assert "1080" in opts["format"]

    def test_quality_720(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path, max_quality=720)
        assert "720" in opts["format"]

    def test_audio_mp3(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path, audio="mp3")
        assert opts["format"] == "bestaudio/best"
        pp_keys = [p["key"] for p in opts.get("postprocessors", [])]
        assert "FFmpegExtractAudio" in pp_keys

    def test_audio_flac(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path, audio="flac")
        pp = {p["key"]: p for p in opts.get("postprocessors", [])}
        assert pp["FFmpegExtractAudio"]["preferredcodec"] == "flac"

    def test_embed_art_default(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path, audio="mp3", embed_art=True)
        pp_keys = [p["key"] for p in opts.get("postprocessors", [])]
        assert "EmbedThumbnail" in pp_keys

    def test_no_embed_art(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path, audio="mp3", embed_art=False)
        pp_keys = [p["key"] for p in opts.get("postprocessors", [])]
        assert "EmbedThumbnail" not in pp_keys

    def test_sponsorblock(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path, sponsorblock=True)
        pp_keys = [p["key"] for p in opts.get("postprocessors", [])]
        assert "SponsorBlock" in pp_keys

    def test_subtitles(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path, subtitles=True)
        assert opts.get("writesubtitles") is True
        pp_keys = [p["key"] for p in opts.get("postprocessors", [])]
        assert "FFmpegEmbedSubtitle" in pp_keys

    def test_cookies_file(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path, cookies="/tmp/cookies.txt")
        assert opts["cookiefile"] == "/tmp/cookies.txt"

    def test_cookies_from_browser(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path, cookies_from_browser="chrome")
        assert opts["cookiesfrombrowser"] == ("chrome",)

    def test_auth_injected(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path, username="user", password="pass")
        assert opts["username"] == "user"
        assert opts["password"] == "pass"

    def test_no_auth_when_none(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path)
        assert "username" not in opts
        assert "password" not in opts

    def test_playlist_flag(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path, playlist=True)
        assert opts["noplaylist"] is False

    def test_no_playlist_by_default(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path)
        assert opts["noplaylist"] is True

    def test_custom_template(self, tmp_path):
        opts = build_ydl_opts(out=tmp_path, filename_template="%(id)s.%(ext)s")
        assert "%(id)s.%(ext)s" in opts["outtmpl"]