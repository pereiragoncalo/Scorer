#!/bin/bash
# Google SDK licence accepted by the project owner in this session, 2026-10-23.
# No preview packages or real payment/release operations are requested.
set -euo pipefail
cd /workspace/Scorer
mkdir -p /workspace/striker-android-build/cache
python3 - <<'PY'
from pathlib import Path
import urllib.request, xml.etree.ElementTree as ET, hashlib
base = Path('/workspace/striker-android-build')
url = 'https://dl.google.com/android/repository/'
with urllib.request.urlopen(url + 'repository2-3.xml') as response:
    metadata = response.read()
(base / 'repository2-3.xml').write_bytes(metadata)
root = ET.fromstring(metadata)
terms = next(item.text for item in root.findall('license')
             if item.attrib.get('id') == 'android-sdk-license')
if hashlib.sha256(terms.encode()).hexdigest() != '1f8729233617b193fd619213792ae16a41b95d2bbbf525dfe66998252ba68b16':
    raise SystemExit('Android SDK licence changed; owner must review new terms')
for p in root.findall('remotePackage'):
    if p.attrib.get('path') != 'cmdline-tools;19.0':
        continue
    for archive in p.findall('./archives/archive'):
        if archive.findtext('host-os') != 'linux':
            continue
        complete = archive.find('complete')
        target = base / complete.findtext('url')
        if not target.exists():
            urllib.request.urlretrieve(url + target.name, target)
        digest = hashlib.new(complete.find('checksum').attrib['type'])
        with target.open('rb') as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b''):
                digest.update(chunk)
        if digest.hexdigest() != complete.findtext('checksum'):
            raise SystemExit('SDK archive verification failed')
        if not (base / 'android-sdk/cmdline-tools/19.0/bin/sdkmanager').exists():
            import subprocess
            stage = base / 'cli19-extracted'
            subprocess.run(['unzip', '-q', str(target), '-d', str(stage)], check=True)
            destination = base / 'android-sdk/cmdline-tools/19.0'
            destination.parent.mkdir(parents=True, exist_ok=True)
            (stage / 'cmdline-tools').rename(destination)
        break
    break
else:
    raise SystemExit('Pinned SDK command line tools unavailable')
link = base / 'android-sdk/tools'
if not link.exists():
    link.symlink_to('cmdline-tools/19.0')
PY
bash tools/android/run.sh bash -c 'set +o pipefail; yes | /work/toolchain/android-sdk/cmdline-tools/19.0/bin/sdkmanager --sdk_root=/work/toolchain/android-sdk "platforms;android-36" "build-tools;36.0.0" "platform-tools" "ndk;28.2.13676358"; exit ${PIPESTATUS[1]}'
