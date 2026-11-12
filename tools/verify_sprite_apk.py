"""Check trusted APK sprite resources and bytecode with its host Python version."""
import io,json,marshal,sys,tarfile,zipfile
from pathlib import Path
artifact,stage=Path(sys.argv[1]),Path(sys.argv[2])
with zipfile.ZipFile(artifact) as archive:
    with tarfile.open(fileobj=io.BytesIO(archive.read('assets/private.tar'))) as tar:
        members={m.name.removeprefix('./'):m for m in tar.getmembers() if m.isfile()}
        def data(path):
            match=next(m for name,m in members.items() if name==path or name.endswith('/'+path))
            return tar.extractfile(match).read()
        manifest=json.loads(data('assets/sprites/manifest.json'))
        assert manifest==json.loads((stage/'assets/sprites/manifest.json').read_text())
        assert manifest['approval_status']=='APPROVED' and manifest['approved_art_revision']==2
        frames=sheets=0
        for c in manifest['characters'].values():
            for a in c['animations'].values():
                for sheet in a['sheets'].values():
                    assert data(sheet['path'])==(stage/sheet['path']).read_bytes();sheets+=1
                for paths in a['individuals'].values():
                    for path in paths:
                        assert data(path)==(stage/path).read_bytes();frames+=1
        for module in ('main','player_portrait','development_ui','retro_sprites','sprite_animation','sprite_textures','stadium_scene','supporter_layout','celebrations','menu_ui','coach_ui','newspaper_ui','competition_views','standings_ui','contextual_help','coach','player_development','world_ui','attendance','retro_props','title_events','title_presentation','honours','career','world_competitions','international_calendar','career_life','injuries','career_records','coach_feedback','league_status','lifestyle_ui','estate_portrait','feedback','finishing_balance','unpredictable_aim'):
            actual=marshal.loads(data(module+'.pyc')[16:])
            expected=compile((stage/(module+'.py')).read_text(),actual.co_filename,'exec',optimize=2)
            assert actual==expected,'Compiled source differs: '+module
        assert data('assets/coaches/team_talk.png')==(stage/'assets/coaches/team_talk.png').read_bytes()
        for name in ('supporters.png','ball.png','trophy.png','newspaper.png'):
            path='assets/sprites/scene/'+name
            assert data(path)==(stage/path).read_bytes(),path
        for name in ('league_status.json',):
            assert data('assets/data/'+name)==(stage/'assets/data'/name).read_bytes()
        for item in ('studio','apartment','house','mansion','utility','sedan','sports','supercar','rose','flowers','necklace','handbag','casual','smart','suit','designer'):
            assert data('assets/lifestyle/'+item+'.png')==(stage/'assets/lifestyle'/(item+'.png')).read_bytes()
        for name in ('outfits.png','forecourt.png'):
            path='assets/lifestyle/scene/'+name;assert data(path)==(stage/path).read_bytes()
        assert frames==248 and sheets==35
        assert not any('/tools/sprite_lab/' in name for name in members)
print('Original revision2 base plus requested celebrations/high tip:',frames,'frames,',sheets,'sheets, exact compiled rendering/runtime source; no sprite-lab build tools.')
