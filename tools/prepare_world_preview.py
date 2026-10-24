"""Create an isolated World test build; never change the Free checkout identity."""
from pathlib import Path
import shutil
import configparser


def prepare():
    source = Path(__file__).resolve().parents[1]
    target = source.parent / 'Scorer-world-preview'
    marker = target / '.scorer-world-preview'
    if target.exists() and not marker.exists():
        raise RuntimeError('Refusing to overwrite an unrelated directory')
    target.mkdir(exist_ok=True)
    marker.write_text('Generated World preview build source. Not a paid release.\n')
    shutil.copytree(source, target, dirs_exist_ok=True, ignore=shutil.ignore_patterns(
        '.git', '.buildozer', 'bin', '__pycache__', 'baseline', 'tests', 'ui_tests', 'docs', 'server', 'release', '*.apk', '*.jks', '*.keystore', '*.pem', '*.p12', 'striker_*career*.json'))
    identity = target / 'edition.py'
    identity.write_text(identity.read_text().replace('WORLD_PREVIEW = False', 'WORLD_PREVIEW = True', 1))
    spec = configparser.ConfigParser(interpolation=None)
    spec.read(target/'buildozer.spec')
    app = spec['app']
    app['title'] = 'SCORER World Preview'
    app['package.name'] = 'preview'
    app['package.domain'] = 'com.clemir.strikerworld'
    app['android.permissions'] = ''
    app['android.add_src'] = 'android/worldsrc'
    for option in ('android.gradle_dependencies','android.meta_data','android.extra_manifest_xml'):
        app.pop(option, None)
    with (target/'buildozer.spec').open('w') as handle:
        spec.write(handle)
    platform = target/'.buildozer/android/platform'
    platform.parent.mkdir(parents=True, exist_ok=True)
    if not platform.is_symlink() and not platform.exists():
        platform.symlink_to('/work/shared-platform', target_is_directory=True)
    print(target)


if __name__ == '__main__':
    prepare()
