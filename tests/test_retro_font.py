"""Real text coverage and typography invariants for the bundled game font."""
from pathlib import Path
import unittest
from fontTools.ttLib import TTFont
from localization import Localizer, retro_supported
from retro_glyphs import RETRO_CODEPOINTS

ROOT=Path(__file__).resolve().parents[1]

class RetroFontTests(unittest.TestCase):
    def test_exported_coverage_matches_real_font_and_names_remain_readable(self):
        with TTFont(ROOT/'assets/fonts/ScorerRetro.ttf') as font:
            cmap=font.getBestCmap()
            self.assertEqual(set(cmap),set(RETRO_CODEPOINTS))
            for text in ('Gonçalo Pereira','São Paulo — 2–1','Atlético · João Félix','Bayern München','Trust 68/100 · Starter ›','Đặng Văn Lâm'):
                self.assertTrue(retro_supported(text),text)
                self.assertTrue(all(c.isspace() or ord(c) in cmap for c in text))
            for char in 'abcdefghijklmnopqrstuvwxyz':
                self.assertNotEqual(cmap[ord(char)],cmap[ord(char.upper())])
            for char in 'gjpqy':
                self.assertLess(font['glyf'][cmap[ord(char)]].yMin,0)
            for digit in '0123456789':
                self.assertEqual(font['hmtx'][cmap[ord(digit)]][0],600)

    def test_primary_font_explicit_exceptions_and_native_script_fallback(self):
        loc=Localizer(True,'en')
        for text in ('TRAINING','Alex Silva','3–1','Coração',''):
            self.assertEqual(Path(loc.font(text)).name,'ScorerRetro.ttf')
        self.assertEqual(loc.font('Splash',explicit='original.ttf'),'original.ttf')
        self.assertEqual(Path(loc.legacy_font('TAP TO START')).name,'Barlow-Regular.ttf')
        self.assertNotEqual(Path(loc.font('日本語')).name,'ScorerRetro.ttf')
        self.assertNotEqual(Path(loc.font('한국어')).name,'ScorerRetro.ttf')
