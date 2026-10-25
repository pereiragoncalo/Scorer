"""Generate an isolated single-app Play build. No upload, purchase activation or signing.

Rehearsal is a release-mode AAB with TEST ads and billing disabled. Production
requires explicit public configuration. Never overwrite the source checkout.
"""
import argparse
import base64
import configparser
import json
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
TEST_APP = 'ca-app-pub-3940256099942544~3347511713'
TEST_IDS = {'banner_id': 'ca-app-pub-3940256099942544/6300978111',
            'interstitial_id': 'ca-app-pub-3940256099942544/1033173712',
            'rewarded_id': 'ca-app-pub-3940256099942544/5224354917'}


def https_url(value):
    if not isinstance(value, str) or any(c.isspace() for c in value):
        return False
    try:
        u = urlsplit(value)
        return u.scheme == 'https' and bool(u.hostname) and not u.username and not u.password and not u.fragment and u.port in (None, 443)
    except ValueError:
        return False


def validate(data, channel):
    errors = []
    if channel not in ('production', 'rehearsal'):
        return ['Unknown release channel']
    if not isinstance(data, dict) or set(data) != {'schema', 'version_code', 'developer_name', 'support_email', 'privacy_url', 'admob', 'billing'}:
        return ['Invalid public release configuration schema']
    if type(data['schema']) is not int or data['schema'] != 1:
        errors.append('Unsupported configuration version')
    if type(data['version_code']) is not int or not 1026625 <= data['version_code'] <= 2100000000:
        errors.append('version_code must be an unused integer >= 1026625; confirm against Play Console')
    ads, billing = data['admob'], data['billing']
    if not isinstance(ads, dict) or set(ads) != {'app_id', *TEST_IDS}:
        errors.append('Invalid AdMob configuration')
    if not isinstance(billing, dict) or set(billing) != {'enabled', 'product_id', 'verify_url', 'license_public_key'}:
        errors.append('Invalid Billing configuration')
    if errors:
        return errors
    if type(billing['enabled']) is not bool or billing['product_id'] != 'scorer_world_upgrade':
        errors.append('Billing must use the fixed non-consumable World product')
    if channel == 'production':
        if not isinstance(data['developer_name'], str) or not 2 <= len(data['developer_name'].strip()) <= 100:
            errors.append('Public developer identity is required')
        if not isinstance(data['support_email'], str) or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', data['support_email']):
            errors.append('Public support email is required')
        if not https_url(data['privacy_url']):
            errors.append('Public HTTPS privacy policy URL is required')
        for key, value in ads.items():
            sep = '~' if key == 'app_id' else '/'
            if (not isinstance(value, str) or not re.fullmatch(r'ca-app-pub-\d{16}' + re.escape(sep) + r'\d{10}', value)
                    or value.startswith('ca-app-pub-3940256099942544')):
                errors.append('Owner production AdMob ID required: ' + key)
        if len({v.split('~')[0].split('/')[0] for v in ads.values() if isinstance(v, str)}) != 1:
            errors.append('All AdMob IDs must belong to the same publisher')
        if len(set(ads.values())) != 4:
            errors.append('Each AdMob placement must have a distinct ID')
        if not billing['enabled']:
            errors.append('World purchase must be configured and approved before this production profile')
    if billing['enabled']:
        if not https_url(billing['verify_url']):
            errors.append('HTTPS purchase-verification endpoint required')
        try:
            # Public X509 SubjectPublicKeyInfo DER, not private signing material.
            key = base64.b64decode(billing['license_public_key'], validate=True)
            from cryptography.hazmat.primitives.serialization import load_der_public_key
            from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
            public = load_der_public_key(key)
            if not isinstance(public, RSAPublicKey) or public.key_size < 2048:
                raise ValueError()
        except Exception:
            errors.append('Valid RSA public key (DER/base64, >=2048 bits) required')
    if channel == 'rehearsal' and billing['enabled']:
        errors.append('Rehearsal never enables payments; use Play licence testers only after explicit approval')
    return errors


