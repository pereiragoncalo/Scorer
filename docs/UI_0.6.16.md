# SCORER 0.6.16 — no empty matches after mandatory training

## Problem and fix
The opponent-dependent generator could round down to zero even after the
mandatory training session. Training goals previously affected opportunities
only indirectly through energy and morale. A new career could therefore finish
two perfect sessions and receive no playable highlights in its first matches.

A completed weekly session now guarantees at least one opportunity. Current
session goals add 0.15 each to the expected count (maximum bonus 0.45), within
the existing opponent cap. Very strong opponents still allow exactly one,
always difficult. Other opponents allow one to two/three after training.
There is still at most one clear chance and no guaranteed goal.

The bonus uses persisted current-week training goals, not career totals or
previous weeks. Older completed sessions without those counters receive the
one-chance floor. Training goals are not added to league scorer statistics.
No save format, physics, opponent-rating/ranking rules or UI layout change.

## Files and validation
career.py, buildozer.spec, tests/test_career.py, ui_tests/test_menus.py, AGENTS.md,
README.md and documentation. Original baseline and existing progress retained.
New regression tests replay a new career's first two weeks, scoring 3/3 in each
training and checking that each match actually opens a shot opportunity. Core
tests check 500 draws per opponent strength after completed/reloaded training,
legacy completion, elite limits and the effect of training goals on extras.
Test totals and actual APK checks are recorded in BUILD_LOG.

Next: update without uninstalling and continue the current career. Confirm
participation in the next matches after training. Physical validation of this
beta remains pending. No AAB or store release signing in this step.
