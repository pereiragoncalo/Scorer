"""Public build metadata, replaced only in isolated Play staging sources."""
CHANNEL = 'beta'
DEVELOPER_NAME = ''
SUPPORT_EMAIL = ''
PRIVACY_URL = ''


def is_store():
    return CHANNEL in ('rehearsal', 'production')


def is_production():
    return CHANNEL == 'production'

# Enable only after the separate World store listing is publicly available.
WORLD_LISTING_READY = False
