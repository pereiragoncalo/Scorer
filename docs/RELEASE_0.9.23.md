# Scorer World 0.9.23 — clearer chances, onside runs and wide deliveries

Removed expected playing time from match notices. Opportunity panels now show a
compact heading, move and context, without repeated introductions. Actual font
metrics fit the translated text below the scoreboard; the wider action stays
reachable. Synchronous first layout prevents an empty/clipped initial viewport.
Shot footer and result messages have explicit viewport width bounds.

Through balls include an opposing defender ahead of the receiver when the pass
is played: together with the goalkeeper, he keeps the runner onside. The defender
is beaten during the build-up and remains behind the receiver at the finish,
leaving only the goalkeeper ahead. Training and penalties retain their isolation.
This provides legal visual positioning; it does not add a general offside referee.

Added deep crosses from the wing (25m wide, 20–26m from the goal line) and corners
from the pitch corner arc. Both show a high animated delivery followed by header
reception. Seven ordinary moves share the existing capped slots; through balls
and penalties keep their reserved slots. No extra attempts or forced goals.
Delivery orientation considers both the passer and receiver's screen positions.

Newspaper photographs have no Illustration caption or reserved caption band.
The story flows beside the photo and expands across the column below it, retaining
all recorded goal minutes, player highlights, match summary and one-page fallback.

Existing careers, training progress, physics, scoring budgets, names, upgrade
package and DEBUG certificate remain compatible. Public 1.0 is unchanged. This
is a World QA upgrade; physical Android installation/playtesting remains pending.

Validation: 375 core tests passed. The full native suite ran182 cases;181 passed
and one old allowlist still expected only five ordinary moves. Added the two new
move types and their minimum header distances to that test; its full60-fixture
rerun passed. Native coverage includes144 notice combinations (four screen/font
profiles × nine languages × four move types with decisive-match context), legal
release/trailing defender positions, unchanged training/penalties, complete photo
wrap and all recorded story text. No runtime changes followed these checks.

The expanded29-view layout matrix passed957 cases across11 resolution/density/
font profiles and Portuguese/German/Japanese, with zero findings. Actual1280x591
notice, release defender, deep cross, corner and newspaper previews were inspected.
Actual APK source/data/artwork checks, competition/progression/save/safety smokes,
API36/arm64, existing DEBUG upgrade certificate and118 ELF/ZIP16KB checks passed.
