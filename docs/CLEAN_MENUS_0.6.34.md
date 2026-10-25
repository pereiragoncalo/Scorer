# Scorer 0.6.34 — remove small explanatory menu copy

Owner requested removal of the small phrases, including Google Ads references.
EntryScreen no longer renders the Free/test-ad or World/ad-free/editor tagline.
The normal panel is shorter and contains the logo and actions. Only real errors
get an entry status label. MainDashboard removes routine contract/training prose
from its footer and the redundant1 DIVISION annotation. It still names the league
and shows dates, scores, energy, morale and season statistics. Normal profile
helper copy and the duplicate training-ad footnote are removed. Training's optional
WATCH AD: +1 MORALE button still clearly identifies its action/reward.

Name/load/save errors remain visible, including a previously hidden corrupt-load
message. Error labels use14sp/accent colour where space permits. Dashboard hero
reinsertion now follows the identity widget, preserving order across compact
resizes after the footer is omitted. Privacy retains actual Google data-processing
and policy disclosures/consent access but removes SDK diagnostic status lines.
No SDK/ad request, gameplay, career/schema, country selection or payment change.
Help and field/statistic labels remain. Native ad labels and consent are untouched.

Changed: menu_ui.py; ui_tests/test_clean_menus.py; buildozer.spec and
 tools/prepare_editions.py0.6.34/code1026634; documentation.189 tests PASS:
122 core/security and67 actual Kivy interface. Two focused tests check absence of
normal boilerplate and continued visibility of name/load/save errors; existing
responsive/draft/locale/gameplay checks pass. Initial65 UI tests passed before
adding the two targeted regressions; the complete67-test run also passed.

Both real arm64 debug APKs compiled sequentially and passed package/version,
launcher icon/label, signature, bundled edition/UI bytecode, SDK/language/font
payload checks, ZIP16KB and118 AArch64 ELF alignments each. Exact hashes/sizes:
[CLEAN_MENUS_0.6.34_artifacts.json](CLEAN_MENUS_0.6.34_artifacts.json).
Both retain the existing debug certificate/private careers for upgrades.
No production signing, Play upload, ad activation or actual phone run claimed.

[Inspected desktop entry](captures/clean-entry-0634.png) and
[desktop main menu](captures/clean-hub-0634.png) are actual Kivy renders, not
Android screenshots. Logs: /workspace/striker-runtime/clean-ui-core.log,
clean-ui-final-tests.log, build-0634-free.log, build-0634-world.log.
Separate unfinished World work in the main checkout was preserved.

Next: install over the corresponding previous edition, verify clean entry/main/
profile/training layouts, then load/save a career on a real phone.
