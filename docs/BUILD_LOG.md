# Build log

## Packaging snapshot, 23/10/2026
- Google Drive v006 used as baseline.
- Verified local `python3 -m py_compile` succeeds.
- Android SDK/NDK and APK/AAB compilation: **not executed or verified**.
- Hardware smoke tests: **not executed**.

## Next run
Codex should append the exact commands, logs, test results and blockers for each task.

## 2026-10-23 — phase 1, source candidate 0.6.1

Read AGENTS.md, README.md, ROADMAP.md and FIRST_CODEX_TASK.md before edits.
Validated archive paths and baseline/main SHA256 against SOURCE_CHECKSUM.txt.
Imported starter in commit 957f7c5; retained Scorer history and a recoverable
Git bundle outside the checkout at /workspace/scorer-before-striker.bundle.

Changes: moved original simulation/career definitions into a headless career.py;
main.py keeps the original Kivy UI and imports its required core symbols. Added
private Android saves, legacy migration, atomic writes with visible error,
generic default Alex Silva, 13 regression/security tests, pinned host dependencies,
workspace Buildozer cache helper and candidate API 36/arm64/NDK28c settings.
No baseline changes; existing saved names remain unchanged.

Commands/results:
- `python3 -m py_compile main.py career.py tools/build_android.py`: PASS.
- `python3 -m unittest discover -s tests -v`: 13 tests PASS, none skipped.
  Covers imports without Kivy, career training/match progress, restart, v1/v2
  saves, invalid JSON, unknown migration versions, no-overwrite migration,
  write failure preserving previous save, private Android path via simulated App,
  FREE boundary, provider failure and save tampering unable to unlock WORLD.
- Installed Buildozer 1.5.0, Kivy 2.3.1, Cython 0.29.37 in external venv.
- `buildozer -v android debug`: FAILED on missing distutils with Python 3.12.
  Installed setuptools 75.8.2, retried: FAILED on read-only ~/.buildozer.
- `python tools/build_android.py -v android debug`: cache corrected; FAILED
  prerequisite check: Java compiler (javac) not found. Retried after spec update,
  same confirmed prerequisite. No native compilation or APK/AAB generated.
- `apt-cache policy ...`: system metadata has no candidates for checked build
  packages; system locations are read-only. Full build image still required.
- Kivy desktop smoke: initial KIVY_HOME parent missing, created parent and retried.
  App opened with SDL2/Mesa llvmpipe, ran event loop and stopped via Clock after
  two seconds, exit 0 and UI_STARTUP_OK. Not an Android/touchscreen test.
- `pyflakes main.py career.py tests tools`: initial unused imports cleaned.
  Remaining diagnostic is original UI local variable `score` assigned but unused;
  no undefined-name diagnostics. Full lint is therefore not a clean pass.
- Read-only upstream p4a clone at pinned commit: NDK recommendation 28c, AGP
  8.11.0, Python recipe 3.14.2, Kivy 2.3.1. Compatibility and 16 KB compliance
  remain UNVERIFIED until native build/output/device tests.

Security audit: no payments enabled; FREE remains fail closed. Baseline excluded
from APK sources to avoid shipping its personal default name. Original optional
Wikipedia badge fetch/image URLs and generated sound/cache paths require follow-up
review. Static reference manifest does not prove actual package policy. No secret
or signing key created. This is not a complete security certification.

Next task: provide full Android build prerequisites, generate debug APK, verify
manifest/ELF alignment and install on real Android hardware before ad-board work.

## 2026-10-23 — resolve cloud toolchain blockers (0.6.1 tooling revision)

No game logic, baseline, payments or advertisements changed in this revision.
The managed Docker daemon was healthy (28.4.0, vfs). Prepared a Docker toolchain
instead of requiring writes to the read-only host system. Added tools/android/
Dockerfile, setup.sh, install_sdk.sh and run.sh; tools/build_android.py now omits
environment values on failures. Added a security regression test for that behaviour.

Evidence and corrections:
- Pulled Python 3.12 Bookworm image with verified Docker digest; pinned digest
  14a4933e6cef421424f7a66d89a3f4eafcbd0d90e0a822251f298e05132dc735.
- Docker build initially needed writable buildx state: BUILDX_CONFIG moved under
  /workspace/striker-android-build/buildx, preserving registry configuration.
- Built image with JDK 17.0.20.1, autoconf 2.71, cmake 3.25.1, compilers and tools.
  Verified executable presence and `pip check` (no broken requirements).
- Mounted session/system CA bundles; refreshed Java trust store outside image.
  Git initially failed TLS trust; added GIT_SSL_CAINFO/CURL_CA_BUNDLE and reran
  with verification enabled. Python user installation initially tried /.local;
  set PYTHONUSERBASE to writable cache and added its scripts directory to PATH.
- Retrieved official SDK metadata using TLS and verified package archives against
  published checksums. Owner accepted Android SDK licence explicitly in chat.
  Latest command line tools changed --licenses semantics; used pinned CLI 19.0.
  Installed API 36, build-tools 36.0.0, platform-tools 37.0.1 and NDK r28c.
  sdkmanager install exited 0. A repeat run of `bash tools/android/setup.sh`
  completed with exit 0, including all 14 tests passing and SDK already installed.
- Buildozer's initial automatic update also installed build-tools 37.0.0. Disabled
  future broad automatic updates via APP_ANDROID_SKIP_UPDATE. No claim that
  native/Gradle build tool selection has been verified.
- Native preparation advanced to SDL2_image/libjxl recursive submodules. Build
  FAILED: proxy CONNECT 403 for https://skia.googlesource.com/skcms. No APK/AAB.
  Partial libjxl submodules need `git submodule update --init --recursive` after
  policy activation; do not silently skip this just because directory exists.
- Current tests: `python3 -m unittest discover -s tests -v`: 14 PASS, no skips.
  Shell syntax checks and Python compilation of build wrapper PASS.
- Saved additive custom network domains (preserving presets): drive.google.com,
  drive.usercontent.google.com, www.openssl.org, openssl.org,
  download.savannah.gnu.org, maven.google.com, skia.googlesource.com.
  These are DRAFT settings, not proven enforced. User review/save/publication
  is required before the blocked operation can be retried meaningfully.
- Drive download still returned 403 before policy activation. No Drive connector,
  runtime identity or secrets are configured. A network allowlist cannot provide
  private-account access; no OAuth credentials were requested or invented.

No hardware USB devices or /dev/kvm are exposed by this machine. Android hardware
acceptance, final manifest checks, ELF 16 KB alignment, signed release generation
and Drive upload remain pending. See ANDROID_BUILD.md for exact resume commands.

Additional tool verification:
- NDK clang 19.0.1 executes; sdkmanager --list_installed confirms the package
  versions above. `adb devices -l` initially failed because numeric Docker user
  had no writable account home. Added an unprivileged passwd account in the
  image with home /work/cache/user (without setting HOME). Retest exited 0;
  daemon started and device list is empty.
- A setup rerun overlapped an in-progress edit of install_sdk.sh and exited 2
  while reading the changing script. Validated the stable script with bash -n
  and reran the installer successfully. Final full setup rerun is recorded in
  /workspace/striker-android-build/cache/setup-final.log.
- The SDK setup now checks the SHA256 of the licence text accepted in this chat;
  changed licence terms stop setup for owner review rather than being accepted
  silently. This is a licence-change guard, not an artifact checksum override.
