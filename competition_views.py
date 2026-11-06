"""Read-only competition membership for the player's current-season standings."""
def involved_competitions(career):
    c=career
    rows=[('league:'+c.league_key,c.current_league)]
    campaigns=[r for r in c.honours['campaigns'] if r['season']==c.season]
    for row in campaigns:
        key=row['competition']
        if key.startswith('league:') and key!='league:'+c.league_key and key[7:] in c.leagues:
            if key not in {k for k,_ in rows}:rows.append((key,c.leagues[key[7:]]))
    book=c.world_competitions
    if not c.world_unlocked or book is None:return rows
    club=c.club.uid if c.club else ''
    nation='nation:'+c.nationality
    selected=c.national_team_eligible or any(value and key.startswith(c.nationality+':') for key,value in book.callups.items())
    for key,cup in book.tournaments.items():
        observed=any(r['competition']==key and r['team_uid'] in cup.teams for r in campaigns)
        if observed or (nation in cup.teams and selected if cup.national else club in cup.teams):rows.append((key,cup))
    return rows
