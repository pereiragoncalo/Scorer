"""Android staging must ship the approved manifest and shared runtime modules."""
import tempfile,unittest,hashlib,json
from pathlib import Path
from tools.prepare_editions import prepare_edition
ROOT=Path(__file__).resolve().parents[1]
class SpritePayloadTests(unittest.TestCase):
    def test_world_stage_contains_exact_approved_art_and_runtime_without_tools_imports(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=prepare_edition('world',Path(tmp)/'world',analytics_endpoint='')
            source=ROOT/'assets/sprites/manifest.json';staged=target/'assets/sprites/manifest.json'
            self.assertEqual(staged.read_bytes(),source.read_bytes())
            manifest=json.loads(staged.read_text());self.assertEqual(manifest['approval_status'],'APPROVED')
            for c in manifest['characters'].values():
                for a in c['animations'].values():
                    for sheet in a['sheets'].values():
                        self.assertEqual((target/sheet['path']).read_bytes(),(ROOT/sheet['path']).read_bytes())
            for module in ('sprite_animation.py','sprite_textures.py','retro_sprites.py','stadium_scene.py','supporter_layout.py'):
                text=(target/module).read_text();self.assertEqual(text,(ROOT/module).read_text())
                self.assertNotIn('tools.sprite_lab',text);self.assertNotIn('from PIL',text)
