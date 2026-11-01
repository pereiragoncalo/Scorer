# Competitive difficulty — Scorer World 0.6.48

The owner requested that maintaining more than one goal per match should be difficult, including the lowest division. This update strengthens physical defending and adds an explicit progression from tier 5 or lower to tier 1. Existing careers, imported aliases and results remain usable.

## Gameplay

Goalkeepers now read both the height and direction of a shot. Low saves lower the gloves towards the ball; high saves jump far enough to contest the upper goal. Rendering and collisions use the same pose and unchanged body volumes. The old fixed high-corner target scored on all 160 seeded trials in both easy and hard chances; that permanent opening has been removed.

Keeper reactions, reading accuracy, footwork, acceleration, dive timing and jumping improve with each promotion. Match difficulty follows the opponent's division, including cross-division cup fixtures; international matches use the top profile. Footwork has bounded speed/acceleration and a committed dive cannot track a new direction in the air. Defenders mark a central and far-side lane before the player chooses a target; the top two divisions use five defenders instead of four. Lane coverage is tighter at higher levels.

The existing timers and aim progression remain. Weekly training, morale benefits and the two/three-opportunity floors remain. A strong performance can still produce several goals: there is no score quota, one-goal cap, dependence on recent goal totals or hidden target spread. Ball launch physics, goal/post geometry, physical collisions and training behaviour remain unchanged. Other goals in the match still use the existing simulation.

## Measured reference, not a human prediction

`tools/calibrate_difficulty.py` executes real fixed-step shot/keeper/defender collisions: 160 seeded samples for each combination of five tiers, easy/hard chance and four target strategies. Both versions use matching seed sets: 6,400 physical shots before and 6,400 after. Target strategies cover the goal area, fixed upper corners, fixed low corners and varied near-corner placements. Every shot resolved.

`tools/project_scoring_seasons.py` then samples independent outcomes from those measured conversion rates over 2,000 synthetic 38-match seasons per tier/strategy. It assumes maximum stamina/morale, completed training with three training goals, three opportunities every match, exact selected targets and no timeouts. Opponent ratings vary around the game's tier centres; no table/form progression is simulated. These are deliberately favourable conditions, not actual played careers or observed human conversion. The numbers are calibration evidence, not an enforced average or guarantee.

For uniformly distributed exact targets inside the goal:

| Division | Previous projected goals/match | New projected goals/match | New seasons above 1 goal/match |
| --- | ---: | ---: | ---: |
| 5 | 1.27 | 0.88 | 14.25% |
| 4 | 1.24 | 0.70 | 0.45% |
| 3 | 1.21 | 0.57 | 0.00% |
| 2 | 1.19 | 0.40 | 0.00% |
| 1 | 1.18 | 0.37 | 0.00% |

The raw physical outcomes and all four projected strategies are in [difficulty_0.6.48.json](difficulty_0.6.48.json). Players can choose other targets, power and timing, so real device/player feedback remains important.

## Delivery and validation

World-only Android candidate: version 0.6.48, versionCode 1026648, same package and existing QA signing certificate. Save and Exit, install over the existing matching World QA APK, then Load Game. This balance update needs no additional server change or name-pack reimport. The debug APK is a test build, not a production-signed Play artifact.

Core and Kivy checks cover the promotion curve, opponent-tier selection, pre-shot marking independent of aim, shared visible hand/collision position, high/low poses, and identical launch velocities across tiers and recent goal totals. Existing save, privacy, career and geometry checks also run. Physical captures were inspected on native Kivy; a physical Android handset was not available in this cloud session.
