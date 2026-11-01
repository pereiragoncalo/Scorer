import io,marshal,tarfile,zipfile,sys
from pathlib import Path
for artifact in sys.argv[1:]:
 with zipfile.ZipFile(artifact) as z:
  archive=next(n for n in z.namelist() if n.endswith('assets/private.tar'))
  with tarfile.open(fileobj=io.BytesIO(z.read(archive))) as t:
   for name in ('main','privacy_requests','anonymous_stats','menu_ui','defensive_difficulty','career','world_competitions','season_transitions','domestic_rules'):
    m=next(m for m in t if m.name==name+'.pyc' or m.name.endswith('/'+name+'.pyc'))
    actual=marshal.loads(t.extractfile(m).read()[16:]);source=Path(name+'.py').read_text()
    assert any(actual==compile(source,actual.co_filename,'exec',optimize=n) for n in (0,1,2)),name+' differs from reviewed source'
 print('Exact compiled World source matches reviewed modules:',Path(artifact).name)
