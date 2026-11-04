# Scorer World 0.9.12 — folded newspaper, original type and every goal

World DEBUG QA update. Save and Exit, install over World QA and Load Game.
Existing careers, aliases, coach portraits and match records remain compatible.
Public launch remains1.0.

## A newspaper inside a reading window

The reader now places a warm paper sheet on a dark backdrop. A folded reverse
half, layered shadows, paper grain, turned corner and crease give the sheet depth.
The illustration is embedded in the article: text flows beside it, below it and
then into the next column. It is no longer a detached permanent image column.
Headlines, print rules and column separation establish a newspaper hierarchy.

Two original typefaces are included: Scorer Press Display for the masthead and
headline, and Scorer Press Pixel for the retro game-style article. The fonts are
built from original hand-drawn5×7 glyph matrices, with Latin accent coverage.
Existing Noto fonts provide CJK/script fallback. Font source and OFL licence are
bundled/documented in SCORER_PRESS_FONTS.md.

Typical reports fit one sheet. The four-goal example was rendered at1280×591 with
density1.4 and fitted one page. Very small windows, maximum-length aliases or
exceptionally long reports use Previous/Next leaf controls, not scrolling or
text deletion. Text flow is checked to retain every non-whitespace character
across leaves; body size is at least12sp. Compact layouts remove a repeated lead
only when its teams/result/competition are already fully shown in the header.

## Every goal and a short match summary

Every recorded goal is reported, with its minute, club and running score.
Wording follows the actual score: opener, equaliser, pull-back, new lead,
regained lead or extended lead. A separate brief summary recognises a comeback,
a late equaliser, a scoreless/scoring draw, winning margin or penalty decision.
No scorers, quotes, possession or unrecorded match incidents are invented.

Older records without complete goal clocks still account for each team's total
and explicitly say the individual times were not recorded. They do not receive
fabricated timings/order. Shootout goals are distinguished from the match score.
The existing personal-mention rule remains: standout performance, or at least
three goalless appearances despite recorded chances. Ordinary players stay out
of the article. Five rotating match illustrations and saved portraits remain.

## Validation and preview

Core checks cover every running score in a3–1, comeback/late-equaliser summaries,
legacy missing-clock totals, original-font glyph coverage and the previous save/
competition invariants. Native tests cover flow conservation, picture embedding,
leaf turns, nine languages, maximum-length CJK aliases and the original phone
proportions. The preview is a real desktop Kivy render of an illustrative test
fixture inspired by the owner's example; it is not a physical Android screenshot
or a reconstruction of the owner's unrecorded middle goal minutes.

Actual APK checks cover API36/arm64, the existing DEBUG upgrade certificate,
16KB ELF/ZIP alignment, exact compiled source and new font bytes, saved portraits,
competition flows and ad-free publishing payload. No production signing,
Google Play submission or live-server change is included. Physical Android
validation remains outstanding.
