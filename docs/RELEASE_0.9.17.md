# Scorer World0.9.17 — responsive heading and navigation fixes

World DEBUG QA upgrade. Install over the existing World QA and Load Game.
Same package, saves and DEBUG upgrade certificate; public1.0 remains separate.

A native layout audit exercised27 app views in11 configurations, across
Portuguese, German and Japanese:891 cases. Resolutions/densities represent16:9,
18.5:9,19.5:9,20:9, a foldable, a compact viewport and the owner's1280×591 example.
One configuration also uses130% text scaling. Tests inspect viewport bounds,
minimum48dp touch dimensions, real font heights in non-shortened labels,
canvas-button bounds, and the newspaper/coach one-screen constraints. Scrollable
content is allowed off-screen inside its scroll container; deliberate ellipsis
in bounded table/name labels is not a text-overflow failure.

The0.9.16 audit flagged16 cases from two causes: fixed coach heading/style/form
heights could clip Noto CJK or enlarged font metrics, and enlarged German Back
actions could extend above the viewport. Coach header/status/error heights now
use actual font measurements. Non-hub navigation headers expand to their minimum
content height. Hub alignment, profile draft retention, one-screen feedback,
newspaper, opportunity mix, penalties, training and trophy rules are unchanged.

After these fixes, all891 audited cases have zero flagged findings. This is
measured desktop Kivy verification of the app's landscape layouts, not a claim
of testing891 physical devices or a guarantee for every possible resolution,
text setting, cutout/system inset or OS window mode. Android remains landscape;
physical-device validation is outstanding. The machine-readable report is
`docs/data/responsive_0.9.17.json`; reproduce with Kivy installed via
`python tools/audit_responsive.py --output /tmp/responsive.json`.

353 core +167 native Kivy tests pass (520 total). New regressions check actual
CJK/enlarged heading metrics and German Back bounds. The actual APK's compiled
changed source/all9catalogues match the reviewed input, with API36/min26, arm64,
the existing certificate,118ELF/ZIP16KB alignment and ad-free payload checks.
No production signing, Google Play submission or live server change was made.
