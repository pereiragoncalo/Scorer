# SCORER 0.6.31 — Android QA APKs

Source: pereiragoncalo/Scorer main commit4846ad9.

NEW in World: player creation asks for name, nationality and starting country.
Independent nationality and country choices, offline localized search and paged
country lists. Continue shows contracts from the selected country; England starts
in Division4. The first accepted contract saves the choices with the career.
Existing World profiles and Free keep name-only editing. Gameplay is unchanged.

Install BOTH APKs for two launcher entries:
Scorer (original S icon) and Scorer World (blue globe/WORLD icon).
These update the corresponding0.6.30 installation without uninstalling.
Each keeps its own private career. Some launchers require dragging apps from
its app drawer to the home screen; no physical launcher test was performed.

- SCORER-Free-0.6.31.apk: English only, one division, existing Free career.
- SCORER-World-0.6.31.apk: separate career, nine offline UI languages:
  English, Portuguese (Portugal), Spanish, German, Italian, Korean, Japanese,
  Simplified Chinese, Vietnamese. Follows phone by default; manual Language
  selection on entry or Help. Names/editor IDs/careers are not translated.

Direct APK files, not ZIPs. Both can be installed together and update their
respective0.6.30 package with the same existing debug certificate; no uninstall
needed. Existing same-app legacy World files cannot automatically cross to the
separate World package. Never uninstall to solve an update problem without a
career backup.

187 tests passed (122 core/security+65 Kivy). Actual arm64 debug APK builds,
manifest/SDK/content/signature checks, ZIP16KB and118 ELF alignments perAPK pass.
These are test builds, not a production Play release. Phone testing is still
required. World competition fidelity remains in development; no purchase or
production ad activation. Free test ads do not earn money; World has no ad SDK.
See main docs/PLAYER_CREATION_0.6.31.md and SHA256SUMS for evidence/checklist.
