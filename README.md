# edl

edgy youtube downloader — 4k, mp3+art, lossless, sponsorblock, playlists

## installation

```bash
pip install edl
```

## requirements

- python 3.10+
- ffmpeg / ffprobe (for audio conversion, subtitle embedding, album art)
  - ubuntu/debian: `sudo apt install ffmpeg`
  - macos: `brew install ffmpeg`
  - windows: https://ffmpeg.org/download.html

## usage

```bash
# show status
edl status

# login (stores credentials in system keyring)
edl login

# logout
edl logout

# download video in 4k
edl dl https://youtube.com/watch?v=example

# download as mp3 with embedded album art
edl dl https://youtube.com/watch?v=example --audio mp3

# download in 1080p
edl dl https://youtube.com/watch?v=example --quality 1080

# download lossless audio
edl dl https://youtube.com/watch?v=example --audio flac

# download full playlist
edl dl https://youtube.com/playlist?list=example --playlist

# skip sponsor segments automatically
edl dl https://youtube.com/watch?v=example --sponsorblock

# embed subtitles
edl dl https://youtube.com/watch?v=example --subtitles

# use cookies from your browser
edl dl https://youtube.com/watch?v=example --cookies-from-browser chrome

# parallel playlist download (4 workers)
edl dl https://youtube.com/playlist?list=example --playlist --concurrent 4

# custom output directory
edl dl https://youtube.com/watch?v=example --out ~/videos
```

## features

- secure credential storage via system keyring
- 4k / 1440p / 1080p / 720p video download
- audio extraction (mp3, flac, opus, m4a, wav) with embedded album art
- playlist downloads with optional concurrency
- sponsorblock integration (auto-skip sponsors, self-promos, interactions)
- subtitle embedding
- browser cookie extraction (chrome, firefox, safari, edge, brave)
- beautiful rich terminal output with progress bars
- cross-platform config management (linux/macos/windows)
