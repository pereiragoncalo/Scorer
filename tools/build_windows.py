"""Build an isolated Windows Scorer Free or World executable from the original Kivy game.

Windows-only packaging; no Android/Play services, payment activation or live adverts.
Never modifies the source tree or either Android product.
"""
from __future__ import annotations

import argparse
import configparser
from pathlib import Path
import re
import shutil
import subprocess
import sys

SOURCE = Path(__file__).resolve().parents[1]
SOURCES = (
    "main.py", "career.py", "menu_ui.py", "domestic_rules.py",
    "edition.py", "advertising.py", "anonymous_stats.py", "analytics_config.py",
    "device_locale.py", "localization.py", "ui_localization.py",
    "android_names.py", "name_packs.py", "world_clubs.py",
    "world_promotion.py", "world_ui.py", "release_settings.py",
)
COMMON_ART = ("icon.png", "menu_logo.png", "menu_stadium.png", "splash.png")
COMMON_FONTS = (
    "Barlow-Regular.ttf", "BarlowCondensed-ExtraBoldItalic.ttf",
    "OFL-Barlow.license", "OFL-BarlowCondensed.license",
)
WORLD_FONTS = (
    "NotoSansCJKjp-Regular.otf", "NotoSansCJKkr-Regular.otf",
    "NotoSansCJKsc-Regular.otf", "OFL-NotoCJK.license",
)
WORLD_TRANSLATIONS = (
    "en.json", "pt.json", "es.json", "de.json", "it.json",
    "ko.json", "ja.json", "zh.json", "vi.json", "countries.json",
    "Unicode.license", "Babel.license",
)
WORLD_DATA = (
    "world_clubs.json", "COUNTRIES-MIT.license",
    "GEONAMES-CCBY4.license", "OPENFOOTBALL-CC0.license",
)


def copy(source: Path, destination: Path):
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def stage(edition: str, output: Path):
    if edition not in ("free", "world"):
        raise ValueError("Edition must be free or world.")
    output = output.resolve()
    source = SOURCE.resolve()
    if output == source or output in source.parents or source in output.parents:
        raise ValueError("Use a fresh staging directory outside the checkout.")
    if output.exists() and any(output.iterdir()):
        raise ValueError("Staging directory is not empty; refusing to overwrite.")
    output.mkdir(parents=True, exist_ok=True)

    for name in SOURCES:
        copy(source / name, output / name)
    copy(source / "desktop/entry.py", output / "desktop_entry.py")
    copy(source / "desktop/updates.py", output / "desktop_updates.py")
    spec = configparser.ConfigParser(interpolation=None)
    if not spec.read(source / "buildozer.spec"):
        raise ValueError("Missing app version")
    version = spec["app"]["version"]
    if not re.fullmatch(r"[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}", version):
        raise ValueError("Invalid release version in buildozer.spec")
    (output / "desktop_build_info.py").write_text(
        f"BUILD_EDITION = {edition!r}\nBUILD_VERSION = {version!r}\n",
        encoding="utf-8",
    )
    copy(source / "desktop/name_files.py", output / "desktop_name_files.py")
    for name in COMMON_ART + (("icon_world.png", "menu_logo_world.png") if edition == "world" else ()):
        copy(source / "assets" / name, output / "assets" / name)
    for name in COMMON_FONTS + (WORLD_FONTS if edition == "world" else ()):
        copy(source / "assets/fonts" / name, output / "assets/fonts" / name)
    if edition == "world":
        for name in WORLD_TRANSLATIONS:
            copy(source / "assets/i18n" / name, output / "assets/i18n" / name)
        for name in WORLD_DATA:
            copy(source / "assets/data" / name, output / "assets/data" / name)

    identity = output / "edition.py"
    text = identity.read_text(encoding="utf-8")
    text, count = re.subn(r"(?m)^WORLD_BUILD = False$", "WORLD_BUILD = " + ("True" if edition == "world" else "False"), text)
    if count != 1 or "WORLD_PREVIEW = False" not in text:
        raise RuntimeError("Unknown edition.py; refusing unsafe Windows staging.")
    identity.write_text(text, encoding="utf-8")

    # Use a native Windows JSON picker without touching the Android sources.
    game = output / "main.py"
    text = game.read_text(encoding="utf-8")
    text, count = re.subn(r"from android_names import NameFiles\b", "from desktop_name_files import NameFiles", text)
    if count != 1:
        raise RuntimeError("Could not find the World JSON picker import.")
    # No advertising surfaces in the Windows community edition.
    text, count = re.subn(
        r"(?m)^            self\._draw_world_promotion_boards\(\)$",
        "            pass  # Windows beta: no promotional boards",
        text,
    )
    if count != 1:
        raise RuntimeError("Could not deactivate the Windows promotional boards")
    game.write_text(text, encoding="utf-8")

    # Remove advertising controls, spacing and claims from Windows menus.
    menu = output / "menu_ui.py"
    menu_text = menu.read_text(encoding="utf-8")
    menu_text, count = re.subn(
        r"(?m)^        banner_fits = .*$",
        "        banner_fits = False  # Windows beta has no advertising",
        menu_text,
    )
    if count != 1:
        raise RuntimeError("Could not remove the Windows banner space")
    menu_text = menu_text.replace("'Privacy & advertising'", "'Privacy'")
    start = menu_text.index("        boost = self._button('WATCH AD: +1 MORALE'")
    end = menu_text.index("\n    def _table_zones(", start)
    menu_text = menu_text[:start] + "        # No reward advertising in the Windows edition.\n" + menu_text[end:]
    start = menu_text.index("        card.label('This version uses Google advertising.'")
    end = menu_text.index("        usage=self.game.usage", start)
    menu_text = (menu_text[:start] +
        "        card.label('This Windows edition is free of advertising and rewarded videos.')\n"
        "        self._privacy_contact(card)\n" + menu_text[end:])
    menu_text = menu_text.replace("Advertising consent is separate.",
                                  "No advertising is shown in the Windows edition.")
    menu.write_text(menu_text, encoding="utf-8")

    # Persistent Windows saves must never live in PyInstaller's onefile temp folder.
    career = output / "career.py"
    career_text = career.read_text(encoding="utf-8")
    old_save = '        else:\n            base = Path(__file__).resolve().parent\n'
    new_save = (
        '        else:\n'
        '            # Persistent separate Windows careers, unaffected by replacing the EXE.\n'
        '            folder = "ScorerWorld" if self._save_slot == "world" else "ScorerFree"\n'
        '            root = os.environ.get("LOCALAPPDATA")\n'
        '            base = (Path(root) if root else Path.home() / ".local" / "share") / "Clemir" / folder\n'
    )
    if career_text.count(old_save) != 1:
        raise RuntimeError("Cannot safely set the persistent Windows save directory")
    career.write_text(career_text.replace(old_save, new_save), encoding="utf-8")

    # World must not contain the Free usage collector or its endpoint.
    if edition == "world":
        (output / "analytics_config.py").unlink()
        (output / "anonymous_stats.py").write_text(
            "class NoStatistics:\n"
            "    enabled=False\n    endpoint=''\n    remote_available=False\n    last_error=''\n"
            "    def begin_session(self): pass\n    def end_session(self): pass\n"
            "    def record(self,*a,**kw): return False\n"
            "    def set_enabled(self,*a): return False\n"
            "    def flush_async(self): return False\n"
            "def create_statistics(*a,**kw): return NoStatistics()\n", encoding="utf-8")
    else:
        # A desktop Free executable has no configured statistics recipient.
        (output / "analytics_config.py").write_text("ENDPOINT = ''\n", encoding="utf-8")

    (output / "BUILD_INFO.txt").write_text(
        f"Scorer {edition.title()} for Windows, built from original Kivy source.\n"
        "Windows community beta: no ads, promotional boards or rewarded videos.\n"
        "Mandatory release check on launch, with 72-hour verified offline grace.\n"
        "Not digitally signed; no AdMob or Google Play services.\n"
        "Free and World are independent editions with separate save slots.\n",
        encoding="utf-8",
    )
    return output


