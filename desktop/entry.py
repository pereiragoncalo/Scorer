"""Desktop entrypoint; leaves the Android entrypoint unchanged."""
from __future__ import annotations
import os
from pathlib import Path
import sys

# Kivy and other runtime components resolve relative assets from the bundle.
BUNDLE = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
os.chdir(BUNDLE)

from main import StrikerApp

if __name__ == "__main__":
    StrikerApp().run()
