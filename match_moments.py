"""Match presentation and timing only: never alter chances, physics or AI scores."""
import random

# Stable club identities from the existing eight-country names-pack mapping.
# Names/aliases are deliberately absent from the shipped rivalry lookup.
DERBIES = frozenset(frozenset(pair) for pair in (
    ('c8d6431e000ec7467295', '00d46be2fe2f866aca10'),
    ('5d27df05665c0406256b', 'd1e35165727184231fcf'),
    ('fd1111e5e54231a2a93f', '1b90a5a7b45d01807901'),
    ('79f1e283c133ea287c86', '09746d7dd23654a57132'),
    ('0a57fa8e31a868f0b6e9', '6b74be0a0c0301dca0bf'),
    ('ba2bfbd0a51871c48b80', '2224dfac92112d65324f'),
    ('0b0e55f7ce27b78e366b', 'e1e8a4498a1104be3486'),
    ('a2fb9f1e2eb7fac49500', '2128f2b8f01e8eeecf3a'),
    ('1783c72961b1da9ec6ce', '7ffa78f5eaccb968a9e8'),
    ('1811a02d3dea0e34d763', '0a85927f40ff51c7b32e'),
    ('b12c65334b70507f4c00', '5f9f7033f562b3fe6218'),
    ('3145ed569b6a9aadd63d', '794dfa592f5ab59b07c2'),
    ('c0f4799cb1271c270fdc', '25978b18d31edad02b79'),
))

TEXT = {
    'equaliser': ('LATE EQUALISER', 'One goal would draw your team level. The match is still live.'),
    'lead': ('LATE CHANCE TO LEAD', 'The scores are level. Take the lead before the final whistle.'),
    'final': ('CUP FINAL', 'A chance on the biggest stage. The final is still in play.'),
    'playoff': ('LEAGUE PLAYOFF', 'League places are at stake in this tie.'),
    'derby': ('DERBY DAY', 'Local rivals, one chance to make your mark.'),
    'survival': ('SURVIVAL RUN-IN', 'Your club is close to the relegation line. Every point matters.'),
}


def match_stakes(career, token, home, away):
    """Snapshot actual fixture context without advancing competitions or RNG.

    Two-legged ties use the already played first leg for late score messages.
    The first leg cannot be described as a late equaliser/winner for the tie.
    """
    context = {'kind': '', 'prior': (0, 0), 'late_allowed': True}
    if token.startswith('world|'):
        _, key, fixture_id = token.split('|', 2)
        book = career.world_competitions
        cup = book.tournaments.get(key) if book else None
        fixture = next((f for f in cup.fixtures if f['id'] == fixture_id), None) if cup else None
        if fixture:
            if key.startswith('playoff:'):
                context['kind'] = 'playoff'
            elif fixture['stage'] == 'Final':
                context['kind'] = 'final'
            legs = [f for f in cup.fixtures if fixture.get('tie') is not None and f.get('tie') == fixture['tie']]
            if len(legs) > 1:
                prior = [f for f in legs if f['leg'] < fixture['leg']]
                context['late_allowed'] = fixture['leg'] == max(f['leg'] for f in legs) and all(f['score'] is not None for f in prior)
                totals = {home.uid: 0, away.uid: 0}
                for f in prior:
                    if f['score'] is not None:
                        totals[f['home']] += f['score'][0]
                        totals[f['away']] += f['score'][1]
                context['prior'] = (totals[home.uid], totals[away.uid])
                # Aggregate messages need explicit wording; keep the tie context
                # rather than confusing the current leg score with the total.
                context['late_allowed'] = False
    elif token == 'cup' and career.cup_round_label == 'Final':
        context['kind'] = 'final'
    if not context['kind'] and frozenset((home.uid, away.uid)) in DERBIES:
        context['kind'] = 'derby'
    if token == 'league' and not context['kind'] and career.world_unlocked:
        from domestic_rules import table_zones, uses_simplified_model
        from career import EUROPE_PYRAMID_DEPTH
        league = career.current_league
        remaining = league.total_rounds - league.round_index
        if 1 <= remaining <= 5:
            table = league.table()
            zones = table_zones(league.tier, len(table), {l.tier for l in career.domestic_leagues(league.country)},
                                simplified=uses_simplified_model(league.country, EUROPE_PYRAMID_DEPTH), country=league.country, league=league)
            if zones.relegation:
                boundary = min(zones.relegation) - 1
                safe, danger = table[boundary - 1], table[boundary]
                actor = career.club
                pos = next((i + 1 for i, c in enumerate(table) if c.uid == actor.uid), 0)
                # Restrict to the direct-drop boundary. Never claim guaranteed
                # safety, especially with unequal split schedules or playoffs.
                if pos and abs(pos - boundary) <= 2 and abs(actor.points - (safe.points if pos > boundary else danger.points)) <= 3:
                    context['kind'] = 'survival'
    return context


def late_opportunity(minutes, first_stoppage, final_minute, seed, important=False):
    """Move at most the last existing chance; independent, deterministic RNG.

    Never inspect future goals, add a chance, change its difficulty index or
    consume career RNG. Existing late chances stay untouched.
    """
    result = list(minutes)
    if not result or result[-1] >= 85 + first_stoppage:
        return result
    rng = random.Random('scorer-moments-v1:' + str(seed))
    if rng.random() < (0.75 if important else 0.45):
        result[-1] = rng.randint(85 + first_stoppage, final_minute - 1)
    return result


def chance_moment(context, minute, home_score, away_score, player_home, used=False):
    """Use only the score actually reached when this chance pauses the clock."""
    if used:
        return ''
    own, other = (home_score, away_score) if player_home else (away_score, home_score)
    if minute >= 85 and context.get('late_allowed', True):
        if own == other - 1:
            return 'equaliser'
        if own == other:
            return 'lead'
    return context.get('kind', '')


def clean_moments(events):
    """Bound optional history data; legacy entries need no migration."""
    if not isinstance(events, (list, tuple)):
        return []
    for item in events[:1]:
        if (isinstance(item, dict) and item.get('kind') in TEXT
                and type(item.get('minute')) is int and 0 <= item['minute'] <= 110
                and item.get('outcome') in ('goal', 'missed')):
            return [{key: item[key] for key in ('kind', 'minute', 'outcome')}]
    return []
