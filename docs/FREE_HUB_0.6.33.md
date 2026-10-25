# Scorer Free 0.6.33 — remove World main-menu action

Owner requested removal from Free's main menu as well as the earlier entry change.
menu_ui.py now adds the WORLD header action only for the World binary.
world_ui.py CompactHub no longer creates a SCORER WORLD action in Free; World
retains World Leagues. Remaining Free buttons fill the existing header/grid
without placeholders, scrolling or smaller touch areas. Offline pitch boards
still promote World. No career, simulation, SDK, payment or language change.

Existing ui_tests/test_menus.py responsive main-menu check now expects ten buttons
and rejects any WORLD button at all six tested density/size combinations. Existing
World/navigation and stadium-promotion tests are retained. Source version/profile
changes: buildozer.spec and tools/prepare_editions.py0.6.33/code1026633.

122 core/security +65 actual Kivy UI tests (187 total) and syntax checks. Actual
Free arm64 debug APK build and package/signature/icon/edition/native SDK/content
checks, ZIP16KB and118 AArch64 ELF alignment checks are recorded in
FREE_HUB_0.6.33_artifact.json. Actual compiled CompactHub has no SCORER WORLD
button constant; edition is fixed Free. The existing entry bytecode still contains
only the expected five entry actions, without a World promotion button.

Desktop Kivy rendering was inspected, not an Android device screenshot. Logs:
/workspace/striker-runtime/hub-core.log, hub-ui.log, build-0633-free.log.
World0.6.31 remains the latest World APK; no World rebuild was needed.
Separate unrelated unfinished World WIP in the checkout remains preserved.

Next: install Free over0.6.32, load its saved career and verify the header/main
buttons and pitch boards on a phone. No physical phone, production signing,
Play publication or production ad activation was performed here.

PASS all187 tests and actual APK checks above. [Inspected desktop render](captures/free-hub-0633.png).
