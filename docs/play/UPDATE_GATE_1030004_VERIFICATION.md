# Verification record — 2026-11-11

Runtime source commit: bb84b18. Delivery branch: codex/world-update-gate.
Unsigned AAB SHA256: d1468ce2b32cfcdec415f87c665ddc253b8d34474e27cef3ec8761d904cd9828
Size: 117218890 bytes. Package com.clemir.scorerworld, numeric code1030004,
name1.0, production/World, API26..36, arm64-v8a. Compiled code1030004 and
app_updates/version_policy/update_ui modules independently inspected using the
packaged Python version. bundletool,118ELF and16KiBZIP checks passed.

Core tests:25passed. Native Kivy update/creation suite:8passed, plus targeted
store-button native tests after adding market URI fallback. Public publisher
CI runs all portable fixture tests including disposable JDK signature validation.

Delivery runs (both successful):
- https://github.com/pereiragoncalo/Scorer/actions/runs/43028838929
- https://github.com/pereiragoncalo/Scorer/actions/runs/43028843842

Anonymous complete downloads of AAB, coordinator, backend installer, signing
helper and publisher matched local SHA256 and byte counts. Temporary transfer
reference removed after those checks. Canonical GitHub Pages privacy disclosure
updated at ebf21fa, deployment43028373365passed; live HTTPS text verified.

Owner signing, backend deployment, Google internal commit, actual Android Play
update-button behavior and offline device smoke remain pending owner execution.
No private credential/key received. No minimum raised for live clients here.
