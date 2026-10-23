import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import career


class CareerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = patch.dict(os.environ, STRIKER_SAVE_DIR=str(self.root / 'saves'))
        self.env.start()
        self.addCleanup(self.env.stop)

    def signed(self):
        c = career.CareerMode()
        c.accept_starting_offer(c.offers[0])
        return c

    def test_damaged_save_is_rejected_without_partial_mutation(self):
        c = self.signed()
        original = json.loads(c.save_path.read_text())
        for field, value in (('national_cup_winners', []), ('morale', float('nan')),
                             ('clubs', [{'name': 'Broken'}]), ('player_name', [])):
            with self.subTest(field=field):
                data = json.loads(json.dumps(original))
                data['career']['goals'] = 999
                data['career'][field] = value
                contents = json.dumps(data)
                c.save_path.write_text(contents)
                before = (c.goals, c.club_name, c.current_league.clubs[0].name)
                c.load()
                self.assertEqual((c.goals, c.club_name, c.current_league.clubs[0].name), before)
                self.assertEqual(c.save_path.read_text(), contents)

    def test_headless_import_has_no_kivy_or_files(self):
        result = subprocess.run([sys.executable, '-c',
            'import career,sys; assert "kivy" not in sys.modules'],
            cwd=Path(career.__file__).parent, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / 'saves').exists())

    def test_default_and_round_trip_preserves_player(self):
        c = self.signed()
        self.assertEqual(c.player_name, 'Alex Silva')
        c.player_name = 'Nome existente'
        c.goals = 7
        c.save()
        restored = career.CareerMode()
        self.assertEqual((restored.player_name, restored.club_name, restored.goals),
                         ('Nome existente', c.club_name, 7))

    def test_free_only_one_division_and_invalid_offer(self):
        c = career.CareerMode()
        self.assertEqual(c.product_mode, 'FREE')
        self.assertEqual(sum(c.is_league_playable(k) for k in c.leagues), 1)
        c.accept_starting_offer('not an offer')
        self.assertEqual(c.club_name, '')
        self.assertFalse(c.restore_world_access())

    def test_provider_failures_fail_closed(self):
        class Broken:
            def has_world_access(self): raise RuntimeError()
            def restore_world_access(self): raise RuntimeError()
        manager = career.EntitlementManager(Broken())
        self.assertFalse(manager.world_unlocked)
        self.assertFalse(manager.restore_world_access())

    def test_save_cannot_unlock_world(self):
        c = self.signed()
        data = json.loads(c.save_path.read_text())
        data['career']['world_unlocked'] = True
        data['career']['league_key'] = 'Portugal|1'
        c.save_path.write_text(json.dumps(data))
        restored = career.CareerMode()
        self.assertFalse(restored.world_unlocked)
        self.assertEqual(restored.league_key, career.FREE_LEAGUE_KEY)
        self.assertIsNotNone(restored._locked_world_career)

    def test_training_and_match_progress_survive_restart(self):
        c = self.signed()
        c.complete_training(3)
        self.assertTrue(c.trained_this_week)
        home, away = c.next_fixture()
        c.finish_match(home, away, 1, 0, forced_score=(2, 1))
        restored = career.CareerMode()
        self.assertGreater(restored.week, 0)
        self.assertEqual((restored.goals, restored.matches, restored.week),
                         (c.goals, c.matches, c.week))

    def test_atomic_failure_keeps_existing_save(self):
        c = self.signed()
        before = c.save_path.read_bytes()
        with patch('career.os.replace', side_effect=OSError('disk')):
            c.goals = 99
            c.save()
        self.assertEqual(c.save_path.read_bytes(), before)
        self.assertEqual(list(c.save_path.parent.glob('*.tmp')), [])
        self.assertIn('guardar', c.message)

    def test_corrupt_save_does_not_crash(self):
        p = self.root / 'saves' / 'striker_career.json'
        p.parent.mkdir()
        p.write_text('{broken')
        self.assertEqual(career.CareerMode().club_name, '')
        self.assertEqual(p.read_text(), '{broken')

    def test_migration_copies_and_never_overwrites(self):
        c = self.signed()
        legacy = self.root / 'striker_career.json'
        legacy.write_bytes(c.save_path.read_bytes())
        c.save_path.unlink()
        with patch('career.__file__', str(self.root / 'career.py')):
            restored = career.CareerMode()
            self.assertEqual(restored.club_name, c.club_name)
            self.assertEqual(legacy.read_bytes(), restored.save_path.read_bytes())
            restored.player_name = 'Existing destination'
            restored.save()
            self.assertEqual(career.CareerMode().player_name, 'Existing destination')

    def test_android_uses_app_private_storage(self):
        fake = types.ModuleType('kivy.app')
        fake.App = types.SimpleNamespace(get_running_app=lambda:
            types.SimpleNamespace(user_data_dir=str(self.root / 'private')))
        os.environ.pop('STRIKER_SAVE_DIR')
        with patch('career.sys.platform', 'android'), patch.dict(sys.modules, {'kivy.app': fake}):
            c = self.signed()
            self.assertEqual(c.save_path.parent, self.root / 'private')
            self.assertEqual(career.CareerMode().club_name, c.club_name)

    def test_legacy_v1_save_and_name_are_preserved(self):
        c = self.signed()
        data = json.loads(c.save_path.read_text())['career']
        data['save_version'] = 1
        data['player_name'] = 'Legacy player'
        c.save_path.write_text(json.dumps(data))
        self.assertEqual(career.CareerMode().player_name, 'Legacy player')

    def test_unrecognised_migration_is_not_copied(self):
        legacy = self.root / 'striker_career.json'
        legacy.write_text('{"save_version": 999}')
        with patch('career.__file__', str(self.root / 'career.py')):
            c = career.CareerMode()
            self.assertFalse(c.save_path.exists())
        self.assertTrue(legacy.exists())

    def test_local_editor_renames_and_preserves_saved_career(self):
        c = self.signed()
        c.goals = 5
        c.rename_current_club('Clube Inventado')
        c.rename_current_competition('Liga Inventada')
        restored = career.CareerMode()
        self.assertEqual(restored.club_name, 'Clube Inventado')
        self.assertIsNotNone(restored.club)
        self.assertEqual(restored.current_league.name, 'Liga Inventada')
        self.assertEqual(restored.goals, 5)

    def test_save_outcome_and_fictional_free_division(self):
        c = self.signed()
        self.assertEqual(c.current_league.name, 'Liga Scorer')
        self.assertTrue(c.save())
        with patch('career.os.replace', side_effect=OSError('disk full')):
            self.assertFalse(c.save())

    def test_explicit_load_leaves_saved_career_untouched_until_selected(self):
        saved = self.signed()
        saved.goals = 17
        saved.save()
        before = saved.save_path.read_bytes()
        fresh = career.CareerMode(autoload=False)
        self.assertEqual(fresh.club_name, '')
        self.assertEqual(fresh.save_path.read_bytes(), before)
        self.assertTrue(fresh.load())
        self.assertEqual(fresh.goals, 17)
        self.assertEqual(fresh.save_path.read_bytes(), before)

    def test_new_game_backup_is_atomic_and_failure_preserves_existing_files(self):
        c = self.signed()
        before = c.save_path.read_bytes()
        self.assertTrue(c.backup_before_new_game())
        backup = c.save_path.with_name('striker_career.previous.json')
        self.assertEqual(backup.read_bytes(), before)
        c.goals = 88
        c.save()
        updated = c.save_path.read_bytes()
        with patch('career.os.replace', side_effect=OSError('disk full')):
            self.assertFalse(c.backup_before_new_game())
        self.assertEqual(c.save_path.read_bytes(), updated)
        self.assertEqual(backup.read_bytes(), before)
        self.assertEqual(list(c.save_path.parent.glob('*.tmp')), [])

    def test_legacy_division_label_migrates_without_losing_progress(self):
        c = self.signed()
        c.goals, c.matches, c.week = 11, 6, 8
        c.save()
        original = json.loads(c.save_path.read_text())
        for old_name in ('England Division 4', 'Divisão Striker', 'Divisão Scorer'):
            data = json.loads(json.dumps(original))
            data['career']['league_name'] = old_name
            c.save_path.write_text(json.dumps(data))
            restored = career.CareerMode()
            self.assertEqual(restored.current_league.name, 'Liga Scorer')
            self.assertEqual((restored.goals, restored.matches, restored.week), (11, 6, 8))
            self.assertEqual(restored.club_name, c.club_name)
            self.assertTrue(all(club.league == 'Liga Scorer' for club in restored.current_league.clubs))

    def test_free_transfer_offers_and_seasons_stay_in_only_one_division(self):
        c = self.signed()
        c.goals, c.matches, c.morale = 100, 10, 20
        self.assertTrue(all(key == career.FREE_LEAGUE_KEY for _, key in c.generate_agent_offers(guaranteed=True)))
        old_club = c.club_name
        c.agent_offers = [('Foreign FC', 'Portugal|1')]
        c.accept_transfer('Foreign FC', 'Portugal|1')
        self.assertEqual(c.club_name, old_club)
        for _ in range(2):
            c.club.points = 9999
            c._finish_season()
            self.assertEqual(c.league_key, career.FREE_LEAGUE_KEY)
            self.assertEqual(sum(c.is_league_playable(key) for key in c.leagues), 1)

    def test_player_name_change_preserves_progress_and_scorer_identity(self):
        c = self.signed()
        old = c.player_name
        c.goals, c.matches = 7, 4
        c.current_league.scorer_goals.update({old: 7, 'Outro Jogador': 3})
        c.save()
        self.assertTrue(c.set_player_name('  Luca   Vale  '))
        restored = career.CareerMode()
        self.assertEqual((restored.player_name, restored.goals, restored.matches), ('Luca Vale', 7, 4))
        self.assertNotIn(old, restored.current_league.scorer_goals)
        self.assertEqual(restored.current_league.scorer_goals['Luca Vale'], 7)
        self.assertEqual(restored.current_league.scorer_goals['Outro Jogador'], 3)

    def test_player_name_validation_and_save_failure_do_not_replace_career(self):
        c = self.signed()
        c.current_league.scorer_goals[c.player_name] = 9
        c.current_league.scorer_goals['Outro Jogador'] = 3
        c.save()
        before = c.save_path.read_bytes()
        for name in ('', 'x', '\n\t', 'Outro Jogador'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                c.set_player_name(name)
        with patch('career.os.replace', side_effect=OSError('disk full')):
            self.assertFalse(c.set_player_name('Luca Vale'))
        self.assertEqual(c.player_name, 'Alex Silva')
        self.assertEqual(c.current_league.scorer_goals['Alex Silva'], 9)
        self.assertNotIn('Luca Vale', c.current_league.scorer_goals)
        self.assertEqual(c.save_path.read_bytes(), before)

    def test_training_once_per_career_week_persists_and_unlocks_after_match(self):
        c = self.signed()
        self.assertTrue(c.begin_training())
        self.assertGreater(c.complete_training(2), 0)
        stats = (c.stamina, c.morale)
        self.assertFalse(c.begin_training())
        self.assertEqual(c.complete_training(3), 0)
        self.assertEqual((c.stamina, c.morale), stats)
        restored = career.CareerMode()
        self.assertTrue(restored.training_used_this_week)
        self.assertFalse(restored.begin_training())
        self.assertEqual((restored.stamina, restored.morale), stats)
        home, away = restored.next_fixture()
        restored.finish_match(home, away, 0, 1, forced_score=(1, 0))
        self.assertFalse(restored.training_used_this_week)
        self.assertTrue(restored.begin_training())
        self.assertGreater(restored.complete_training(1), 0)

    def test_training_reservation_survives_abandonment_and_new_season_resets(self):
        c = self.signed()
        self.assertTrue(c.begin_training())
        restored = career.CareerMode()
        self.assertFalse(restored.trained_this_week)
        self.assertTrue(restored.training_used_this_week)
        self.assertFalse(restored.begin_training())
        restored._finish_season()
        self.assertFalse(restored.training_used_this_week)
        self.assertTrue(restored.begin_training())

    def test_training_save_failures_preserve_reservation_and_rewards(self):
        c = self.signed()
        before = c.save_path.read_bytes()
        with patch('career.os.replace', side_effect=OSError('disk full')):
            self.assertFalse(c.begin_training())
        self.assertFalse(c.training_used_this_week)
        self.assertEqual(c.save_path.read_bytes(), before)
        self.assertTrue(c.begin_training())
        reserved = c.save_path.read_bytes()
        stats = (c.stamina, c.morale)
        with patch('career.os.replace', side_effect=OSError('disk full')):
            self.assertEqual(c.complete_training(3), 0)
        self.assertEqual((c.stamina, c.morale), stats)
        self.assertTrue(c.training_used_this_week)
        self.assertFalse(c.trained_this_week)
        self.assertEqual(c.save_path.read_bytes(), reserved)

    def test_older_completed_training_without_reservation_field_stays_locked(self):
        c = self.signed()
        c.complete_training(3)
        data = json.loads(c.save_path.read_text())
        data['career'].pop('training_session_week')
        c.save_path.write_text(json.dumps(data))
        restored = career.CareerMode()
        self.assertTrue(restored.training_used_this_week)
        self.assertFalse(restored.begin_training())

    def test_baseline_immutable(self):
        p = Path(career.__file__).parent / 'baseline/Striker-P0-05-v006.py'
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),
                         'fed211d2ec63fe0275390b13ed4a1bcfcd18fa61238460b04b67d80ebca6205b')


if __name__ == '__main__':
    unittest.main()
