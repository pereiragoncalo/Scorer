"""Ranked promotion/relegation with played playoff brackets and stable identities."""
def promotion_format(country,lower_tier,simplified=False):
    if simplified:return 3,()
    if country=='England' and lower_tier==4:return 3,(4,5,6,7)
    if country=='England' and lower_tier==5:return 1,(2,3,4,5,6,7)
    return 2,(3,4,5,6)

def exchange_pyramid(leagues,country,winners,simplified=False):
    pyramid=sorted((l for l in leagues if l.country==country),key=lambda l:l.tier)
    original={l.key:list(l.clubs) for l in pyramid};out={l.key:set() for l in pyramid};incoming={l.key:[] for l in pyramid};moves=[]
    for upper,lower in zip(pyramid,pyramid[1:]):
        if lower.tier!=upper.tier+1:continue
        direct,playoff=promotion_format(country,lower.tier,simplified)
        up=lower.table()[:direct]
        if playoff:
            winner=winners.get(f'playoff:{country}:{lower.tier}')
            eligible={lower.table()[i-1].uid for i in playoff}
            if winner not in eligible:raise ValueError('Completed playoff winner required')
            up.append(next(c for c in lower.clubs if c.uid==winner))
        down=upper.table()[-len(up):]
        for source,target,clubs in ((lower,upper,up),(upper,lower,down)):
            out[source.key].update(c.uid for c in clubs);incoming[target.key].extend(clubs)
            moves.extend({'uid':c.uid,'from':source.key,'to':target.key} for c in clubs)
    # Validate every boundary first; no cascades or half-applied pyramid changes.
    proposed={l.key:[c for c in original[l.key] if c.uid not in out[l.key]]+incoming[l.key] for l in pyramid}
    before=[c.uid for l in pyramid for c in original[l.key]];after=[c.uid for l in pyramid for c in proposed[l.key]]
    if len(set(before))!=len(before) or set(before)!=set(after) or len(after)!=len(set(after)) or any(len(proposed[l.key])!=len(original[l.key]) for l in pyramid):raise ValueError('Invalid ranked movement')
    for l in pyramid:
        l.clubs=proposed[l.key]
        for c in l.clubs:c.tier,c.league=l.tier,l.name
    return moves
