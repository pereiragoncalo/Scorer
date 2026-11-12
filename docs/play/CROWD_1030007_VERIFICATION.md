# Verification — 12 November 2026

Source a27f0b55d17a0740d082a09226e5752f5edd2958. Supporter sprites scale25%larger
at all projected distances (.72→.90, floor4→5, cap31→38.75); aspect/feet unchanged.
Only stadium_scene.py and release metadata change runtime behavior. Approved PNG
assets, player/keeper scales, camera, physics and seating logic untouched.

18native club-stadium/celebration/retro-sprite tests pass. Actual staged-production
same-camera before/after screenshots inspected: bigger seated supporters, stable
player size and team allocation. Training crowd remains hidden. No new test that
merely duplicates the size constants was introduced.

AAB117222875bytes, SHA256
a4d031bfaec599df76fb56e7a458be3af76f14cde453a261974f2f7cae26ac6d.
Numeric1030007/name1.0/World/production. bundletool/118ELF/16KiBZIP checks pass;
packaged1030007and new crowd height constants independently inspected using the
matching Python interpreter. Original remains unsigned; inspection APK uses only
a disposable/public debug inspection key.

Successful public delivery actions:
https://github.com/pereiragoncalo/Scorer/actions/runs/43218076750
https://github.com/pereiragoncalo/Scorer/actions/runs/43218082506
Publisher fixture suite runs24tests, including JDK fixtures in CI and actual AAB
digest locally. Anonymous full AAB/coordinator/signing-helper/publisher downloads
matched local bytes and SHA256. Temporary transfer ref removed after checks.

Uploader1.5 now prints the exact minimum/latest activation command following
successful or idempotent publish, explicitly AFTER confirmed Play availability.
No live minimum changed, backend deployed, Play API invoked, private credential
received or actual-device success claimed in this cloud task. Owner must run
CROWD_1030007.md commands and validate on phone. Includes all prior1030006fixes.
