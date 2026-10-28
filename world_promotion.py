"""Local SCORER World promotion: no tracking, network assets or pitch interaction."""
WORLD_PACKAGE = 'com.clemir.scorerworld'
WORLD_LISTING_URL = 'https://play.google.com/store/apps/details?id=' + WORLD_PACKAGE
ROTATION_SECONDS = 25
WINDOWS_MESSAGES = ('YOUR COMPANY HERE', 'SPONSOR THIS STADIUM', 'SCORER WORLD', 'WORLD LEAGUES')
MESSAGES = ('SCORER WORLD', 'WORLD LEAGUES', 'LOCAL NAME EDITOR', 'PLAY AD-FREE')


def campaign_message(elapsed, offset=0, desktop=False):
    messages=WINDOWS_MESSAGES if desktop else MESSAGES
    return messages[(max(0, int(elapsed)) // ROTATION_SECONDS + offset) % len(messages)]


def board_segments():
    # Behind the goal line, outside the goal/net and playing rectangle.
    # Each pair is the bottom edge in pitch metres; render as a vertical surface.
    back = [((a, -3.5), (b, -3.5)) for a, b in
            [(-33, -25), (-24, -16), (-15, -7.8), (7.8, 15), (16, 24), (25, 33)]]
    side = [((35.3, a), (35.3, a + 5)) for a in (1, 7, 13, 19, 25)]
    return tuple(back + side)


def listing_url(settings):
    # Publication readiness is public build configuration, never inferred from
    # a successful browser launch or an installation. Do not link to a dead page.
    return WORLD_LISTING_URL if settings.WORLD_LISTING_READY is True else None
