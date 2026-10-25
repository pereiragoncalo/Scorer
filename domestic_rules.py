"""Owner-selected simplified model, separate from researched national formats.

These rules are a game design choice, not a claim about real-world regulations.
Historical third/fourth-tier objects may be retained for save compatibility, but
are excluded from new starts, browsing, transfers and simulation.
"""

PRIORITY_AMERICAS = frozenset({'Brazil', 'Argentina', 'Mexico'})


def uses_simplified_model(country, european_depths):
    return country not in european_depths and country not in PRIORITY_AMERICAS


def division_depth(country, european_depths):
    if country in european_depths:
        return european_depths[country]
    return 4 if country in PRIORITY_AMERICAS else 2


def standing_zone(tier, position, team_count):
    """Only the two-tier simplified model uses these zone labels."""
    if tier not in (1, 2) or not 1 <= position <= team_count or team_count < 6:
        return ''
    if tier == 2 and position <= 3:
        return 'Promotion'
    if tier == 1 and position > team_count - 3:
        return 'Relegation'
    return ''


def exchange_three(upper, lower):
    """Exchange ranked clubs together, preserving identities and table sizes.

    Validate both divisions before any mutation. Never select displaced clubs by
    rating or create replacement identities. Return the promoted/relegated UIDs.
    """
    if upper.country != lower.country or upper.tier != 1 or lower.tier != 2:
        raise ValueError('Expected adjacent divisions of the same country')
    clubs = upper.clubs + lower.clubs
    if min(len(upper.clubs), len(lower.clubs)) < 6:
        raise ValueError('Insufficient clubs for three promotions/relegations')
    if any(not c.uid for c in clubs) or len({c.uid for c in clubs}) != len(clubs):
        raise ValueError('Club identities must be unique before movement')
    down, up = upper.table()[-3:], lower.table()[:3]
    down_ids, up_ids = {c.uid for c in down}, {c.uid for c in up}
    upper.clubs = [c for c in upper.clubs if c.uid not in down_ids] + up
    lower.clubs = [c for c in lower.clubs if c.uid not in up_ids] + down
    for league in (upper, lower):
        for club in league.clubs:
            club.tier, club.league = league.tier, league.name
    return up_ids, down_ids
