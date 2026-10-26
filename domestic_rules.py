"""Owner-selected simplified model, separate from researched national formats.

These rules are a game design choice, not a claim about real-world regulations.
Historical third/fourth-tier objects may be retained for save compatibility, but
are excluded from new starts, browsing, transfers and simulation.
"""

from dataclasses import dataclass


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



@dataclass(frozen=True)
class TableZones:
    """Eligibility places in the current game model, not verified national rules."""
    promotion: tuple = ()
    playoff: tuple = ()
    relegation: tuple = ()
    archived: bool = False
    provisional: bool = False

    def at(self,position):
        if position in self.promotion:return 'promotion'
        if position in self.playoff:return 'playoff'
        if position in self.relegation:return 'relegation'
        return ''


def table_zones(tier,team_count,active_tiers,*,simplified):
    """Match existing 3-up / simulated4–7 /2-down career eligibility.

    The owner's two-tier fallback instead uses3-up/3-down and no playoffs.
    A league cannot promote/relegate beyond the available active pyramid.
    """
    if tier not in active_tiers:return TableZones(archived=simplified and tier>2)
    if team_count<6:return TableZones()
    up=3 if tier-1 in active_tiers else 0
    down=(3 if simplified else 2) if tier+1 in active_tiers else 0
    playoff=tuple(range(4,min(7,team_count-down)+1)) if up and not simplified else ()
    return TableZones(tuple(range(1,up+1)),playoff,
                      tuple(range(team_count-down+1,team_count+1)) if down else (),provisional=not simplified)
