import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from desktop_launcher import configure
from tools.windows.build import stage_windows,build,ROOT

class WindowsFreeTests(unittest.TestCase):
    def test_windows_stage_is_fixed_free_without_world_or_android_payload(self):
        with tempfile.TemporaryDirectory() as folder:
            target=stage_windows(Path(folder)/'source')
            ns={};exec((target/'edition.py').read_text(),ns)
            self.assertFalse(ns['WORLD_BUILD']);self.assertFalse(ns['WORLD_PREVIEW'])
            self.assertIn('DESKTOP_WINDOWS = True',(target/'release_settings.py').read_text())
            self.assertEqual((target/'analytics_config.py').read_text(),"ENDPOINT = ''\n")
            for item in ('server','android','tools','buildozer.spec','billing.py','assets/i18n','assets/icon_world.png','assets/menu_logo_world.png','striker_career.json','scorer_usage.json'):
                self.assertFalse((target/item).exists(),item)
            self.assertFalse(list((target/'assets/fonts').glob('*Noto*')))
            for item in ('assets/icon.png','assets/menu_logo.png','assets/splash.png','assets/menu_stadium.png','assets/fonts/Barlow-Regular.ttf'):
                self.assertTrue((target/item).is_file(),item)
    def test_save_directory_independent_of_resource_extraction_directory(self):
        before=Path.cwd()
        try:
            with tempfile.TemporaryDirectory() as folder,patch.dict(os.environ,{},clear=True):
                os.environ['LOCALAPPDATA']=str(Path(folder)/'profile')
                directory=configure(ROOT)
                self.assertEqual(directory,(Path(folder)/'profile/Clemir/Scorer/Free').resolve())
                self.assertEqual(Path(os.environ['STRIKER_SAVE_DIR']),directory)
                self.assertTrue(directory.is_dir());self.assertNotEqual(directory,ROOT)
                from career import CareerMode
                c=CareerMode(autoload=False);self.assertEqual(c.save_path.parent,directory)
                c.set_player_name('Windows Test');c.accept_starting_offer(c.offers[0])
                self.assertTrue(c.save());self.assertTrue(c.save_path.exists())
        finally:os.chdir(before)
    def test_explicit_test_override_preserved_across_relaunch(self):
        before=Path.cwd()
        try:
            with tempfile.TemporaryDirectory() as folder,patch.dict(os.environ,{'STRIKER_SAVE_DIR':folder}):
                self.assertEqual(configure(ROOT),Path(folder).resolve())
                p=Path(folder)/'striker_career.json';p.write_text('existing progress')
                self.assertEqual(configure(ROOT),Path(folder).resolve());self.assertEqual(p.read_text(),'existing progress')
        finally:os.chdir(before)
    def test_missing_assets_fail_before_changing_directory_or_creating_save(self):
        before=Path.cwd()
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(RuntimeError):configure(folder)
            self.assertEqual(Path.cwd(),before)
    def test_staging_refuses_source_and_nonempty_destination(self):
        with self.assertRaises(ValueError):stage_windows(ROOT)
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder)/'keep.txt').write_text('keep')
            with self.assertRaises(ValueError):stage_windows(folder)
            self.assertEqual((Path(folder)/'keep.txt').read_text(),'keep')
    def test_linux_build_cannot_be_misrepresented_as_windows_executable(self):
        with patch('tools.windows.build.sys.platform','linux'):
            with self.assertRaisesRegex(RuntimeError,'Build Scorer-Free.exe on Windows'):build('unused')
