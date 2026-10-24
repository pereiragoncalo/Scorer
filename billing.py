"""Fail-closed Python facade for the native Play Billing/verified licence bridge.

The cached boolean is a snapshot: never change gameplay entitlements mid-shot.
The game adopts a newly verified entitlement only at a safe menu boundary.
"""
class PlayWorldAccess:
    def __init__(self, bridge=None, activity=None):
        self.bridge, self.activity = bridge, activity
        if bridge is None:
            try:
                from kivy.utils import platform
                if platform == 'android':
                    from jnius import autoclass
                    self.activity = autoclass('org.kivy.android.PythonActivity').mActivity
                    self.bridge = autoclass('com.clemir.striker.billing.WorldBilling')
            except Exception:
                self.bridge = None
        self._access = self.verified_now()

    def verified_now(self):
        try:
            return self.bridge is not None and self.bridge.hasAccess(self.activity) is True
        except Exception:
            return False

    def has_world_access(self):
        return self._access is True

    def restore_world_access(self):
        self.restore()
        return self._access

    def _call(self, method):
        try:
            if self.bridge is not None:
                return getattr(self.bridge, method)(self.activity)
        except Exception:
            pass
        return None

    def prepare(self): self._call('prepare')
    def purchase(self): self._call('purchase')
    def restore(self): self._call('restore')

    @property
    def status(self):
        return self._call('status') or 'Purchases are not available in this build. No charge has been made.'

    @property
    def price(self):
        return self._call('price') or ''

    @property
    def can_purchase(self):
        return self._call('canPurchase') is True
