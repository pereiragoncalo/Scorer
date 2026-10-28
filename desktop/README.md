# Scorer on Windows — development build

This is **the original Python/Kivy Android game**, reused for Windows. It is **not** the HTML/web edition.

The desktop build is deliberately isolated from Android: it does not change `main.py` in the repository or enable Google Play, AdMob, paid unlocks or production publication.

## Editions

- **ScorerFree.exe**: independent English Free career, no advertising, no ad-reward buttons, no advertising space and no promotional stadium boards. No advertising SDK or receiving endpoint.
- **ScorerWorld.exe**: separate World career and nine-language UI, with local desktop JSON import/export. Does not use the Free collector.

Both are standalone, Windows 10/11 64-bit beta candidates; no Python installation should be required for the player. Game assets and fonts are bundled. Saves use the Kivy app data directory, not the temporary executable extraction folder.

## Mandatory version checking

A version check runs **before Kivy** at every launch, using the public GitHub `desktop/releases.json` manifest. The executable checks its own edition against the official current version.

- **Outdated**: a blocking update dialog opens the official Scorer GitHub releases page. No gameplay is permitted until the updated EXE is installed.
- **Current**: gameplay continues. The check only stores the last verified version, official release URL and timestamp in LOCALAPPDATA; no name, career, statistics or device identifier is sent.
- **Offline / GitHub unavailable**: a previously verified current version has a **72-hour** offline grace period; after that, the player must go online to verify. A previously detected mandatory update blocks even while offline. First launch must be online.
- **Free and World**: independent release entries and update caches. No data conversion and no change to existing career saves.

The game does **not** silently download or execute an EXE; players choose the release on the verified GitHub page. HTTPS is required and release links are restricted to this repository. The connection to GitHub can expose the user's IP address to GitHub as with any web request.

**Release protocol**: first build, test, sign when available and publish the new Windows executable as an actual GitHub release. Only *after* that release is public, change the relevant edition's version and URL in `desktop/releases.json` on the **main** branch. Setting a newer version in the manifest before publishing a usable EXE locks existing players out. Keep the `buildozer.spec` app version aligned with the Windows executable version at build time (future platform-specific versioning may separate this). The version source and manifest are independent so that a release can be staged and tested before enforcement.

This update check is for the Windows build only. Android Play builds should use Play's official Immediate In-App Updates API once Play distribution and device testing are available. Direct APK sideloads need a separate trusted update flow and cannot use Play Immediate Updates.

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
6. Confirm that update checks (current/outdated/offline/invalid manifest) work, and that **there are no advertising placements** or reward ad controls.
7. Run a malware scan and review third-party font/data licences. Distribute test builds as **beta only**.
8. Windows executables are **not code-signed**; SmartScreen may warn. Do not tell users to disable Windows protections. Obtain a code-signing certificate and complete release tests for public distribution.

Run the isolated updater tests: `python -m unittest discover -s tests -p test_windows_updates.py -v`. Build pipelines also run them before packaging. Windows executable smoke tests have not yet been run.\n\nNo payment/licensing/DRM is implemented. A paid World Windows release should **not** be distributed as a raw unlocked executable without making a conscious piracy/licensing decision.
