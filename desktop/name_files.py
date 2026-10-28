"""Desktop JSON name import/export picker. No Android/JNI dependencies."""
from __future__ import annotations
from pathlib import Path
from threading import Thread

from kivy.clock import Clock

MAX_BYTES = 256 * 1024

class NameFiles:
    def __init__(self, on_import, on_message):
        self.on_import = on_import
        self.on_message = on_message
        self.busy = False

    def _notify(self, message):
        Clock.schedule_once(lambda _dt: self.on_message(message))

    def pick(self, text=None):
        if self.busy:
            return
        self.busy = True

        def work():
            try:
                import tkinter as tk
                from tkinter import filedialog
                root = tk.Tk()
                root.withdraw()
                try:
                    root.attributes("-topmost", True)
                    options = {"parent": root, "filetypes": [("JSON name packs", "*.json")]}
                    if text is None:
                        path = filedialog.askopenfilename(title="Import Scorer names", **options)
                        if path:
                            file = Path(path)
                            if file.stat().st_size > MAX_BYTES:
                                raise ValueError("JSON file exceeds 256 KiB.")
                            raw = file.read_text(encoding="utf-8-sig")
                            Clock.schedule_once(lambda _dt: self.on_import(raw))
                    else:
                        path = filedialog.asksaveasfilename(
                            title="Export Scorer names", defaultextension=".json",
                            initialfile="scorer_names.json", **options)
                        if path:
                            Path(path).write_text(text, encoding="utf-8")
                            self._notify("Names template exported. Edit the JSON and import to preview.")
                finally:
                    root.destroy()
            except (OSError, UnicodeError, ValueError, RuntimeError) as error:
                self._notify("Could not read or write the JSON file: " + str(error)[:160])
            finally:
                self.busy = False

        Thread(target=work, daemon=True).start()
