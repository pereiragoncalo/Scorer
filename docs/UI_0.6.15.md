# SCORER 0.6.15 — opponent-dependent opportunities

## Behaviour
The chance plan is chosen once at kick-off using the actual opponent, both
at home and away. Opponent quality and league position reduce the expected
number of personal highlights and the probability of a clear chance. Energy
and morale still matter. At most one clear chance is ever allocated.

| Opponent pressure | Maximum chances | Clear-chance allocation |
| --- | ---: | --- |
| Very strong (≥0.72) | 1 | None; every chance is hard |
| Strong (≥0.50) | 2 | 15% chance of one clear opportunity |
| Lower | 3 | Up to 60%, decreasing as pressure rises |

Zero chances remains possible. These caps are limits, not guaranteed counts.
Physical shot difficulty, scoring, training, saved progress and rival scorer
statistics are unchanged.

## Quality and position
Quality is the rating normalised between 45 and 90. Domestic table position
is normalised from 1 (leader) to 0 (bottom). Ranking weight rises from zero
before any matches to 45% after five; rating supplies the remainder. An elite
rating (≥84.6), or a top-15% table place after at least five games, enforces
pressure of at least 0.80. This ensures very strong opponents cannot allocate
a clear chance even when player condition is excellent.

Cups use the opponent's own domestic league table, not the player's table.
Where no matching domestic table exists, including national teams, only
rating is used. Existing simulations of league results remain unchanged.

## Files and tests
career.py adds an immutable opponent chance profile and uses it in chance_count;
main.py passes the actual opponent at kick-off and uses the same profile for
the clear-chance allocation. Also changed buildozer.spec, tests/test_career.py,
ui_tests/test_menus.py, AGENTS.md, README.md and documentation.

38 core/build/security + 32 real Kivy tests passed (70). New tests cover quality
and rank effects, 500 paired seeded draws for weak/strong sides, unplayed-table
handling, a cup opponent's own table, national-team fallback and home/away
match integration with very strong/weak opponents. Existing chance-type and
maximum-one-clear tests use an explicit weak profile to isolate that policy.
No UI layout change or new visual asset. APK evidence is in BUILD_LOG.

Next: update without uninstalling and compare chances across strong leaders,
mid-table and weaker opponents. Physical validation of this beta and long-term
human balancing remain pending. No AAB or store release signing in this step.
