#!/bin/bash
# Google SDK licence accepted by the project owner in this session, 2026-10-23.
# No preview packages or real payment/release operations are requested.
set -euo pipefail
cd /workspace/Scorer
mkdir -p /workspace/striker-android-build/cache
python3 - <<'PY'
from pathlib import Path
import hashlib, subprocess, tempfile, urllib.request, xml.etree.ElementTree as ET
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
destination = base / 'android-sdk/cmdline-tools/19.0'
if not (destination / 'bin/sdkmanager').is_file():
    archives = (
        archive
        for package in root.findall('remotePackage')
        if package.attrib.get('path') == 'cmdline-tools;19.0'
        for archive in package.findall('./archives/archive')
        if archive.findtext('host-os') == 'linux'
    )
    archive = next(archives, None)
    if archive is None:
        raise SystemExit('Pinned SDK command line tools unavailable')
    complete = archive.find('complete')
    with tempfile.TemporaryDirectory(prefix='cli19-', dir=base) as temporary:
        stage = Path(temporary)
        download = stage / Path(complete.findtext('url')).name
        urllib.request.urlretrieve(url + download.name, download)
        with download.open('rb') as source:
            digest = hashlib.file_digest(source, complete.find('checksum').attrib['type'])
        if digest.hexdigest() != complete.findtext('checksum'):
            raise SystemExit('SDK archive verification failed')
        subprocess.run(['unzip', '-q', str(download), '-d', str(stage)], check=True)
        destination.parent.mkdir(parents=True, exist_ok=True)
        (stage / 'cmdline-tools').rename(destination)
link = base / 'android-sdk/tools'
if not link.exists():
    link.symlink_to('cmdline-tools/19.0')
PY
bash tools/android/run.sh bash -c 'set +o pipefail; yes | /work/toolchain/android-sdk/cmdline-tools/19.0/bin/sdkmanager --sdk_root=/work/toolchain/android-sdk "platforms;android-36" "build-tools;36.0.0" "platform-tools" "ndk;28.2.13676358"; exit ${PIPESTATUS[1]}'
