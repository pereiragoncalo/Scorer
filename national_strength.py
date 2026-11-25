"""Fixed game estimates for European national teams."""
from itertools import permutations

EURO_RATINGS = {
    'Spain': 94, 'France': 93, 'England': 92, 'Portugal': 91,
    'Germany': 90, 'Netherlands': 89, 'Italy': 88, 'Belgium': 87,
    'Croatia': 86, 'Switzerland': 84, 'Denmark': 83, 'Austria': 82,
    'Turkey': 82, 'Ukraine': 81, 'Norway': 81, 'Serbia': 80,
    'Poland': 80, 'Czechia': 79, 'Sweden': 79, 'Scotland': 78,
    'Hungary': 78, 'Wales': 77, 'Greece': 77, 'Romania': 76,
    'Slovakia': 76, 'Slovenia': 75, 'Georgia': 74, 'Albania': 73,
    'Russia': 73, 'Republic of Ireland': 72, 'Bosnia and Herzegovina': 71,
    'Finland': 71, 'North Macedonia': 70, 'Israel': 70, 'Iceland': 69,
    'Montenegro': 68, 'Kosovo': 68, 'Northern Ireland': 67, 'Bulgaria': 66,
    'Armenia': 64, 'Luxembourg': 63, 'Belarus': 62, 'Kazakhstan': 62,
    'Azerbaijan': 60, 'Estonia': 58, 'Cyprus': 57, 'Moldova': 56,
    'Lithuania': 55, 'Latvia': 54, 'Faroe Islands': 53, 'Malta': 47,
    'Andorra': 42, 'Gibraltar': 39, 'Liechtenstein': 37, 'San Marino': 32,
}


def is_euro(key):
    return key == 'euro' or key.startswith('euro_q')


def euro_rating(key, team):
    return EURO_RATINGS.get(team['country'], team['rating']) if is_euro(key) else team['rating']


def euro_goal_means(key, home, away):
    if is_euro(key) and home in EURO_RATINGS and away in EURO_RATINGS:
        from career import realistic_goal_means
        return realistic_goal_means(EURO_RATINGS[home], EURO_RATINGS[away],
                                    rating_scale=10.0, neutral=key == 'euro')
    return None


def seeded_order(teams, groups, rng):
    ranked = sorted(teams, key=lambda row: (-EURO_RATINGS[row['country']], row['uid']))
    ordered = []
    for start in range(0, len(ranked), groups):
        pot = ranked[start:start + groups]
        rng.shuffle(pot)
        ordered.extend(pot)
    return ordered


def last_sixteen(tables, qualified):
    """Pair group winners with third-place teams or runners-up from other groups."""
    winners = [rows[0]['uid'] for rows in tables]
    runners = [rows[1]['uid'] for rows in tables]
    thirds = qualified[len(winners) + len(runners):]
    group = {row['uid']: index for index, rows in enumerate(tables) for row in rows}
    # Two runners-up join the four thirds in the seeded half; the other four
    # form two runner-up ties. First try the existing ranking order.
    opponents = thirds + runners[:2]
    paired = next(order for order in permutations(opponents)
                  if all(group[a] != group[b] for a, b in zip(winners, order)))
    return winners + runners[2:4] + list(reversed(paired + tuple(runners[4:])))
