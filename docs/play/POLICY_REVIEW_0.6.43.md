# Google Play review — ad-free Scorer0.6.43

Reviewed2026-10-30 against official pages fetched directly. Owner waived review of
the unavailable email; do not imply this document read that private email or Play
Console. No app-store submission, payment/advertising activation or approval.

## Changes completed

- Remove all ads/UMP SDK dependencies and Android Java source set, AdMob metadata,
  banner reservation, rewarded-training UI and stadium sponsor/World-promotion
  panels from all three editions. Native factory never initializes a bridge;
  AndroidAds wrapper removed. Existing careers/morale remain intact.
- Separate-app production preparation no longer demands AdMob IDs or same-app
  World billing. Nonempty ad IDs or enabled billing are now rejected. Both package
  IDs can be checked explicitly; static verifier forbids ad/billing native classes,
  forbidden permissions and ad metadata, rather than requiring those old bridges.
- Rewrite current listing, privacy draft and Data Safety inventory to match ad-free
  Free/World, active optional usage and named completed-season sharing. Remove
  obsolete promises of local-only counters, no-Internet World and same-app purchase.
- Add safety reminder before public name sharing: nickname, no full real name,
  contact or school information. This is NOT parental verification/moderation.

## Before production — real remaining work

1. Public owner-approved legal/developer identity, support contact and working HTTPS
   privacy-policy URL. Current release config has placeholders/empty fields and
   production validation correctly blocks them. Privacy draft is not hosted or
   owner-approved. Do not publish private statistics mailbox as support by inference.
2. Fill Data Safety for BOTH apps: actual optional interaction/error counters and
   public chosen name/team/gameplay records. Includes developer server/Cloudflare
   handling; ad-free does NOT mean no data collected. Declare Contains ads=No only
   for verified new artifacts. Do not reuse old AdMob or billing declarations.
3. Audience/content rating: owner said general audience including minors. Public
   player/team names are user-generated information and may be identifying. Define
   appropriate adult controls, safety/reporting/moderation and age approach under
   applicable Families/UGC policies before production; current Share confirmation
   and warning alone are insufficient to claim compliance. Do not secretly change
   audience to adults. Existing no-login design does not automatically settle all
   deletion questions; explain/remove published profiles and support deletion.
4. Verify laptop server v2 actually deployed (last probe status in artifact metadata),
   test real public record publish/delete, offline/restore and private stats access.
   No administrator credentials in app. New ad-free release needs no server schema
   change; completed-season v2 upgrade from0.6.42 remains a separate laptop step.
5. Native release AAB with non-debug manifest, protected upload key/Play App Signing,
   unused version code and actual Play pre-launch/device testing. Current delivered
   QA APKs use debug upgrade key and Windows EXE is unsigned; neither is a claim
   of production-signed Play artifact. Existing tools sign/verify but no upload
   key or public Play access is configured in this executor.
6. If personal developer account was created after2023-11-13 and has not already
   satisfied the requirement: closed testing with >=12testers continuously opted
   in for14days, then application for production access. Phone verification alone
   does not replace testing/production access. If starting on2026-10-30,14days
   reaches2026-11-13; do not promise a public Play launch onNov6 without completed
   eligibility. Direct Android testing/distribution is a separate path.

## Verified platform requirements / limitations

Official target-API page states new apps/updates need Android16/API36 from
2026-08-31. Project target36/min26/arm64 satisfies this static requirement. Re-check
future deadlines before upload. Native16KB support must be verified on actual
AAB/APK libraries/packaging and tested in a16KB environment; earlier candidates
passed ZIP/118ELF checks. These are not evidence of a physical16KB device test.

Current competitive World country models remain provisional. Listing must not say
all real league regulations, continental/country competitions or anti-cheat are
complete. Use real app captures and accurate content descriptions.

## Official sources consulted

- Target API: https://support.google.com/googleplay/android-developer/answer/11926878?hl=en
- Personal account testing: https://support.google.com/googleplay/android-developer/answer/14151465?hl=en
- User Data/privacy/deletion: https://support.google.com/googleplay/android-developer/answer/10144311?hl=en
- Families/social features: https://support.google.com/googleplay/android-developer/answer/9893335?hl=en
-16KB support: https://developer.android.com/guide/practices/page-sizes

Actual fetched page extracts retained only in runtime /tmp policy text files;
no private email, account/password or Play Console data accessed. This is an
engineering review of known code/public policies, not Google approval or a claim
that outstanding publication requirements were implemented.

## Completed QA artifacts

176core/security +98Kivy UI PASS (274unique checks), plus6native Windows staging
checks and frozen smoke. Old tests expecting banner/Google test-ad copy/reward
buttons were updated to the explicit no-ad requirement; unchanged career backup,
training, saves, scoreboard, optional stats and season records still pass.

Both Android APKs actually compiled and DEX-scanned: no GMA/UMP/Billing/custom ad
bridge classes. Both retain original debug upgrade certificate, target36/min26,
only Internet/network-state permissions and ZIP16KB/118ELF16KB alignment PASS.
Native Windows run41192102865/sourceb1ac79f PASS: actual adfree_release flag,
empty stadium promotion texture cache, no backend, gameplay/save/records renders.
Native archive verifies no AndroidAds wrapper and no sponsor draw code. These
remain debug Android and unsigned Windows QA builds, not production-signed AABs
or real phone tests. Public v2 last probe remained404; laptop migration is still
separate from this ad removal. No server/DNS/mail/Play Console changes made here.

Production AAB audit wrapper now accepts explicit free/world identity and no
longer demands purchase tests; syntax checked, not run on a new production AAB.

[Scorer-Free-0.6.43.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.43/Scorer-Free-0.6.43.apk)

[Scorer-World-0.6.43.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.43/Scorer-World-0.6.43.apk)

[Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.43/Scorer-Free.exe)
