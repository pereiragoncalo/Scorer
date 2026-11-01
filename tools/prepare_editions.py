"""Stage independent Free/World QA APK sources; no publication or payment activation."""
import argparse
import configparser
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.play.prepare import ROOT, prepare


def prepare_edition(product, target, source=ROOT, analytics_endpoint=None, channel='rehearsal', config=None, publication=None):
    if product not in ('free', 'world'):
        raise ValueError('Choose free or world')
    from anonymous_stats import valid_endpoint
    if analytics_endpoint is None:
        ns={};exec((Path(source)/'analytics_config.py').read_text(),ns)
        analytics_endpoint=ns['ENDPOINT']
    if analytics_endpoint and not valid_endpoint(analytics_endpoint):
        raise ValueError('Analytics needs an HTTPS /v1/usage endpoint')
    source = Path(source)
    launch=json.loads((source/'release/world-launch.json').read_text())
    config_name='play.production.example.json' if channel=='production' else 'play.example.json'
    config = dict(config) if config is not None else json.loads((source/'release'/config_name).read_text())
    if channel=='rehearsal':config['version_code']=launch['next_test_version_code']
    if channel=='production':
        if product not in launch['play_products']:raise ValueError('Only Scorer World is approved for the current Google Play launch; Free remains legacy QA only')
        from tools.play.publication import validate_publication
        errors=validate_publication(publication)
        if errors:raise ValueError('\n'.join(errors))
        if type(config.get('version_code')) is not int or config['version_code']<=launch['next_test_version_code']:raise ValueError('Production versionCode must be above the 0.9 test code; confirm it is unused in Play Console')
    if channel=='rehearsal':config['billing']['enabled'] = False
    target = prepare(config, Path(target), channel, source)
    identity = target/'edition.py'
    text = identity.read_text().replace('WORLD_PREVIEW = True', 'WORLD_PREVIEW = False')
    text = text.replace('WORLD_BUILD = False', 'WORLD_BUILD = '+str(product == 'world'), 1)
    identity.write_text(text)
    spec = configparser.ConfigParser(interpolation=None); spec.read(target/'buildozer.spec')
    app = spec['app']
    app['title'] = 'Scorer World' if product == 'world' else 'Scorer'
    app['icon.filename'] = 'assets/icon_world.png' if product == 'world' else 'assets/icon.png'
    app['package.domain'], app['package.name'] = 'com.clemir', 'scorerworld' if product == 'world' else 'striker'
    app['version'] = launch['production_version'] if channel=='production' else launch['next_test_version']
    app['android.numeric_version'] = str(config['version_code'])
    (target/'release_settings.py').write_text((target/'release_settings.py').read_text()+"\nWORLD_LISTING_READY = False\n")
    # Both products share a Python/Kivy native distribution, not an Android identity.
    app['p4a.extra_args'] = '--dist_name=striker'
    app['scorer.shared_native_dist'] = 'striker'
    # In-app billing has no role in either separate product.
    (target/'billing.py').unlink(missing_ok=True)
    shutil.rmtree(target/'android/src/com/clemir/striker/billing', ignore_errors=True)
    # Both Android editions share the ad-free Java source set and no monetization SDK.
    app['android.add_src']='android/worldsrc'
    app['android.permissions']='INTERNET,ACCESS_NETWORK_STATE'
    for option in ('android.meta_data','android.gradle_dependencies','android.extra_manifest_xml'):
        app.pop(option,None)
    shutil.rmtree(target/'android/src',ignore_errors=True)
    (target/'analytics_config.py').write_text('ENDPOINT = '+repr(analytics_endpoint)+'\n')
    if product == 'free':
        (target/'assets/icon_world.png').unlink(missing_ok=True)
        (target/'assets/menu_logo_world.png').unlink(missing_ok=True)
        # Free always renders English and carries no extra-language assets.
        shutil.rmtree(target/'assets/i18n',ignore_errors=True)
        for font in (target/'assets/fonts').glob('*Noto*'):font.unlink()

    with (target/'buildozer.spec').open('w') as f:spec.write(f)
    # Do not ship historical in-app mode state or obsolete QA launch scripts.
    (target/'career_mode_state.py').unlink(missing_ok=True)
    (target/'privacy_requests.py').unlink(missing_ok=True)
    (target/'.scorer-edition').write_text(product+'\nBuild preparation only. No store upload or payment activation.\n')
    return target


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--edition',choices=('free','world'),required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--channel',choices=('rehearsal','production'),default='rehearsal')
    p.add_argument('--config',type=Path)
    p.add_argument('--publication-config',type=Path)
    p.add_argument('--analytics-endpoint',default=None,help='Public HTTPS /v1/usage URL; omitted uses configured owner endpoint, empty disables uploads')
    args=p.parse_args();print(prepare_edition(args.edition,args.output,analytics_endpoint=args.analytics_endpoint,channel=args.channel,config=json.loads(args.config.read_text()) if args.config else None,publication=json.loads(args.publication_config.read_text()) if args.publication_config else None))
