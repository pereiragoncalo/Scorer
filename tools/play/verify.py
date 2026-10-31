"""Inspect the actual AAB/APK for single-app Play release invariants.

Manifest XML must come from bundletool dump manifest (AAB) or apkanalyzer (APK).
This does not replace upload signing, Play pre-launch reports or device tests.
"""
import argparse
import io
import json
from pathlib import Path
import tarfile
import xml.etree.ElementTree as ET
import zipfile

ANDROID = '{http://schemas.android.com/apk/res/android}'
FORBIDDEN_PERMISSIONS = {'com.google.android.gms.permission.AD_ID',
    'android.permission.ACCESS_ADSERVICES_AD_ID', 'android.permission.ACCESS_ADSERVICES_ATTRIBUTION',
    'android.permission.ACCESS_ADSERVICES_TOPICS', 'android.permission.MANAGE_EXTERNAL_STORAGE',
    'android.permission.READ_EXTERNAL_STORAGE', 'android.permission.WRITE_EXTERNAL_STORAGE',
    'android.permission.QUERY_ALL_PACKAGES', 'android.permission.ACCESS_FINE_LOCATION',
    'android.permission.CAMERA', 'android.permission.RECORD_AUDIO','com.android.vending.BILLING'}


def inspect_manifest(text,expected_package='com.clemir.striker'):
    root = ET.fromstring(text)
    app = root.find('application'); sdk = root.find('uses-sdk')
    if root.get('package') != expected_package: raise ValueError('Wrong application identity')
    if int(root.get(ANDROID+'versionCode', '0')) < 1026625: raise ValueError('Stale version code')
    if sdk is None or int(sdk.get(ANDROID+'targetSdkVersion', '0')) < 36: raise ValueError('Target SDK too old')
    if int(sdk.get(ANDROID+'minSdkVersion', '0')) != 26: raise ValueError('Unexpected minimum SDK')
    if app is None or app.get(ANDROID+'debuggable', 'false') != 'false': raise ValueError('Debuggable artifact')
    if app.get(ANDROID+'allowBackup') != 'false': raise ValueError('Backup must be disabled')
    if app.get(ANDROID+'usesCleartextTraffic') != 'false': raise ValueError('Cleartext networking must be disabled')
    permissions = {p.get(ANDROID+'name') for p in root.findall('uses-permission')}
    if permissions & FORBIDDEN_PERMISSIONS: raise ValueError('Forbidden permissions: '+str(permissions & FORBIDDEN_PERMISSIONS))
    if 'android.permission.INTERNET' not in permissions:
        raise ValueError('Online features Internet permission missing')
    if any(e.get(ANDROID+'name')=='com.google.android.gms.ads.APPLICATION_ID' for e in root.findall('application/meta-data')):
        raise ValueError('Advertising metadata remains')
    if any('com.clemir.strikerworld' in p.get(ANDROID+'name', '') for p in root.findall('queries/package')):
        raise ValueError('Legacy companion-app query remains')
    return root, sorted(permissions)


def verify(artifact, manifest, channel,expected_package='com.clemir.striker'):
    root, permissions = inspect_manifest(manifest,expected_package)
    with zipfile.ZipFile(artifact) as archive:
        names = archive.namelist()
        if any(n.startswith(('base/lib/armeabi', 'lib/armeabi')) for n in names): raise ValueError('Unexpected 32-bit payload')
        dex = b''.join(archive.read(n) for n in names if n.endswith('.dex'))
        for forbidden in (b'Lcom/google/android/gms/ads/',b'Lcom/google/android/ump/',b'Lcom/clemir/striker/ads/',b'Lcom/android/billingclient/',b'Lcom/clemir/striker/billing/'):
            if forbidden in dex:raise ValueError('Advertising/billing code packaged: '+forbidden.decode())
        if b'Lcom/clemir/striker/files/LocalNameFiles;' not in dex:raise ValueError('Local document bridge absent')
        private = next(n for n in names if n.endswith('assets/private.tar'))
        with tarfile.open(fileobj=io.BytesIO(archive.read(private))) as payload:
            files = payload.getnames()
            for expected in ('career.pyc','edition.pyc','release_settings.pyc','world_ui.pyc','name_packs.pyc','world_clubs.pyc'):
                if not any(n.endswith('/'+expected) or n == expected for n in files): raise ValueError('Missing '+expected)
            if any('/server/' in '/'+n or n.lower().endswith(('.pem','.jks','.keystore','.p12')) or 'striker_career' in n or 'striker_world_career' in n or n.endswith('release.local.json') for n in files):
                raise ValueError('Private state or server/signing material packaged')
            data_member = next(m for m in payload if m.name.endswith('assets/data/world_clubs.json'))
            import json
            data = json.load(payload.extractfile(data_member))
            if data.get('version') != 1 or len(data.get('clubs', {})) != 9896:
                raise ValueError('World presentation catalogue missing or incomplete')
            edition = next(m for m in payload if m.name.endswith('/edition.pyc') or m.name == 'edition.pyc')
            # Flag is checked separately with the built Python version; do not unmarshal untrusted input here.
            if edition.size > 16384: raise ValueError('Unexpected edition module')
    return {'package':root.get('package'), 'version_code':root.get(ANDROID+'versionCode'),
            'channel':channel,'permissions':permissions,'static_checks':'pass',
            'device_tests':'pending','in_app_billing':'absent','production_signing':'not established'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('artifact',type=Path);parser.add_argument('--manifest',required=True,type=Path)
    parser.add_argument('--channel',choices=('rehearsal','production'),required=True)
    parser.add_argument('--package',choices=('com.clemir.striker','com.clemir.scorerworld'),default='com.clemir.striker')
    args=parser.parse_args()
    print(json.dumps(verify(args.artifact,args.manifest.read_text(),args.channel,args.package),indent=2))
