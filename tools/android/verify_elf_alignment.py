"""Inspect real ELF LOAD segments, including p4a's compressed Python bundle."""
import argparse
import io
from pathlib import Path
import subprocess
import tarfile
import tempfile
import zipfile


def native_files(archive):
    for name in archive.namelist():
        if not (name.endswith('.so') or name.endswith('.tar')):
            continue
        content = archive.read(name)
        if content.startswith(b'\x7fELF'):
            yield name, content
        elif name.endswith('libpybundle.so') or name.endswith('.tar'):
            with tarfile.open(fileobj=io.BytesIO(content)) as bundle:
                for member in bundle:
                    if member.isfile() and member.name.endswith('.so'):
                        source = bundle.extractfile(member)
                        content = source.read()
                        if not content.startswith(b'\x7fELF'):
                            raise ValueError(f'Non-ELF native extension: {member.name}')
                        yield name + ':' + member.name, content


def verify(apk, readelf):
    count = 0
    failures = []
    with zipfile.ZipFile(apk) as archive, tempfile.TemporaryDirectory() as temp:
        binary = Path(temp) / 'library.so'
        for name, content in native_files(archive):
            if content[5] != 1 or int.from_bytes(content[18:20], "little") != 183:
                raise ValueError(f"Non-arm64 ELF packaged in arm64 APK: {name}")
            binary.write_bytes(content)
            output = subprocess.check_output([readelf, '--program-headers', '--wide', str(binary)], text=True)
            loads = [line.split() for line in output.splitlines() if line.strip().startswith('LOAD ')]
            if not loads or any(int(fields[-1], 16) < 16384 for fields in loads):
                failures.append(name)
            count += 1
    if not count:
        raise ValueError('No ELF files found')
    if failures:
        raise ValueError('Insufficient ELF alignment: ' + ', '.join(failures))
    print(f'PASS: {count} ELF files have LOAD alignment >= 16 KB (including bundled Python extensions)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('apk')
    parser.add_argument('--readelf', required=True)
    args = parser.parse_args()
    verify(args.apk, args.readelf)
