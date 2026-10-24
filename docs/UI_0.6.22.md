# SCORER 0.6.22 — native AdMob TEST integration

User now requires network advertising revenue and confirms no AdMob account yet,
with a general audience including minors. The old no-AdMob restriction is superseded
by that request. Implemented the real native SDK bridge, not a fake ad overlay.

See [account setup, privacy, limits and remaining activation](ADMOB_SETUP.md).
Includes a 320x50 dp test banner on the entry menu after touching the splash.
A separate 64 dp footer prevents button overlap; tiny screens suppress the banner.
It is removed on navigation; splash and gameplay remain ad-free.
Only official test IDs are compiled in. No revenue or live ad serving is claimed.

## Validation

56 core/build/security tests and 41 actual Kivy tests pass (97 total). Ad-break
tests cover cooldown, frequency, duplicate completion, failures, no late showing,
no startup fullscreen, banner visibility transitions, desktop no-op and SDK exception isolation. Kivy tests verify final
Continue only, single match registration, Privacy before load/from hub, return
navigation, preserved save, banner/footer control separation and the full phone layout matrix. Existing gameplay,
training, schedule and touch/saves regressions pass. Syntax/whitespace/baseline pass.

Initial menu tests correctly found the new Privacy action changed exact button
counts; expectations updated while retaining all bounds/touch/overlap checks.
The new match test initially omitted loading its saved career; fixed fixture setup
and reran the full suite. No gameplay failures suppressed.

Actual APK built with Java compiler/D8/manifest merger and pinned GMA25.5.0/UMP4.0.0.
Checked DEX contains ScorerAds, InterstitialAd, UMP and official test-unit ID; the
private Python archive contains advertising.pyc, no saves or private signing keys.
Actual manifest has the official test app ID, version1026622/0.6.22, min26/target36.
Signature v2 is the existing debug certificate; ZIP16KB and all 118 AArch64 ELF
alignment checks pass. Ad-ID/three AdServices permissions are absent. Other SDK
permissions and privacy impact are documented in ADMOB_SETUP.md.

Desktop real-GL screenshots of entry/hub/privacy inspected:
/workspace/striker-runtime/scorer-0622-{entry,hub,privacy}0001.png. No screenshots
of an actual ad and no Android runtime/consent/load/show test have been performed.
SDK compilation and mocks do NOT establish successful ad presentation or revenue.

APK 37,175,750 bytes (larger due to native advertising SDK dependencies).
SHA256 28b4abdaf13cebdb3a75df32c895c352366b416d4ae6058f5be705db2ff75cc7.
Logs build-0.6.22-banner.log / verify-0.6.22.log outside source in striker-runtime.

Next: owner creates AdMob app/account and supplies public app/unit IDs; phone
checks TEST load/show/dismiss, consent unavailable, offline, rotation, resume and
frame performance; finish public privacy policy/store/data declarations; only
then prepare production activation after review. No AAB/Play publication here.
