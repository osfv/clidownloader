from rich.console import Console
from rich.theme import Theme

THEME = Theme({
    "info": "bold white",
    "success": "bold green",
    "error": "bold red",
    "warn": "bold yellow",
    "accent": "bold cyan",
    "muted": "dim white",
})

console = Console(theme=THEME)


def print_banner() -> None:
    from rich.panel import Panel
    from rich.text import Text
    banner = Text()
    banner.append("edl", style="bold cyan")
    banner.append("  //  edgy youtube downloader", style="dim white")
    banner.append("\n4k  •  mp3  •  lossless  •  playlists  •  sponsorblock", style="dim cyan")
    console.print(Panel(banner, border_style="cyan", padding=(0, 2)))


def info(msg: str) -> None:
    console.print(f"[info]{msg}[/info]")


def success(msg: str) -> None:
    console.print(f"[success]✓ {msg}[/success]")


def error(msg: str) -> None:
    console.print(f"[error]✗ {msg}[/error]")


def warn(msg: str) -> None:
    console.print(f"[warn]! {msg}[/warn]")