"""Promote the existing Scorer World 1030042 release from Internal to Alpha."""
import argparse
import fcntl
import hashlib
import os
from pathlib import Path
import sys
import tempfile
from urllib.parse import quote
from urllib.request import urlopen
import runpy

VERSION = 1030042
SIGNED = Path("/home/clemir/Scorer-World-1.0-1030042-r2.aab")
HELPER = 'https://raw.githubusercontent.com/pereiragoncalo/Scorer/6cf4e4fcd6963fee20c1c2c6a226e9eba6391e30/tools/play/bastion_play_internal.py'
HELPER_SHA = 'bc0725dac5c1132ce4542d76e9d3777ade333ea2a83ba23cde457def0594e983'


def codes(release):
    return {int(code) for code in release.get('versionCodes', [])}


def promote(client, base, api_error, publish, signed_digest):
    edit_id = client.api('POST', base, {})['id']
    edit = base + '/' + quote(edit_id, safe='')
    commit_attempted = False
    try:
        internal = client.api('GET', edit + '/tracks/internal')['releases']
        alpha = client.api('GET', edit + '/tracks/alpha').get('releases', [])
        bundles = client.api('GET', edit + '/bundles').get('bundles', [])
        bundle = next((row for row in bundles if int(row['versionCode']) == VERSION), None)
        if bundle is None or bundle.get('sha256', '').lower() != signed_digest:
            raise ValueError('O bundle 1030042 na Google Play não corresponde ao AAB assinado desta revisão.')
        if any(VERSION in codes(row) and row.get('status') == 'completed' for row in alpha):
            print('O 1030042 já consta de uma release concluída na Alpha.')
            return
        source = next((row for row in internal if VERSION in codes(row)
                       and row.get('status') == 'completed'), None)
        if source is None:
            raise ValueError('O 1030042 não consta de uma release concluída em Internal.')
        if any(any(code > VERSION for code in codes(row)) for row in alpha):
            raise ValueError('A Alpha já contém uma versão superior.')
        if len(alpha) > 1 or any(row.get('status') != 'completed' for row in alpha):
            raise ValueError('A Alpha tem várias releases ou uma release pendente. Verifica a Play Console.')
        if not publish:
            print('1030042 em Internal. A Alpha pode receber a promoção.')
            return

        release = {'name': '1.0 (1030042)', 'status': 'completed',
                   'versionCodes': [str(VERSION)]}
        if source.get('releaseNotes'):
            release['releaseNotes'] = source['releaseNotes']
        result = client.api('PUT', edit + '/tracks/alpha',
                            {'track': 'alpha', 'releases': [release]})
        confirmed = result.get('releases', [])
        if (result.get('track') != 'alpha' or len(confirmed) != 1
                or codes(confirmed[0]) != {VERSION} or confirmed[0].get('status') != 'completed'):
            raise ValueError('A Google Play devolveu uma release diferente da esperada.')
        client.api('POST', edit + ':validate')
        commit_attempted = True
        try:
            client.api('POST', edit + ':commit?changesInReviewBehavior=ERROR_IF_IN_REVIEW')
        except Exception as error:
            if isinstance(error, api_error) and 400 <= error.status < 500:
                commit_attempted = False
                raise
            raise RuntimeError('A resposta ao commit perdeu-se. Confirma o estado na Play Console antes de repetir.') from error
        print('1030042 submetido à Alpha. Confirma na Play Console quando estiver disponível.')
    finally:
        if not commit_attempted:
            try:
                client.api('DELETE', edit)
            except Exception:
                print('A edição temporária não pôde ser eliminada. Expira automaticamente.', file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish', action='store_true', help='Submeter a promoção à Google Play')
    args = parser.parse_args()
    os.umask(0o077)
    with tempfile.TemporaryDirectory(prefix='scorer-alpha-') as temporary:
        with urlopen(HELPER, timeout=30) as response:
            data = response.read(128 * 1024)
        if hashlib.sha256(data).hexdigest() != HELPER_SHA:
            raise ValueError('Checksum do cliente da Google Play inválido.')
        path = Path(temporary) / 'play_api.py'
        path.write_bytes(data)
        helper = runpy.run_path(str(path))
        private = helper['private_directory'](helper['PRIVATE'])
        fd = os.open(private / 'play-internal.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            client = helper['Client'](helper['load_account'](helper['CREDENTIALS']))
            if not SIGNED.is_file() or SIGNED.is_symlink():
                raise ValueError('Falta o AAB assinado da revisão nova. Publica primeiro em Internal.')
            promote(client, helper['BASE'], helper['APIError'], args.publish, helper['sha'](SIGNED))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        sys.exit(f'Promoção interrompida. {error}')
