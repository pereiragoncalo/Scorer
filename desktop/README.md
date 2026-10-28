# Scorer on Windows — development build

This is **the original Python/Kivy Android game**, reused for Windows. It is **not** the HTML/web edition.

The desktop build is deliberately isolated from Android: it does not change `main.py` in the repository or enable Google Play, AdMob, paid unlocks or production publication.

## Editions

- **ScorerFree.exe**: independent English Free career. No advertising SDK or receiving endpoint.
- **ScorerWorld.exe**: separate World career and nine-language UI, with local desktop JSON import/export. Does not use the Free collector.

Both are standalone, Windows 10/11 64-bit beta candidates; no Python installation should be required for the player. Game assets and fonts are bundled. Saves use the Kivy app data directory, not the temporary executable extraction folder.

## Build locally

On a Windows 64-bit machine with Python 3.11 and Git:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r desktop/requirements-windows.txt
.\.venv\Scripts\python.exe tools/build_windows.py --edition free --output "$env:TEMP\scorer-stage-free" --dist "dist\windows"
.\.venv\Scripts\python.exe tools/build_windows.py --edition world --output "$env:TEMP\scorer-stage-world" --dist "dist\windows"
```

Use fresh empty staging directories on each build. Builds **must** be produced on Windows: PyInstaller does not cross-compile a Windows exe from Linux. Alternatively, run the included GitHub Actions workflow manually and download its build artefacts.

## Verification before distribution

1. Test Free and World on Windows 10/11 64-bit, ideally a clean PC without Python.
2. Confirm splash, menus, practice, match shooting, half-time, score, completed game, saving and reloading.
3. Confirm independent saves and World language choice.
4. In World, export names JSON, import it, preview and cancel/apply safely.
5. Confirm closing the window does not damage careers; confirm there are no Android-only exceptions.
6. Run a malware scan and review third-party font/data licences. Distribute test builds as **beta only**.
7. Windows executables are **not code-signed**; SmartScreen may warn. Do not tell users to disable Windows protections. Obtain a code-signing certificate and complete release tests for public distribution.

No payment/licensing/DRM is implemented. A paid World Windows release should **not** be distributed as a raw unlocked executable without making a conscious piracy/licensing decision.
