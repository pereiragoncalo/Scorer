# Scorer World 0.9.14 — goal headlines, wide aim and training before every match

World DEBUG QA update; public launch remains1.0. Install over World QA and load
the existing career. Package/save identity and upgrade certificate are unchanged.

Every recorded personal goal now earns a player-name headline and a personal
paragraph, including a single goal in a draw or defeat. The short edition follows
the same rule. A normal goal is described as a goal, not automatically called
crucial. Older saved reports with recorded personal goals also receive this
highlight; older history without personal evidence still receives none. The
three-game negative-run rule for scoreless performances stays in place.

The horizontal aim follows a complete smooth sweep from one flank to the other,
with amplitude goal-half-width+0.40m and a safety bound half-width+0.45m. It reaches
both posts and slightly outside, rather than the previous weighted waves often
cancelling near the goalkeeper. The vertical target stays within the goal's
ball-clearance limits. Outside-post shots can miss physically; keeper proportions,
ball physics and the0.9.13 timing/difficulty improvements are retained.

Training is now required before EACH match, including club, cup/playoff and
national appearances in the same calendar week. The previous gate only checked
the week, so World fixtures could reuse an earlier session. All completed-match
paths now consume the session before saving, making the next Play action locked.
A session is credited only after three persisted shots. Rewards use persisted
goals, never the caller's supplied score. Partial sessions resume normally and
save failures cannot duplicate rewards. Menu copy describes per-match practice.

Upgrade note: completed training from saves without the new gate version is
invalidated once, since the old completion could already have been reused for a
World fixture. That first next match requires a fresh session. Partial training,
career stats, aliases, standings and history remain intact. New completed
sessions persist and reload normally. Repeated practice stays blocked until a
match is completed; the calendar still advances only through its existing rules.

Validation:345 core and154 native Kivy tests. Regressions cover both goal/post
edges across28,800 aim positions, every-goal headlines/body/short edition,
three-shot completion and authoritative rewards, same-week club/national matches,
reload, migration and the actual Play action throughout partial training.
The Portuguese preview is an actual desktop Kivy render of an illustrative3–1
with one recorded personal goal, at1280×591/density1.4, fitting one paper leaf.
It is not a physical Android screenshot or a real-match reconstruction.

Actual APK checks include exact compiled source/data, package/API36/arm64,
existing DEBUG upgrade certificate,118 aligned ELF files/16KB ZIP alignment,
competition persistence and ad-free rehearsal publishing payload. The compiled
smoke test exercises the three-shot gate, same-week national consumption/reload
and personal headline after defeat. No physical-device testing, production
signing, Google Play upload or live-server changes were performed.
