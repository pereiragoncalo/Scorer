# Scorer0.6.46 — publication preparation and remaining external gates

Owner decisions: Gonçalo Pereira, public support/privacy goncalo@clemir.com,
verified active Play account, intended audience includes minors, **both apps free**.
No upload, rollout, payment or new tunnel performed.

## Implemented

- Detailed first-run disclosure before the first usage transmission; no usage
  toggle. Continue explicitly acknowledges a notice, not name or analytics consent.
- Public features default locked. Adult date check (discarded locally), salted
  PIN, persisted lockout and controls to enable/disable social features. Parent
  lock stops publication and queues withdrawal. No claimed identity verification
  or automatic proof of lawful parental authorization.
- Explicit community terms + Share, separate from counters. New v3 public records
  remain hidden until approved. Old uploading clients cannot bypass review/terms.
- In-game report reasons and persistent local publisher blocking; public IDs never
  expose ownership/admin tokens. Private dashboard review/reject/ban/unban/erase.
- Safe local career export/import for each edition, compatible semantic validation,
  preview/confirm, atomic save and previous-career backup. Android SAF and desktop
  file picker; no PINs, counters, private online credentials or cross-edition import.
- Periodic server retention, aggregate-only backups with7day rotation, public
  /privacy /terms /delete page implementation with operator facts/config gate.
-59publication messages translated in all9World catalogues. No English fallback
  for the new disclosure/guardian/report/transfer messages covered by the new test.
- Production staging supports separate package/channel/public metadata and explicit
  review attestations. Production bundle audit requires a non-debug expected upload
  certificate, actual compiled channel/metadata,16KB and bundle-derived APK checks.
- Correct store-size icons/feature art, complete EN/PT listing drafts, Data Safety,
  operator/legal review document, server update and final acceptance instructions.

## What cannot be marked completed by this cloud session

1. **Laptop deployment:** new server files, public policy configuration and actual
   public v3 publish/moderate/report/remove acceptance. Instructions in
   [SERVER_0.6.46.md](SERVER_0.6.46.md). Existing deployed v2/usage are not silently
   changed. New app usage still works on old server; v3 ranking needs this update.
2. **Actual legal/provider review:** appropriate basis and rights handling for
   automatic analytics with minors, real Cloudflare terms/logging/transfers,
   adult controls and operating moderation. See [assessment](LEGAL_BASIS_REVIEW.md).
   No fabricated legal-basis declaration or consent proof. Production gates remain
   false until reviewed; current public policy fields are intentionally incomplete.
3. **Production upload signing:** protected owner upload key and its Console
   certificate. Rehearsal AABs can be inspected unsigned; debug APKs are for direct
   QA upgrades, not Play production. No new durable upload key is invented in the
   disposable cloud or bundled in Git. Signing tool is ready for the owner's key.
4. **Installed Android testing:** Play-generated split APKs,16KB runtime/pre-launch,
   real touches, final Android screenshots, signature-transition/export recovery
   and device behaviour. Desktop/Kivy/native Windows smoke is not a phone test.
5. **Console:** final forms/IARC, countries, free pricing, app-access instructions,
   upload/pre-launch/closed test/production access if required for either package.
   Owner confirmed account verified; do not request that verification again.
6. **Operating approvals:** owner review of exact policy/materials, rights to
   original artwork and actual human moderation/support. Code doesn't supply a
   moderator or approve a public rollout.

The missing items above require external access, evidence or owner/operator
judgment, not another speculative rewrite. No claim that Google has approved the
apps or that all production gates are already green.

## Tests/artifacts

See RELEASE_0.6.46_artifacts.json after builds. All synthetic telemetry/ranking
checks use local or fake transport; no QA counters or names added to owner server.
Final verified source revision is recorded in that file. Existing unrelated local
competition changes are preserved separately and are not represented as shipped.

## Manual acceptance order

Save/exit on installed0.6.45, install matching0.6.46QA signed with the same debug
key, Load Game and verify progress. Export the career to a private selected file.
Do not uninstall until the file has actually been written and a restore tested.
Then test the final Play candidate's same-edition import before relying on it.
Free and World remain independent; the export does not migrate ownership tokens,
so withdraw public records before deleting the old installation/data.

On laptop: install reviewed server, finish reviewed public config, verify public
pages and v3, exercise moderation/removal. On Play: finalize legal/content forms,
sign with actual upload key, install from test track and run pre-launch/phone tests.
