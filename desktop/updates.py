"""Mandatory Windows release check with a short verified-offline grace period.

Only reads a fixed public HTTPS manifest: no accounts, advertising, telemetry,
background downloads, automatic execution or modification of career saves.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

MANIFEST_URL = "https://raw.githubusercontent.com/pereiragoncalo/Scorer/main/desktop/releases.json"
MAX_MANIFEST_BYTES = 8192
MAX_CACHE_BYTES = 4096
GRACE_SECONDS = 72 * 60 * 60
VERSION_RE = re.compile(r"^[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}$")


@dataclass(frozen=True)
class Check:
    state: str               # 'current', 'required', or 'unavailable'
    installed: str
    latest: str = ""
    download_url: str = ""
    offline: bool = False


def version_tuple(version: str) -> tuple[int, int, int]:
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        raise ValueError("Invalid version")
    return tuple(map(int, version.split(".")))


def checked_release_url(value: str) -> str:
    if not isinstance(value, str) or len(value) > 300 or any(c.isspace() for c in value):
        raise ValueError("Invalid release URL")
    url = urlsplit(value)
    if (url.scheme != "https" or url.hostname != "github.com" or url.port not in (None, 443)
            or url.username or url.password or url.query or url.fragment
            or not url.path.startswith("/pereiragoncalo/Scorer/releases")):
        raise ValueError("Release URL must belong to the official Scorer GitHub releases")
    return value


def validate_manifest(raw: bytes, edition: str) -> tuple[str, str]:
    if edition not in ("free", "world") or len(raw) > MAX_MANIFEST_BYTES:
        raise ValueError("Unexpected update manifest")
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict) or data.get("schema") != 1:
        raise ValueError("Unsupported update manifest")
    products = data.get("windows")
    if not isinstance(products, dict):
        raise ValueError("Missing Windows release entries")
    product = products.get(edition)
    if not isinstance(product, dict) or set(product) != {"version", "url"}:
        raise ValueError("Invalid release entry")
    version_tuple(product["version"])
    return product["version"], checked_release_url(product["url"])


def cache_location(edition: str) -> Path:
    if edition not in ("free", "world"):
        raise ValueError("Invalid edition")
    base = os.environ.get("LOCALAPPDATA")
    folder = Path(base) if base else Path.home() / ".local" / "share"
    return folder / "Clemir" / ("ScorerWorld" if edition == "world" else "ScorerFree") / "update-check.json"


def read_cache(path: Path, edition: str):
    try:
        if path.stat().st_size > MAX_CACHE_BYTES:
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("edition") != edition:
            return None
        version = data["version"]
        version_tuple(version)
        url = checked_release_url(data["url"])
        timestamp = data["checked_at"]
        if type(timestamp) is not int or timestamp <= 0:
            return None
        return version, url, timestamp
    except (OSError, ValueError, KeyError, TypeError):
        return None


def write_cache(path: Path, edition: str, version: str, url: str, now: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         dir=path.parent, prefix=".scorer-update-",
                                         delete=False) as stream:
            temporary = Path(stream.name)
            json.dump({"edition": edition, "version": version, "url": url,
                       "checked_at": now}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary:
            temporary.unlink(missing_ok=True)


def check_update(edition: str, installed: str, path: Path | None = None,
                 now: int | None = None, open_url=urlopen) -> Check:
    """Never silently accept unknown release state, except a recent verified cache."""
    version_tuple(installed)
    if edition not in ("free", "world"):
        raise ValueError("Invalid edition")
    path = path or cache_location(edition)
    now = int(datetime.now(timezone.utc).timestamp()) if now is None else now
    remote = None
    try:
        request = Request(MANIFEST_URL, headers={
            "User-Agent": "Scorer-Update/1", "Cache-Control": "no-cache"})
        with open_url(request, timeout=6) as response:
            payload = response.read(MAX_MANIFEST_BYTES + 1)
        remote = validate_manifest(payload, edition)
    except (OSError, ValueError, UnicodeError, TypeError):
        pass

    if remote is not None:
        latest, url = remote
        try:
            write_cache(path, edition, latest, url, now)
        except OSError:
            # A read-only profile does not disable a fresh mandatory update decision.
            pass
        return Check("required" if version_tuple(installed) < version_tuple(latest) else "current",
                     installed, latest, url)

    cached = read_cache(path, edition)
    if cached:
        latest, url, checked_at = cached
        if version_tuple(installed) < version_tuple(latest):
            return Check("required", installed, latest, url, offline=True)
        age = now - checked_at
        if 0 <= age <= GRACE_SECONDS:
            return Check("current", installed, latest, url, offline=True)
    return Check("unavailable", installed, offline=True)


def enforce_update(edition: str, installed: str) -> bool:
    """Run before loading Kivy. Never load the game if an update is required."""
    result = check_update(edition, installed)
    if result.state == "current":
        return True

    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.withdraw()
    try:
        root.attributes("-topmost", True)
        if result.state == "required":
            choice = messagebox.askyesno(
                "Scorer — atualização obrigatória",
                f"Versão instalada: {installed}\n"
                f"Nova versão: {result.latest}\n\n"
                "É necessário atualizar para continuar a jogar. "
                "Os dados da carreira continuam guardados.\n\n"
                "Abrir a página oficial para descarregar?",
                parent=root)
            if choice:
                import webbrowser
                webbrowser.open(result.download_url, new=2)
        else:
            messagebox.showerror(
                "Scorer — verificação de versão",
                "Não foi possível confirmar se esta é a versão mais recente.\n\n"
                "Liga o computador à Internet e abre novamente o jogo. "
                "Depois de uma verificação válida, podes jogar até 72 horas offline.",
                parent=root)
    finally:
        root.destroy()
    return False
