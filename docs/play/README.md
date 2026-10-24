# Google Play preparation — SCORER 0.6.25

This is preparation, not an upload or activation. The owner's Play Console account
is under verification; owner AdMob IDs, public support/policy details, production
signing, deployed verification service and real Play purchase testing are absent.
Do not describe the rehearsal AAB as ready for public production.

## Product and current implementation

One app, **com.clemir.striker**. New Free careers start in Scorer League with no country selection. Existing Free careers retain their single league.
A **one-time non-consumable INAPP** product, `scorer_world_upgrade`, enables World,
the passive local names editor/importer, promotion/transfer access and ad-free play.
No subscription, external checkout, companion app or second career installation.
Do not consume this purchase. The store, not a hardcoded UI string, supplies price.
The World database has 212 football regions/758 fictional domestic tiers, not every
real regional/amateur league. The international model remains simplified.

Native Billing Library **8.0.0** queries current product/purchases, supports pending
purchases and reconnection, handles cancellation/already-owned, restores ownership
on launch/resume and provides Google checkout only when details/price are ready.
No pending, cancelled or merely locally acknowledged JSON unlocks World.
Backend verification must succeed before an RSA-signed installation-bound licence
is cached. Offline validity is seven days, followed by an online ownership check.
Refund/cancellation checks occur on restore and licence renewal; no instant offline
revocation or tamper-proof DRM is claimed. There is no deployed RTDN handler.

The server checks the exact Play package/product/token using Android Publisher API,
requires PURCHASED and unconsumed, acknowledges verified new purchases immediately,
and signs a bounded licence containing package/product/installation/nonce/expiry.
No card data, player name, career save, signing private key or Google service-account
credential enters the client verification request. Tokens must never appear in logs.
The Python facade adopts a verified snapshot only at safe menus, never mid-shot.
The owner correction in 0.6.26 keeps Free and World in distinct save slots within
the same application. Free uses striker_career.json; World uses striker_world_career.json.
World starts its own player/contracts; it never imports Free progress. Switching saves
the selected career first and blocks on write failure; new-game backups are slot-specific.
World ownership does not enable paid features inside the Free career.
An inaccessible World career remains stored for restore, never silently deleted.

## Reproducible rehearsal

From the source checkout, using the managed build environment:

```sh
python tools/play/prepare.py --channel rehearsal --output /workspace/Scorer-play-qa-0626
SCORER_SOURCE_ROOT=/workspace/Scorer-play-qa-0626 bash tools/android/run.sh python tools/build_android.py -v android release
```

Use a fresh empty staging directory for each revision. The source checkout/package
identity is never rewritten. Builds share the native platform and must run sequentially.
The SDK licence was already accepted by the owner. No new contract is accepted here.
Rehearsal is a genuine release-mode **unsigned AAB**, labelled SCORER Play QA, with
Google TEST ads, BillingConfig.ENABLED=false and WORLD_PREVIEW=false. It contains the
billing and SAF classes but cannot start a purchase. It cannot generate ad revenue.
Signing a universal APK for inspection with the existing DEBUG key is a test action,
not production signing. Do not upload an unsigned/debug-signed bundle to production.

Actual artifact validation, with bundletool 1.18.1 from google/bundletool:

```sh
java -jar /workspace/striker-android-build/bundletool-all-1.18.1.jar validate --bundle=PATH.aab
java -jar /workspace/striker-android-build/bundletool-all-1.18.1.jar dump manifest --bundle=PATH.aab --module=base > /tmp/scorer-manifest.xml
java -jar /workspace/striker-android-build/bundletool-all-1.18.1.jar dump config --bundle=PATH.aab > /tmp/scorer-bundle-config.json
python tools/play/verify.py PATH.aab --manifest /tmp/scorer-manifest.xml --channel rehearsal
bash tools/android/run.sh python tools/android/verify_elf_alignment.py PATH.aab --readelf /work/toolchain/android-sdk/ndk/28.2.13676358/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-readelf
```

`PATH.aab` used inside the container must be under its mounted source directory.
Verify `PAGE_ALIGNMENT_16K` in bundle config and inspect a bundletool-generated APK
with apksigner/zipalign plus the ELF checker. Static checks are not a 16KiB device run.
The build wrapper fixes Buildozer's literal shell quotes on the two XML argv options;
no shell evaluation or upstream source modification is used.

## Public production configuration

Copy `release/play.example.json` to **release.local.json**, which Git ignores.
Only PUBLIC settings belong in this file: developer display identity, support email,
HTTPS policy URL, unused versionCode, owner's four AdMob IDs, product ID, HTTPS
verification endpoint and RSA PUBLIC key (SubjectPublicKeyInfo DER/base64).
Never add store passwords, private keys, service-account JSON or purchase tokens.

```sh
python tools/play/prepare.py --config release.local.json --channel production --check
python tools/play/prepare.py --config release.local.json --channel production --output /workspace/Scorer-play-production-CANDIDATE
```

