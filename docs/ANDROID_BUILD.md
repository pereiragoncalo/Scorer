# Android build — phase 1 (0.6.1, not an APK release)

Use the existing checkout; do not create a worktree for cloud tasks.

## Verified development workflow

From `/workspace/Scorer`:

```sh
python3 -m venv /workspace/striker-venv
/workspace/striker-venv/bin/python -m pip install -r requirements-dev.txt
python3 -m py_compile main.py career.py tools/build_android.py
python3 -m unittest discover -s tests -v
mkdir -p /workspace/striker-runtime/kivy
KIVY_HOME=/workspace/striker-runtime/kivy STRIKER_SAVE_DIR=/workspace/striker-runtime/saves /workspace/striker-venv/bin/python main.py
```

The career/simulation was moved without redesign into `career.py`; importing it
uses only the standard library and opens no window. `main.py` remains the Kivy
entry point. Baseline SHA256 is verified by tests. Desktop defaults stay beside
the source; STRIKER_SAVE_DIR is an explicit desktop/test override. Android uses
the running App.user_data_dir. Legacy saves are copied once, with the original
retained and an existing destination never overwritten. Saves use same-directory
atomic replacement; write failures leave the old save intact and show a message.
Android storage was tested with a simulated App, not on hardware.

## Cloud Android toolchain — prepared 2026-10-23

The missing host JDK/build packages were resolved with the managed Docker daemon.
`tools/android/Dockerfile` pins the Python 3.12 Bookworm base image by digest and
installs JDK 17, autoconf/automake/libtool, pkg-config, C/C++ tools, cmake/ninja,
zip/unzip and development headers. Builds use the task user's UID 1000.
Host system files and HOME are unchanged. Session proxy and CA verification are
preserved for Git, Python, curl and Java; session CA files are mounted at runtime,
not embedded in the image. Java uses a refreshed external trust store.

From `/workspace/Scorer` in this managed cloud environment:

```sh
bash tools/android/setup.sh
bash tools/android/run.sh python tools/build_android.py -v android debug
# Only after actual debug/device acceptance, prepare the release AAB:
bash tools/android/run.sh python tools/build_android.py -v android release
```

`setup.sh` was executed successfully, including repeat installation. It installs
stable SDK packages: API 36, build-tools 36.0.0, platform-tools and NDK
28.2.13676358 (r28c). CLI tools are pinned to version 19.0 because the newest CLI
changed its licence command contract. Official metadata was fetched via verified
HTTPS; downloaded archives were checked against Google's published checksums.
The owner explicitly accepted the Google Android SDK terms in this chat on
2026-10-23; the setup script records acceptance for these stable packages only.
Do not add preview licences under that authorization.

State is retained outside the checkout under `/workspace/striker-android-build`:
`android-sdk/`, `cache/` (Gradle, Python user packages, Java trust store, Buildozer
cache and logs). The Docker image is `striker-android-build:phase1`.
Live containers are disposable. If the image is absent in a future task, rerun
setup after the managed Docker daemon health check described by the runtime skill.
Runtime paths inside the container start with `/work`.
`APP_ANDROID_SKIP_UPDATE=1` prevents Buildozer's broad automatic SDK updates.
The first bootstrap ran before this correction and additionally installed
build-tools 37.0.0; both installed versions were recorded, not represented as
an exclusively 36.0.0 build. Actual Gradle tool selection is still unverified.
Build outputs remain in `.buildozer/` and `bin/`; no application artifact exists.

### Current build blocker and exact resume point

Buildozer passed Java/SDK/NDK checks, installed p4a host dependencies and downloaded
native sources. It then failed while recursively cloning SDL2_image's libjxl
submodule: `https://skia.googlesource.com/skcms` returned proxy CONNECT 403.
The required domain was saved in the environment configuration draft; a draft
save does not apply the policy. Review/save/publish the environment configuration
to activate it. Do not bypass the proxy, TLS verification or dependency checks.

After a meaningful policy change, verify access and finish the partial checkout
before resuming. The original p4a recipe skips nonempty checkout directories, so
simply retrying without repairing missing submodules can hide this prerequisite:

```sh
bash tools/android/run.sh git ls-remote https://skia.googlesource.com/skcms HEAD
bash tools/android/run.sh git -C /work/source/.buildozer/android/platform/build-arm64-v8a/build/bootstrap_builds/sdl2/jni/SDL2_image/external/libjxl submodule update --init --recursive
bash tools/android/run.sh python tools/build_android.py -v android debug
```

The preflight/submodule commands above are pending the network change, not claimed
as passed. No source mirrors, submodule versions or checksums were substituted.
Raw external build logs live in `cache/build-debug.log`; build command failures
now omit environment values. Do not share logs blindly.

Drive remains separate: the session exposes no Google Drive connector or identity.
`drive.google.com` and `drive.usercontent.google.com` were added to the draft;
network permission alone does not authenticate private downloads/uploads. The
uploaded starter ZIP already supplied the source. Delivery to Drive still needs
an authenticated connection made available to this session, or manual ZIP sync.

`buildozer.spec` selects debug APK, release AAB, target API 36, min/NDK API 26,
arm64-v8a, Kivy 2.3.1, NDK 28c and pins python-for-android master commit
58d21141f17c889bf8585f5665921d72028f8831. Upstream sources were inspected:
its Python recipe defaults to 3.14.2 and its Gradle plugin to 8.11.0. These are
**candidate settings, not a validated combination**. The outer Python tested here is 3.12.14; the pinned container uses 3.12.15. Some upstream recommendation constants remain stale (MAX_NDK_VERSION
25 vs recommended 28c). Resolve build errors using evidence, not lowered targets.

NDK r28 and modern AGP are appropriate starting points for 16 KB pages, but do
not establish compliance. Inspect every generated arm64 .so with llvm-readelf
(LOAD alignment >= 0x4000), run Android build-tools `zipalign -c -P 16 -v 4`
on the APK, inspect the final manifest, and install/run on a 16 KB Android device
or emulator (`adb shell getconf PAGE_SIZE` must report 16384). Check AAB-generated
APKs with bundletool too. No ELF, APK or AAB is available yet for those checks.

## Release gates

- Actual Android install, touchscreen/landscape, match completion, career restart,
  app-private save migration, offline use and 16 KB tests remain unrun.
- Release signing keys must stay outside Git; inject securely when signing.
  `android release` alone does not establish a signed, tested release.
- Inspect generated manifest: docs/AndroidManifest.release.reference.xml is not
  automatically merged. Verify backup/cleartext/debuggable policy in the output.
- Existing optional Wikipedia badge requests and remotely supplied image URLs
  need a privacy/content review; they were preserved, not approved for release.
  Current spec has no requested permissions; actual network behaviour is untested.
- Existing sounds/cache paths also need installed-package writable-path testing.
- No advertisements, payments, publication or sponsor contacts in this phase.
- Baseline, docs, tests, tools, saves and keys are excluded from app packaging.
