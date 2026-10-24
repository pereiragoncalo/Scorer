import unittest
from advertising import AdBreaks, create_ad_breaks


class Backend:
    def __init__(self):
        self.loaded = True
        self.shows = 0
        self.prepares = 0
        self.privacy = 0
        self.banners = []
    def entry_visible(self, visible): self.banners.append(visible)
    def prepare(self): self.prepares += 1
    def ready(self): return self.loaded
    def show(self):
        self.shows += 1
        self.loaded = False
        return True
    def privacy_options(self): self.privacy += 1
    def status(self): return 'Test ad ready'


class AdvertisingTests(unittest.TestCase):
    def setUp(self):
        self.time = 0
        self.backend = Backend()
        self.ads = AdBreaks(self.backend, now=lambda: self.time)

    def finish(self, key):
        self.ads.match_completed(key)
        return self.ads.continue_after_match()

    def test_only_natural_break_after_three_matches_and_three_minutes(self):
        self.time = 181
        self.assertFalse(self.finish('first'))
        self.assertFalse(self.finish('second'))
        self.assertEqual(self.backend.shows, 0)
        self.assertTrue(self.finish('third'))
        self.assertEqual(self.backend.shows, 1)
        self.backend.loaded = True
        self.assertFalse(self.finish('fourth'))
        self.assertFalse(self.finish('fifth'))
        self.assertFalse(self.finish('sixth'))
        self.time += 181
        self.assertTrue(self.finish('seventh'))
        self.assertEqual(self.backend.shows, 2)

    def test_offline_or_slow_load_cannot_show_later_or_on_repeated_continue(self):
        self.time = 200
        self.backend.loaded = False
        for key in range(3): self.assertFalse(self.finish(key))
        self.backend.loaded = True
        self.assertFalse(self.ads.continue_after_match())
        self.assertEqual(self.backend.shows, 0)
        self.assertTrue(self.finish(3))
        self.assertFalse(self.ads.continue_after_match())
        self.assertEqual(self.backend.shows, 1)

    def test_no_fullscreen_from_start_privacy_or_duplicate_match_registration(self):
        self.ads.start()
        self.ads.privacy_options()
        self.assertEqual(self.backend.privacy, 1)
        self.time = 300
        for _ in range(4): self.ads.match_completed('same match')
        self.assertFalse(self.ads.continue_after_match())
        self.assertEqual(self.ads.since_break, 1)
        self.assertEqual(self.backend.shows, 0)
        self.assertEqual(self.ads.status, 'Test ad ready')

    def test_entry_banner_visibility_is_separate_from_fullscreen_breaks(self):
        self.ads.entry_visible(False)
        self.ads.entry_visible(True)
        self.ads.entry_visible(True)
        self.ads.entry_visible(False)
        self.assertEqual(self.backend.banners, [False, True, False])
        self.assertEqual(self.backend.shows, 0)
        self.assertFalse(self.ads.pending)

    def test_backend_exceptions_and_desktop_remain_playable(self):
        class Broken:
            def __getattr__(self, name): raise RuntimeError('offline or unavailable bridge')
        for backend in (None, Broken()):
            ads = AdBreaks(backend, now=lambda: self.time)
            ads.start()
            ads.privacy_options()
            self.time += 500
            for key in range(4):
                ads.match_completed(key)
                self.assertFalse(ads.continue_after_match())
            self.assertIn('Android', ads.status)
        self.assertIsNone(create_ad_breaks().backend)
