import configparser
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch
import edition
from tools.prepare_editions import prepare_edition
from world_promotion import board_segments, campaign_message, listing_url, WORLD_LISTING_URL


class EditionTests(unittest.TestCase):
    def test_identity_is_fixed_by_binary_not_billing_or_save(self):
        with patch.object(edition,'WORLD_PREVIEW',False):
            for world,mode in ((False,'free'),(True,'world')):
                with patch.object(edition,'WORLD_BUILD',world):
                    self.assertEqual(edition.product_mode(),mode)
                    self.assertIs(edition.entitlement_provider().has_world_access(),world)

    def test_staging_produces_different_packages_and_native_capabilities(self):
        before=Path('edition.py').read_bytes()
        with tempfile.TemporaryDirectory() as temp:
            products={}
            for product in ('free','world'):
                root=prepare_edition(product,Path(temp)/product)
                spec=configparser.ConfigParser(interpolation=None);spec.read(root/'buildozer.spec')
                products[product]=spec['app']['package.domain']+'.'+spec['app']['package.name']
                self.assertEqual(spec['app']['title'],'Scorer World' if product=='world' else 'Scorer')
                expected_icon='assets/icon_world.png' if product=='world' else 'assets/icon.png'
                self.assertEqual(spec['app']['icon.filename'],expected_icon)
                self.assertEqual((root/expected_icon).read_bytes(),Path(expected_icon).read_bytes())
                if product=='free':
                    self.assertFalse((root/'assets/icon_world.png').exists())
                    self.assertFalse((root/'assets/menu_logo_world.png').exists())
                else:self.assertEqual((root/'assets/menu_logo_world.png').read_bytes(),Path('assets/menu_logo_world.png').read_bytes())
                self.assertFalse((root/'billing.py').exists())
                self.assertFalse((root/'android/src/com/clemir/striker/billing').exists())
                self.assertFalse((root/'server').exists())
                self.assertNotIn('billingclient',spec['app'].get('android.gradle_dependencies',''))
                self.assertIn('WORLD_PREVIEW = False',(root/'edition.py').read_text())
                if product=='world':
                    self.assertFalse((root/'android/src').exists())
                    self.assertFalse(spec['app'].get('android.permissions',''))
                    self.assertNotIn('android.meta_data',spec['app'])
                    self.assertNotIn('android.gradle_dependencies',spec['app'])
                    self.assertIn('WORLD_BUILD = True',(root/'edition.py').read_text())
                else:
                    self.assertIn('play-services-ads',spec['app']['android.gradle_dependencies'])
                    self.assertIn('WORLD_BUILD = False',(root/'edition.py').read_text())
            self.assertEqual(products,{'free':'com.clemir.striker','world':'com.clemir.scorerworld'})
        self.assertEqual(Path('edition.py').read_bytes(),before)

    def test_boards_are_outside_playing_area_and_leave_goal_clear(self):
        self.assertEqual(len(board_segments()),11)
        for a,b in board_segments():
            for x,y in (a,b):
                self.assertTrue(y<0 or abs(x)>34)
                if y<0:self.assertGreaterEqual(abs(x),7.8)
            self.assertNotEqual(a,b)

    def test_campaign_rotates_without_per_frame_texture_changes(self):
        self.assertEqual(campaign_message(0),campaign_message(24.99))
        self.assertNotEqual(campaign_message(24.99),campaign_message(25))
        self.assertEqual(campaign_message(0),campaign_message(100))
        self.assertEqual(campaign_message(-50),campaign_message(0))

    def test_store_link_requires_actual_published_listing_configuration(self):
        self.assertIsNone(listing_url(types.SimpleNamespace(WORLD_LISTING_READY=False)))
        self.assertEqual(listing_url(types.SimpleNamespace(WORLD_LISTING_READY=True)),WORLD_LISTING_URL)

    def test_staging_refuses_unknown_identity_and_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):prepare_edition('pirated',Path(temp)/'bad')
            root=Path(temp)/'existing';root.mkdir();(root/'career.json').write_text('preserve')
            with self.assertRaises(ValueError):prepare_edition('world',root)
            self.assertEqual((root/'career.json').read_text(),'preserve')
