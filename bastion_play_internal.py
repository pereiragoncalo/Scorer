"""Check or publish Scorer World 1030042 to Google Play Internal from the bastion."""
import argparse
import fcntl
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import sys
import tempfile
from urllib.request import urlopen
import zipfile

VERSION = 1030042
BUNDLE = 'Scorer-World-1.0-1030042-unsigned.aab'
TRANSFER_URL = 'https://raw.githubusercontent.com/pereiragoncalo/Scorer/transfer-world-1030042-r2/'
PART_BYTES = 8 * 1024 * 1024
BUNDLE_SHA = 'a4c0ca14b10634c1ec4d70b81d60148c25bf73485da10fd995fa5e503b030ecc'
BUNDLE_BYTES = 123969834
UPLOADER_SHA = 'bc0725dac5c1132ce4542d76e9d3777ade333ea2a83ba23cde457def0594e983'
SIGNER_SHA = '5492d1fa8de0e3072960a0c34eaf05548cdaaa51c84f154d8ef579c885fa6761'
SOURCE = 'https://raw.githubusercontent.com/pereiragoncalo/Scorer/6cf4e4fcd6963fee20c1c2c6a226e9eba6391e30/tools/play/'
SIGNED = Path('/home/clemir/Scorer-World-1.0-1030042-r2.aab')


def load_helper(directory, filename, expected):
    with urlopen(SOURCE + filename, timeout=30) as response:
        source = response.read(128 * 1024)
    if hashlib.sha256(source).hexdigest() != expected:
        raise ValueError('SHA-256 inesperado para ' + filename)
    path = directory / filename
    path.write_bytes(source)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_bundle(artifact, directory, sha):
    destination = directory / BUNDLE
    if artifact.suffix.lower() == '.zip':
        with zipfile.ZipFile(artifact) as archive:
            entries = [entry for entry in archive.infolist()
                       if Path(entry.filename).name == BUNDLE]
            if len(entries) != 1 or entries[0].file_size != BUNDLE_BYTES:
                raise ValueError('O ZIP deve conter exatamente o AAB 1030042 auditado')
            with archive.open(entries[0]) as source, destination.open('xb') as output:
                shutil.copyfileobj(source, output)
    else:
        if artifact.stat().st_size != BUNDLE_BYTES:
            raise ValueError('Tamanho inesperado do AAB 1030042')
        shutil.copyfile(artifact, destination)
    if sha(destination) != BUNDLE_SHA:
        raise ValueError('SHA-256 do AAB 1030042 não corresponde ao da compilação')
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--publish', nargs='?', const=True, type=Path, metavar='ZIP_OU_AAB')
    args = parser.parse_args()

    os.umask(0o077)
    with tempfile.TemporaryDirectory(prefix='scorer-1030042-') as temporary:
        directory = Path(temporary)
        uploader = load_helper(directory, 'bastion_play_internal.py', UPLOADER_SHA)
        uploader.private_directory(uploader.PRIVATE)
        fd = os.open(uploader.PRIVATE / 'play-internal.lock',
                     os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            client = uploader.Client(uploader.load_account(uploader.CREDENTIALS))
            if args.check:
                uploader.publish(client, None, '', check_only=True)
                return

            if args.publish is True:
                print('A descarregar o AAB 1030042 do GitHub…', flush=True)
                bundle = directory / BUNDLE
                with bundle.open('xb') as output:
                    for part, offset in enumerate(range(0, BUNDLE_BYTES, PART_BYTES)):
                        size = min(PART_BYTES, BUNDLE_BYTES - offset)
                        url = TRANSFER_URL + f'aab.part.{part:02d}'
                        with urlopen(url, timeout=90) as response:
                            data = response.read(size + 1)
                        if len(data) != size:
                            raise ValueError(f'Tamanho inválido na parte {part:02d} do AAB')
                        output.write(data)
                if bundle.stat().st_size != BUNDLE_BYTES or uploader.sha(bundle) != BUNDLE_SHA:
                    raise ValueError('O AAB descarregado não corresponde ao AAB 1030042 auditado')
            else:
                bundle = copy_bundle(args.publish, directory, uploader.sha)
            uploader.VERSION = VERSION
            uploader.PAYLOAD = uploader.payload_digest(bundle)
            uploader.internal_release = lambda: {
                'track': 'internal',
                'releases': [{
                    'name': '1.0 (1030042) - season form and lifestyle',
                    'versionCodes': [str(VERSION)],
                    'status': 'completed',
                    'releaseNotes': [{
                        'language': 'en-US',
                        'text': 'Added angled one-on-ones and more lifestyle purchases. Includes stronger World form penalties, lasting squad investment and more realistic European results.',
                    }],
                }],
            }

            if not os.path.lexists(SIGNED):
                signer = load_helper(directory, 'sign_local_bundle.py', SIGNER_SHA)
                signer.sign_bundle(
                    bundle, SIGNED, uploader.PRIVATE / 'scorer-upload.p12',
                    signer.getpass.getpass('Palavra-passe da chave de upload (oculta): '),
                    BUNDLE_SHA, uploader.CERT,
                )
            signed = uploader.snapshot_signed(SIGNED, directory)
            digest = uploader.verify_signed(signed)

            # Rewrite the old fixed version in the original uploader's diagnostics.
            uploader.print = lambda *parts, **kwargs: print(
                *(str(part).replace('1030039', str(VERSION)) for part in parts),
                **kwargs,
            )
            uploader.publish(client, signed, digest)
            print('Faixa Internal verificada. A disponibilização aos testadores requer a publicação na Alpha.')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('Interrompido: ' + str(error).replace('1030039', str(VERSION)), file=sys.stderr)
        sys.exit(1)
