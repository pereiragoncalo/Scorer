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

## Build prerequisites and commands

The current machine has a Java 21 runtime, **no javac**, and no prepared SDK/NDK.
APT metadata has no package candidates and system directories are read-only.
Provide a Linux Android build image with a full JDK (17+; verify compatibility
with the selected Gradle), git, unzip/zip, C/C++ build tools, autoconf, automake,
libtool, pkg-config, cmake, zlib/ffi/SSL development headers, SDK command line
tools, Android platform 36 and NDK r28c. Use platform/official package signatures
and checksums and keep TLS verification enabled. Accept SDK licences only after
reviewing their terms; automatic acceptance remains disabled.

```sh
cd /workspace/Scorer
export PATH=/workspace/striker-venv/bin:$PATH
python tools/build_android.py -v android debug
# After debug install and actual device acceptance:
python tools/build_android.py -v android release
```

The helper changes only Buildozer's global cache location to
`/workspace/striker-build-cache` (override STRIKER_BUILD_CACHE on another machine).
It does not change HOME. Local build output is .buildozer/ and bin/.
Set APP_ANDROID_SDK_PATH and APP_ANDROID_NDK_PATH to provisioned SDK/NDK paths
if needed (Buildozer configuration environment overrides). Buildozer 1.5.0's
SDK bootstrap is old; an existing modern SDK may need its sdkmanager path adapted
or a reviewed Buildozer update. This has not been exercised past the javac check.

`buildozer.spec` selects debug APK, release AAB, target API 36, min/NDK API 26,
arm64-v8a, Kivy 2.3.1, NDK 28c and pins python-for-android master commit
58d21141f17c889bf8585f5665921d72028f8831. Upstream sources were inspected:
its Python recipe defaults to 3.14.2 and its Gradle plugin to 8.11.0. These are
**candidate settings, not a validated combination**. The host Python tested here
is 3.12.14. Some upstream recommendation constants remain stale (MAX_NDK_VERSION
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
