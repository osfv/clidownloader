from __future__ import annotations

from pathlib import Path
from typing import Optional

import yt_dlp
from rich.progress import (
    BarColumn, DownloadColumn, Progress, SpinnerColumn,
    TextColumn, TimeRemainingColumn, TransferSpeedColumn,
)

from edl.colors import console, error, info, success, warn
from edl.utils import check_ffmpeg

AUDIO_FORMATS = ("mp3", "m4a", "opus", "flac", "wav")
VIDEO_QUALITIES = (2160, 1440, 1080, 720, 480, 360)


def _make_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
    )


def build_ydl_opts(*, out, audio=None, embed_art=True, max_quality=2160,
                   playlist=False, filename_template="%(title)s [%(id)s].%(ext)s",
                   cookies=None, cookies_from_browser=None, sponsorblock=False,
                   subtitles=False, username=None, password=None,
                   progress=None, task_id=None) -> dict:
    out.mkdir(parents=True, exist_ok=True)

    def _hook(d):
        if progress is None or task_id is None:
            return
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            done = d.get("downloaded_bytes", 0)
            if total:
                progress.update(task_id, completed=done, total=total)
        elif d["status"] == "finished":
            if total := d.get("total_bytes"):
                progress.update(task_id, completed=total, total=total)

    opts = {
        "outtmpl": str(out / filename_template),
        "progress_hooks": [_hook],
        "quiet": True,
        "no_warnings": True,
        "noplaylist": not playlist,
    }

    if username and password:
        opts["username"] = username
        opts["password"] = password
    if cookies:
        opts["cookiefile"] = cookies
    if cookies_from_browser:
        opts["cookiesfrombrowser"] = (cookies_from_browser,)

    postprocessors = []

    if audio:
        opts["format"] = "bestaudio/best"
        postprocessors.append({"key": "FFmpegExtractAudio", "preferredcodec": audio, "preferredquality": "0"})
        if embed_art:
            opts["writethumbnail"] = True
            postprocessors += [{"key": "EmbedThumbnail"}, {"key": "FFmpegMetadata", "add_metadata": True}]
    else:
        q = max_quality
        opts["format"] = (
            f"bestvideo[height<={q}][ext=mp4]+bestaudio[ext=m4a]"
            f"/bestvideo[height<={q}]+bestaudio"
            f"/best[height<={q}]"
        )
        if subtitles:
            opts["writesubtitles"] = True
            opts["subtitleslangs"] = ["en"]
            postprocessors.append({"key": "FFmpegEmbedSubtitle"})

    if sponsorblock:
        postprocessors.append({"key": "SponsorBlock", "categories": ["sponsor", "selfpromo", "interaction"]})
        postprocessors.append({"key": "ModifyChapters", "remove_sponsor_segments": ["sponsor", "selfpromo", "interaction"]})

    if postprocessors:
        opts["postprocessors"] = postprocessors

    return opts


def download(url, *, out, audio=None, embed_art=True, max_quality=2160,
             playlist=False, filename_template="%(title)s [%(id)s].%(ext)s",
             cookies=None, cookies_from_browser=None, sponsorblock=False,
             subtitles=False, username=None, password=None,
             concurrent_downloads=1) -> bool:
    if audio and not check_ffmpeg():
        return False

    with _make_progress() as prog:
        task_id = prog.add_task("downloading...", total=None)
        opts = build_ydl_opts(
            out=out, audio=audio, embed_art=embed_art, max_quality=max_quality,
            playlist=playlist, filename_template=filename_template,
            cookies=cookies, cookies_from_browser=cookies_from_browser,
            sponsorblock=sponsorblock, subtitles=subtitles,
            username=username, password=password, progress=prog, task_id=task_id,
        )

        if concurrent_downloads > 1 and playlist:
            opts["concurrent_fragment_downloads"] = concurrent_downloads

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                title = info_dict.get("title", url)
                prog.update(task_id, description=f"[cyan]{title[:60]}[/cyan]")

                if not playlist and info_dict.get("_type") == "playlist":
                    error("this is a playlist — add --playlist to download all items")
                    return False

                ydl.download([url])

        except yt_dlp.utils.DownloadError as e:
            error(f"download failed: {e}")
            return False
        except Exception as e:
            error(f"unexpected error: {e}")
            return False

    success(f"done: {title}")
    return True