The template intentionally fails production checks. IDs must be real, distinct,
from one publisher and not Google's TEST publisher. Production preparation requires
verified purchase-service configuration and billing enabled, to prevent presenting
an unusable paid feature as finished. Setting a config boolean is not authorisation:
obtain the owner's explicit approval and complete tests before enabling real payments.
Build unsigned, then sign outside Buildozer with the owner's protected **upload key**;
Play App Signing protects the actual application signing key. Do not pass passwords
through build command lines/logs or commit keys. Use a full JDK (not just a JRE); see `sign_aab.sh` for env-only signing.
Verify the upload certificate against the Console, not merely that any signature exists.
A package name becomes fixed once registered; check it before the first upload.
VersionCode must exceed every uploaded version, including internal/closed tracks.

**Beta compatibility:** existing APKs use a debug certificate. A future different
Play app-signing certificate cannot update those APKs in place even with the same
package. Do not uninstall a beta without preserving its private career. Both career slots remain in the same signed installation; a supported
cross-certificate beta-to-store save-transfer flow still needs an explicit decision
and device validation. Do not enrol the debug key as a production key to avoid this.

## Play Console tasks, in order

1. Finish developer identity/account verification. Create/confirm Android app
   com.clemir.striker; default game UI is English. Choose free app with in-app purchases,
   not a paid separate World app. No account passwords or tax/bank documents in chat.
2. Configure Play App Signing and an upload certificate; securely retain recovery
   material outside this repository. First use internal testing, not public production.
3. Deploy the verifier as described in [server setup](../../server/README.md), with
   the Console-linked Google Cloud identity authorised for this app's purchase API.
   Configure the RSA public key and HTTPS endpoint in a release candidate.
4. Create one INAPP product scorer_world_upgrade, set localised descriptions/prices
   and availability. Decide and approve price and activation with the owner. Set up
   licence testers and test-track accounts; no genuine payment is needed for tests.
5. Test approved billing-enabled candidates **installed by Google Play**: product and
   currency, approved/cancelled/slow-approved/slow-declined purchases, network loss,
   backend denial/outage, immediate acknowledgement, process death before/after grant,
   Restore after reinstall/new device, duplicate callback, account change/refund,
   licence expiry/offline clock rollback, and career preservation. Mock tests do not
   satisfy this gate. Do not test by clicking real advertisements.
6. AdMob account and ad units can be created before Play verification completes.
   App review/verification, store linkage, ad serving and consent setup are separate
   requirements. Enter actual owner IDs only after approval; register test devices.
   The current child/under-age + G + non-personalised configuration remains mandatory.
7. Complete app-content forms: ads yes, in-app purchases when activated, accurate target
   audience including minors, Families/SDK eligibility, IARC questionnaire (do not invent
   a rating), app access (no SCORER login), privacy policy and Data Safety. Use
   [data inventory](DATA_SAFETY.md), verify current Google SDK disclosures and Console
   rules rather than copying a guessed final declaration.
8. Complete English/Portuguese listing drafts, public support contact and policy,
   512px store icon/feature graphic and **real current Android screenshots**. Existing
   desktop captures are not proof of Android execution. See [listing drafts](STORE_LISTING.md).
9. Run pre-launch report and actual touch/landscape/save/offline/ads/billing/import
   checks on phones plus 16KiB Android; resolve crashes and policy findings.
   Complete any closed-test/production-access requirement shown for this account.
10. Review exact signed AAB, manifest, certificates, checksums, disclosures and test
    evidence. Ask for explicit approval only then. No upload, rollout or payment
    activation was performed during preparation.

Policies and SDK status can change. Target36/min26, ARM64, Billing8 and 16KiB static
checks are current project choices; the Console must confirm applicable deadlines,
allowed SDK versions, required testing and final review at submission time.

Official references to review before submission:
- https://support.google.com/googleplay/android-developer/answer/9859152
- https://support.google.com/googleplay/android-developer/answer/10787469
- https://support.google.com/googleplay/android-developer/answer/14151465
- https://developer.android.com/google/play/billing/integrate
- https://developer.android.com/google/play/billing/security
- https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.products/get
- https://developer.android.com/guide/practices/page-sizes
- https://developers.google.com/admob/android/privacy/play-data-disclosure

These links are references, not a claim that live policies were retrieved in this
restricted environment or that Google has approved this application.

## Recorded evidence

Historical [0.6.25 AAB readiness and hashes](READINESS_0.6.25.json) record
79 core/security tests and 46 Kivy tests passed, actual AAB/static checks and remaining
account/device/service/signing gates. See [full build log](../BUILD_LOG.md).

The 0.6.26 code/Android APK is validated separately in [the revision report](../UI_0.6.26.md).
Rebuild and validate the AAB from the final chosen source revision before signing/upload.

Current 0.6.27 World presentation, editor format and morale rules are in
[the revision report](../WORLD_0.6.27.md). The same-app owner QA test entitlement
must remain false in any production/rehearsal submission candidate.
