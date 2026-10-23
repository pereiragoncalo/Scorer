"""Keep pip TLS verification when p4a filters certificate environment variables."""
import configparser
from pathlib import Path


def configure(path: Path) -> None:
    config = configparser.ConfigParser()
    if path.exists():
        with path.open(encoding='utf-8') as source:
            config.read_file(source)
    if not config.has_section('global'):
        config.add_section('global')
    config.set('global', 'cert', '/run/ca-bundle.crt')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as output:
        config.write(output)


if __name__ == '__main__':
    configure(Path('/workspace/striker-android-build/cache/user/.config/pip/pip.conf'))
