import unittest
from pathlib import Path
from fontTools.ttLib import TTFont

class PressFontTests(unittest.TestCase):
    def test_original_display_and_retro_faces_have_latin_accent_coverage(self):
        root=Path('assets/fonts')
        for filename in ('ScorerPressPixel.ttf','ScorerPressDisplay.ttf'):
            font=TTFont(root/filename)
            try:
                cmap=font.getBestCmap()
                for char in 'SCORER DAILY Ponte Preta São Luís João Açores Nguyễn Đặng Việt 32 51 67 90 — ()':
                    self.assertIn(ord(char),cmap,(filename,char))
                self.assertIn('Scorer Press',font['name'].getDebugName(1))
            finally:font.close()
        self.assertTrue((root/'OFL-ScorerPress.license').is_file())
