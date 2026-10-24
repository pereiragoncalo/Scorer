#!/bin/bash
set -euo pipefail
scorer_apk="$1"
scorer_edition="$2"
scorer_sdk=/work/toolchain/android-sdk
scorer_tools="$scorer_sdk/build-tools/36.0.0"
"$scorer_tools/apksigner" verify --verbose --print-certs "$scorer_apk"
"$scorer_tools/zipalign" -c -P 16 4 "$scorer_apk"
python tools/android/verify_elf_alignment.py "$scorer_apk" --readelf "$scorer_sdk/ndk/28.2.13676358/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-readelf"
"$scorer_tools/aapt" dump badging "$scorer_apk"
"$scorer_tools/aapt" dump permissions "$scorer_apk"
"$scorer_tools/aapt" dump xmltree "$scorer_apk" AndroidManifest.xml
/work/shared-platform/build-arm64-v8a/build/other_builds/hostpython3/desktop/hostpython3/native-build/python tools/verify_apk_edition.py "$scorer_apk" "$scorer_edition"
