"""Read-only Windows hub data. Browsing must not advance fixtures or RNG."""
from dataclasses import dataclass

@dataclass(frozen=True)
class FixtureRow:
    home: str
    away: str
    focus: bool

@dataclass(frozen=True)
class ScorerRow:
    rank: int
    player: str
    club: str
    goals: int
    focus: bool

@dataclass(frozen=True)
class DashboardData:
    round_number: int
    fixtures: tuple
    scorers: tuple
    next_match: tuple | None
    hero_rank: int
    hero_league_goals: int


def dashboard_data(career):
    league=career.current_league
    fixtures=tuple(FixtureRow(career.display_club(home),career.display_club(away),
                             career.club_name in (home.name,away.name))
                   for home,away in (league.pairings() if league.round_index<league.total_rounds else ()))
    ranking=dict(league.scorer_goals);ranking.setdefault(career.player_name,0)
    scorers=[]
    for rank,(raw,goals) in enumerate(sorted(ranking.items(),key=lambda pair:(-pair[1],pair[0])),1):
        focus=raw==career.player_name
        if focus:
            player,club=career.player_name,career.display_text(career.club_name)
        elif raw.endswith(')') and ' (' in raw:
            player,club=raw.rsplit(' (',1);club=career.display_text(club[:-1])
        else:player,club=career.display_scorer(raw),''
        scorers.append(ScorerRow(rank,player,club,goals,focus))
    upcoming=career.next_match()
    next_match=(upcoming[0],career.display_club(upcoming[1]),career.display_club(upcoming[2])) if upcoming else None
    hero=next(row for row in scorers if row.focus)
    return DashboardData(league.round_index+1,fixtures,tuple(scorers),next_match,hero.rank,hero.goals)
