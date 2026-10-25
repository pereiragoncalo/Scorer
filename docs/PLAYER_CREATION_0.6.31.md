# SCORER 0.6.31 — World nationality and starting country

The owner requested all three choices on the new World player-name screen.
Name, nationality and starting country appear together; nationality and start
country initially use the existing phone-country suggestion but can be changed
independently. Selecting a UI language does not change these values. Nationality
is stored as the canonical country identifier for the player. The starting country
selects its lowest active division (England4) and generates first contracts there.
This change does not implement or certify national-team/continental simulation.

Country pickers search both canonical English names and localized country labels,
with bounded pages (two choices on short displays, six on taller displays), no
scroll list. Cancel closes the picker without applying a country; selecting a
country changes only the form draft. Draft name/choices survive validation errors,
redraws and rotation within the current session. On Android resume an open picker
closes before locale refresh, preserving the form draft and editable name.

Continue validates all choices before changing career fields or consuming offer
randomness. The existing first-contract acceptance saves nationality and league
through the existing career schema. As before, an uncontracted creation is not a
saved playable career; killing the app before accepting a club does not save the
form draft. No background upload or new storage/permission is introduced. Free
keeps its English name-only setup, while established World profiles can change
the name only. Existing nationality, stats, league and club are preserved.

Files: career.py guarded configure_new_player, main.py creation/draft routing and
resume cleanup, menu_ui.py compact fields and paged country popup, nine message
catalogues (218 messages each), tests/test_player_creation.py and
ui_tests/test_player_creation.py, buildozer.spec/tools/prepare_editions.py version
0.6.31/code1026631, documentation. Unrelated unfinished World tournaments and
badge-removal work in the main checkout remain preserved outside this release.

Validation:122 core/security tests +65 actual Kivy UI tests =187 PASS. Tests cover
independent Brazil nationality/Japan or Mexico start, localized search returning
canonical IDs, England4, reload after first contract, invalid/tampered inputs,
Free/established-career rejection, rollback on mocked save failure, previous-save
preservation, draft/error/cancel handling and responsive touch controls at
1280x640,640x360,360x640 with density1.6. Nine catalogues preserve placeholders
and pass used-glyph coverage. A Portuguese desktop Kivy render was inspected;
this is not an Android device screenshot. Initial tests exposed a missing World
form game reference and an incorrect test assumption about pre-contract saves;
these were corrected before the final passing checks.

Logs: /workspace/striker-runtime/player-core-final2.log, player-ui-final.log,
player-catalogue-final.log. Actual sequential arm64 debug build logs:
build-0631-world.log and build-0631-free.log. Actual package/signature/icon/language
and native SDK checks plus ZIP16KB/118 ELF alignment results are recorded in
PLAYER_CREATION_0.6.31_artifacts.json. Existing packages and debug certificate
are retained for updates; launcher names/icons stay Scorer and Scorer World.

Next phone checks: install World over0.6.30; start a NEW World career, search and
select nationality/start country, type an accented name, rotate and background the
app, confirm contracts come from the selected country, accept one and save/reload.
Verify an existing career is unchanged and Free still has name-only creation.
No physical Android test, production signing, Play publication, live payments or
ad activation was performed.

Both real APKs PASS actual version/package/launcher art/signature checks,
Python3.14 bundled edition evaluation, actual configure_new_player/PlayerCountryPicker
bytecode presence, language/font/SDK checks, ZIP16KB and118 ELF alignments each.
World carries218 messages per language; Free has no extra language assets.
The merged main checkout with preserved unrelated WIP also passes122 core and65
Kivy tests (187). No physical device run was performed.

[Inspected Portuguese desktop Kivy form](captures/world-player-0631.png).
