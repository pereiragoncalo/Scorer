import unittest
from unittest.mock import patch
from test_menus import isolated_game,settle

class KitUITests(unittest.TestCase):
    def test_training_uses_current_club_after_international_match_and_editor_import(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=g.career;c.accept_starting_offer(c.offers[0]);g._career_started=True
            g.match_home=c.leagues['Portugal|1'].clubs[0];g.match_away=c.leagues['Portugal|1'].clubs[1];g.match_is_international=True
            g.shot_context='training';expected=c.kit_for_club(c.club)
            self.assertEqual(g._match_outfield_kits()[0],expected)
            c.display_aliases['clubs'][c.club.uid]='My edited name'
            g.view='training';g.draw();settle();self.assertEqual(g._match_outfield_kits()[0],expected)
            c.attend_coach_meeting();g.start_training();settle();self.assertEqual(g.view,'shot');self.assertEqual(g._match_outfield_kits()[0],expected)
    def test_match_resolves_opponent_actual_uid_with_no_name_pack(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=g.career;c.accept_starting_offer(c.offers[0]);g._career_started=True;g.shot_context='match';g.match_is_international=False
            opponent=next(x for x in c.leagues['Portugal|1'].clubs if sum(abs(a-b) for a,b in zip(c.kit_for_club(c.club)[0][:3],c.kit_for_club(x)[0][:3]))>=.42)
            for home,away in [(c.club,opponent),(opponent,c.club)]:
                g.match_home,g.match_away=home,away
                self.assertEqual(g._match_outfield_kits(),(c.kit_for_club(c.club),c.kit_for_club(opponent)))
    def test_vitoria_bahia_player_and_training_use_red_black_without_reimport(self):
        from career import hex_rgba
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=g.career;club=next(cl for league in c.leagues.values() for cl in league.clubs if cl.uid=='f9554f2ce1ab5ff99892')
            c.league_key=next(k for k,l in c.leagues.items() if club in l.clubs);c.club_name=club.name
            c.display_aliases['clubs'][club.uid]='Vitória BA'
            c.save();self.assertTrue(c.load())
            opponent=next(cl for cl in c.current_league.clubs if cl.uid!=club.uid)
            expected=tuple(hex_rgba(v) for v in ('FF0000','FFFFFF','FFFFFF','000000'))
            for home,away in ((c.club,opponent),(opponent,c.club)):
                g.match_home,g.match_away=home,away;g.match_is_international=False;g.shot_context='match'
                self.assertEqual(g._match_outfield_kits()[0],expected)
            g.match_is_international=True;g.shot_context='training'
            self.assertEqual(g._match_outfield_kits()[0],expected)
