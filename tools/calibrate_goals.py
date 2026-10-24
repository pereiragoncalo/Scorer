"""Seeded fictional season calibration, with no changes to a user's saves."""
import json
import random
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from career import CareerClub, WorldLeague


def experiment(seasons=100):
    goals=home_goals=away_goals=draws=nil_nil=five_plus=matches=0
    top_scorers=[]
    for seed in range(seasons):
        rng=random.Random(71000+seed)
        clubs=[CareerClub(f'Fictional{i:02d}', 'England', 'Calibration', 4, 59+16*i/23) for i in range(24)]
        league=WorldLeague('England', 'Calibration', 4, clubs)
        for round_index in range(46):
            for home,away in league.pairings(round_index):
                a,b=league.simulate_fixture(home,away,rng)
                matches+=1;goals+=a+b;home_goals+=a;away_goals+=b
                draws+=a==b;nil_nil+=a==b==0;five_plus+=a+b>=5
        assert sum(league.scorer_goals.values()) == sum(c.goals_for for c in clubs)
        top_scorers.append(max(league.scorer_goals.values(),default=0))
    return dict(seasons=seasons,matches=matches,goals_per_match=goals/matches,
        home=home_goals/matches,away=away_goals/matches,draw_rate=draws/matches,
        nil_nil_rate=nil_nil/matches,five_plus_rate=five_plus/matches,
        top_scorer_mean=sum(top_scorers)/len(top_scorers),top_scorer_min=min(top_scorers),top_scorer_max=max(top_scorers))

if __name__ == '__main__':
    print(json.dumps(experiment(),indent=2,sort_keys=True))
