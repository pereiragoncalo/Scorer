# Scorer World 0.9.4 QA

## Game rules

Every one of212 countries now has exactly two playable league destinations and a10-club FIFO reserve. Existing active league sizes remain.3 clubs promote/relegate between1 and2, without playoffs. The original bottom3 in Division2 exchange with the first3 reserve clubs; relegated clubs are appended to the queue. Both boundaries use the frozen final tables, so clubs arriving from Division1 cannot be relegated twice and incoming reserve clubs cannot immediately promote. Queue membership/order, UIDs, league sizes and imported names persist across saves and seasons. The reserve has no league schedule or training/play/transfer destination. Country browsing shows the10 names.

When the player's club leaves Division2, the player is released and gets5 genuine active-tier offers (3 domestic,2 foreign), can find more and sign outside the normal window. Save, load, career export/import and exit work without a club. The calendar returns no fixture on release; the native Play flow routes straight to Agent, keeping the release message. Signing a new-season contract before fixtures begin preserves cup eligibility. The normal training gate and contracted transfer windows remain.

## Compatibility

Domestic save model2 persists reserve queues and contract state. Old saves reconstruct their original catalogue/membership before the new reserve is added. Careers already below2 become free agents immediately; personal stats, name, attributes, fixture history and drawn cup results/dates remain. Existing promotion playoffs are retired. Already drawn old cup fields can contain historical lower-tier clubs; new domestic cups use only active tiers1/2. Higher objects stay hidden solely for stable old UID/name/history compatibility and never enter the active league simulation or new transfers. First migrated write backs up original bytes to `.two-divisions-backup.json`; a failed backup prevents replacement.

The World club presentation catalogue gained702 previously missing UID defaults using existing local cities; previous rows/identities are untouched. Year rollover now clears the actual won/drawn/lost fields as well as played/points, preventing old wins appearing in the new table. Completed personal season records and archive are retained.

## Names and delivery

Updated v1 JSON has352 real clubs:272active and80reserve across the eight supported real-name countries. All active aliases match the previous corrected file. Reserve aliases use verified third-tier membership and follow stable UIDs through rotation. Import does not reset simulated movement. Actual game capacities can represent a subset of real teams; the model is a game rule, not official country regulations. European club reference2026/27, Brazil/Argentina2026; player source remains July2026. Other countries retain fictional local names. No backend/tunnel/token change needed.

## Verification

245 unique core and119 unique native Kivy UI tests passed (364 total). Full baseline243/118passed, then targeted suites cover the added calendar-release and updated-name-pack cases plus final fixes. Tests cover all212 country destinations/pools, frozen movement and global identities, FIFO ordering over saves, relegation/release, offers/out-of-window signing, export/reload, next_match stop, cup eligibility, bad-pool rejection, actual0.9.3 England4/Portugal1 migration fixtures/history/first-write backup, updated-name import and the real native Agent/Play/country views. Expectations for the retired starts/playoffs were updated to the new rules.

Actual APK: package com.clemir.scorerworld, versionCode1026904, existing debug upgrade certificate,118ELF/16KB +zip alignment. Exact compiled source and presentation data verified. Compiled-calendar smoke actually relegates a player, rotates the reserve, exports/reloads as a free agent and signs outside the window. No real Android handset or Play Console acceptance is claimed. Startup agreement, editor, direct leaderboard and physical shot balance from0.9.3 remain. Public launch stays1.0.
