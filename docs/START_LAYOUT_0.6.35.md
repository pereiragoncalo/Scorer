# Scorer 0.6.35 — new-career confirmation / menu logo

The owner supplied an oversized Android confirmation screenshot with an entry
banner overlapping its buttons. The new CareerStartDialog is a themed ModalView:
its wrapped heading, paragraph, padding and fixed action row determine its height;
width is at most520dp and both dimensions remain bounded by the Window. It has
an opaque rounded panel to prevent underlying controls bleeding through, with
existing localized backup explanation and explicit Cancel / New Game controls.
No new wording or translation API is needed. Backup is still required before
replacing the current career; failure and Cancel leave its save unchanged.

EntryScreen places its logo at the screen top left, separately from the central
compact actions. Its header/footer reservation avoids logo/buttons/native-banner
overlap; compact controls use48dp (normal52dp), never smaller. The existing layout
regression now applies the actual48dp entry minimum while retaining52dp elsewhere.

Shared MenuLogo renders the original unedited assets/menu_logo.png, aligned left,
with native gold WORLD in bundled Barlow Condensed ExtraBold Italic for World
only. It appears in entry, normal hub and compact hub; no extra image asset or
font dependency was generated. World is product branding and is never translated.
Launcher icons/names, splash credits, private saves and existing languages remain.

Entry ads are explicitly hidden before opening the new-career and exit modals.
Entry layout also checks both modal references, so rotation cannot re-show them.
Cancel restores a banner only in entry when screen space permits. Successful
confirmation changes to profile before dismissal, avoiding transient restoration.
This adds no ad placements, SDK, payment, Internet permission or production ad IDs.

Files: main.py, menu_ui.py, world_ui.py; focused ui_tests/test_start_dialog.py;
updated entry minimum in ui_tests/test_menus.py; buildozer.spec and
 tools/prepare_editions.py0.6.35/code1026635; docs.193 tests PASS:122 core/security
and71 actual Kivy. Four new tests cover compact content/rotation bounds, banner
suppression/cancel/confirmation/backup failure, top-left Free/World branding and
wrapped German confirmation. A final four-test run passed after making the panel
opaque. Existing data, language, gameplay and responsive tests pass.

The initial UI suite had one older52dp-only entry assertion; it was updated to
reflect the existing project48dp minimum for compact entry controls. An initial
visual check found background controls faintly showing through; the final panel
is opaque and re-rendered. Native Free was rebuilt after that final style change.

[Final desktop Free confirmation](captures/free-confirm-0635.png) and
[World entry/logo](captures/world-entry-0635.png) are actual Kivy renders, not
Android device screenshots. Test logs: /workspace/striker-runtime/layout-core.log,
layout-ui-final.log, layout-ui-focused-final.log. Real sequential arm64 debug
builds: build-0635-free-final.log and build-0635-world.log. Exact APK evidence:
START_LAYOUT_0.6.35_artifacts.json. No physical phone run or Play upload claimed.
Separate unfinished World WIP in the main checkout remains preserved.

Next phone checks: install each APK over its previous edition; verify top-left
logo/World word, open New Game with an existing career, rotate, cancel and check
its save; reopen and confirm a backed-up new career. Confirm the native banner
never covers the modal, and returns only after cancellation to entry.

Both final APKs PASS actual package/version/icon/signature/edition, bundled
CareerStartDialog/MenuLogo/main modal ad guard and opaque-panel keyword checks,
language/font/SDK payload checks, ZIP16KB and118 ELF LOAD alignments each. The
merged main checkout with unrelated WIP also passes122 core and71 Kivy tests.
No physical Android test was performed.
