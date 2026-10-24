# SCORER 0.6.17 — research and goal calibration

## Real-world reference
The FREE game uses one fictional division corresponding to an English fourth
level career. League Two is therefore the primary scoring reference; Premier
League figures are a comparison, not a universal target for all divisions.

| Competition | Season | Matches | Goals | Goals/match |
| --- | --- | ---: | ---: | ---: |
| League Two | 2022/23 | 552 | 1294 | 2.344 |
| League Two | 2023/24 | 552 | 1645 | 2.980 |
| League Two | 2024/25 | 552 | 1377 | 2.495 |
| **League Two pooled** | **3 seasons** | **1656** | **4316** | **2.606** |
| Premier League | 2022/23 | 380 | 1084 | 2.853 |
| Premier League | 2023/24 | 380 | 1246 | 3.279 |
| Premier League | 2024/25 | 380 | 1115 | 2.934 |

League Two pooled: 27.11% draws, 7.79% nil-nil, 12.92% with five or more goals.
Home/away split rounds to **1.43 / 1.18 goals per match**.

Historical shot data supplies a separate sanity check:

| Competition | Season | Goals | Shots | On target | Goals/shots |
| --- | --- | ---: | ---: | ---: | ---: |
| League Two | 2017/18 | 1458 | 12152 | 4711 | 12.00% |
| League Two | 2018/19 | 1409 | 12225 | 4662 | 11.53% |
| Premier League | 2017/18 | 1018 | 9290 | 3190 | 10.96% |
| Premier League | 2018/19 | 1072 | 9606 | 3309 | 11.16% |

League Two pooled: **11.76% goals per shot**, **30.59% goals per shot on target**.
These are team ratios, including penalties/own goals in score totals, not exact
non-penalty individual conversion probabilities. The shot seasons are older
than the results reference and must not be described as current-season data.
A selected highlight has different quality from the average of all shots:
forcing every clear chance or penalty to have an 11.76% conversion would be wrong.

