"""Owner-selected simplified model, separate from researched national formats.

These rules are a game design choice, not a claim about real-world regulations.
Historical third/fourth-tier objects may be retained for save compatibility, but
are excluded from new starts, browsing, transfers and simulation.
"""

from dataclasses import dataclass


PRIORITY_AMERICAS = frozenset({'Brazil', 'Argentina', 'Mexico'})


def uses_simplified_model(country, european_depths):
    return True  # Owner: every World country now uses the same two-tier model.


def division_depth(country, european_depths):
    return 2


def standing_zone(tier, position, team_count):
    """Only the two-tier simplified model uses these zone labels."""
    if tier not in (1, 2) or not 1 <= position <= team_count or team_count < 6:
        return ''
    if tier == 2 and position <= 3:
        return 'Promotion'
    if tier in (1,2) and position > team_count - 3:
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


def table_zones(tier,team_count,active_tiers,*,simplified,country="",league=None):
    """Match existing 3-up / simulated4–7 /2-down career eligibility.

    The owner's two-tier fallback instead uses3-up/3-down and no playoffs.
    A league cannot promote/relegate beyond the available active pyramid.
    """
    if tier not in active_tiers:return TableZones(archived=simplified and tier>2)
    if team_count<6:return TableZones()
    if simplified and country:
        from domestic_playoffs import profile,eligible_table,direct_up
        p=profile(country,bool(league and league.format_key));direct=p['direct'];shape=p['shape']
        extra=2 if shape in ('parallel','argentine') else 1 if shape else 0
        if tier==1:
            n=direct if p['upper'] else direct+extra
            return TableZones(playoff=tuple(sorted(team_count+i+1 for i in p['upper'])),relegation=tuple(range(team_count-n+1,team_count+1)) if n else ())
        table=eligible_table(league) if league else None
        positions=tuple(p['places']) if shape!='argentine' else tuple(range(1,min(16,team_count-p['reserve_direct'])+1))
        if league and shape=='italian' and len(direct_up(league))==3:direct=3;positions=()
        promotion=tuple(range(1,direct+1))
        if table:
            original={c.uid:i+1 for i,c in enumerate(league.table())}
            promotion=tuple(original[c.uid] for c in table[:direct])
            positions=tuple(original[table[i-1].uid] for i in positions if i<=len(table))
        down=p['reserve_direct'];reserve_po=tuple(team_count+i+1 for i in p['reserve_places'])
        if league and p['reserve_shape']=='playout' and league.table()[-5].points-league.table()[-4].points>4:down+=1;reserve_po=()
        return TableZones(promotion,tuple(sorted(positions+reserve_po)),tuple(range(team_count-down+1,team_count+1)) if down else ())
    from season_transitions import promotion_format
    direct,places=promotion_format(country,tier,simplified)
    up=direct if tier-1 in active_tiers else 0
    if tier+1 in active_tiers:
        next_direct,next_playoff=promotion_format(country,tier+1,simplified)
        down=next_direct+bool(next_playoff)
    else:down=3 if simplified and tier==2 else 0
    playoff=tuple(p for p in places if p<=team_count-down) if up else ()
    return TableZones(tuple(range(1,up+1)),playoff,
                      tuple(range(team_count-down+1,team_count+1)) if down else (),provisional=False)
