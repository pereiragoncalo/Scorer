"""Publish the audited AAB's bytes and bind the bastion scripts to the build."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import xml.etree.ElementTree as ET

source, output = map(Path, sys.argv[1:])
bundle = source / 'bin/Scorer-World-1.0-1030043-unsigned.aab'
report = json.loads((source / 'qa-aab-report.json').read_text())
with bundle.open('rb') as stream:
    digest = hashlib.file_digest(stream, 'sha256').hexdigest()
size = bundle.stat().st_size
assert report['sha256'] == digest and report['size_bytes'] == size
assert report['compiled_source_verified'] and report['bundletool_validated']
xml = ET.parse(source / 'bundle-manifest.xml').getroot()
android = '{http://schemas.android.com/apk/res/android}'
assert xml.attrib['package'] == 'com.clemir.scorerworld'
assert xml.attrib[android + 'versionCode'] == '1030043'
assert xml.attrib[android + 'versionName'] == '1.0'
with bundle.open('rb') as stream:
    for part in range(256):
        data = stream.read(8 * 1024 * 1024)
        if not data:
            break
        (output / f'aab.part.{part:02d}').write_bytes(data)
    else:
        raise ValueError('Unexpectedly large bundle')
uploader = Path(__file__).with_name('bastion_publish_1030043.py').read_text()
uploader = re.sub(r'^BUNDLE_SHA = .*$', 'BUNDLE_SHA = '+repr(digest), uploader, flags=re.M)
uploader = re.sub(r'^BUNDLE_BYTES = .*$', 'BUNDLE_BYTES = '+str(size), uploader, flags=re.M)
(output / 'bastion_play_internal.py').write_text(uploader)
shutil.copyfile(Path(__file__).with_name('promote_alpha_1030043.py'),
                output / 'promote_alpha_1030043.py')
for name in ('qa-aab-report.json', 'bundle-manifest.xml'):
    shutil.copyfile(source / name, output / name)