def create_icon(stage_dir: Path, edition: str):
    from PIL import Image
    art = stage_dir / "assets" / ("icon_world.png" if edition == "world" else "icon.png")
    icon = stage_dir / "scorer.ico"
    with Image.open(art) as image:
        image.convert("RGBA").save(icon, format="ICO", sizes=[
            (16, 16), (24, 24), (32, 32), (48, 48), (64, 64),
            (128, 128), (256, 256),
        ])
    return icon


def package(stage_dir: Path, edition: str, dist: Path):
    if sys.platform != "win32":
        raise RuntimeError("The .exe must be compiled on Windows.")
    icon = create_icon(stage_dir, edition)
    name = "ScorerWorld" if edition == "world" else "ScorerFree"
    dist.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--clean", "--onefile", "--windowed",
        "--name", name, "--icon", str(icon),
        "--add-data", f"{stage_dir / 'assets'};assets",
        "--paths", str(stage_dir),
        "--distpath", str(dist),
        "--workpath", str(stage_dir / "_pyinstaller_work"),
        "--specpath", str(stage_dir),
        "--hidden-import", "tkinter",
        str(stage_dir / "desktop_entry.py"),
    ]
    subprocess.run(cmd, cwd=stage_dir, check=True)
    exe = dist / (name + ".exe")
    if not exe.is_file() or exe.stat().st_size < 500_000:
        raise RuntimeError(f"No usable executable created at {exe}")
    return exe


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--edition", choices=("free", "world"), required=True)
    parser.add_argument("--output", type=Path, required=True, help="Fresh staging directory (outside repository)")
    parser.add_argument("--dist", type=Path, required=True, help="Output folder for the executable")
    parser.add_argument("--stage-only", action="store_true")
    args = parser.parse_args()
    target = stage(args.edition, args.output)
    if not args.stage_only:
        print(package(target, args.edition, args.dist))
    else:
        print(target)


if __name__ == "__main__":
    main()
