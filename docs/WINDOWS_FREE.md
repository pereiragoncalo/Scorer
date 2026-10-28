# Scorer Free for Windows — first desktop candidate

Owner selected Free only. This is the original Python/Kivy game, English-only,
one playable division and fictional clubs, not a web conversion or World unlock.
Existing mouse/keyboard shot controls are retained. No simulation balancing,
career schema, Android package/version or payments were changed.

## Build (Windows10/11 x64, Python3.12 x64)

    python -m venv .venv-windows
    .venv-windows\Scripts\python -m pip install -r tools/windows/requirements.txt
    .venv-windows\Scripts\python tools/windows/build.py --output dist/windows

Output: dist/windows/Scorer-Free.exe, single-file portable executable with the
original icon; it extracts runtime dependencies to a temporary directory. No
Python installation required on the target PC. Distribution is an unsigned QA
candidate, not an installer or Microsoft Store/Authenticode-signed release.
Windows SmartScreen may flag unsigned/unfamiliar software; signing is pending.
Linux staging is supported via --stage-only but building an EXE requires Windows.

The GitHub workflow windows-free.yml builds with a native Windows2022 runner,
then launches the actual frozen EXE from another working directory with isolated
saves. It checks splash->entry->new career->offer->weekly training->save/reload,
fixed Free access, no ad backend/no stats upload, and captures the hub. The run's
smoke.json must say platform=win32,frozen=true,ok=true. A Linux source render is
not a Windows executable test. Workflow artifacts are retained14days; no public
store upload or release is performed by CI.

## Persistence and controls

Careers: %LOCALAPPDATA%\Clemir\Scorer\Free\striker_career.json. Statistics and
Kivy logs/settings share that private Free directory. Moving/updating the EXE
must not remove progress. No automatic Android career transfer is implemented.
Explicit STRIKER_SAVE_DIR is retained for controlled development/testing. Bundled
resources never store player progress; launcher resolves resources independently
of the shortcut's working directory. Title-bar close opens save/exit confirmation,
with cancellation and failed-save protection; it does not silently discard a save.

Mouse clicks navigate/aim/shoot; Space shoots, arrows/WASD adjust aim, C restores
automatic aim. Escape uses existing back/exit confirmation. Window resizes using
the existing responsive Kivy interface. Minimum hardware is not yet certified;
Kivy needs supported OpenGL graphics or its bundled Windows ANGLE alternative.

## Advertising/privacy

AdMob is Android-only and is NOT a Windows revenue source. Windows shows local
stadium promotion panels, hides the unavailable reward-video button and uses
truthful desktop Privacy text. No real sponsor/production-ad service is enabled.
Optional aggregate statistics stay default-off with an empty endpoint/local-only.
No SMTP credentials, collector/backend, signing keys, career JSON, World art/CJK
catalogues, billing or Android Java sources are staged. World Python compatibility
code still exists but edition access is fixed Free, never a launcher flag.

## Verification/status

Core/staging/save-boundary and actual Kivy UI suites run against an isolated clean
snapshot, preserving unrelated pending World/career work. The native Windows
workflow must succeed before claiming that the EXE built or ran. Physical Windows
mouse/keyboard/audio/full match/relaunch/resize and suspend tests remain required.
A source smoke test exercises new career/training/save/reload using real Kivy on
Linux; it is not physical Windows validation. No Windows test result is implied
by the pre-existing Android APK results. Build evidence will be recorded below.
