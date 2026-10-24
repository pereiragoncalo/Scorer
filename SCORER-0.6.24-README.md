# SCORER 0.6.24 — World preview, help and local contracts

## What is delivered

Two actual Android debug APKs, with separate app/private-save identities:

| Artifact | Package | Mode |
| --- | --- | --- |
| SCORER Free 0.6.24 | com.clemir.striker | Free, one chosen division per career, existing test advertising |
| SCORER World Preview 0.6.24 | com.clemir.strikerworld.preview | Unlocked TEST preview, ad-free, no purchases or commercial ownership check |

The preview is not a paid/store release. No payment, checkout, production store
URL or automatic Free-to-World career migration is enabled. The Free career is
preserved in its existing app; World starts and saves separately. Upgrade opens
an information page first, explaining these differences. OPEN INSTALLED WORLD
PREVIEW launches only the named installed companion with a matching signature;
otherwise it explains how to install the preview. No silent unlock, charge or
career replacement. Real pricing, distribution/licensing and publication still
require owner decisions, tests and explicit approval.

## Contracts and help

New careers read java.util.Locale on Android, offline, once per new career.
Locale region takes priority (pt-PT -> Portugal, pt-BR -> Brazil, en-US -> United
States); supported language fallback then England if ambiguous. Welsh/Scottish
Gaelic GB locales select Wales/Scotland; plain English GB defaults to England.
This is a language/region suggestion, not GPS/IP detection. The UI stays English.

Initial contracts use the suggested country's lowest modelled division, with an
explicit ENGLAND DIVISION 4 option. Each switch happens before signing a club.
Free may choose one starting country but cannot transfer/promote into another
playable division. Save/load retains that choice; legacy saves retain England|4.
A save's edition flag never grants World access. Existing careers do not move
when the phone language changes. Contract buttons fit ordinary landscape phones;
compact windows retain scrolling where needed for forms.

HELP is on both the post-splash entry menu and main hub. Four short pages explain
new/load/contract, mandatory weekly training, aiming/power/chances/half-time,
automatic saves, optional ads and World/editor. Back returns to the menu that
opened Help and does not auto-load or save an unselected career. Main hub keeps
all eleven actions visible without scrolling, using a compact grid on small
windows rather than squeezing touch buttons below 48dp.

## World model — scope is fictional

212 football countries/regions, 758 domestic divisions and 9,896 fictional clubs.
Existing European national depth is retained; other regions have four fictional
tiers. Yemen added to the original catalogue. This is not a claim to reproduce
every real regional/amateur league or a licensed/current real-world database.
Defaults contain no official name packs or club art. Legacy international status/
national-team systems remain the original simplified model; this preview does
not claim fully simulated worldwide international competitions.

Country catalogue has search and six entries/page; each division has a compact
standings view and EDIT NAMES. Agent offers can cross worldwide leagues in World;
Free agent offers remain in its selected single division. Untouched countries are
simulated on demand with independent seeded RNG, avoiding 758 league updates on
every phone match or consuming the player's chance RNG by browsing. Visited league
club order, tables, scorer totals and schedule version persist across reload.

Promotion/relegation audit found the original club could remain in both divisions.
The season transition now swaps it with the displaced club, preserving both stable
club IDs and division sizes. Free's selected local league cannot accidentally
move back to England at season rollover. Shorter local leagues scale cup dates so
all eight cup rounds can take place before the next season. England's existing
46-round dates/schedule are unchanged.

## Local names editor and JSON

Navigate World -> country -> division -> EDIT NAMES. Previous/Next Club selects
within that division. Edit the club/league text and SAVE NAMES. This changes display
aliases only: canonical career keys, kits, scores, goal attribution, tables and
fixtures are not renamed/reindexed. Stable club UID follows a club on promotion;
NPC display-name aliases use that UID plus persistent scorer-role slot.

EXPORT TEMPLATE creates a user-selected JSON document using Android's Storage
Access Framework. It includes that division's clubs, league and twelve squad
scorer names/club. Edit the values, keep IDs/version/section names, then IMPORT JSON.
Preview counts/names before APPLY NAMES or CANCEL. No scripts, macros, network
imports or silent applying. User-chosen cloud document providers may themselves
sync files; SCORER does not automatically upload careers/name packs.

