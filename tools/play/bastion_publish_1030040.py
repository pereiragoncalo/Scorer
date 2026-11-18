"""Check or publish Scorer World 1030040 to Google Play Internal from the bastion."""
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

VERSION = 1030040
BUNDLE = 'Scorer-World-1.0-1030040-unsigned.aab'
BUNDLE_SHA = 'cd93d4dd0d42c0c555d7d4f959d70fc2a2bb79729e7387aeba0a6d666ec46ad0'
BUNDLE_BYTES = 123962887
UPLOADER_SHA = 'bc0725dac5c1132ce4542d76e9d3777ade333ea2a83ba23cde457def0594e983'
SIGNER_SHA = '5492d1fa8de0e3072960a0c34eaf05548cdaaa51c84f154d8ef579c885fa6761'
SOURCE = 'https://raw.githubusercontent.com/pereiragoncalo/Scorer/6cf4e4fcd6963fee20c1c2c6a226e9eba6391e30/tools/play/'
SIGNED = Path('/home/clemir/Scorer-World-1.0-1030040.aab')


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
                raise ValueError('O ZIP deve conter exatamente o AAB 1030040 auditado')
            with archive.open(entries[0]) as source, destination.open('xb') as output:
                shutil.copyfileobj(source, output)
    else:
        if artifact.stat().st_size != BUNDLE_BYTES:
            raise ValueError('Tamanho inesperado do AAB 1030040')
        shutil.copyfile(artifact, destination)
    if sha(destination) != BUNDLE_SHA:
        raise ValueError('SHA-256 do AAB 1030040 não corresponde ao da compilação')
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--publish', type=Path, metavar='ZIP_OU_AAB')
    args = parser.parse_args()

    os.umask(0o077)
    with tempfile.TemporaryDirectory(prefix='scorer-1030040-') as temporary:
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

            bundle = copy_bundle(args.publish, directory, uploader.sha)
            uploader.VERSION = VERSION
            uploader.PAYLOAD = uploader.payload_digest(bundle)
            uploader.internal_release = lambda: {
                'track': 'internal',
                'releases': [{
                    'name': '1.0 (1030040) - season balance',
                    'versionCodes': [str(VERSION)],
                    'status': 'completed',
                    'releaseNotes': [{
                        'language': 'en-US',
                        'text': 'Match opportunities now vary with form, morale, fitness and opposition. Training and scoreless matches affect morale more.',
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
