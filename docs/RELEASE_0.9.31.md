# Scorer World0.9.31 — all involved standings and contextual help

World Standings now opens a competition selector from the raised title button.
It includes the current league, current club cups and promotion playoffs, observed
current-season leagues/cups at former clubs, and national competitions when the
player is eligible, called up or has participated. Eliminated competitions remain
available for that season. Group tables open on the player's team; the group
button cycles groups. Fixtures switches to dated results. Knockout rounds show
real drawn fixtures and penalties rather than invented league points. All rows
remain accessible through pages; browsing does not advance cups or consume RNG.
Club/league aliases and the existing promotion zone/rules display remain intact.

Help is now specific to its screen, opening over that screen instead of navigating
to a global manual. Buttons cover normal menus, notices, player, club, training,
confidence, standings, records, calendar, World/editor, newspaper, coach and match/
shot screens. Splash artwork is unchanged. Training owns focus/XP and finishing
criteria guidance; confidence owns trust/role guidance; player owns objectives.
New paragraphs are translated into all nine languages and justified. Settings and
Language remain accessible from the entry/hub help panel. Help closes with Close
or Android Back, preserves drafts and does not acknowledge a mandatory meeting,
skip the newspaper or grant training completion. While open, elapsed time, ball,
shot countdown, match flow, shooting and keyboard shortcuts are paused. The actual
help touch works with the opportunity notice visible. Narrow scoreboards reserve
space for the game help button; wide displays retain the existing280dp width.

No physics, scoring, competition formats, save schema, analytics, server or
monetization change. Root badge/mode-state/menu-test WIP is excluded from staging.
QA0.9.31/code1026931 keeps the package and existing debug upgrade certificate,
arm64, API36/min26, no ads/IAP; public1.0 is unchanged. Physical Android acceptance
is pending; this is not a Play submission.

Validation:400 core cases completed,3 skipped; all7 focused new native cases and
8 language regressions pass.297 responsive menu cases across11 pixel/density/font
profiles and English/German/Japanese have zero findings. League/selector/help
screenshots were visually inspected. Stale old-global-help/notice/group expectations
were updated; the final full209-case native rerun passed. Android signature,
ZIP16KB, all118 ELF alignments,208 sprites/30 sheets, exact compiled main/UI/new
help/standings modules, ad-free/edition/safety/save checks and actual APK read-only
competition membership pass. Final native evidence is recorded in BUILD_LOG.md.

[Download APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.31/Scorer-World-0.9.31.apk).
