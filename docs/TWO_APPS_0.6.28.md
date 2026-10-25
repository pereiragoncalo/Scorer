# SCORER 0.6.28 — independent Android products

The owner's decision on 2026-10-25 replaces the single-app World purchase plan.
No store publication, price activation or real purchase was performed.

| Product | Android package | Career | Advertising |
| --- | --- | --- | --- |
| SCORER Free | com.clemir.striker | Existing private striker_career.json; one Scorer League | Test AdMob plus local SCORER World stadium promotion |
| SCORER World | com.clemir.scorerworld | Separate private striker_world_career.json; World/editor | No AdMob SDK, network permissions or promotion boards |

Both can be installed together. Free's package and debug certificate stay compatible
with the earlier Free/QA installation; no uninstall is required for that upgrade.
World is a new installation. No automatic copying of Free progress or historical
same-app World saves is attempted. Those old files are not deleted from Free.
The previous permanent one-way in-app mode preference no longer controls Free.

## Promotion

Eleven physical-looking board surfaces sit outside the playing rectangle, with
space behind and beside the goal. They rotate SCORER World, world leagues, local
editor and ad-free messages every25seconds. Textures are generated locally and
cached (four messages); no remote artwork, tracking, click area or physics object
is added. Boards are rendered before players and the ball, never over them.

Free's entry/hub World action opens an information page explaining a separate app
and career. No in-app Buy/Restore exists. The store button stays disabled until
WORLD_LISTING_READY is explicitly enabled for the actual published World listing;
its only destination is the fixed com.clemir.scorerworld Google Play page.

[Desktop Kivy capture of the Free boards](captures/free-0628-world-boards.png).
This is a real desktop rendering, not an Android device screenshot. A first capture
exposed mirrored texture coordinates; these were corrected and visually rechecked.

## Build reproducibility

Use fresh staging directories outside the checkout:

```bash
python tools/prepare_editions.py --edition free --output /workspace/Scorer-free-0628
python tools/prepare_editions.py --edition world --output /workspace/Scorer-world-0628
SCORER_SOURCE_ROOT=/workspace/Scorer-free-0628 bash tools/android/run.sh python tools/build_android.py -v android debug
SCORER_SOURCE_ROOT=/workspace/Scorer-world-0628 bash tools/android/run.sh python tools/build_android.py -v android debug
```

The source checkout's edition stays Free. Both staging products force
WORLD_PREVIEW=false and exclude root billing.py, native BillingClient code,
server/config/key/save material. World retains only the native local-files bridge.
Test advertising is never claimed to generate revenue. These profiles prepare QA
APKs, not production listings or signing configurations.

The first World build failed because Buildozer used the application package name
as the native distribution directory while p4a reused `striker`. The wrapper now
uses the explicitly configured shared native distribution for path lookup as well.
This shares compiled Python/Kivy libraries, not application identities or saves.
Both final builds succeeded sequentially with this configuration.

Historical preview and single-app release CLIs are retired. The old billing/server
source remains dormant for history/testing; neither final APK contains the Google
Play Billing SDK or the app's WorldBilling bridge. World access comes from the
separate World build, not a claimed verified in-app purchase or anti-piracy check.

## Validation

- 108 core/security tests and 53 actual Kivy interface tests passed (161 total).
- New tests cover separate identities, native capability stripping, stage safety,
  fixed-store-link gating, board placement/rotation/cache, ignored legacy purchase
  callbacks, and World/Free career isolation. Existing gameplay/save/UI tests pass.
- Actual final APK manifests: distinct package IDs, version0.6.28/code1026628,
  minAPI26/targetAPI36. No Google Play Billing permission or SDK in either APK.
- Free actually contains ScorerAds and test IDs. World actually excludes the AdMob
  SDK and Internet permission, and contains the local editor files bridge.
- Both APKs' actual bundled edition.pyc were evaluated with matching Python3.14:
  Free=false/World=true for WORLD_BUILD; WORLD_PREVIEW=false in both.
- Both have valid existing debug signatures, ZIP alignment16KB and all118 AArch64
  ELF LOAD alignments at least16KB. Certificate SHA256 remains
  84c17cdf31e2ee7c6e9c082bde539df6822bf48267a0603de9814d6e2846ef49.
- [Artifact sizes and SHA256 hashes](TWO_APPS_0.6.28_artifacts.json).

Logs are under /workspace/striker-runtime: two-apps-core-final.log,
two-apps-ui-release.log, build-0628-free-final.log and build-0628-world-final.log.
The exact verified application change was developed in an isolated source snapshot;
separate unfinished tournament work was preserved and is not part of these APKs.

## Device checks still required

Install both APKs together. Confirm separate launcher entries; Free updates and
loads its existing career; World starts a separate career; create/save/reopen each;
train and play a match; check board visibility during chances and full-time; check
World has no ads; test the World editor import/export on Android. No physical phone
or live store purchase test was performed in this environment.

National regulation fidelity and full continental/national-team simulation remain
in development. These test APKs are not presented as finished paid releases.
Production advertising, support/privacy URLs, release signing, store listings,
paid-app pricing and public publication still need completion and owner approval.
