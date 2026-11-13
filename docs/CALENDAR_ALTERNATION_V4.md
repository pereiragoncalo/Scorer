# More alternating league venues — pending next Android build

The owner's Portugal Division2 complaint is confirmed: v3 prevented three home
or away games in succession but allowed frequent HH/AA pairs. Across an eighteen
club,34game double round robin, v3 produced164 repeated-venue transitions and up
to12per club. New v4 has48in total and at most3per club. The second leg preserves
the first leg's opponent order with every home/away fixture reversed. No three
consecutive home/away matches; each club plays17at home and17away.

The same fixed construction is validated for every even size6–64: total3n−6
repeats, no club above3, balanced home/away counts. Leagues of two clubs retain the trivial
alternation; odd sizes keep frozen v3. The unused4club exception retains its
existing balanced fallback because mirror order plus max-two is incompatible
for that compact schedule. Official multi-leg/split competition structures stay
unchanged. Cup/national matches interleaved in the calendar are separate draws
and do not promise league-style alternation.

Runtime uses frozen data in alternating_schedule.py, not a solver and not the
career RNG. Version3's existing table is unchanged. Build-only candidate tooling
is tools/build_alternating_schedules.py; never replace a shipped version's data.

## Existing saves

An optional persisted schedule_variant identifies a prevalidated eighteen-club
v3 prefix continuation. Eligible first-leg saves can change only unplayed
fixtures, retaining every completed opponent/venue and all results, statistics,
club identities and the active player's future repetition count or better.
Migration occurs only if it strictly reduces remaining repeated venues. Invalid
variants are rejected atomically. Save/reload must retain identical future
fixtures. A save with an incompatible played prefix stays on its old calendar;
new seasons reset to v4. Once the first leg is fixed, its mirrored return
fixtures cannot be freely reoriented without breaking the owner's constraints.

This source correction is not in the currently delivered1030019AAB. Pending next
build together with the season review/local-contact net corrections.

Audit data: data/calendar_alternation_v4/portugal2.json and .csv. C=home, F=away;
rows are demonstrative team slots rather than the owner's private save.
