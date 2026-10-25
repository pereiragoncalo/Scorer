# SCORER 0.6.29 — Android QA APKs

Source: pereiragoncalo/Scorer main commit57c6e17.

- SCORER-Free-0.6.29.apk: English only, one division, existing Free career.
- SCORER-World-0.6.29.apk: separate career, nine offline UI languages:
  English, Portuguese (Portugal), Spanish, German, Italian, Korean, Japanese,
  Simplified Chinese, Vietnamese. Follows phone by default; manual Language
  selection on entry or Help. Names/editor IDs/careers are not translated.

Direct APK files, not ZIPs. Both can be installed together and update their
respective0.6.28 package with the same existing debug certificate; no uninstall
needed. Existing same-app legacy World files cannot automatically cross to the
separate World package. Never uninstall to solve an update problem without a
career backup.

179 tests passed (118 core/security+61 Kivy). Actual arm64 debug APK builds,
manifest/SDK/content/signature checks, ZIP16KB and118 ELF alignments perAPK pass.
These are test builds, not a production Play release. Phone testing is still
required. World competition fidelity remains in development; no purchase or
production ad activation. Free test ads do not earn money; World has no ad SDK.
See main docs/LANGUAGES_0.6.29.md and SHA256SUMS for evidence/checklist.
