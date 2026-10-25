"""Stage independent Free/World QA APK sources; no publication or payment activation."""
import argparse
import configparser
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.play.prepare import ROOT, prepare


def prepare_edition(product, target, source=ROOT):
    if product not in ('free', 'world'):
        raise ValueError('Choose free or world')
    source = Path(source)
    config = json.loads((source/'release/play.example.json').read_text())
    config['version_code'] = 1026632
    config['billing']['enabled'] = False
    target = prepare(config, Path(target), 'rehearsal', source)
    identity = target/'edition.py'
    text = identity.read_text().replace('WORLD_PREVIEW = True', 'WORLD_PREVIEW = False')
    text = text.replace('WORLD_BUILD = False', 'WORLD_BUILD = '+str(product == 'world'), 1)
    identity.write_text(text)
    spec = configparser.ConfigParser(interpolation=None); spec.read(target/'buildozer.spec')
    app = spec['app']
    app['title'] = 'Scorer World' if product == 'world' else 'Scorer'
    app['icon.filename'] = 'assets/icon_world.png' if product == 'world' else 'assets/icon.png'
    app['package.domain'], app['package.name'] = 'com.clemir', 'scorerworld' if product == 'world' else 'striker'
    app['version'], app['android.numeric_version'] = '0.6.32', '1026632'
    # Both products share a Python/Kivy native distribution, not an Android identity.
    app['p4a.extra_args'] = '--dist_name=striker'
    app['scorer.shared_native_dist'] = 'striker'
    # In-app billing has no role in either separate product.
    (target/'billing.py').unlink(missing_ok=True)
    shutil.rmtree(target/'android/src/com/clemir/striker/billing', ignore_errors=True)
    app['android.gradle_dependencies'] = ','.join(x for x in app.get('android.gradle_dependencies','').split(',') if 'billingclient' not in x)
    if product == 'world':
        app['android.add_src'] = 'android/worldsrc'
        app['android.permissions'] = ''
        for option in ('android.meta_data','android.gradle_dependencies','android.extra_manifest_xml'):
            app.pop(option, None)
        shutil.rmtree(target/'android/src', ignore_errors=True)
    else:
        app['android.add_src'] = 'android/src'
        (target/'assets/icon_world.png').unlink(missing_ok=True)
        # Free always renders English and carries no extra-language assets.
        shutil.rmtree(target/'assets/i18n',ignore_errors=True)
        for font in (target/'assets/fonts').glob('*Noto*'):font.unlink()

    with (target/'buildozer.spec').open('w') as f:spec.write(f)
    # Do not ship historical in-app mode state or obsolete QA launch scripts.
    (target/'career_mode_state.py').unlink(missing_ok=True)
    (target/'.scorer-edition').write_text(product+'\nQA build. No production store or payment activation.\n')
    return target


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--edition',choices=('free','world'),required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();print(prepare_edition(args.edition,args.output))