def prepare(config, target, channel, source=ROOT):
    errors = validate(config, channel)
    if errors:
        raise ValueError('\n'.join(errors))
    source, target = Path(source).resolve(), Path(target).resolve()
    if target == source or source in target.parents or target in source.parents:
        raise ValueError('Staging must be outside the source checkout')
    if target.exists() and any(target.iterdir()):
        raise ValueError('Use a fresh empty staging directory; refusing stale or unrelated files')
    target.mkdir(parents=True, exist_ok=True)
    # Explicit allowlist; no saves, tests, signing keys, local config or server credentials.
    for item in source.glob('*.py'):
        shutil.copyfile(item, target/item.name)
    shutil.copyfile(source/'buildozer.spec', target/'buildozer.spec')
    def ignored(directory, names):
        return [n for n in names if n == '__pycache__' or n.startswith('.') or
                (Path(n).suffix.lower() in ('.jks', '.keystore', '.pem', '.p12', '.log') or
                (Path(n).suffix.lower() == '.json' and not (Path(directory) == source/'assets/data' and n == 'world_clubs.json')))]
    for directory in ('assets', 'android', 'tools'):
        shutil.copytree(source/directory, target/directory, ignore=ignored)
    (target/'edition.py').write_text((target/'edition.py').read_text().replace('WORLD_PREVIEW = True', 'WORLD_PREVIEW = False'))
    (target/'release_settings.py').write_text('\n'.join(f'{key} = {value!r}' for key, value in {
        'CHANNEL': channel, 'DEVELOPER_NAME': config['developer_name'], 'SUPPORT_EMAIL': config['support_email'],
        'PRIVACY_URL': config['privacy_url']}.items()) +
        '\n\ndef is_store(): return True\ndef is_production(): return CHANNEL == "production"\n')
    spec = configparser.ConfigParser(interpolation=None)
    spec.read(target/'buildozer.spec'); app = spec['app']
    app['title'] = 'SCORER' if channel == 'production' else 'SCORER Play QA'
    app['package.domain'], app['package.name'] = 'com.clemir', 'striker'
    app['android.numeric_version'] = str(config['version_code'])
    app['android.allow_backup'] = 'False'
    app['android.release_artifact'] = 'aab'
    app['android.meta_data'] = 'com.google.android.gms.ads.APPLICATION_ID=' + (config['admob']['app_id'] if channel == 'production' else TEST_APP)
    with (target/'buildozer.spec').open('w') as out: spec.write(out)
    ids = config['admob'] if channel == 'production' else TEST_IDS
    java = ('package com.clemir.striker.ads;\npublic final class AdsConfig {\n'
            f' public static final boolean TEST_MODE = {str(channel != "production").lower()};\n')
    for field, key in [('INTERSTITIAL', 'interstitial_id'), ('BANNER', 'banner_id'), ('REWARDED', 'rewarded_id')]:
        java += f' public static final String {field} = {json.dumps(ids[key])};\n'
    (target/'android/src/com/clemir/striker/ads/AdsConfig.java').write_text(java+'}\n')
    billing = config['billing']
    java = ('package com.clemir.striker.billing;\npublic final class BillingConfig {\n'
            f' public static final boolean ENABLED = {str(billing["enabled"]).lower()};\n')
    for field, key in [('PRODUCT', 'product_id'), ('VERIFY_URL', 'verify_url'), ('LICENSE_PUBLIC_KEY', 'license_public_key')]:
        java += f' public static final String {field} = {json.dumps(billing[key])};\n'
    (target/'android/src/com/clemir/striker/billing/BillingConfig.java').write_text(java+'}\n')
    (target/'.scorer-play-staging').write_text(channel+'\n')
    # Existing managed container provides shared platform; builds must be sequential.
    platform = target/'.buildozer/android/platform'; platform.parent.mkdir(parents=True, exist_ok=True)
    platform.symlink_to('/work/shared-platform', target_is_directory=True)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT/'release/play.example.json')
    parser.add_argument('--channel', choices=('rehearsal', 'production'), default='rehearsal')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(); data = json.loads(args.config.read_text())
    errors = validate(data, args.channel)
    if errors: parser.exit(2, '\n'.join(errors)+'\n')
    if args.check: print('Public release configuration valid:', args.channel); return
    if args.output is None: parser.error('--output is required')
    print(prepare(data, args.output, args.channel))


if __name__ == '__main__':
    raise SystemExit('Single-app release CLI is retired. Use tools/prepare_editions.py for separate Free/World QA builds.')
