"""Public build metadata, replaced only in isolated Play staging sources."""
CHANNEL = 'beta'
DEVELOPER_NAME = 'Gonçalo Pereira'
SUPPORT_EMAIL = 'goncalo@clemir.com'
PRIVACY_URL = 'https://pereiragoncalo.github.io/Scorer/privacy/'


def is_store():
    return CHANNEL in ('rehearsal', 'production')


def is_production():
    return CHANNEL == 'production'

# Enable only after the separate World store listing is publicly available.
WORLD_LISTING_READY = False
