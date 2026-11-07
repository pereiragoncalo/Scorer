"""Two active divisions and a persistent FIFO reserve of ten clubs per country.
Archived league objects exist only to preserve old UIDs, names and save history.
"""
POOL_SIZE=10
MOVEMENT=3
RELEGATED_MESSAGE='Your club left Division 2. You are free to sign for another club.'
LEGACY_RELEASE_MESSAGE='Lower divisions were retired. You are now free to sign for a club.'


def rotate_reserve(lower,archive,queue,down=None,up=None):
    """Validate then exchange bottom three with the oldest three reserve clubs."""
    if lower.tier!=2 or archive.tier!=3 or lower.country!=archive.country:raise ValueError('Invalid reserve boundary')
    all_clubs=lower.clubs+archive.clubs;by_id={c.uid:c for c in all_clubs}
    if len(by_id)!=len(all_clubs) or len(queue)!=POOL_SIZE or len(set(queue))!=POOL_SIZE:raise ValueError('Invalid reserve identities')
    if not set(queue)<={c.uid for c in archive.clubs}:raise ValueError('Reserve club is not in the archive')
    down=list(down) if down is not None else lower.table()[-MOVEMENT:]
    if len({c.uid for c in down})!=len(down) or any(c not in lower.clubs for c in down):raise ValueError('Invalid reserve relegation')
    up=list(up) if up is not None else [by_id[uid] for uid in queue[:len(down)]]
    if len(up)!=len(down) or len({c.uid for c in up})!=len(up) or any(c.uid not in queue for c in up):raise ValueError('Invalid reserve promotions')
    lower.clubs=[c for c in lower.clubs if c not in down]+up
    archive.clubs=[c for c in archive.clubs if c not in up]+down
    for league in (lower,archive):
        for club in league.clubs:club.tier,club.league=league.tier,league.name
    return [uid for uid in queue if uid not in {c.uid for c in up}]+[c.uid for c in down],[{'uid':c.uid,'from':source.key,'to':target.key} for source,target,clubs in ((lower,archive,down),(archive,lower,up)) for c in clubs]


class TwoDivisionCareer:
    def _ensure_reserves(self):
        from career import WORLD_COUNTRIES
        if any(f'{country}|3' not in self.leagues or f'{country}|2' not in self.leagues for country in WORLD_COUNTRIES):
            self._build_world({country:3 for country in WORLD_COUNTRIES})
        for country in WORLD_COUNTRIES:
            if country not in self.relegation_pools:
                self.relegation_pools[country]=sorted(c.uid for c in self.leagues[country+'|3'].clubs)[:POOL_SIZE]

    def reserve_clubs(self,country):
        ids=self.relegation_pools[country];clubs={c.uid:c for c in self.leagues[country+'|3'].clubs}
        return [clubs[uid] for uid in ids]

    def _free_agent_offers(self):
        country=self.current_league.country
        domestic=[(c.name,l.key) for l in self.domestic_leagues(country) if l.tier==2 for c in l.clubs]
        from league_status import league_band
        status=league_band(country,2)
        foreign=[(c.name,l.key) for l in self.domestic_leagues() if l.country!=country and l.tier==2 and league_band(l.country,2)>=status for c in l.clubs]
        self.agent_offers=self.rng.sample(domestic,min(5-min(2,len(foreign)),len(domestic)))+self.rng.sample(foreign,min(2,len(foreign)))
        self.last_offer_week=self.week
        return self.agent_offers

    def _release_contract(self,message,club=None):
        club=club or self.club;country=self.current_league.country
        self.released_club={'uid':club.uid,'name':club.name,'country':country,'season':self.season} if club else self.released_club
        self.free_agent=True;self.club_name='';self.league_key=country+'|2';self.free_start_key=self.league_key
        self.cup_active=False;self.called_up=False;self.message=message
        self._active_world_countries.add(country);self._free_agent_offers()

    def _restore_two_divisions(self,data):
        from career import WORLD_COUNTRIES
        legacy=data.get('domestic_model_version')!=2
        self._needs_two_division_backup=legacy
        self._ensure_reserves()
        if not legacy:
            pools=data.get('relegation_pools')
            if not isinstance(pools,dict) or set(pools)!=set(WORLD_COUNTRIES):raise ValueError('Missing reserve pools')
            for country,queue in pools.items():
                available={c.uid for c in self.leagues[country+'|3'].clubs}
                if not isinstance(queue,list) or len(queue)!=POOL_SIZE or any(not isinstance(uid,str) for uid in queue) or len(set(queue))!=POOL_SIZE or not set(queue)<=available:raise ValueError('Invalid reserve pool')
            self.relegation_pools={c:list(q) for c,q in pools.items()}
        elif self.world_competitions is not None:
            # Keep already drawn cups/results and dates from the old career.
            # Only obsolete promotion playoffs are retired; new cups use tiers1/2.
            self.world_competitions.tournaments={k:v for k,v in self.world_competitions.tournaments.items() if not k.startswith('playoff:')}
        if self.current_league.tier>2:
            self._release_contract(LEGACY_RELEASE_MESSAGE)
        elif self.free_agent:
            if self.club_name:raise ValueError('A free agent cannot also hold a contract')
            if not self.agent_offers:self._free_agent_offers()
            self.message=data.get("message") if data.get("message") in (RELEGATED_MESSAGE,LEGACY_RELEASE_MESSAGE) else RELEGATED_MESSAGE
        elif not self.club:
            raise ValueError('Missing player contract')
        self.free_start_key=self.current_league.country+'|2'
        self._repair_qualifiers()
        if legacy:self.world_membership={k:[c.uid for c in l.clubs] for k,l in self.leagues.items()}

    def _repair_qualifiers(self):
        if not self.qualification_snapshot:return
        active={c.uid:c for l in self.domestic_leagues() for c in l.clubs}
        fields=self.qualification_snapshot['entries'];reserved={t['uid'] for k,teams in fields.items() if not k.startswith('nations_') for t in teams if t['uid'] in active}
        for key,teams in fields.items():
            if key.startswith('nations_'):continue
            for index,team in enumerate(teams):
                if team['uid'] in active:continue
                candidates=[c for l in self.domestic_leagues(team['country']) if l.tier==1 for c in l.table() if c.uid not in reserved]
                if not candidates:raise ValueError('No active qualification replacement')
                c=candidates[0];teams[index]={'uid':c.uid,'name':c.name,'country':c.country,'rating':c.rating,'tier':c.tier};reserved.add(c.uid)
