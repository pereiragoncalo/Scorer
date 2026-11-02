import io,marshal,tarfile,zipfile,sys
from pathlib import Path
for artifact in sys.argv[1:]:
 with zipfile.ZipFile(artifact) as z:
  archive=next(n for n in z.namelist() if n.endswith('assets/private.tar'))
  with tarfile.open(fileobj=io.BytesIO(z.read(archive))) as t:
   for name in ('main','anonymous_stats','online_safety','world_ui','menu_ui','defensive_difficulty','career','world_competitions','season_transitions','two_divisions','domestic_rules','club_kits'):
    m=next(m for m in t if m.name==name+'.pyc' or m.name.endswith('/'+name+'.pyc'))
    actual=marshal.loads(t.extractfile(m).read()[16:]);source=Path(name+'.py').read_text()
    assert any(actual==compile(source,actual.co_filename,'exec',optimize=n) for n in (0,1,2)),name+' differs from reviewed source'
   for relative in ('assets/data/world_clubs.json','assets/data/club_kits.json'):
    member=next(m for m in t if m.name==relative or m.name.endswith('/'+relative))
    assert t.extractfile(member).read()==Path(relative).read_bytes(),relative+' differs from reviewed data'
 print('Exact compiled World source matches reviewed modules:',Path(artifact).name)
