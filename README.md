<div align="center">

# ⬇️ edl

**a better video downloader.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

`edl` is a yt-dlp CLI wrapper that cuts the noise. 4K video, lossless audio, SponsorBlock, playlist concurrency, and browser cookie support — all from one clean command.

</div>

---

## 📦 Installation

```bash
pip install git+https://github.com/osfv/clidownloader.git
```

> Requires **Python 3.10+** and **pip 21+**

### FFmpeg (required for audio & subtitles)

| Platform | Command |
|----------|---------|
| Ubuntu / Debian | `sudo apt install ffmpeg` |
| macOS | `brew install ffmpeg` |
| Windows | [ffmpeg.org/download.html](https://ffmpeg.org/download.html) |

---

## 🚀 Usage

```bash
# Check status
edl status

# Authenticate (credentials stored in system keyring)
edl login
edl logout
```

### Downloading

```bash
# Download video in best quality (up to 4K)
edl dl https://youtube.com/watch?v=example

# Download as MP3 with embedded album art
edl dl https://youtube.com/watch?v=example --audio mp3

# Download lossless audio
edl dl https://youtube.com/watch?v=example --audio flac

# Download at a specific resolution
edl dl https://youtube.com/watch?v=example --quality 1080

# Download a full playlist
edl dl https://youtube.com/playlist?list=example --playlist

# Download playlist with 4 parallel workers
edl dl https://youtube.com/playlist?list=example --playlist --concurrent 4

# Skip sponsor segments automatically
edl dl https://youtube.com/watch?v=example --sponsorblock

# Embed subtitles
edl dl https://youtube.com/watch?v=example --subtitles

# Use cookies from your browser (for age-restricted / members-only content)
edl dl https://youtube.com/watch?v=example --cookies-from-browser chrome

# Save to a custom output directory
edl dl https://youtube.com/watch?v=example --out ~/videos
```

---

## ✨ Features

- 🔐 **Secure auth** — credentials stored in your system keyring, never in plaintext
- 🎬 **4K/1440p/1080p/720p** video download
- 🎵 **Audio extraction** — MP3, FLAC, Opus, M4A, WAV with embedded album art
- 📃 **Playlist support** — download entire playlists with optional concurrency
- 🚫 **SponsorBlock** — auto-skip sponsors, self-promos, and interaction reminders
- 💬 **Subtitle embedding** — bake subs directly into the output
- 🍪 **Browser cookies** — Chrome, Firefox, Safari, Edge, Brave
- 📊 **Rich terminal UI** — progress bars and clean output via [rich](https://github.com/Textualize/rich)
- 🖥️ **Cross-platform** — Linux, macOS, Windows

---

## 🗂️ Project Structure

```
clidownloader/
├── edl/                # Core package
├── tests/              # Test suite
├── pyproject.toml      # Project metadata & build config
├── requirements.txt    # Runtime dependencies
└── requirements-dev.txt  # Dev dependencies
```

---

## 🤝 Contributing

1. Fork the repo
2. Install dev dependencies: `pip install -r requirements-dev.txt`
3. Make your changes and add tests
4. Open a pull request

---

## 📄 License

MIT.
