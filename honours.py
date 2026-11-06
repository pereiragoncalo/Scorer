"""Personal trophy cabinet backed by observed participation and actual winners."""
import copy
FIELDS=('season','competition','title','team_uid','team','country')
def fresh():return dict(version=1,campaigns=[],trophies=[])
def clean(raw):
    result=fresh()
    if not isinstance(raw,dict) or raw.get('version')!=1:return result
    for key,limit in (('campaigns',256),('trophies',512)):
        rows=raw.get(key,[])
        if not isinstance(rows,list):continue
        for row in rows[:limit]:
            if (isinstance(row,dict) and type(row.get('season')) is int and 2026<=row['season']<=2500
                and all(isinstance(row.get(k),str) and 0<len(row[k])<=256 and row[k].isprintable() for k in FIELDS[1:])):
                value={k:row[k] for k in FIELDS}
                if value not in result[key]:result[key].append(value)
    return result

def participate(c,key,title,team_uid,team,country):
    row=dict(season=c.season,competition=key,title=title,team_uid=team_uid,team=team,country=country)
    if row not in c.honours['campaigns']:c.honours['campaigns']=(c.honours['campaigns']+[row])[-256:]

def award(c,row):
    if row not in c.honours['trophies']:
        c.honours['trophies']=(c.honours['trophies']+[copy.deepcopy(row)])[-512:]
        from title_events import enqueue
        enqueue(c,row)

def collect(c,book=None,league=None):
    for row in c.honours['campaigns']:
        if row['season']!=c.season:continue
        key=row['competition']
        if league is not None and key=='league:'+league.key:
            table=league.table()
            from domestic_formats import player_finished
            finished=league.round_index>=league.total_rounds or (table and player_finished(league,table[0].uid))
            if table and finished and table[0].uid==row['team_uid']:award(c,row)
        if book is not None and key in book.tournaments:
            cup=book.tournaments[key]
            if cup.kind!='qualifying' and not key.startswith(('playoff:','reserve:')) and cup.champion==row['team_uid']:award(c,row)


def collect_season(c,book=None):
    collect(c,book)
    campaigns={row['competition'][7:]:row for row in c.honours['campaigns']
               if row['season']==c.season and row['competition'].startswith('league:')}
    for key,row in campaigns.items():
        league=c.leagues.get(key)
        if league is None:continue
        collect(c,league=league)
        from domestic_formats import player_finished
        table=league.table()
        finished=league.round_index>=league.total_rounds or (table and player_finished(league,table[0].uid))
        goals=league.scorer_goals.get(c.player_name,0)
        if finished and goals>0 and goals==max(league.scorer_goals.values(),default=0):
            award(c,dict(row,competition='scorer:'+key,title='Golden Boot'))
