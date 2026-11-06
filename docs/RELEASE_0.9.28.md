# Scorer World 0.9.28 — visitor sectors, stewards and player scale

Supporter banners have been removed. Club shirt colours are mixed per seat with
stable non-periodic randomness, without consuming gameplay randomness or changing
colours during redraws. Home/away colours and scoring-side celebrations remain.

The visitor club's own ground capacity now determines the lower-deck allocation.
The visual model uses up to 20,000 seats for a corner-only sector; larger visitor
clubs also occupy the next behind-goal bay, stopping at its first staircase.
This is a game presentation rule, not a claim about real ticket allocations. The
home club still determines the actual stadium size/tiers; no club facts changed.
Upper-tier spectators and the rest of the ground wear home colours.

Two files of fluorescent-green stewards line EACH flanking staircase, following
the lower-deck steps. Their stair lanes are clear of spectators. Stewards use a
separate cached mesh and never jump for goals. Training has no fans or stewards.

All outfield roles and goalkeeper now use a 1.80 m upright reference projected at
their own world position, relative to the unchanged 2.44 m goal. The transparent
sprite canvas and old .72/.76/.80 physics multipliers no longer shrink the art.
Upright ink calibration is 40 pixels for outfield players and 39 for the keeper;
crouching/jumping/diving poses retain natural height changes. Approved sprite
PNGs are unchanged. Existing low 1.31 m headers use the approved crouched contact
pose instead of jumping above the ball; ball launch remains immediate.

Only rendering/animation selection changed: movement, camera, ball flight,
collision volumes, goalkeeper skeleton, scoring, controls, training gates and
saves retain their existing behaviour. The actual physical hitboxes were not
resized to the sprite rectangles. Android texture recovery from0.9.27 remains.

Validation: broad coverage included 387 core cases (3 skipped) and 197 real Kivy
cases. Two obsolete assertions failed initially: the rehearsal version was pinned
to0.9.25, and a sprite test still expected the old high-header frame. Corrected
the version assertion to use the authoritative release configuration and the
header assertion to use the low-ball contact contract. All 6 edition cases and
all 4 sprite integration cases then passed in focused reruns. All 10 stadium/club/
celebration cases and 4 asset/clock/articulation/calibration cases passed. Syntax
checks and the exact Android staging-resource guard passed. No production code
changed for those two test fixes.

The report images compare synthetic visitor capacities 5000/60000 in the same
70000-seat host ground; they do not replace real club data. The height image adds
a test-only upright actor/ruler beside the actual goal. This calibration actor
is not added to gameplay. Actual training and low-header scenes were inspected.

The built World DEBUG QA APK uses 1026928, API36/min26, arm64 and the existing
upgrade certificate. Actual compiled rendering/stadium/layout/runtime source,
approved 168 frames/24 sheets and manifest match exactly. ZIP16KB and all 118 ELF
alignment checks pass, as do existing edition/ad-free/safety/competition/save
checks. The build input commit precedes the release source by only the two
excluded test fixes; both commits are recorded in the artifact metadata.
Physical Android installation/playtesting remains pending. No Play submission,
production1.0, gameplay-balance, server or save-schema change.
