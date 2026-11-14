# Scorer World 1.0 (1030024)

Goal-net contact now sweeps both the moving ball and the deforming sheet.
Normals keep their outward orientation; endpoint recovery uses the nearest
actual finite sheet after rope constraints. This closes moving/folding-panel
escapes without an invisible fixed goal box. Legal goal presentation begins at
the exact goal-line crossing and advances the remaining step, preventing fast
oblique entries from starting beyond a side panel. Passive energy and glancing
side travel remain covered by regression tests.

When retrieving a goal while losing, the player follows the actual presentation
ball, waits for it to stop and reaches its resting position before completing
pickup. The ball is hidden/carried only once secured, and the cloth then releases
its occupied pocket. No fixed entry-point target or2.6-second hide timer.

One nearest opponent closes the athlete during buildup, aiming and shot, using
the same world position for rendering and collisions. Other opponents retain
the cohesive block. Penalties and free-kick walls before the kick remain legal;
existing physical collisions decide blocks, without an automatic scripted miss.

The original60-case sweep reproduced13 escapes before and zero envelope escapes
after the correction. Eight exact historical cases cover containment and passive
energy.22 broad pure tests plus focused moving-sheet/final nine checks pass;
38 broad native Kivy checks plus final five focused checks and retrieval priority
pass. The same package, career/save format and upload certificate are retained.
Physical Android acceptance remains owner-side. No backend patch is needed.

Keep1030022 as the known available minimum while Play distributes1030024; never
require the new version before it is offered to every intended player/track.
Update through Play without uninstalling or clearing data.

Download: https://github.com/pereiragoncalo/Scorer/releases/tag/world-1.0-1030024
Commands: docs/play/FIXES_1030024.md
