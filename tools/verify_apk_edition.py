"""Inspect trusted APK bytecode with the SAME Python version used to build it."""
import io
import marshal
import sys
import tarfile
import zipfile

with zipfile.ZipFile(sys.argv[1]) as apk:
    with tarfile.open(fileobj=io.BytesIO(apk.read('assets/private.tar'))) as archive:
        member = next(m for m in archive if m.name.endswith('/edition.pyc') or m.name == 'edition.pyc')
        code = marshal.loads(archive.extractfile(member).read()[16:])
flags = [value for value in code.co_consts if type(value) is bool]
expected = sys.argv[2] == 'world'
assert flags == [expected], flags
print('Compiled edition verified:', 'World preview' if expected else 'Free')
