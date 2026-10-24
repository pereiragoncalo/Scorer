"""Between-match advertising; no SDK/network imports on desktop or core import."""
from time import monotonic


class AdBreaks:
    MIN_MATCHES = 1
    MIN_SECONDS = 60

    def __init__(self, backend=None, now=monotonic):
        self.backend = backend
        self.now = now
        self.since_break = 0
        self.last_break = now() - self.MIN_SECONDS
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

    def prepare_reward(self):
        self._call('prepare_reward')

    def show_reward(self, context):
        if self._call('show_reward', context) is True:
            self.last_break = self.now()  # Never stack a forced break after an opt-in ad.
            return True
        self.prepare_reward()
        return False

    @property
    def pending_reward(self):
        raw = self._call('pending_reward')
        if isinstance(raw, str) and raw.count('|') == 1 and len(raw) <= 160:
            return tuple(raw.split('|'))
        return None

    def acknowledge_reward(self, token):
        self._call('acknowledge_reward', token)

    @property
    def break_status(self):
        return self._call('break_status') or 'Full-screen ads are unavailable.'

    @property
    def reward_status(self):
        return self._call('reward_status') or 'Reward ads are available on Android only.'

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

    def prepare_reward(self):
        self.bridge.prepareReward(self.activity)

    def show_reward(self, context):
        return bool(self.bridge.showReward(self.activity, context))

    def pending_reward(self):
        return str(self.bridge.peekReward(self.activity))

    def acknowledge_reward(self, token):
        self.bridge.acknowledgeReward(self.activity, token)

    def break_status(self):
        return str(self.bridge.getBreakStatus())

    def reward_status(self):
        return str(self.bridge.getRewardStatus())

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
