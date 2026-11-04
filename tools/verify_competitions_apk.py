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
        news=module('newspaper');coach=module('coach');moments=module('match_moments');assert moments.chance_moment({},88,0,1,True)=='equaliser'
        formats=module('domestic_formats');kits=module('club_kits');competitions=module('world_competitions');module('promotion_playoffs');access=module('domestic_playoffs');calendar=module('international_calendar');module('two_divisions');module('season_transitions');rules=module('domestic_rules');hon=module('honours');career=module('career');competitions=module('world_competitions')
        import edition
        assert edition.WORLD_BUILD and not edition.WORLD_PREVIEW
        with tempfile.TemporaryDirectory() as directory:
            os.environ['STRIKER_SAVE_DIR']=directory
            c=career.CareerMode(edition.entitlement_provider(),autoload=False,save_slot='world');c.accept_starting_offer(c.offers[0]);c.next_match();assert c.world_competitions
            assert not c.coach_meeting_required and c.begin_training()
            c.record_coach_performance(0,1,[],False,key_match=True)
            assert c.coach_meeting_required and not c.begin_training()
            assert c.attend_coach_meeting() and not c.coach_meeting_required and c.begin_training()
            c.save();assert c.load() and not c.coach_meeting_required
            for portrait in coach.PORTRAITS:assert Path(portrait).is_file()
            face=c.coach_portrait;c.save();assert c.load() and c.coach_portrait==face
            for photo in news.PHOTOS:assert Path(photo).is_file()
            home,away=c.next_fixture()
            press=news.make_report(news.fresh_state(),dict(date='2026-11-04',competition='League',country=c.current_league.country,status='1-1'),home,away,home.uid,(1,1),0,1,[])
            assert news.clean_state(press)==press and press['report']['photo']==0
            from localization import Localizer
            story=news.article(press['report'],Localizer(False).tr,lambda e,side:e[side],c.player_name,'League')
            assert not story['mentions_player'] and '1-1' in story['paragraphs'][0]
            assert c.domestic_format_version==1 and len(formats.catalogue())==38
            assert [len(l.clubs) for l in c.domestic_leagues('Spain')]==[20,22]
            assert [len(l.clubs) for l in c.domestic_leagues('Brazil')]==[20,20]
            assert c.leagues['Scotland|1'].total_rounds==38
            assert c.leagues['Finland|2'].total_rounds==27
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
            phased=career.CareerMode(edition.entitlement_provider(),autoload=False,save_slot='world',starter_country='Austria')
            phased.league_key='Austria|1';phased.club_name=phased.current_league.clubs[0].name
            league=phased.current_league
            import random
            before=None
            for round_number in range(22):
                for h,a in league.pairings():league.simulate_fixture(h,a,random.Random(round_number),forced_score=(1,0))
                if round_number==21:before={c.uid:c.points for c in league.clubs}
                league.advance_round()
            assert [len(g) for g in league.format_groups]==[6,6]
            points={c.uid:c.points for c in league.clubs};assert points=={uid:p//2 for uid,p in before.items()}
            assert phased.save()
            reloaded=career.CareerMode(edition.entitlement_provider(),save_slot='world')
            assert formats.state(reloaded.current_league)==formats.state(league)
            reloaded.current_league.table();assert {c.uid:c.points for c in reloaded.current_league.clubs}==points
            old=career.CareerMode(edition.entitlement_provider(),autoload=False,save_slot='world',starter_country='Spain',domestic_formats=False)
            old.accept_starting_offer(old.offers[0]);assert len(old.current_league.clubs)==18
            reloaded=career.CareerMode(edition.entitlement_provider(),save_slot='world');assert reloaded.domestic_format_version==0 and len(reloaded.current_league.clubs)==18



print('Actual APK bytecode: World fixtures/qualifying/brackets and career save/reload verified; no network sent')

print('Actual APK: two divisions, ten-club FIFO reserves, relegation release, free-agent export/reload/signing verified')

print('Actual APK: 352 built-in club colour palettes resolve without real-name import and survive aliases')

print('Actual APK: persisted French playoff ladder, top-three foreign-league call-up criterion and FIFA window dates verified')

print('Actual APK: 38-country capacities, Austrian split/half-points/reload and legacy layout preservation verified')

print('Actual APK: conditional coach requests and offline newspaper report/photo data verified')

print("Actual APK: ten coach portraits and saved appearance selection verified")

assert 'ScorerPressPixel.ttf' in Path('newspaper_ui.py').read_text()
report=dict(home='Home',away='Away',home_uid='h',away_uid='a',actor_uid='h',score=[3,1],status='3-1',events=[dict(minute=m,half=1 if m<46 else 2,side=s) for m,s in ((32,'home'),(51,'away'),(67,'home'),(90,'home'))],goals=0,negative_run=0,standout=False,photo=0)
story=news.article(report,Localizer(False).tr,lambda e,side:e[side],'Player','League')
assert len(story['goals'])==4 and story['goals'][-1]['score']==[3,1]
print('Actual APK: all four goals, changing score and match summary verified')
with tempfile.TemporaryDirectory() as tmp:
    os.environ['STRIKER_SAVE_DIR']=tmp
    c=career.CareerMode(edition.entitlement_provider(),autoload=False,save_slot='world');c.accept_starting_offer(c.offers[0])
    assert not c.trained_this_week and c.complete_training(3)==0 and c.begin_training()
    for shot in range(3):
        assert not c.trained_this_week and c.complete_training(3)==0
        assert c.record_training_shot(shot==0)
    assert c.complete_training(3)>0 and c.trained_this_week
    c._ensure_competitions();book=c.world_competitions;own='nation:'+c.nationality;other=next(n for n in book.nations if n!=own)
    f=dict(id='friendly:training-gate',home=own,away=other,week=c.week,stage='International friendly',score=None)
    book.friendlies[f['id']]=f;week=c.week
    h=c._competition_club(book.nations[own]);a=c._competition_club(book.nations[other])
    c.finish_match(h,a,1,0,competition='world|friendly|'+f['id'],forced_score=(1,3))
    assert c.week==week and not c.trained_this_week and c.training_shots_taken==0
    assert c.load() and not c.trained_this_week and c.complete_training(3)==0
    story=news.article(c.press_state['report'],Localizer(False).tr,lambda e,side:e[side],c.player_name,'International friendly')
    assert story['mentions_player'] and c.player_name in story['headline'] and c.player_name in story['mention']
    assert 'crucial' not in story['mention']
print('Actual APK: three persisted training shots required, same-week national match consumes training, every goal gets newspaper headline')

c._ensure_competitions();book=c.world_competitions;own=c.club
other=next(team for team in c.current_league.clubs if team.uid!=own.uid)
rows=[dict(uid=team.uid,name=team.name,country=team.country,rating=team.rating,tier=team.tier) for team in (own,other)]
cup=competitions.Tournament('qa:honours','QA trophy',rows,'qa-trophy',kind='knockout',start_week=c.week)
book.tournaments[cup.key]=cup;f=cup.fixtures[0];f['week']=c.week
h=c._competition_club(cup.teams[f['home']]);a=c._competition_club(cup.teams[f['away']])
score=(1,0) if h.uid==own.uid else (0,1)
c.finish_match(h,a,0,0,competition='world|'+cup.key+'|'+f['id'],forced_score=score)
assert any(t['competition']==cup.key and t['team_uid']==own.uid for t in c.honours['trophies'])
assert c.post_match_stage=='newspaper'
state=c.honours;assert c.load() and c.honours==state and c.post_match_stage=='newspaper'
print('Actual APK: observed cup-final participation awards a saved personal trophy and persists the newspaper queue')
