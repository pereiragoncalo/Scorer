# Scorer World 0.9.11 — single-page news, coach portraits and World editor

World DEBUG QA update. Save and Exit, install over World QA and Load Game.
Existing careers, competitions, aliases and training progress are retained.
Public release remains1.0.

## Newspaper fits the screen

SCORER DAILY now uses a measured single-page layout without a ScrollView.
Wide screens place the illustration beside the article. Narrow screens place it
beside the headline and use the full remaining width for the report. Typography,
spacing and photo size adapt to the available area rather than cropping text or
adding ellipses. Back remains a48dp action.

The body uses the current factual article on larger screens and a concise
editorial edition when space is limited. Teams, result, competition and any
eligible personal highlight/negative run remain visible. Repeated score/margin
prose is removed in the tightest layouts; very long fixture names use a score-led
heading. Body type remains at least12sp in the tested layouts. Recorded goal
clocks and the existing rules for mentioning the player are preserved.

Phone tests include320×240, landscape/portrait sizes, all nine languages and
maximum-length club aliases, including CJK names, without hidden article lines.
These are host typography/layout checks, not physical Android screenshots.

## Coach at the desk

Requested meetings show one of ten original fictional coach portraits, seated
behind an office desk. The current appearance is saved and remains stable when
opening meetings or reloading. Signing for another club selects a different face,
including when the new club's initial hash would collide with the previous one.
Promotions/renames of the same club UID do not change the coach's portrait.

Legacy saves adopt an appearance without resetting career state. Optional stored
appearance data is bounded to a club UID and one of ten bundled portrait indices;
malformed data cannot request a file path or discard the career. Selection uses
no match RNG. Existing coach personalities and conditional meeting requests
remain unchanged. Photos are original unbranded illustrations, not real managers.

## Editor inside World

Names Editor is removed from the normal, compact and inherited Windows main
menus. Open **World > Names Editor > Import names file**. The action sits beside
World's country search; existing Edit Names access from a league remains.
Editor Back and Android Back/Escape return to World. Free cannot open the editor.
The names JSON files published for0.9.10 remain compatible; no ID/layout change.

## Validation

Core and native Kivy checks cover saved portraits, hash collisions, actual
transfers/reload, legacy/malformed data, single-page type measurement, readable
body text, unchanged conditional player mentions, stable photos, World-only editor
navigation and all supported languages. Final counts are in artifact evidence.

The actual APK is checked for API36/arm64, existing DEBUG upgrade certificate,
16KB ELF/ZIP alignment, exact compiled source and portrait/news/font bytes,
competition/save flows and ad-free publishing payload. No physical Android
validation, production signing, Play submission or live-server change is claimed.
