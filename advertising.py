"""Between-match advertising; no SDK/network imports on desktop or core import."""
from time import monotonic


class AdBreaks:
    MIN_MATCHES = 3
    MIN_SECONDS = 180

    def __init__(self, backend=None, now=monotonic):
        self.backend = backend
        self.now = now
        self.since_break = 0
        self.last_break = now()
        self.last_match = None
        self.pending = False
        self.entry_shown = None

    def start(self):
        self._call('prepare')

    def _call(self, name, *args):
        try:
            return getattr(self.backend, name)(*args) if self.backend else None
        except Exception:
            # Ad availability must never block career progression or saves.
            return None

    def entry_visible(self, visible):
        visible = bool(visible)
        if visible == self.entry_shown:
            return
        self.entry_shown = visible
        self._call('entry_visible', visible)

    def match_completed(self, match_key):
        if match_key == self.last_match:
            return
        self.last_match = match_key
        self.since_break += 1
        self.pending = True
        self._call('prepare')

    def continue_after_match(self):
        # Consume the natural break even if offline. Never show an ad later
        # because an asynchronous load finished after the player moved on.
        if not self.pending:
            return False
        self.pending = False
        if (self.since_break < self.MIN_MATCHES
                or self.now() - self.last_break < self.MIN_SECONDS):
            return False
        if not self._call('ready'):
            return False
        if self._call('show') is not True:
            return False
        self.since_break = 0
        self.last_break = self.now()
        return True

    @property
    def status(self):
        return self._call('status') or 'Test ads are available on Android only.'

    @property
    def privacy_required(self):
        return bool(self._call('privacy_required'))

    def privacy_options(self):
        self._call('privacy_options')


class AndroidTestAds:
    """Java bridge is locked to Google's official test ad units."""
    def __init__(self):
        from jnius import autoclass
        self.activity = autoclass('org.kivy.android.PythonActivity').mActivity
        self.bridge = autoclass('com.clemir.striker.ads.ScorerAds')

    def entry_visible(self, visible):
        self.bridge.setEntryBannerVisible(self.activity, visible)

    def prepare(self):
        self.bridge.prepare(self.activity)

    def ready(self):
        return bool(self.bridge.isReady())

    def show(self):
        # Java atomically reserves the ready ad before posting to the UI thread.
        return bool(self.bridge.showAtBreak(self.activity))

    def status(self):
        return str(self.bridge.getStatus())

    def privacy_required(self):
        return bool(self.bridge.isPrivacyOptionsRequired())

    def privacy_options(self):
        self.bridge.showPrivacyOptions(self.activity)


def create_ad_breaks(android=False):
    backend = None
    if android:
        try:
            backend = AndroidTestAds()
        except Exception:
            pass
    return AdBreaks(backend)
