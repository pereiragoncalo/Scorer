# Scorer World0.9.34 QA — career, presentation and difficulty

The championship captain now runs with articulated legs and straight raised arms,
carrying the trophy at the authored wrist anchors. Continue uses the standard
rounded MenuTile and real touch handling. The calendar resolves the next playable
week before the title talk so the weekly focus is acknowledged for that week;
this removes the second same-day weekly talk. The special talk merges due club
focus choices and pending individual topics.

The dashboard's player, club, training and play actions share one equal-sized row.
Morale/fitness and division/role information is larger and centred. Coach screens
show only the dressing-room picture. Feedback combines varied outcome and
personality phrases, retains key-performance context, and mandates praise or a
keep-focused response for a hat-trick. Individual meetings can follow five-game
scoring droughts or transfer proposals.

Players start at18, receive a fixed weekly contract wage and can buy16 illustrated
items from their player screen: four homes, cars, gifts and outfits. The initial
home is a club-provided studio. Wages are paid once per calendar week, including
weeks without fixtures, without duplicate payment on reload or multi-game weeks.
Purchases are local, saved and reversible on failed writes; no real-money billing
or gameplay attribute rewards. At38 and every subsequent season the player may
retire or continue. After38, opportunity quantity and decision time decline and
shot flight becomes slower. Retirement is saved and stops further play/training.

Competitive touch now shoots at the moving marker instead of overriding it by
tapping a corner. Manual practice aiming remains available. The aim is a bounded
stochastic path with irregular changes, not a repeating sine sweep. Opportunity
base time is40% of the previous allocation with a1.3s minimum; earned focus time
bonuses are then added in full. The intended marker remains the ballistic target,
without hidden launch scatter or score caps. AI/team goal budgets do not add a
full teammate simulation on top of a personal scoring contribution.

Hat-tricks use the knee-slide celebration. If the team is still losing, retrieving
the ball takes priority: the player runs into the goal, picks up a visual ball
attached to the hands and heads toward midfield. The original ball solver stays
independent. Penalties show four waiting players from each team outside the area
and penalty arc; corners add three teammates and crosses add one. Supporters are
larger; top-five clubs fill their allocated home/away sectors, while partial
attendance has a ragged lower fringe. Plain-shirt palettes correct Benfica and
other identified solid home shirts; existing club colours stay UID-bound.

The new-game form stores a favourite club. Agent offers respect equal/higher
league-status bands and prioritise the same country until the player stands out.
Eligible standout players receive a favourite-club offer. The newspaper uses a
PNG paper sprite under its dynamic photo and text. The approved208 base actor
frames are unchanged;32 original carrying/retrieval frames bring the total to240,
with34 sheets.

Leaderboard categories are Season and Career. Career totals are tracked club
career totals, not fabricated sums of best-season records. The additive v4 server
implementation and a self-contained installer for bastion are included. The owner
will execute that installer; remote deployment is not performed from this cloud
environment. Existing v3 seasonal records remain supported. Career publication is
explicit; viewing does not publish records.

League prestige covers212 game countries using UEFA association coefficients and
FIFA national-ranking proxies, with five game bands and explicit unranked
fallbacks. The complete five-year official club-table request is **not finished**:
499 game identities have results-derived presets,301 have five available seasons;
disciplinary deductions, some tie-breaks and phased final tables still require
verification. Unknown/fictitious clubs use labelled game baselines. See
[data coverage](data/reputation/README.md); these presets must not be described as
complete verified official standings.

This is an existing-debug-key QA candidate. Physical Android playtesting remains
pending. Google Play production1.0 is unchanged.
