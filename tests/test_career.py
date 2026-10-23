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
        self.assertEqual(c.current_league.name, 'Divisão Striker')
        self.assertTrue(c.save())
        with patch('career.os.replace', side_effect=OSError('disk full')):
            self.assertFalse(c.save())

    def test_baseline_immutable(self):
        p = Path(career.__file__).parent / 'baseline/Striker-P0-05-v006.py'
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),
                         'fed211d2ec63fe0275390b13ed4a1bcfcd18fa61238460b04b67d80ebca6205b')


if __name__ == '__main__':
    unittest.main()
