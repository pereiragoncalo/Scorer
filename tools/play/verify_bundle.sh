#!/bin/bash
# Static audit of a trusted local AAB; derived APK uses the known DEBUG key only.
set -euo pipefail
if [ "$#" -ne 3 ]; then
    echo 'Usage: verify_bundle.sh INPUT.aab rehearsal|production NEW_REPORT_DIRECTORY' >&2
    exit 2
fi
scorer_bundle="$1"
scorer_channel="$2"
scorer_report="$3"
case "$scorer_channel" in rehearsal|production) ;; *) exit 2 ;; esac
if [ ! -f "$scorer_bundle" ] || [ -e "$scorer_report" ]; then
    echo 'Bundle must exist; report directory must be a fresh path.' >&2
    exit 2
fi
mkdir -p "$scorer_report"
scorer_bundletool="${BUNDLETOOL_JAR:-/work/toolchain/bundletool-all-1.18.1.jar}"
scorer_sdk="${ANDROID_SDK_ROOT:-/work/toolchain/android-sdk}"
scorer_test_key="${SCORER_TEST_KEYSTORE:-/work/cache/android-user/debug.keystore}"
java -jar "$scorer_bundletool" validate --bundle="$scorer_bundle" > "$scorer_report/bundletool-validation.txt"
java -jar "$scorer_bundletool" dump manifest --bundle="$scorer_bundle" --module=base > "$scorer_report/manifest.xml"
java -jar "$scorer_bundletool" dump config --bundle="$scorer_bundle" > "$scorer_report/bundle-config.json"
python tools/play/verify.py "$scorer_bundle" --manifest "$scorer_report/manifest.xml" --channel "$scorer_channel" > "$scorer_report/static-report.json"
python - "$scorer_report/bundle-config.json" <<'PY'
import json,sys
with open(sys.argv[1]) as f: config=json.load(f)
assert config['optimizations']['uncompressNativeLibraries']['alignment']=='PAGE_ALIGNMENT_16K'
print('PASS: AAB requests 16KiB native ZIP alignment')
PY
python tools/android/verify_elf_alignment.py "$scorer_bundle" --readelf "$scorer_sdk/ndk/28.2.13676358/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-readelf" > "$scorer_report/elf.txt"
# Public Android DEBUG key/password; never an upload/production key. No purchase enabled.
java -jar "$scorer_bundletool" build-apks --bundle="$scorer_bundle" --output="$scorer_report/inspection.apks" --mode=universal \
    --ks="$scorer_test_key" --ks-pass=pass:android --ks-key-alias=androiddebugkey --key-pass=pass:android > "$scorer_report/apks-generation.txt" 2>&1
python - "$scorer_report" <<'PY'
from pathlib import Path
import sys,zipfile
p=Path(sys.argv[1])
with zipfile.ZipFile(p/'inspection.apks') as z: (p/'inspection-universal-debug-signed.apk').write_bytes(z.read('universal.apk'))
PY
scorer_apk="$scorer_report/inspection-universal-debug-signed.apk"
"$scorer_sdk/build-tools/36.0.0/apksigner" verify --verbose --print-certs "$scorer_apk" > "$scorer_report/apk-signature.txt"
"$scorer_sdk/build-tools/36.0.0/zipalign" -c -P 16 4 "$scorer_apk"
/work/shared-platform/build-arm64-v8a/build/other_builds/hostpython3/desktop/hostpython3/native-build/python tools/verify_apk_edition.py "$scorer_apk" free
jarsigner -verify "$scorer_bundle" > "$scorer_report/aab-signature.txt"
sha256sum "$scorer_bundle" "$scorer_apk" > "$scorer_report/SHA256SUMS"
echo 'Static audit passed. Check AAB signing status separately; device/Play purchase tests remain mandatory.'
