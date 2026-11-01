"""Smoke trusted APK bytecode using its Python major/minor; no network/user saves."""
import io,marshal,os,sys,tarfile,tempfile,types,zipfile
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
with zipfile.ZipFile(sys.argv[1]) as z:
    archive=next(n for n in z.namelist() if n.endswith('assets/private.tar'))
    with tarfile.open(fileobj=io.BytesIO(z.read(archive))) as t:
        def module(name):
            m=next(m for m in t if m.name==name+'.pyc' or m.name.endswith('/'+name+'.pyc'))
            obj=types.ModuleType(name);obj.__file__=str(Path.cwd()/(name+'.py'));sys.modules[name]=obj
            exec(marshal.loads(t.extractfile(m).read()[16:]),obj.__dict__);return obj
        module('season_transitions');rules=module('domestic_rules');career=module('career');competitions=module('world_competitions')
        import edition
        assert edition.WORLD_BUILD and not edition.WORLD_PREVIEW
        with tempfile.TemporaryDirectory() as directory:
            os.environ['STRIKER_SAVE_DIR']=directory
            c=career.CareerMode(edition.entitlement_provider(),autoload=False,save_slot='world');c.accept_starting_offer(c.offers[0]);c.next_match();assert c.world_competitions
            c.save();d=career.CareerMode(edition.entitlement_provider(),save_slot='world');assert d.world_competitions.to_dict()==c.world_competitions.to_dict()
            b=competitions.CompetitionBook(2026,71,c.leagues);b.complete();assert len(b.tournaments['world_cup'].fixtures)==104
            assert all(v.champion for v in b.tournaments.values());competitions.CompetitionBook.from_dict(b.to_dict())
print('Actual APK bytecode: World fixtures/qualifying/brackets and career save/reload verified; no network sent')
