from __future__ import annotations

import getpass
import sys
from pathlib import Path
from typing import Optional

import click

from edl.auth import (
    delete_credentials,
    get_credentials,
    get_stored_username,
    is_logged_in,
    store_password,
    store_username,
)
from edl.colors import console, error, info, print_banner, success, warn
from edl.download import AUDIO_FORMATS, VIDEO_QUALITIES, download
from edl.utils import get_default_download_dir


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """edl \u2014 edgy youtube downloader"""
    print_banner()
    if ctx.invoked_subcommand is None:
        if is_logged_in():
            info(f"logged in as [accent]{get_stored_username()}[/accent]")
        else:
            warn("not logged in. run [accent]edl login[/accent] to authenticate")
        click.echo(ctx.get_help())


@cli.command()
def login() -> None:
    """Store YouTube credentials securely."""
    info("enter your youtube credentials")
    try:
        username = click.prompt("username").strip()
        if not username:
            error("username cannot be empty")
            sys.exit(1)
        password = getpass.getpass("password: ")
        if not password:
            error("password cannot be empty")
            sys.exit(1)
    except KeyboardInterrupt:
        error("\nlogin cancelled")
        sys.exit(1)

    ok_u = store_username(username)
    ok_p = store_password(username, password)
    if ok_u and ok_p:
        success(f"logged in as {username}")
    else:
        error("failed to store credentials")
        sys.exit(1)


@cli.command()
def logout() -> None:
    """Remove stored credentials."""
    username = get_stored_username()
    if not username:
        warn("not logged in")
        return
    if delete_credentials(username):
        success(f"logged out ({username})")
    else:
        error("failed to remove credentials")


@cli.command()
def status() -> None:
    """Show login state and config location."""
    from edl.auth import get_config_path
    if is_logged_in():
        success(f"logged in as [accent]{get_stored_username()}[/accent]")
    else:
        warn("not logged in")
    info(f"config: [muted]{get_config_path()}[/muted]")


@cli.command()
@click.argument("url")
@click.option("--playlist", is_flag=True, help="Download entire playlist")
@click.option("--audio", type=click.Choice(AUDIO_FORMATS), default=None, help="Extract audio in given format")
@click.option("--no-art", is_flag=True, help="Skip embedding album art")
@click.option("--quality", type=click.Choice([str(q) for q in VIDEO_QUALITIES]), default="2160", show_default=True, help="Max video quality (height)")
@click.option("--out", type=click.Path(), default=None, help="Output directory (default: ~/Downloads)")
@click.option("--template", default="%(title)s [%(id)s].%(ext)s", show_default=True, help="yt-dlp filename template")
@click.option("--cookies", type=click.Path(exists=True), help="Cookies file path")
@click.option("--cookies-from-browser", type=click.Choice(["chrome", "firefox", "safari", "edge", "brave"]), default=None, help="Extract cookies from browser")
@click.option("--sponsorblock", is_flag=True, help="Skip sponsor segments via SponsorBlock")
@click.option("--subtitles", is_flag=True, help="Embed English subtitles (video only)")
@click.option("--concurrent", type=click.IntRange(1, 16), default=1, show_default=True, help="Parallel fragment downloads for playlists")
def dl(url, playlist, audio, no_art, quality, out, template, cookies, cookies_from_browser, sponsorblock, subtitles, concurrent) -> None:
    """Download a video, audio, or playlist from URL."""
    out_path = Path(out).expanduser().resolve() if out else get_default_download_dir()
    username, password = get_credentials()

    ok = download(
        url, out=out_path, audio=audio, embed_art=not no_art,
        max_quality=int(quality), playlist=playlist, filename_template=template,
        cookies=cookies, cookies_from_browser=cookies_from_browser,
        sponsorblock=sponsorblock, subtitles=subtitles,
        username=username, password=password, concurrent_downloads=concurrent,
    )
    sys.exit(0 if ok else 1)


def main() -> None:
    cli()