Each import: UTF-8 JSON version1, <=256KiB/4096 names; only clubs/leagues/players
sections, known IDs, 2–56 printable characters, no markup, controls or URLs. All
validation occurs before mutation. Native reads are byte-bounded with strict UTF-8;
document reads/writes run off the Android UI thread, returning preview via Kivy
Clock. No storage permission or arbitrary path text is used. Invalid/cancelled
imports do not change names. Private atomic backup precedes applying; failed save
rolls aliases back. Multiple packs merge; saved aggregate can cover the full model.

Aliases resolve by club UID and country context. Same-name fictional clubs in
other countries do not inherit another club's imported name. Goalkeepers/players/
teams on native match scoreboard, badges, final notice, menus, rankings and fixtures
use display names without modifying internal scoring identity. Performance cache
uses a small per-country map and revision counter, not a full JSON dump per frame.
Example: docs/data/world_names_example.json (Portugal Division4, fictional names).

## Evidence and limitations

67 core/build/security tests +44 real Kivy tests pass (111 total), syntax, whitespace
and immutable baseline checks pass. Added locale mapping/fallbacks, Free one-division
selection/persistence, World access boundary, all regions, persistent visited
World tables, import/alias save/reload and rollback, unknown/oversized/URL/control/
markup/schema rejection, same-name cross-country isolation, preserved scorer goals,
promotion club uniqueness/IDs/division size and eight cup rounds in a short season.
Actual Kivy tests cover Help origin/Back, Upgrade without charge/unlock, World
search/navigation and names editing without changing the player's career league,
plus all prior touch/physics/training/ads/layout regressions. Exact action counts
were updated for Help/Upgrade while keeping all bounds/minimum-size checks.

Real desktop GL captures inspected at 1280x589/density1.64: free hub/contracts/help/
upgrade and World catalogue/editor in /workspace/striker-runtime/scorer-0624-*.png.
These are not Android screenshots. Final appearance matches the compact contracts
and editor captures with all primary actions visible. Physical Locale results,
opening the installed companion, Android document picker, IME/rotation, phone FPS
and broader script/font coverage remain device tests. Do not call World a finished
commercial Android release based on desktop checks or compilation.

Both APKs actually compiled. Buildozer/p4a initially hit a mixed disposable pip
packaging venv while creating the second distribution. Preserved that venv outside
source and recreated packaging env; retained native compiler caches. World then
built successfully. Final logs: build-0.6.24-free-final.log and
build-0.6.24-world-final.log; static logs verify-0.6.24-{free,world}.log. A diagnostic
first probed a non-existent hostpython3 executable; reran with the actual built
hostpython binary and verified each APK's compiled edition flag (Free false,
World true), not just its source title.

Both actual APKs: API26 minimum, target36, arm64, versionCode1026624, same existing
debug signaturev2, ZIP16KiB and 118 AArch64 ELF LOAD alignments pass. World DEX has
LocalNameFiles and no Google Ads classes; its manifest has no Internet or Billing
permission. Free retains test AdMob and no Billing/AD_ID/AdServices permissions.
Private Python archives contain expected modules, no saves or signing keys.

## Builds and next task

Free: bash tools/android/run.sh python tools/build_android.py -v android debug
World: python tools/prepare_world_preview.py, then
SCORER_SOURCE_ROOT=/workspace/Scorer-world-preview bash tools/android/run.sh python tools/build_android.py -v android debug
Build sequentially; native caches are shared but source/app identity are separate.
Free's edition.py stays False in the repository; generated World copy is True.

Next: owner tests both APKs, Help/Upgrade launch, a new local/English contract,
World season/transfer and JSON export/edit/import/save/reload on Android. Then
agree production World packaging/licensing, pricing, privacy/store declarations,
explicit save-migration policy and distribution approval. No real charge today.

## APK hashes

free: Scorer-0.6.24-arm64-debug.apk, 37213558 bytes, SHA256 `9eea2039e1c2c9442b33a9d9abbaee34aa58dd9bc8bcea2277ccb98c61d5d2ce`.

world: Scorer-World-Preview-0.6.24-arm64-debug.apk, 30253267 bytes, SHA256 `e455976eca0a6264249eaa024b88b875b9085dad954d9736b5848cc197b604e2`.

