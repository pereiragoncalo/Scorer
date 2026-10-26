# Scorer World 0.6.37 QA APK — standings eligibility zones

Source main commit2851bfb. Own standings and browsed leagues show P/PO/R places,
green/amber/red, with a tappable localized Rules key and explicit no-up/no-down/
no-playoffs boundaries. Neutral hero highlight; paged tables,48dp controls.

IMPORTANT: markers follow CURRENT GAME eligibility, not certified national
regulations. Priority-country playoff outcomes are still simulated (legacy35%
hero promotion chance for places4–7); no knockout playoff fixtures or complete
national formats/NPC movement were implemented. The rules dialog explicitly
explains this. Owner fallback stays two tiers,3-up/3-down, no playoffs.
No season resolver, RNG, save/schema, identities or fixture changes.

200 tests PASS. Actual World arm64 debug APK, signature/manifest/edition/UI/rules/
neutral colour/messages/SDK/wordmark/font/language contents, ZIP16KB and118 ELF
alignment checks PASS. Update matching World0.6.36 without uninstalling; same
package/debug certificate. No physical phone/Play test claimed. No ads/Billing
SDK or payment activation. Latest Free APK remains0.6.35. Direct APK, no ZIP.
See source docs/STANDINGS_0.6.37.md and SHA256SUMS.
