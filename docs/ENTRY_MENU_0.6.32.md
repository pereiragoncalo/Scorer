# Scorer Free 0.6.32 — post-splash menu

Owner requested removal of the Scorer World action from the entry screen.
EntryScreen now has only New Game, Load Game, Help, Privacy, Exit; New Game
fills its row. World retains Language. Free hub promotion and stadium boards
remain. No career, gameplay, SDK, payment or language behaviour changed.

Files: menu_ui.py, existing entry-menu assertion in ui_tests/test_menus.py,
buildozer.spec/tools/prepare_editions.py version0.6.32/code1026632, documentation.
No new test duplicates were added for this reversible UI change.

PASS122 core/security +65 actual Kivy=187 tests. Real Free arm64 debug APK
compiled. Actual APK package com.clemir.striker, launcher Scorer/original icon,
version/code, API36, same debug certificate and SDK checks PASS. Actual bundled
EntryScreen.__init__ bytecode has no SCORER WORLD button constant and retains all
five expected actions. Free has no language assets or Billing SDK; existing test
AdMob remains. ZIP16KB and all118 AArch64 ELF LOAD alignments >=16KB PASS.

[Artifact hash/size](ENTRY_MENU_0.6.32_artifact.json).
[Inspected desktop Kivy rendering](captures/free-entry-0632.png); not an Android
screenshot. Logs: /workspace/striker-runtime/entry-core.log, entry-ui.log,
build-0632-free.log. No physical Android test or public Play upload was performed.
World0.6.31 remains the latest World APK; source staging version is prepared for
future builds. Separate unrelated unfinished World WIP was preserved.

Next: install Free over0.6.31 and verify the entry menu and saved career on a phone.
