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
# Read named assignments: World has True and False constants, not a single flag.
namespace={}
exec(code,namespace)
expected = sys.argv[2] == 'world'
assert namespace['WORLD_BUILD'] is expected
assert namespace['WORLD_PREVIEW'] is False
print('Compiled edition verified:', 'World' if expected else 'Free')
