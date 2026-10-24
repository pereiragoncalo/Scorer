# SCORER 0.6.18 — balanced home/away league calendar

## Rules
- Alternate home and away. Each club has at most one pair of consecutive home
  or away appearances per leg, including the transition into the return leg.
- No run of three home or away league appearances, including across the break.
- Each opponent is faced once per leg, with the venue reversed in the return.
  Every club has the same total number of home and away league games.
- Return rounds are reversed with a two-round offset. This prevents an extra
  home/away break at the leg boundary and avoids an immediate rematch in the
  actual leagues (four or more clubs).
- For the 24-club FREE league: 23 matches per leg, 46 per season, 23 home and
  23 away. Rules concern league rounds; cup draws retain their independent
  venues and can interrupt the visible home/away sequence across competitions.

## Existing careers
schedule_version is an optional field in save format v2. New careers/seasons
use version 2. Older schedules are version 1. An older save is upgraded now
only if every completed league fixture has exactly the same opponent/venue
in the new schedule (normally zero or one completed round in FREE).

Incompatible seasons keep their original complete calendar until the season
ends, then switch to version 2. This avoids rewriting played matches or making
the same club host both meetings. Existing results, progress, player names,
training, scorer data and other save fields remain intact. Reloading preserves
the selected calendar; unsupported schedule versions fail without replacing
current state. No new save-format version or new permissions.

## Implementation and tests
WorldLeague.pairings changes only the round ordering/venue assignment. The
circle pairing has a fixed bye for odd-sized test leagues; their round count
includes byes correctly. Current shipped league sizes are even. The native
menu, calendar, match launcher and simulation all use the same pairing method.
No UI geometry, gameplay physics or artwork changes.

47 core/build/security + 37 real Kivy tests passed (84). Exhaustive schedule
checks for all sizes 2–32 verify opponent coverage/uniqueness, one appearance
per round, reversed venues, equal totals, break limits per leg and across the
transition, no triples, and season bounds. Original legacy schedule snapshots
for 5/24 clubs match their previous hashes. Save regressions cover zero/one/two
completed rounds, preserved historical fixtures/stats, safe migration, new-season
switch, stable reload and invalid-version rollback. Kivy verifies the same
fixture in the calendar, main menu and actual match launch.

The first UI integration check inherited a tiny viewport where the dashboard
intentionally hides the team summary. Set an explicit 960×540 test viewport
and restore it afterwards; the actual layout behaviour was retained.

Files: career.py, buildozer.spec, tests/test_career.py, ui_tests/test_menus.py,
AGENTS.md, README.md and documentation. Immutable baseline preserved. APK
compilation and static checks are recorded in BUILD_LOG.

Next: update without uninstalling and check the league calendar in a new or
compatible season. The complete in-progress legacy season may remain unchanged
as explained above. Physical validation of this beta remains pending; no AAB
or store release signing in this step.
