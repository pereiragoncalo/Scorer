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

    def test_morale_slower_loss_and_larger_goal_reward(self):
        c = self.signed()
        c.morale = 10
        c._update_attributes(0, 3)
        self.assertAlmostEqual(c.morale, 9.25)
        c._update_attributes(1, 2)
        self.assertAlmostEqual(c.morale, 9.95)
        c.morale = 19.9
        c._update_attributes(3, 0)
        self.assertEqual(c.morale, 20)
        c.morale = 0.1
        c._update_attributes(0, 3)
        self.assertEqual(c.morale, 0)

    def test_fictional_squad_names_stable_and_migrate_without_losing_goals(self):
        c = self.signed()
        league = c.current_league
        names = [league.squad_names(club.name)[0] for club in league.clubs]
        self.assertEqual(len(names), len(set(names)))
        club = league.clubs[0]
        roster = league.squad_names(club.name)
        self.assertEqual(roster, league.squad_names(club.name))
        self.assertEqual(len(set(roster)), 12)
        old = f'Silva ({club.name})'
        new = f'{roster[0]} ({club.name})'
        league.scorer_goals = {old: 9, new: 2, c.player_name: 5, 'Custom Rival': 3}
        c.save()
        restored = career.CareerMode()
        self.assertTrue(restored.load())
        scores = restored.current_league.scorer_goals
        self.assertEqual(sum(scores.values()), 19)
        self.assertEqual(scores[new], 11)
        self.assertNotIn(old, scores)
        self.assertEqual(scores[c.player_name], 5)
        restored.current_league.migrate_scorer_names(c.player_name)
        self.assertEqual(scores[new], 11)

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
                         ('Nome Existente', c.club_name, 7))

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
        self.assertIn('save', c.message)

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
            self.assertEqual(career.CareerMode().player_name, 'Existing Destination')

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
        self.assertEqual(career.CareerMode().player_name, 'Legacy Player')

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
        self.assertEqual(c.current_league.name, 'Scorer League')
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
        for old_name in ('England Division 4', 'Divisão Striker', 'Divisão Scorer', 'Liga Scorer'):
            data = json.loads(json.dumps(original))
            data['career']['league_name'] = old_name
            c.save_path.write_text(json.dumps(data))
            restored = career.CareerMode()
            self.assertEqual(restored.current_league.name, 'Scorer League')
            self.assertEqual((restored.goals, restored.matches, restored.week), (11, 6, 8))
            self.assertEqual(restored.club_name, c.club_name)
            self.assertTrue(all(club.league == 'Scorer League' for club in restored.current_league.clubs))

    def test_english_dates_and_old_portuguese_save_feedback(self):
        from datetime import date
        expected = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                    'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')
        for month, abbreviation in enumerate(expected, 1):
            self.assertEqual(career.CareerMode.format_date(date(2026, month, 2)),
                             f'02 {abbreviation} 2026')
        c = self.signed()
        c.goals, c.week = 8, 3
        c.save()
        data = json.loads(c.save_path.read_text())
        data['career']['message'] = 'Treino concluído: 2/3 golos. Energia aumentou.'
        data['career']['league_name'] = 'Liga Scorer'
        data['career']['fixture_history'] = [{'date': '2026-07-12',
            'competition': 'Liga Scorer', 'home': c.club_name, 'away': 'Nome Próprio',
            'status': 'Jornada 1', 'played': True}]
        c.save_path.write_text(json.dumps(data))
        restored = career.CareerMode()
        self.assertEqual(restored.message, 'Career loaded.')
        self.assertEqual(restored.current_league.name, 'Scorer League')
        self.assertEqual((restored.goals, restored.week), (8, 3))
        self.assertEqual(restored.fixture_history[0]['status'], 'Matchweek 1')
        self.assertEqual(restored.fixture_history[0]['competition'], 'Scorer League')
        self.assertEqual(restored.fixture_history[0]['away'], 'Nome Próprio')

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
        self.assertTrue(restored.begin_training())
        self.assertEqual(restored.training_shots_taken, 0)
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

    def test_partial_training_resumes_without_resetting_or_duplicate_rewards(self):
        c = self.signed()
        self.assertTrue(c.begin_training())
        self.assertTrue(c.record_training_shot(True))
        restored = career.CareerMode()
        self.assertTrue(restored.begin_training())
        self.assertEqual((restored.training_shots_taken, restored.training_session_goals), (1, 1))
        before = restored.save_path.read_bytes()
        with patch('career.os.replace', side_effect=OSError('disk full')):
            self.assertFalse(restored.record_training_shot(False))
        self.assertEqual(restored.training_shots_taken, 1)
        self.assertEqual(restored.save_path.read_bytes(), before)
        self.assertTrue(restored.record_training_shot(False))
        self.assertTrue(restored.record_training_shot(True))
        self.assertFalse(restored.record_training_shot(True))
        self.assertGreater(restored.complete_training(restored.training_session_goals), 0)
        stats = (restored.stamina, restored.morale)
        restored = career.CareerMode()
        self.assertFalse(restored.begin_training())
        self.assertEqual(restored.complete_training(3), 0)
        self.assertEqual((restored.stamina, restored.morale), stats)

    def test_highlight_count_is_bounded_and_varies_with_condition(self):
        c = self.signed()
        c.stamina = c.morale = 20
        c.rng.seed(9921)
        fit = [c.chance_count() for _ in range(500)]
        c.stamina = c.morale = 2
        c.rng.seed(9921)
        tired = [c.chance_count() for _ in range(500)]
        self.assertTrue(all(0 <= value <= 3 for value in fit + tired))
        self.assertGreater(sum(fit), sum(tired))
        self.assertGreater(len(set(fit)), 1)

    def test_player_initials_format_on_save_and_legacy_load_with_scorer_key(self):
        c = self.signed()
        self.assertTrue(c.set_player_name('  joão   da silva  '))
        self.assertEqual(c.player_name, 'João Da Silva')
        self.assertTrue(c.set_player_name('sean McDonald'))
        self.assertEqual(c.player_name, 'Sean McDonald')
        c.player_name = 'gonçalo pereira'
        c.goals, c.matches = 11, 8
        c.current_league.scorer_goals = {'gonçalo pereira': 11, 'Other Scorer': 5}
        c.save()
        restored = career.CareerMode()
        self.assertEqual((restored.player_name, restored.goals, restored.matches), ('Gonçalo Pereira', 11, 8))
        self.assertEqual(restored.current_league.scorer_goals, {'Gonçalo Pereira': 11, 'Other Scorer': 5})
        self.assertTrue(restored.save())
        self.assertEqual(career.CareerMode().player_name, 'Gonçalo Pereira')

    def test_initials_collision_preserves_scores_and_failed_rename_keeps_save(self):
        c = self.signed()
        c.current_league.scorer_goals.update({'Luca Vale': 9, c.player_name: 3})
        c.save()
        before = c.save_path.read_bytes()
        with self.assertRaises(ValueError):
            c.set_player_name('luca vale')
        self.assertEqual(c.save_path.read_bytes(), before)
        with patch('career.os.replace', side_effect=OSError('disk full')):
            self.assertFalse(c.set_player_name('joão da silva'))
        self.assertEqual(c.player_name, 'Alex Silva')
        self.assertEqual(c.save_path.read_bytes(), before)
        c.player_name = 'luca vale'
        c.current_league.scorer_goals['luca vale'] = 2
        c.save()
        restored = career.CareerMode()
        self.assertEqual(restored.current_league.scorer_goals['Luca Vale'], 9)
        self.assertEqual(restored.current_league.scorer_goals['luca vale'], 2)

    def test_opponent_quality_and_table_position_both_reduce_opportunities(self):
        c = self.signed()
        clubs = c.current_league.clubs
        opponent = next(club for club in clubs if club.name != c.club_name)
        for index, club in enumerate(clubs):
            club.played, club.points = 12, 12 + index // 3
        opponent.points, opponent.rating = 12, 45
        weak_quality = c.opponent_chance_profile(opponent)
        opponent.rating = 90
        high_quality = c.opponent_chance_profile(opponent)
        self.assertGreater(high_quality.pressure, weak_quality.pressure)
        self.assertEqual((high_quality.max_chances, high_quality.clear_chance_probability), (1, 0))
        opponent.rating, opponent.points = 60, 0
        bottom = c.opponent_chance_profile(opponent)
        opponent.points = 36
        top = c.opponent_chance_profile(opponent)
        self.assertGreater(top.pressure, bottom.pressure)
        self.assertEqual((top.max_chances, top.clear_chance_probability), (1, 0))
        c.stamina = c.morale = 20
        opponent.rating, opponent.points = 45, 0
        c.rng.seed(17000)
        weak_counts = [c.chance_count(opponent) for _ in range(500)]
        opponent.rating, opponent.points = 95, 36
        c.rng.seed(17000)
        strong_counts = [c.chance_count(opponent) for _ in range(500)]
        self.assertTrue(all(0 <= n <= 1 for n in strong_counts))
        self.assertTrue(all(strong <= weak for strong, weak in zip(strong_counts, weak_counts)))
        self.assertGreater(sum(weak_counts), sum(strong_counts))

    def test_chance_profile_uses_opponents_own_table_and_no_unplayed_rank(self):
        c = self.signed()
        league = next(league for league in c.leagues.values() if league.country == 'Germany' and league.tier == 1)
        opponent = league.clubs[-1]
        opponent.rating = 60
        for club in league.clubs:
            club.played, club.points = 0, 0
        unplayed = c.opponent_chance_profile(opponent)
        league.clubs.reverse()
        self.assertEqual(c.opponent_chance_profile(opponent), unplayed)
        for club in league.clubs:
            club.played, club.points = 8, 8
        opponent.points = 24
        cup_profile = c.opponent_chance_profile(opponent)
        self.assertEqual((cup_profile.max_chances, cup_profile.clear_chance_probability), (1, 0))
        national = career.CareerClub('National opponent', 'Germany', 'National Team', 1, 95)
        self.assertEqual(c.opponent_chance_profile(national).max_chances, 1)
        self.assertEqual(c.opponent_chance_profile(national).clear_chance_probability, 0)

    def test_completed_training_guarantees_a_chance_even_against_elite_opponents(self):
        c = self.signed()
        c.begin_training()
        for _ in range(3):
            self.assertTrue(c.record_training_shot(True))
        c.complete_training(3)
        c = career.CareerMode()
        for rating in (45, 70, 95):
            opponent = career.CareerClub('Test opponent', 'England', 'Test league', 4, rating)
            cap = c.opponent_chance_profile(opponent).max_chances
            c.rng.seed(991)
            counts = [c.chance_count(opponent) for _ in range(500)]
            self.assertTrue(all(1 <= count <= cap for count in counts))
            if rating == 95:
                self.assertEqual(set(counts), {1})
                self.assertEqual(c.opponent_chance_profile(opponent).clear_chance_probability, 0)
        # Older completed saves without training counters also receive the floor.
        c.training_session_week = -1
        self.assertGreaterEqual(c.chance_count(), 1)

    def test_training_goals_help_extra_chances_without_bypassing_opponent_caps(self):
        c = self.signed()
        c.last_training_week = c.training_session_week = c.week
        c.stamina = c.morale = 10
        c.training_session_goals = 0
        c.rng.seed(991)
        no_goals = [c.chance_count() for _ in range(500)]
        c.training_session_goals = 3
        c.rng.seed(991)
        three_goals = [c.chance_count() for _ in range(500)]
        self.assertTrue(all(a <= b <= 3 for a, b in zip(no_goals, three_goals)))
        self.assertGreater(sum(three_goals), sum(no_goals))

    def test_league_scorers_conserve_goals_and_exclude_cup_goals(self):
        c = self.signed()
        home, away = c.next_fixture()
        player_home = home.name == c.club_name
        c.finish_match(home, away, 1, 1, forced_score=(2, 1) if player_home else (1, 2))
        league = c.current_league
        self.assertEqual(sum(league.scorer_goals.values()), sum(club.goals_for for club in league.clubs))
        self.assertEqual(league.scorer_goals[c.player_name], 1)
        scorer_before = dict(league.scorer_goals)
        c.finish_match(c.club, next(club for club in league.clubs if club.name != c.club_name),
                       2, 0, forced_score=(2, 0), competition='cup')
        self.assertEqual(c.goals, 3)
        self.assertEqual(league.scorer_goals, scorer_before)
        restored = career.CareerMode()
        self.assertEqual(restored.goals, 3)
        self.assertEqual(restored.current_league.scorer_goals[c.player_name], 1)

    def test_scorer_roles_share_existing_goals_without_merging_club_names(self):
        import random
        clubs = [career.CareerClub('United One', 'England', 'Test', 4, 60),
                 career.CareerClub('United Two', 'England', 'Test', 4, 60)]
        league = career.WorldLeague('England', 'Test', 4, clubs)
        league._add_scorers(clubs[0], 10000, random.Random(177))
        self.assertEqual(sum(league.scorer_goals.values()), 10000)
        self.assertTrue(0.29 <= max(league.scorer_goals.values())/10000 <= 0.35)
        league._add_scorers(clubs[1], 1000, random.Random(178))
        self.assertEqual(sum(league.scorer_goals.values()), 11000)
        self.assertTrue(any('(United One)' in name for name in league.scorer_goals))
        self.assertTrue(any('(United Two)' in name for name in league.scorer_goals))

    def test_empirical_goal_budget_and_expected_personal_contribution(self):
        import random
        home, away = career.realistic_goal_means(70, 70)
        self.assertAlmostEqual(home, 1.43)
        self.assertAlmostEqual(away, 1.18)
        for ratings in ((90, 50), (50, 90), (70, 70)):
            a,b=career.realistic_goal_means(*ratings)
            self.assertAlmostEqual(a+b, 2.61)
            self.assertGreater(a, 0)
            self.assertGreater(b, 0)
        rng=random.Random(1492)
        totals=[career.poisson_goal(rng, home)+career.poisson_goal(rng, away) for _ in range(10000)]
        self.assertAlmostEqual(sum(totals)/len(totals), 2.61, delta=0.06)
        self.assertTrue(0.10 < sum(n>=5 for n in totals)/len(totals) < 0.15)
        self.assertEqual(career.expected_highlight_goals(0, 0.6), 0)
        self.assertAlmostEqual(career.expected_highlight_goals(1, 0), 0.20)
        self.assertAlmostEqual(career.expected_highlight_goals(3, 0.6), 0.786)

    def test_balanced_double_round_robin_for_even_and_odd_leagues(self):
        from collections import Counter
        for count in range(2, 33):
            with self.subTest(clubs=count):
                clubs=[career.CareerClub(str(i),'England','Test',4,60) for i in range(count)]
                league=career.WorldLeague('England','Test',4,clubs)
                half=league.total_rounds//2
                venues={club.name:['',''] for club in clubs}
                opponents=[Counter(),Counter()]
                directed=Counter()
                for round_number in range(league.total_rounds):
                    fixtures=league.pairings(round_number)
                    self.assertEqual(len(fixtures), count//2)
                    playing=[]
                    for home,away in fixtures:
                        self.assertNotEqual(home.name,away.name)
                        playing.extend((home.name,away.name))
                        venues[home.name][round_number//half]+='H'
                        venues[away.name][round_number//half]+='A'
                        opponents[round_number//half][tuple(sorted((home.name,away.name)))]+=1
                        directed[(home.name,away.name)]+=1
                    self.assertEqual(len(playing),len(set(playing)))
                self.assertEqual(opponents[0],opponents[1])
                self.assertEqual(len(opponents[0]),count*(count-1)//2)
                self.assertTrue(all(n==1 for n in opponents[0].values()))
                self.assertTrue(all(n==1 for n in directed.values()))
                for halves in venues.values():
                    for pattern in halves:
                        self.assertEqual(len(pattern),count-1)
                        self.assertLessEqual(sum(a==b for a,b in zip(pattern,pattern[1:])),1)
                        self.assertLessEqual(abs(pattern.count('H')-pattern.count('A')),1)
                    crossing=halves[0][-1:]+halves[1]
                    self.assertLessEqual(sum(a==b for a,b in zip(crossing,crossing[1:])),1)
                    full=''.join(halves)
                    self.assertEqual(full.count('H'),count-1)
                    self.assertEqual(full.count('A'),count-1)
                    self.assertNotIn('HHH',full)
                    self.assertNotIn('AAA',full)
                self.assertEqual(league.pairings(-1),[])
                self.assertEqual(league.pairings(league.total_rounds),[])
                league.round_index=1
                self.assertEqual(league.pairings(),league.pairings(1))

    def test_legacy_calendar_matches_original_fixture_snapshot(self):
        for count,digest in ((5,'274d3dd0ba10d717304a55dda1b2b5b57b049682f244c113a9381eeb73af28b5'),
                             (24,'610a672a086cb2d69697acad311a07c291ede564a4a1b2b762265a014f5e8993')):
            clubs=[career.CareerClub(str(i),'England','Test',4,60) for i in range(count)]
            league=career.WorldLeague('England','Test',4,clubs,schedule_version=1)
            fixtures=[[(int(h.name),int(a.name)) for h,a in league.pairings(r)] for r in range(league.total_rounds)]
            actual=hashlib.sha256(json.dumps(fixtures,separators=(',',':')).encode()).hexdigest()
            self.assertEqual(actual,digest)

    def test_calendar_save_round_trip_and_safe_legacy_upgrade(self):
        def fixtures(league):
            return [[(h.name,a.name) for h,a in league.pairings(r)] for r in range(league.total_rounds)]
        for played in (0,1,2):
            with self.subTest(played=played):
                c=career.CareerMode(autoload=False)
                c.accept_starting_offer(c.offers[0]);c.cup_active=False
                for league in c.leagues.values():
                    league.schedule_version=1
                for _ in range(played):
                    home,away=c.next_fixture()
                    c.finish_match(home,away,1,0,forced_score=(1,0) if home.name==c.club_name else (0,1))
                c.save()
                before=fixtures(c.current_league)
                history=list(c.fixture_history)
                stats=(c.goals,c.matches,c.week,c.club.points)
                data=json.loads(c.save_path.read_text());data['career'].pop('schedule_version')
                c.save_path.write_text(json.dumps(data))
                restored=career.CareerMode()
                self.assertEqual(restored.current_league.schedule_version,2 if played<=1 else 1)
                self.assertEqual((restored.goals,restored.matches,restored.week,restored.club.points),stats)
                self.assertEqual(restored.fixture_history,history)
                after=fixtures(restored.current_league)
                self.assertEqual(after[:played],before[:played])
                if played>=2:
                    self.assertEqual(after,before)
                    restored._finish_season()
                    self.assertTrue(all(league.schedule_version==2 for league in restored.leagues.values()))
                restored.save()
                loaded=career.CareerMode()
                self.assertEqual(loaded.current_league.schedule_version,2)
                self.assertEqual(fixtures(loaded.current_league),fixtures(restored.current_league))

    def test_unknown_saved_calendar_version_does_not_replace_active_career(self):
        c=self.signed();before=c.player_name
        data=json.loads(c.save_path.read_text());data['career']['schedule_version']=999
        data['career']['player_name']='Unexpected'
        c.save_path.write_text(json.dumps(data));raw=c.save_path.read_bytes()
        self.assertFalse(c.load())
        self.assertEqual(c.player_name,before)
        self.assertEqual(c.save_path.read_bytes(),raw)

    def test_baseline_immutable(self):
        p = Path(career.__file__).parent / 'baseline/Striker-P0-05-v006.py'
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),
                         'fed211d2ec63fe0275390b13ed4a1bcfcd18fa61238460b04b67d80ebca6205b')


if __name__ == '__main__':
    unittest.main()
