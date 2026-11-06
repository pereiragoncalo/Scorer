"""Deterministic visual turnout, based on collective league results only."""
def turnout(club,league=None):
    played=max(0,getattr(club,'played',0));points=max(0,getattr(club,'points',0))
    if not played:return .66
    ppg=min(1.,points/max(1,played*3))
    rank=.5
    if league is not None:
        rows=league.table();index=next((i for i,t in enumerate(rows) if t.uid==club.uid),None)
        if index is not None:rank=1.-index/max(1,len(rows)-1)
    performance=.8*ppg+.2*rank
    evidence=min(1.,played/5.)
    return round(max(.35,min(.98,.35+.63*(.492*(1-evidence)+performance*evidence))),4)

def team_turnout(career,club):
    if club is None:return 0.
    if str(club.uid).startswith('nation:') and career.world_competitions is not None:
        from types import SimpleNamespace
        book=career.world_competitions
        fixtures=[f for cup in book.tournaments.values() if cup.national for f in cup.fixtures]+list(book.friendlies.values())
        played=sorted((f for f in fixtures if f.get('score') is not None and club.uid in (f['home'],f['away'])),key=lambda f:(f['week'],f.get('date',''),f['id']))[-8:]
        points=0
        for f in played:
            own=0 if f['home']==club.uid else 1;a,b=f['score'][own],f['score'][1-own]
            points+=3 if a>b else 1 if a==b else 0
        return turnout(SimpleNamespace(played=len(played),points=points))
    league=career.leagues.get(str(club.country)+'|'+str(club.tier))
    return turnout(club,league)

def fixture_snapshot(game,home,away):
    token=(getattr(home,'uid',''),getattr(away,'uid',''),repr(getattr(game,'match_opportunity_seed',None)))
    saved=getattr(game,'_attendance_snapshot',None)
    if saved and saved[0]==token:return saved[1]
    result={'home':team_turnout(game.career,home),'away':team_turnout(game.career,away)}
    game._attendance_snapshot=(token,result)
    return result

def occupied_seats(seats,fractions,noise):
    """Fill each home/away section from its highest physical row downwards."""
    sectors={}
    for seat in seats:
        x,y,z,code,team,tier=seat
        section='corner' if x>36.2 and y<-4 else 'side' if x>36.2 else 'goal'
        sectors.setdefault((team,section),[]).append(seat)
    result=[]
    for (team,section),values in sectors.items():
        values.sort(key=lambda s:(-s[2],noise(*s[:4])))
        count=round(len(values)*max(0.,min(1.,fractions.get(team,0.))))
        result.extend(values[:count])
    return result
