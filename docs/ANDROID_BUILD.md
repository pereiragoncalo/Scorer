# Android build and verification

## Latest candidate — 0.6.2 FREE

Responsive career menus and save-before-exit confirmation. Actual debug APK:
`bin/striker-0.6.2-arm64-v8a-debug.apk`, 20,774,313 bytes.
SHA256 `87b55632503d132a357fec2c3583d29715d2d3b23d02b9c51623b9859327b387`.
20 core/security tests plus 8 real Kivy UI tests pass. Signature v2, ZIP alignment
and all 118 AArch64 ELF files' >=16 KB alignment pass. Same package and debug
certificate as 0.6.1. Install as an update to preserve career data; do not uninstall
or clear application storage. User reports 0.6.1 runs without crashes; 0.6.2 needs
its own device tests. No AAB/release artifact or paid World application yet.
Use the verification commands below with version 0.6.2. See BUILD_LOG.md for
layout matrix and PRODUCT_MODEL.md for the clarified two-app plan.


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
an exclusively 36.0.0 build. Actual packaging subsequently selected build-tools 37.0.0.
Build outputs remain in `.buildozer/` and `bin/`; a development APK is now available; see verification below.

### Build after publication — debug APK produced

The user's publication applied runtime configuration revision 2. A fresh
`git ls-remote https://skia.googlesource.com/skcms HEAD` succeeded. Completed the
partial libjxl submodules, then built Python 3.14.2, OpenSSL, SDL and Kivy.
Two additional environment fixes were needed: pip's isolated recipe environment
filters CA variables, so setup writes a cert-only pip configuration under the
container user's home; Java requires explicit proxy properties, derived from
Docker's reachable proxy inside the container. Verification remains enabled.

The first generated APK failed inspection: unpinned chardet 7.7.0 had introduced
17 x86_64 native extensions into the Python bundle. Pinned pure-Python chardet
5.2.0 in buildozer.spec. The p4a distribution cache does not distinguish recipe
versions, so the old generated distribution had to be removed. Removed only
stale chardet target files and the generated dist; retained native recipe caches.
The packaging virtualenv also held both pip 25.3 and 26.2.2 metadata and failed
an internal import; recreated only that generated virtualenv. The corrected
build completed successfully. Do not reuse an old distribution blindly after
changing dependency pins; inspect the final artifact, including Python bundles.

First-phase artifact: `bin/striker-0.6.1-arm64-v8a-debug.apk`, 20,761,765 bytes.
SHA256: `00211bb14422a9eeff5b4ab6ba3ea227b2e174c490fee7dbfdca215b61586a2b`.
This is signed with a development/debug key, not a distribution release.

Verified on the actual corrected APK:

```sh
bash tools/android/run.sh python tools/android/verify_elf_alignment.py bin/striker-0.6.1-arm64-v8a-debug.apk --readelf /work/toolchain/android-sdk/ndk/28.2.13676358/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-readelf
bash tools/android/run.sh /work/toolchain/android-sdk/build-tools/36.0.0/apksigner verify --verbose bin/striker-0.6.1-arm64-v8a-debug.apk
bash tools/android/run.sh /work/toolchain/android-sdk/build-tools/36.0.0/zipalign -c -P 16 4 bin/striker-0.6.1-arm64-v8a-debug.apk
```

All 118 ELF libraries are AArch64, with LOAD alignment >= 16 KB, including Python
extensions inside the compressed libpybundle.so. Signature v2 and ZIP alignment
checks pass. chardet 5.2.0 imported and detected ASCII correctly in the built
host Python. App payload contains career.pyc, main.pyc, sitecustomize.pyc and
p4a environment settings; baseline/tests/tools were not included.

The generated manifest reports package com.clemir.striker, version 0.6.1,
min SDK 26, target/compile SDK 36, arm64-v8a and landscape. No requested Android
permissions were reported. Debuggable and allowBackup are true: expected
for development, but backup/release manifest policy must be resolved before
release. APK generation used build-tools 37.0.0 (reported in build log).

18 regression/security tests pass under outer Python 3.12 and built host Python
3.14.2. ADB has no attached devices. **Installation, real gameplay, touchscreen,
restart persistence and 16 KB device execution have not been tested.** No AAB or
release APK was generated. Do not call this a functional Android release yet.

Logs are retained outside Git in `/workspace/striker-android-build/cache/`:
build-after-publish.log, build-after-trust-fix.log, build-after-java-proxy.log,
build-after-container-proxy.log, build-chardet-pinned.log,
build-clean-distribution.log, build-clean-packaging-venv.log.
Do not share raw logs blindly. Buildozer environment values are suppressed.

Drive remains separate: the session exposes no Google Drive connector or identity.
`drive.google.com` and `drive.usercontent.google.com` were added to the draft;
network permission alone does not authenticate private downloads/uploads. The
uploaded starter ZIP already supplied the source. Delivery to Drive still needs
an authenticated connection made available to this session, or manual ZIP sync.

`buildozer.spec` selects debug APK, release AAB, target API 36, min/NDK API 26,
arm64-v8a, Kivy 2.3.1, NDK 28c and pins python-for-android master commit
58d21141f17c889bf8585f5665921d72028f8831. Upstream sources were inspected:
its Python recipe defaults to 3.14.2 and its Gradle plugin to 8.11.0. These settings have now completed a debug APK build; device execution is still pending. The outer Python tested here is 3.12.14; the pinned container uses 3.12.15. Some upstream recommendation constants remain stale (MAX_NDK_VERSION
25 vs recommended 28c). Resolve build errors using evidence, not lowered targets.

NDK r28 and modern AGP are appropriate starting points for 16 KB pages, but do
not establish compliance. Inspect every generated arm64 .so with llvm-readelf
(LOAD alignment >= 0x4000), run Android build-tools `zipalign -c -P 16 -v 4`
on the APK, inspect the final manifest, and install/run on a 16 KB Android device
or emulator (`adb shell getconf PAGE_SIZE` must report 16384). Check AAB-generated
APKs with bundletool too. The APK ELF/ZIP checks passed as documented above; AAB/device checks remain pending.

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
