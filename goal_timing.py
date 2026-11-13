"""Seeded event timing with soft separation; never changes goals or chance count."""
def spaced_minutes(rng,available,count,occupied=()):
    pool=list(available);chosen=[];other=list(occupied)
    for _ in range(min(count,len(pool))):
        def weight(minute):
            distance=min((abs(minute-t)for t in other+chosen),default=100)
            return .03 if distance<=1 else .12 if distance<=3 else .5 if distance<=5 else 1.
        weights=[weight(t)for t in pool]
        value=rng.choices(pool,weights=weights,k=1)[0];chosen.append(value);pool.remove(value)
    return sorted(chosen)

def goal_events(rng,home,away,final_minute,chances):
    # Counts are already sampled by the original score model. Keep them exact.
    pool=[t for t in range(2,final_minute+1)if t not in chances]
    needed=home+away
    times=spaced_minutes(rng,pool,needed,chances)
    # Extremely high scorelines remain possible; no cap or discarded goals.
    while len(times)<needed:times.append(rng.randint(2,final_minute))
    sides=['home']*home+['away']*away;rng.shuffle(sides)
    return sorted(zip(times,sides),key=lambda row:row[0])
