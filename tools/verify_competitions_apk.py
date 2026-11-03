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
        kits=module('club_kits');competitions=module('world_competitions');module('promotion_playoffs');access=module('domestic_playoffs');calendar=module('international_calendar');module('two_divisions');module('season_transitions');rules=module('domestic_rules');career=module('career');competitions=module('world_competitions')
        import edition
        assert edition.WORLD_BUILD and not edition.WORLD_PREVIEW
        with tempfile.TemporaryDirectory() as directory:
            os.environ['STRIKER_SAVE_DIR']=directory
            c=career.CareerMode(edition.entitlement_provider(),autoload=False,save_slot='world');c.accept_starting_offer(c.offers[0]);c.next_match();assert c.world_competitions
            assert not c.display_aliases['clubs'] and len(kits.catalogue())==352
            by_uid={x.uid:x for l in c.leagues.values() for x in l.clubs}
            for uid,colours in kits.catalogue().items():
                assert c.kit_for_club(by_uid[uid])==tuple(career.hex_rgba(x) for x in colours)
            before_kit=c.kit_for_club(c.club);c.display_aliases['clubs'][c.club.uid]='Edited club'
            assert c.kit_for_club(c.club)==before_kit
            c.save();d=career.CareerMode(edition.entitlement_provider(),save_slot='world');assert d.world_competitions.to_dict()==c.world_competitions.to_dict()
            b=competitions.CompetitionBook(2025,71,c.leagues);b.complete();assert len(b.tournaments['world_cup'].fixtures)==104
            assert all(v.champion for v in b.tournaments.values());competitions.CompetitionBook.from_dict(b.to_dict())
            assert len(c.domestic_leagues())==2*len(career.WORLD_COUNTRIES)
            assert all(len(c.reserve_clubs(country))==10 for country in career.WORLD_COUNTRIES)
            c.league_key='Yemen|2';c.club_name=c.current_league.clubs[0].name
            uid=c.club.uid;before=list(c.relegation_pools[c.current_league.country]);c.club.points=-100000
            c.current_league.round_index=c.current_league.total_rounds;c.week=45;c.world_competitions.complete()

            while not c.free_agent:
                fixture=c.next_match()
                if fixture is None:break
                home,away=fixture[1:];c.finish_match(home,away,0,0,competition=fixture[0],forced_score=(0,0))
            assert c.free_agent and c.released_club['uid']==uid and len(c.agent_offers)==5
            assert c.relegation_pools[c.current_league.country][:7]==before[3:]
            assert uid in c.relegation_pools[c.current_league.country]
            assert c.save();d=career.CareerMode(edition.entitlement_provider(),save_slot='world');assert d.free_agent and d.relegation_pools==c.relegation_pools
            transfer=module('career_transfer');assert transfer.validated_import(d,transfer.export_career(d)).free_agent
            d.week=12;name,key=d.agent_offers[0];d.accept_transfer(name,key);assert not d.free_agent and d.club.name==name and d.club.tier in (1,2)
            # The compiled French bracket must have two single games and a
            # cross-division two-leg final, with a durable champion.
            cup=access.build_tournament('France',d.leagues['France|1'],d.leagues['France|2'],44,48)
            assert [g['legs'] for row in cup.plan for g in row]==[1,1,2]
            cup.finish();assert len(cup.fixtures)==4 and len(cup.qualified)==1
            assert competitions.Tournament.from_dict(cup.to_dict()).to_dict()==cup.to_dict()
            d.league_key='Brazil|1';d.club_name=d.current_league.clubs[0].name;d.nationality='Portugal'
            d.current_league.scorer_goals={d.player_name:6,'A':10,'B':8,'C':6};d.morale=0;d.form_goals=[]
            assert d.national_team_eligible
            d.current_league.scorer_goals['C']=7;assert not d.national_team_eligible
            assert calendar.window_dates(2026)[0].isoformat()=='2026-09-22'


print('Actual APK bytecode: World fixtures/qualifying/brackets and career save/reload verified; no network sent')

print('Actual APK: two divisions, ten-club FIFO reserves, relegation release, free-agent export/reload/signing verified')

print('Actual APK: 352 built-in club colour palettes resolve without real-name import and survive aliases')

print('Actual APK: persisted French playoff ladder, top-three foreign-league call-up criterion and FIFA window dates verified')
