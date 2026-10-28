"""Desktop entrypoint; refuses to launch an outdated Scorer edition."""
from __future__ import annotations
import os
from pathlib import Path
import sys

from desktop_build_info import BUILD_EDITION, BUILD_VERSION
from desktop_updates import enforce_update

# Check first, before loading the game engine; no gameplay without an allowed version.
if __name__ == "__main__":
    if not enforce_update(BUILD_EDITION, BUILD_VERSION):
        raise SystemExit(0)

    # Kivy resolves relative art/audio from the executable's extracted bundle.
    BUNDLE = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    os.chdir(BUNDLE)
    from kivy.resources import resource_add_path
    resource_add_path(str(BUNDLE))
    from main import StrikerApp

    StrikerApp().run()
