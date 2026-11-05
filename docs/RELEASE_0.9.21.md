# Scorer World 0.9.21 — compact player and training screens

World DEBUG QA upgrade; install over the previous World QA and Load Game.
Same package, upgrade certificate, careers and saved progression. Public1.0 unchanged.

Training displays the selected skill, shots/goals, level/XP, energy/morale and
session controls. Its focus picker contains the four skill values and selection
buttons. It opens only within Training; the player and confidence views no longer
contain focus controls or training explanations.

The player screen directly shows season/career objectives in one outer panel,
with name/save/cancel controls preserved. The two plain goal columns align at the
top. Explanatory paragraphs, the development tabs/link and the trophy presentation
were removed from this view as requested; existing trophy and career data remain
saved. Detailed goal information is now in Help.

Coach Trust shows current trust, status, expected minutes and the last appearance/
trust change. Tap the existing green trust value on the regular hub to open it;
compact hubs provide a Coach Trust action. This adds no new normal-hub button row.

Help now has twelve reachable pages, including the existing translated XP/focus,
skill-effect, role/minute, confidence-change and objective explanations. Paragraphs
remain justified in all nine languages; page clamping and the counter use the
actual edition's page count. The first four help pages retain their prior order.

No shot, training-reward, confidence, goal, save-schema, collection or server
behaviour was changed. The animated opportunity/reception flow remains intact.

Validation:30 focused edition/localisation/progression tests passed. The full
native suite ran178 cases; old assertions about a four-page Help boundary and
compact-menu action counts were updated, and the nine affected tests passed on
rerun. Native coverage includes objectives-only player content, one outer panel,
retained names/trophies/data, value-only training/trust, real touch navigation,
training-only focus selection/locking, unchanged XP and actual drills, all moved
Help content, justified paragraphs and reachable last-page navigation.

The targeted layout matrix checks profile/training/confidence/help/hub across11
size/density/font configurations and Portuguese/German/Japanese:165 cases, zero
findings after the final text/column layout adjustment. Representative English
player, training, confidence, focus-picker and Help screens were inspected.
Development details and objectives may scroll inside their existing panel on tiny
viewports; normal landscape player objectives share one panel.

Actual APK checks passed for exact compiled source/data, focused XP persistence,
role logic, competition/save/edition/publishing smokes, existing DEBUG certificate,
API36/arm64 and16KB ELF/ZIP alignment. Physical Android installation/playtesting
remains pending; this is QA, not Play production approval.
