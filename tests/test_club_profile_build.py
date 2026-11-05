"""Build-time source parsing: requires mwparserfromhell, never an app dependency."""
import importlib.util,unittest
@unittest.skipUnless(importlib.util.find_spec('mwparserfromhell'),'optional build dependency')
class SourceParser(unittest.TestCase):
    def test_winners_are_counted_but_runners_up_and_playoffs_are_not_titles(self):
        from tools.build_club_profiles import honours
        source='''==Honours==
*[[Championship]]
**Champions: [[2020 Championship|2020]], [[2022 Championship|2022]]
**Runners-up: 2021
**Play-off winners: 2023
*[[Cup]]: 3
===Individual honours===
*[[Player award]] (9): 2020
'''
        self.assertEqual(honours(source),[dict(title='Championship',count=2),dict(title='Cup',count=3)])
    def test_html_references_do_not_turn_access_dates_into_capacity(self):
        from tools.build_club_profiles import capacity
        self.assertEqual(capacity('35,618<ref>Accessed 2026-11-05</ref>'),35618)
        self.assertIsNone(capacity('<ref>Accessed 2026-11-05</ref>'))
    def test_position_tables_and_parenthesised_wins_are_not_confused(self):
        from tools.build_club_profiles import honours
        source='''==Honours==
{| class="wikitable"
|-
|[[League]]
|Champions
|2001, 2003
|-
|[[Other League]]
|Runners-up
|1999, 2000, 2001
|}
*[[Cup]]
**Winners (1): 2004
'''
        self.assertEqual(honours(source),[dict(title='League',count=2),dict(title='Cup',count=1)])