## Sources and reproducibility
1. [openfootball/england](https://github.com/openfootball/england/tree/9ee7a0c351805c99cc334478a9bf04b7d0432fec),
   seasons 2022-23, 2023-24 and 2024-25, files `1-premierleague.txt` and
   `4-league2.txt`; CC0 public data. [League Two 2024/25 source](https://github.com/openfootball/england/blob/9ee7a0c351805c99cc334478a9bf04b7d0432fec/2024-25/4-league2.txt).
2. [Football-Data.co.uk historical CSV mirror](https://github.com/jokecamp/FootballData/tree/53a64a101e064879bade9458bdaf7a76662a7523/football-data.co.uk/england),
   `2017-2018` / `2018-2019`, `Premier.csv` / `League 2.csv`.
   [Column definitions and source attribution](https://github.com/jokecamp/FootballData/blob/53a64a101e064879bade9458bdaf7a76662a7523/football-data.co.uk/README.md).
   The direct provider URL returned HTTP 403 in this environment; these public
   archived copies were used instead. Recent result counts come from source 1.

`docs/data/real_football_reference.json` contains aggregates and SHA-256 hashes
for every input file. No real club/player packs or raw datasets are shipped.
`tools/analyse_football_data.py` reproduces the aggregates from local copies,
rejecting incomplete seasons (380/552 expected fixtures).

## Audit findings and implementation
- A direct tap previously produced almost perfectly repeatable shots at the
  corner. Against the old hard profile the fixed-corner experiment scored
  206/240 (85.8%); the easy profile scored 240/240. This was not measured by
  the earlier random-target benchmark and explains the human feedback.
- Match-only launch accuracy now depends on pressure, condition and power.
  Intent is selected by touch; a sampled launch error sets the physical ball
  trajectory once. Hard kicks use standard deviation 0.95 m horizontally and
  0.65 m vertically before condition/control adjustment; clear kicks use
  0.40/0.30 m, penalties 0.20/0.16 m. These parameters are game calibration
  choices, not directly measured values from the result CSVs. Misses occur by
  the ball crossing outside the goal; no post-shot outcome quota is imposed.
- Ordinary match kicks use 18–26 m/s horizontal speed rather than 24–35 m/s.
  The old 0.78 s flight limit was also corrected (up to 1.15 s) so long
  attempts are not artificially accelerated back above that nominal speed.
  Hard keepers react in 0.14–0.22 s and move more effectively before diving.
  Training retains its original launch accuracy/speed and three-shot workflow.
- Team scores use a 2.61 expected total split by strength/home advantage.
  Actual scores use Poisson sampling and have no hard cap. The player's team
  reserves the expected personal contribution (0.18 per hard highlight plus
  the extra clear-chance value to 0.51) before sampling teammate goals. These
  rates are rounded from the physical random-target benchmark, not real xG.
- NPC goals used to be shared uniformly over twelve scorers. Existing team
  goals now use persistent role weights 32/18/12/8/7/6/5/4/3/2/2/1; no extra
  rival goals are created. Role weights are an explicit modelling assumption,
  not a player-level result established by these aggregate sources. Full club
  names prevent players from different clubs with the same first word merging.
- A confirmed accounting bug allocated the player's league goals to NPCs too.
  NPC allocation now excludes them, and total scorer goals equal team goals
  in new league histories. Cup goals remain in career totals, but no longer
  enter the league scorer table. The UI uses the league counter rather than
  overwriting it with the all-competitions career counter.
- Opponent-dependent chance limits and the guaranteed trained participation
  remain. Older accumulated scores are retained: old saves lack enough detail
  to reconstruct every historic duplicate/cup attribution safely. Corrections
  apply going forward; a new career is not required.

## Validation
43 core/build/security + 36 real Kivy tests passed (79). New regressions verify
scorer-goal conservation, cup separation/save reload, role allocation/full-name
identity, empirical goal means/distribution, match goal-budget reservation home
and away, physical launch dispersion and untouched training. Previous tests
cover trained participation, difficulty, layouts, timing, persistence and input.

`docs/data/simulation_0.6.17.json` stores measured results. All tools use temporary
saves and seeded randomness; no user career is used. The baseline is source
commit `da3db00` (0.6.16), extracted into a separate temporary directory.

| Experiment | Before | After |
| --- | ---: | ---: |
| Simulated club goals/match, 100 seasons / 55200 fixtures | 2.720 | 2.620 |
| Simulated club games with 5+ goals | 13.97% | 12.58% |
| Mean leading scorer / season (fictional roles) | 13.82 | 29.31 |
| Hard shots at fixed corners, 240 samples | 85.8% | 30.0% |
| Clear shots at fixed corners, 240 samples | 100% | 48.3% |
| Complete playable games, instant-corner bot, 100 games | 3.64 goals/game | 2.81 goals/game |
| Same bot: personal goals / 100 games | 190 | 67 |
| Same bot: games with 5+ goals | 28% | 13% |

Random-target physical samples after: hard 44/240 (18.3%), clear 122/240 (50.8%).
Another 100 complete games with random on-goal target intent yielded 2.85
combined goals/game and 37 personal goals. These are small seeded bot samples,
not guarantees, statistical confidence intervals or Android/human testing.
The bot aims instantly, so it does not test shot-clock difficulty. The full
match tool runs actual training, planning, AI events, shot physics, half-time
and career progression, with domestic cup/call-ups disabled for league comparability.
Across-match sequences diverge between versions; they are controlled seeded
experiments, not fixture-for-fixture causal pairs.

Reproduce with the development Kivy interpreter:
- `python tools/calibrate_goals.py`
- `SDL_VIDEODRIVER=offscreen python tools/balance_shots.py --samples 240 --strategy corners`
- `SDL_VIDEODRIVER=offscreen python tools/calibrate_playable.py --matches 100 --strategy corners`

## Release and next task
Changed career.py, main.py, menu_ui.py, buildozer.spec, tests/test_career.py,
ui_tests/test_menus.py, tools/balance_shots.py, three new research/calibration
tools, AGENTS.md, README.md and this report/data. Baseline and save format v2
preserved. No menu geometry or artwork changes. APK evidence is in BUILD_LOG.

Update without uninstalling and play several matches against varied opponents.
Confirm aiming feels fair and compare goal frequency over a meaningful sample.
Physical phone testing is still pending; this is a beta, not a proven universal
realism model. FREE is calibrated to League Two; other worldwide league scoring
regimes have not been individually researched/calibrated. No AAB or store
release signing in this step.
