import os
import json
import keyring
from pathlib import Path
from typing import Optional
from edl.colors import error, success, warn

SERVICE_NAME = "edl"


def get_config_dir() -> Path:
    """Return platform-appropriate config directory."""
    if os.name == "nt":
        base = os.environ.get("APPDATA", "~")
    elif os.name == "posix":
        sysname = os.uname().sysname
        if sysname == "Darwin":
            base = os.path.expanduser("~/Library/Application Support")
        else:
            base = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    else:
        base = "~"
    config_dir = Path(base).expanduser() / "edl"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_path() -> Path:
    return get_config_dir() / "config.json"


def load_config() -> dict:
    path = get_config_path()
    if path.exists():
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_config(config: dict) -> bool:
    try:
        get_config_path().write_text(json.dumps(config, indent=2))
        return True
    except OSError:
        return False


def get_stored_username() -> Optional[str]:
    return load_config().get("username")


def store_username(username: str) -> bool:
    config = load_config()
    config["username"] = username
    return save_config(config)


def get_password(username: str) -> Optional[str]:
    try:
        return keyring.get_password(SERVICE_NAME, username)
    except Exception:
        return None


def store_password(username: str, password: str) -> bool:
    try:
        keyring.set_password(SERVICE_NAME, username, password)
        return True
    except Exception as e:
        warn(f"couldn't store password in keyring: {e}")
        return False


def delete_credentials(username: str) -> bool:
    try:
        keyring.delete_password(SERVICE_NAME, username)
        config = load_config()
        config.pop("username", None)
        save_config(config)
        return True
    except Exception:
        return False


def is_logged_in() -> bool:
    username = get_stored_username()
    return bool(username and get_password(username))


def get_credentials() -> tuple[Optional[str], Optional[str]]:
    """Return (username, password) if logged in, else (None, None)."""
    username = get_stored_username()
    if not username:
        return None, None
    password = get_password(username)
    return (username, password) if password else (None, None)