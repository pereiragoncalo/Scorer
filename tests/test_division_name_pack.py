import copy,json,os,tempfile,unittest,gzip,csv
from pathlib import Path
from unittest.mock import patch
from career import CareerMode
from tools.build_division_name_pack import load_registry,normalize,build
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'docs/data/real_divisions_2026.json'
PACK=ROOT/'docs/data/name-packs/Scorer-World-Real-Names-Divisions-2026.json'
PREVIOUS=ROOT/'docs/data/name-packs/Scorer-World-Real-Names-Europe-Brazil-Argentina-2026-07.json'
class Access:
    def has_world_access(self):return True

class DivisionNamePackTests(unittest.TestCase):
    def test_every_real_club_belongs_to_its_initial_division_and_is_unique(self):
        registry,lookups=load_registry(MANIFEST);pack=json.loads(PACK.read_text());seen=set()
        with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,STRIKER_SAVE_DIR=t):
            c=CareerMode(Access(),autoload=False,save_slot='world');clean=c.preview_names(pack)
            for league in c.leagues.values():
                for club in league.clubs:
                    if club.uid not in clean['clubs']:continue
                    team=lookups[league.country][normalize(clean['clubs'][club.uid])]
                    self.assertIn(team,registry[league.country,league.tier]['teams'])
                    self.assertNotIn(team['identity'],seen);seen.add(team['identity'])
            self.assertEqual(len(seen),494);self.assertEqual(len(clean['leagues']),29)
    def test_known_wrong_division_regressions_and_reserve_identities(self):
        report=json.loads(PACK.with_suffix('.provenance.json').read_text());rows=report['assignments']
        actual={(r['country'],r['club']):r['tier'] for r in rows}
        for country,name,tier in [('Portugal','Belenenses',3),('Portugal','Mafra',3),('Portugal','Oliveirense',3),('Portugal','Vitória de Setúbal',4),('Portugal','Marítimo',1),('Portugal','AFS',2),('England','West Ham United',2),('Spain','Valencia',1),('Brazil','Ceará',2),('Argentina','River Plate',1)]:
            self.assertEqual(actual[country,name],tier)
        registry,_=load_registry(MANIFEST)
        chaves=next(t for t in registry['Portugal',2]['teams'] if t['name']=='Chaves')
        reserve=next(t for t in registry['Portugal',4]['teams'] if t['name']=='Chaves B')
        self.assertEqual(chaves['wiki_path'],reserve['wiki_path']);self.assertNotEqual(chaves['identity'],reserve['identity'])
        self.assertEqual(len(registry['Argentina',2]['teams']),36) # Distinct San Martín clubs must not collapse.
    def test_upgrade_clears_all_old_player_alias_slots_and_keeps_progress_backup_reload(self):
        old=json.loads(PREVIOUS.read_text());new=json.loads(PACK.read_text())
        self.assertTrue(set(old['clubs'])<=set(new['clubs']));self.assertTrue(set(old['players'])<=set(new['players']))
        with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,STRIKER_SAVE_DIR=t):
            c=CareerMode(Access(),autoload=False,starter_country='Portugal',save_slot='world');c.accept_starting_offer(c.offers[0]);c.goals=17;c.apply_names(old)
            before_bytes=c.save_path.read_bytes();before=json.loads(before_bytes)['career'];c.apply_names(new);after=json.loads(c.save_path.read_text())['career']
            self.assertEqual([k for k in before if before[k]!=after[k]],['display_aliases'])
            self.assertEqual(c.save_path.with_suffix('.names-backup.json').read_bytes(),before_bytes)
            restored=CareerMode(Access(),autoload=True,starter_country='Portugal',save_slot='world');self.assertEqual(restored.display_aliases,new);self.assertEqual(restored.goals,17)
            # Fictional fallback slots replace former real names when the newly assigned club lacks a sourced squad.
            report=json.loads(PACK.with_suffix('.provenance.json').read_text())
            clubs={club.uid:(league,club) for league in c.leagues.values() for club in league.clubs}
            for row in report['assignments']:
                league,club=clubs[row['uid']];defaults=league.squad_names(club.name)
                for slot in range(12):
                    key=f'{club.uid}:{slot}'
                    if slot<len(row['real_player_names']):self.assertEqual(new['players'][key],row['real_player_names'][slot])
                    elif key in old['players']:self.assertEqual(new['players'][key],defaults[slot])
    def test_ambiguous_alias_fails_instead_of_guessing_a_club(self):
        data=json.loads(MANIFEST.read_text());data['divisions'][0]['teams'][0]['aliases'].append(data['divisions'][0]['teams'][1]['name'])
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'bad.json';p.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,'Ambiguous club'):load_registry(p)

    def test_generation_does_not_depend_on_shuffled_initial_club_order(self):
        with tempfile.TemporaryDirectory() as folder:
            clubs=Path(folder)/'clubs.csv.gz';players=Path(folder)/'players.csv.gz'
            with gzip.open(clubs,'wt') as f:f.write('club_id,name,domestic_competition_id\n1,FC Porto,PO1\n')
            with gzip.open(players,'wt') as f:f.write('player_id,name,last_season,position,current_club_id,market_value_in_eur\n1,Source Player,2025,Attack,1,1000\n')
            expected,_=build(players,clubs,MANIFEST,PREVIOUS)
            def reversed_career(*args,**kwargs):
                c=CareerMode(*args,**kwargs)
                for league in c.leagues.values():league.clubs.reverse()
                return c
            with patch('career.CareerMode',side_effect=reversed_career):actual,_=build(players,clubs,MANIFEST,PREVIOUS)
            self.assertEqual(actual,expected)
