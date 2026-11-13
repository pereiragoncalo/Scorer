## 2026-11-13 — rolling sphere comparison, simulation only

Owner explicitly requests only simulations and no compilation/new version. Added isolated tools/net_lab rolling-contact experiment with a moving sphere, impulse exchange/position stabilization, contact friction, turf resistance and travel-based spin. Same input for taut vs slack installation; side contact precedes rear contact, pocket peaks at the side/back junction and sphere continues rolling until stopped. Slack hem is free to gather at the ground corner, with fixed mouth/top/centre supports. Two checks pass: finite continuous ground trajectory/side→back ordering/material response/retention, and identical30/60capture-rate replay. Actual Kivy comparison exported at100%and50%, inspected near junction. No production code, app version, build/signing/publishing or update-policy change. Artifacts: docs/data/rolling_nets.

## 2026-11-13 — final seam continuity correction, 1030017

The dynamic seam sweep found up to10cm of mismatch between interpolated box panels despite the earlier vertex-subset weld test passing. Side height rows are now also rows of the back sheet, removing independent hanging edge nodes. A1µm coordinate weld tolerance handles algebraically equal Windows coordinates crossing decimal-rounding boundaries. New test sweeps101seam points under impact, both sides, mobile/full, box/veil and Windows dimensions; gaps below10µm required. Final59pure +30native cases pass, plus25publisher scenarios (24pass/1existing hostJDKskip); full AAB1030017audit passes including exact compiled source,248frames/35sheets and118ELF16KB. Final visual sequence and25%replay same-time frame are pixel-identical. New test also proves resting cache reprojects Kivy mutable viewport values and120redraws do not accumulate groups. Pure7case solver suite passes; new Android262box/223veil particles, Windows536box/453veil. Near-post strong peak unchanged at0.9965m. Candidate1030016and uploader1.15already on GitHub are superseded; Google Play was not invoked from cloud. Final target1030017/uploader1.16, original key only. Final AAB118181377bytes/SHA256e708652b1f075e5d41ddfe7b72618c07dacacd8aea42546681a5cf6a3619b7a5. Delivery workflows43414677782and43414672964passed; all9public downloads verified byte-for-byte anonymously, including AAB/uploader/helper/guide/videos/previews. Exact derived APK tar also excludes net_lab/reference JSON/demo videos. Owner signing, live Play submission/update policy and device acceptance remain pending.

## 2026-11-13 — Scorer 1 deformable nets and development lab

Inspected main.py physical ball/net collisions, goal-line registration, ripples and painter order; goal_nets.py styles/lattice/frame geometry and staging. Existing Ball/collision/scoring logic remains authoritative. New gravity-loaded slack rest geometry, welded panels/anchors, vector Verlet springs, structural/shear links, stretch constraints, damping and sleep in net_cloth.py. Shared cached Kivy line meshes with local foreground strands in net_render.py; presentation-only event/ball adapter in net_presentation.py. Main resets cloth per shot and advances it at1/120along ball steps, and between shots to avoid frozen deformations. Projection extracted byte-identically into goal_projection.py. Square/hexagon and veil/box stay UID-bound.

Standalone tools/net_lab shares the exact modules, with7presets,8parameters, direction/force/UV controls, repeat/pause/step,100/50/25%,A/B,validated JSON/reference and frame capture. No career/game instances. Lab is excluded from production staging. Mobile218particles/full446 keeps shared algorithm, reducing measured per-step CPU from~3.3ms to~1.4ms in initial desktop measurements; not handset FPS. Initial visual exports compared loose/stiffer material and slow motion; final evidence follows.

58pure regressions pass (including all presets, recovery, finite states, anchors, force response, symmetry, replay rates and staging),30native cases pass (including real UI controls, render caches/mesh limits/resolutions/Windows geometry, and20pairs/40physical trajectories with presentation enabled/disabled). Corrected simulator title-property collision, capture frame counter, mirrored shot yaw and stale test setup; no game trajectory changes. Additional between-shot recovery regression included. Native clipboard warnings reflect missing optional Linux xclip/xsel helpers in dev lab only. Actual Android/Windows handset/executable acceptance is not claimed.

## 2026-11-13 — 30-day openings/closes dashboard

Owner requests only totals of openings/closes in last30days and a daily breakdown. /admin now shows two totals and30descending UTC receipt-day rows including today/zeros. Existing sessions/sessions_ended mapped to openings/normal closes; background/resume/forced-stop and delayed/offline delivery semantics unchanged, disclosed inline. No invented events, no new game build or collection setting change. Authenticated /v1/activity limits the report to the two counters; existing /v1/totals stays compatible. Moderation/privacy controls remain at /admin/manage. Update other backend packagers to include the separated management page.

Real Chromium via Playwright: desktop/mobile390px, correct101/81fixture totals,30rows including zero days, bad/cleared token, separate management, no JS errors/horizontal overflow. Screenshots are synthetic fixture data. New HTTP/window/leap-day/rollback/unknown-version checks pass. Broader20case run:19pass and one existing stale legal-policy assertion expecting “voluntary”, contradicted by owner1030005startup agreement and unchanged baseline config; no policy change in this task. Focused collector/current-installer suite passes. Standalone three-file installer passes --check; pinned installed-source guard, private backup and rollback; no credential/database/minimum changes. Live deployment awaits owner bastion execution. Delivery workflow43396685750passed all14focused cases and public installer bytes/SHA verified anonymously. First packaging attempt differed between Python3.12/3.14gzip defaults; replaced compression with canonical JSON/base64 so both produce identical bytes. Standalone embedded files exactly match source.

## 2026-11-13 — 1030015 training opportunities and stadium nets

Training reuses make_delivery/_start_opportunity for all ten match types; local weekly seed preserves opportunity on resume. Three shots, coach focus, atomic reservation/reward rules unchanged. Five per side (including hero/keeper), fluorescent sleeveless bib recolouring over pale sleeves; no source art changes. Home stadium empty seats retained.

Four stable UID-based net dressings: square/hexagon × legacy veil/stanchions or box/three detached rear posts and cords. Box swept rear/roof/side collisions match rendered dimensions; shared deformation field seals seams. Original goal mouth and line scoring retained. GLES2 line meshes kept below24000indices.

91 core regressions passed. Native training/save/geometry/mesh/balance checks and actual Kivy screenshots recorded with release evidence. Initial tests found a missing no-club fallback and zero-duration opportunity retaining prior buildup state; corrected. Focus fixture updated to use reserved session state. Android build/audit and public attachment verification follow.

Android1030015 rebuilt successfully (118159992bytes; SHA256e25aaefc92d9c87bf96cf36422c6557d91228c21654038a4d7b55faeca342ebf). Production/bundletool/118ELF16KB/ZIP16KB/derived debug inspection and exact compiled runtime/assets audit all passed. 105core +30native cases passed;25publisher scenarios24pass/1existing hostJDKskip. Original248frames/35sheets unchanged. Four runtime screenshots and concise evidence in docs/data/training_nets_1030015. Runtime sourcefc537d1; subsequent source commits only update historical empty-training test expectations. Full source build never included unrelated main.py WIP. Old /workspace/deliverables archived to /tmp/scorer-deliverables-archive with its original path symlinked to recover temporary build space.

## 2026-11-12 — World1.0 / 1030014 calendar, locker room and accessibility

Owner requests easier play, two-leg round robin in identical opponent order and
maxTWOhome/away streaks for all clubs, then adds seated-player locker-room training.
117core cases pass, covering frozen v3fixtures2–64except4 (mathematically incompatible
compact4-team mirror+max2, unused regular size), same return order/reversed venues,
all pair counts, first-leg balance and saved-prefix compatibility. Current regular
sizes10–24and split groups6+supported; existing official3/4leg/split structures stay.
Early v2seasons upgrade only if all played fixtures identical; others retain old
schedule to rollover. No runtime solver; frozen version3digest is save compatibility.
Normal aim*.75/decision*1.6, header*.78/*1.6plus close aid, stronger duel/penalty aids
and keeper-only delay/read spread; launch/collision geometry unchanged. Paired480
exact-corner shots compare13/14: long-shot goals tier1 10→15/30, tier4 9→16/30;
other exact-target types already almost all goals. This is not human conversion.

New original room and reference-character seated art, shader club palette, no scroll,
48dp controls, current XP/progress/energy and start/resume/coach gate retained. Native
responsive/font checks4languages×3sizes, start/resume and real atomic-save-failure
pass. Initial FloatLayout composition looked wrong despite valid bounds; replaced
with BoxLayout and actual screenshots checked. Initial save mock omitted the real
error message; os.replace failure fixture now exercises real rollback and passes.
7native finishing/launch cases pass.25publisher cases:24pass/one full-JDK-only skip.
Actual AAB compiled, bundletool/static1030014/production/118ELF16KB/derived APK and
exact compiled new modules/art/all248frames/35sheets pass. Runtime sources match
361b3a1(test fix only after staged runtime commitdd28ba5). Public delivery follows;
owner signing/Play commit/phone acceptance/conditional minimum remain pending.

1030013delivery verified: bundle workflow43314926835 and publisher43314890916
succeeded. Anonymous full AAB/coordinator/signing-helper/uploader downloads match
all local bytes/SHA256. AAB117232899bytes,
057e64e3fc68d5bf6008883b3246107d6bf794f6cd8bc11e7f5ea98522365654;
uploader1.12SHA2567ddb630b3c0ea5d58d8da494f5f1d7a9fd9434df2a1cfa4382dcb65a0340c935.
Owner signing/internal commit/physical balance acceptance and conditional minimum
activation remain pending. Preserve minimum0until Play availability and acceptance.

## 2026-11-12 — World1.0 / 1030013 modest finishing ease

Owner requests a little more penalties/one-on-ones and less effective keepers for
placed shots. Runtime sourcefc6de19. Penalties5→8%per fixture, shared scheduling/
NPC goal-reservation constant. Clear chances6–22→8–28%by opponent pressure, still
at most one and unchanged personal chance counts. Clean outer kick/free-kick
shots add up to60ms read delay,35%read spread and16cm centreward misread. Smooth/
symmetric, central/off-target/header/penalty placement neutral; existing controls,
ballistics, physical collisions and saves unchanged. Graphics fix retained.
59core cases and15native cases pass; paired central reads and launch vectors are
identical.400physical exact-corner shots compare placement help off/on with the
same seeds: tier1long shots4→15goals/50, tier4long10→19/50; first-time45/50unchanged
in both tiers. Exact targets isolate keeper tuning, not human conversion/quotas.
Results and reproducible calibrate_placement.py retained.25publisher scenarios:
24pass/one existing full-JDK-only fixture skip. Actual unsigned1030013AAB compiled;
bundletool/static/code1030013/production,118ELF16KB, derived APK, all248frames/35sheets
and exact compiled main/career/finishing runtime pass. Public download checks follow.
Owner signing/Play commit/phone
acceptance pending; minimum stays0until availability and acceptance.

1030012delivery verified: bundle workflow43307506227 and publisher43307488869
succeeded. Anonymous complete AAB/coordinator/signing-helper/uploader downloads
match all local bytes/SHA256. AAB117232260bytes,
39805b189c10f8d751e0e2110156eac05d04a2ef16080892087790105c23d85a;
uploader1.11SHA2569c4c7c7a8f8a5ff1eb3e037cb94260645d973f80bdcf58bcbfdb553bf2876350.
Owner signing/internal commit, actual handset crash acceptance and conditional
minimum activation remain pending. Preserve minimum0through verification.

## 2026-11-12 — World1.0 / 1030012 bounded mobile graphics

Owner reports crash on training entry. Actual installed code/club asked and pending;
no device crash stack yet. A concrete stress defect is reproduced:150000-capacity
training generates77400indices in one chair batch, above Kivy's65535COUNT limit.
Prior tests checked only maximum index VALUE and missed this. All stand batches
now split at24000indices; crowd1024fans => maximum18432indices. Source3965523.
20existing native seat/stadium/celebration/attendance cases pass. The new maximum
training/full-attendance regression initially used a wrong Offer fixture (strings,
not objects); corrected to use a league opponent, then passes. Actual production
start_training entry with10900chairs renders successfully; screenshot inspected.
25publisher cases:24pass/one existing full-JDK-only skip. No assets, saves, physics,
package/key changes. Main/stand/crowd batching only; visible version remains.
Actual1030012AAB built. Bundletool/static/code1030012/production,118ELF16KB,
derived APK, all248frames/35sheets and exact compiled main/stadium runtime pass.
Public delivery results follow. Exact device
crash resolution remains pending owner handset test; keep minimum0until acceptance.

## 2026-11-12 — uploader1.10 fixes owner-observed1030011 release-name400

The prepared name had51characters; Google permits50. Shortened to23characters
and added preflight length validation before signing and before any publish API
edit/upload.25publisher scenarios:24pass/one host full-JDK-only fixture skipped;
50accepted,51/empty rejected with zeroAPIcalls. Original1030011AAB/payload/signing
certificate unchanged. Reuse the already signed bastion AAB/account/key; retry1.10.
Workflow43253335634succeeded and anonymous uploader download matched SHA256
33d0133451f61b8ac09ce0a5a604e0d6799aeb0381d1f373559524c55d012a91.
Owner retry/livecommit pending; do not raise minimum until Play delivery verified.

1030011delivery verified: bundle workflow43251993116 and publisher43251841246
succeeded. Anonymous full AAB/coordinator/signing-helper/uploader downloads match
local SHA256/byte counts. AAB117232041bytes, SHA256
0e7161dfd8997f36841abb3bdb2e5e17857f1ebc4f1eb2e8fb7e9c6fdbee6324.
Uploader1.9SHA25680ad62b16fe5bb4d43619b1c98d2dd22988fda0552cf624cdb8434a1a1f048f2.
Owner bastion signing/internal commit pending; minimum remains0until actual Play
availability/install is verified. No claim that rebuild fixes Play delivery.

## 2026-11-12 — World1.0 / 1030011 rebuild and installed build label

Owner APK Analyzer proves installed1030009, despite Console advertising1030010.
Owner explicitly requests rebuild/commit11. New numeric code1030011; package,
owner certificate, saves and1030010chairs/earlier fixes retained. Entry and Settings
show v1.0 (actual installed versionCode), using Android PackageManager with staged
fallback. Footer width220dp to fit code; bounded labels stay inside the viewport.
14native stadium/seat/update-gate cases pass; staged production footer checked at
1280x591/960x540density1.6 and640x360density1.0; screenshot visually inspected.
Actual new unsigned AAB built.24publisher scenarios:23pass, one existing full-JDK
fixture skip. Minimum stays0during delivery verification; latest may become1030011.
Higher mandatory minimum requires confirmed Play installation/availability. This
rebuild does not establish or promise resolution of Play propagation/account issues.
Bundletool/static World-production/code1030011,118ELF16KB, derived inspection APK,
all248frames/35sheets and exact compiled runtime including the new menu pass.
Public download evidence follows; owner signs/commits on bastion.

1030010public delivery verified: bundle workflow43241501384 and publisher43241431680
succeeded. Anonymous complete downloads of AAB/coordinator/signing helper/uploader
match local SHA256/byte counts. AAB117231830bytes, SHA256
c74b72170da47e7f99a25d1c1514ae61d2482e8ef6ec1f6898293833f49e7bf3.
Uploader1.8SHA2561192051a22a4326ac620642396acccf9b1832834f9ccb093c4e233ebe42b1234.
Owner signs/publishes internally, confirms availability, then activates minimum/latest1030010.

## 2026-11-12 — World1.0 / 1030010 stadium seats

Runtime sourceb9e08908e3147afc531e4a8d80eba449003cea92. Individual permanent
chairs in the home primary colour throughout the ground, including visitors.
Training uses own-club chairs with no spectators/stewards. Three original atlas
bands form a seated torso/thigh/shin pose; scoring fans rise into their existing
cheer frames and return. Original PNGs/current scale, occupancy, aisles and physics
unchanged. Cached chair geometry and bounded4500-fan mesh batches retain GLES
unsigned-short indices.30native stadium/seat/celebration/attendance cases pass;
actual match/training screenshots inspected. Preview fixture initially used Free;
reran explicitly in World.24publisher scenarios:23pass and existing full-JDK fixture
skip on host; actual new pinned AAB payload matches. Android AAB compiled; bundletool/static production/code1030010 checks,118ELF16KB,
derived APK, all248frames/35sheets and exact compiled stadium/portrait/keeper/header
runtime pass. Public download results recorded separately below. Owner-side
signing/Play submission/minimum activation/phone playtest remain pending.

1030009delivery verified: workflows43237779081(bundle) and43237703376(publisher)
succeeded. Anonymous full downloads matched all four local files: AAB117229442bytes,
SHA25676e41903488e56f1a1755551783214a6ab64f85f84ca287dd7d2edbb4f931505;
coordinator285ae4a0254f9ad38fac6bb9c263d5e5580179f34193ba7b1744e9b59182deb2;
uploader1.7SHA25655d323d6b915e916111d9913d6b075289a94405a5b7c12b556eb163e5e6cbdbe.
Owner-side signing/Play commit/update-policy activation/phone validation are pending.

## 2026-11-12 — World1.0 / 1030009 portrait, keeper and header candidate

Runtime source03c076a. Three-column player stats/white-T-shirt passport portrait
and editable name/age/monthly-salary captions. Forward-foreshortened frontal catches
retain physical glove attachment. Real jumping central glove contacts tip the active
ball above the crossbar; new original contact sprite plus existing recovery frames.
Header hold/contact uses the forehead at1.65m. Original240PNGframes unchanged.
14portrait/refinement/creation cases, three responsive save/layout sizes,17combined
native keeper/header/opportunity/difficulty/portrait cases and11asset/opportunity
cases pass. Actual staged screenshots reviewed. Initial tip test fixture missed the
central bound; corrected to an actual central-jump phase, then physical integration
crossed above the bar.24publisher scenarios pass across host and full-JDK Docker runs: the host checks
the actual pinned AAB; Docker checks the disposable real-signing fixture. Each run
skips only the other environment’s unavailable fixture.
Actual combined unsigned AAB built; bundletool/static/World-production/version1.0,
code1030009,118ELF16KB and derived inspection APK pass. All248frames/35sheets
and exact compiled keeper/header/portrait runtime match the staged sources. Owner signing, internal
Play commit, phone acceptance and minimum activation remain owner-side.

## 2026-11-09 — World0.9.39 training touch and estate portrait

Public APK verified HTTP200/attachment:118304435bytes, SHA2569ef4d290b6b24b54913e960c39d1b37a945c2caa5a3b46d6169322b177a88d4f. Workflow42623550381 succeeded. Both original generated PNGs, compiled portrait/selection source and all packed regression checks passed. Temporary transfer branch removed.

Sourcea3bc6943c4dbab5f0643ed84b681ac5db762f4bf; World1026939, existing debug upgrade certificate, API36/min26 arm64. Hide archived friendly calendar rows and old queued friendly paper, preserve earned statistics; national attendance official-only. Training result input precedes stale menu, redraws synchronously and waits for explicit tap rather than2.55s auto-advance. Same press never shoots next; third tap immediately shows summary. Match timing unchanged.

My Assets composes original forecourt/five-outfit atlas with independently best owned house and parked car by unit price. Provided defaults do not add ownership; no unowned car. Collection retains every purchase/gift. Nearest texture regions; cached CoreImage objects retain reload references. Sources/generation provenance in assets/lifestyle/scene/README.md. No0.9.38 finishing/ballistic/price changes; preserve unrelated WIP.

433core cases/3existing skips,235clean-source native cases,19focused cases and165responsive cases/zero findings. First broad UI run found3obsolete expectations (Feedback entry, close-header control time, Argentina call-up requiring an official2027/28 fixture); these were corrected and the complete clean suite passed. New tests exercise stale-menu first tap, six-second wait, immediate third-tap summary, independent best assets/no unowned car, friendly history filtering and queued-report migration. Reviewed final portraits for empty, mixed and highest tiers. Actual APK package/signature,118ELF16KB/ZIP16KB, compiled source and both generated PNG assets verified. Physical Android acceptance and prior official club-history audit remain pending.

## 2026-11-09 — World0.9.38 situational finishing balance

Public APK verified HTTP200/attachment:114461175bytes, SHA2564f029c6c75d27f294ab75eee1b72c381182c29ca04c46d30f8e3968482403f4d. Workflow42614504702 succeeded. Compiled tuning/neutral controls and all packed regression checks passed. Temporary transfer branch removed.

Sourcef6fab585f803264a5511ae63a16c3894911f5b7f; World1026938, existing debug upgrade certificate, API36/min26 arm64. Pure finishing profile: penalties*.60aim/*2.2time/+180mskeeper/error*2.5; one-on-ones*.80/*1.5/+90ms/*1.6; close headers*.95/*1.12/+15ms/*1.08, smooth7–10m fade. Full focus-time bonus stays unscaled. No change to marker target, launch solver, save/collision geometry, tier differences or chance frequencies; preserve unrelated WIP.

428core cases/3existing skips and17clean-source native cases passed.2400paired physical shots with fixed target/seed pairs: top keeper penalties15%→72.5%, one-on-ones23.3%→53.3%, close headers40%→44.2%; tier4:21.7%→77.5%,37.5%→71.7%,60.8%→63.3%. Distant headers and normal shots retain identical outcome counts. Targets bypass marker/timer skill; these are controlled comparisons, not human rates. Native tests prove launch velocities unchanged and earned bonuses retained. Actual APK package/signature,118ELF16KB/ZIP16KB and compiled tuning/runtime source checks verified. Physical handset test and prior official club-history audit remain pending.

## 2026-11-09 — World0.9.37 feedback button

Public APK verified HTTP200/attachment:114459739bytes, SHA256a0825de09bb30ad08c250a82aef558c258b26ddacf8267ce1403de605effda42. Workflow42607706948 succeeded. Compiled feedback mailto recipient/subject and all packed regression checks passed. Temporary transfer branch removed.

Source9cd4eeae721ede68c0ad41fd59c1c57c415e2b81; World1026937, existing debug upgrade certificate, API36/min26 arm64. Feedback in entry/hub/compact menu; spare normal-header space preserves existing action positions/alignment. Android UI-thread ACTION_SENDTO opens an email draft to public support; user sends manually, no automatic submission or attachments. Missing-handler fallback is localized, copyable and measured to fit; nine-language labels. Gameplay/save/physics modules unchanged.

7clean-source native cases passed, including mocked Android UI-thread intent/recipient/subject, actual menu touch, no-handler main-clock callback, copying fallback, entry access and main-menu bounds.12fallback layouts across4languages/3sizes fit their text/buttons;99responsive cases/zero findings. Reviewed native screenshots. Actual APK package/signature,118ELF16KB/ZIP16KB and packed compiled-source/public-contact checks verified. Physical Android mail-client/handset acceptance remains pending; prior official club-history audit limits remain.

## 2026-11-07 — World0.9.36 removes national friendlies

Public APK verified HTTP200/attachment:114456099bytes, SHA256f3f342dd0b5c543e59add912fc8d5c131e4c079d67e46e364e56a94b9b617f0d. Delivery workflow42418877562 succeeded. Packed source, legacy migration and official-tournament preservation checks passed. Temporary transfer branch removed.

Source cb2f7fd9036fabea7f5f6132bca2385bbdbd85c5 (runtime identical to87583c5; later changes isolate unit fixtures from random injury rolls). No friendly generation, selection or upcoming-calendar rows. Book reload/scheduling drops unplayed legacy friendlies; completed results/caps/goals and official tournaments are preserved. Legacy Free random-national substitution removed. Explicit already-started legacy result completion remains compatible.

The full regression exposed a prior injury-calendar marker bug: completed team fixtures missed personally were marked unplayed. Separate player_played from played and repair0.9.35 absence entries on load; no change to injury risk or personal stats. Training/calendar/transfer unit fixtures now explicitly suppress random new injuries; dedicated injury probability/distribution/recovery cases remain enabled.426core cases/3existing skips,70targeted logic cases and13clean native UI/training cases passed. Existing dashboard layout/art is unchanged. Actual APK signature/package/API36/min26/118ELF16KB/ZIP16KB and packed runtime migration checks verified. Physical handset test and prior full official club-history audit remain pending.

## 2026-11-07 — World0.9.35 dashboard, lifestyle and short injuries

Final public download verified HTTP200/attachment:114458343bytes, SHA2567310fdfb79fd245c94dc096b06bc229db2e130931a542cfada9721c81267aef1, workflow42415727191 succeeded. Source07ed486b63d7925453052c81470e1d4fbeef347e matches packed runtime. All final payload checks passed, including compiled injury absence/save/reload and no personal credit. Temporary transfer branch removed.

Source 07ed486b63d7925453052c81470e1d4fbeef347e; World1026935, existing debug upgrade certificate, API36/min26 arm64. Restore original player/club and training/play rows, equal dimensions/columns; proportional measured season fields, Lifestyle on hub. Separate shopping and owned-assets catalogues; no club-studio phrase. Saved short injury risk1–3% per completed appearance, six names,1–3 missed fixtures; simulate full team budget, preserve personal appearances/form/trust/attributes and count recovery once per fixture. Preserve physics and unrelated WIP.

422core cases/3existing skips,222clean native cases and13targeted native cases;231responsive cases/zero findings and66final hub cases/zero findings. All season labels, including numbers/captions/league, use measured font fitting after a separate short-phone text-height check found clipping missed by the initial shortened-label audit. Initial UI failures were the old expected button count; added Lifestyle raises that count by one. Short panels required measured single-line variants for stats and the lifestyle salary summary. Screenshots reviewed. Actual APK package/signature/version,118ELF16KB and ZIP16KB verified; packed source/data/runtime injury checks are retained in release evidence. Physical handset test pending; historical official-table audit limits from0.9.34 remain.

## 2026-11-07 — World0.9.34 career expansion

Public download HTTP200/attachment verified:114450183bytes, SHA256356b29d04ee8504991757d2977e9ef7918fec87348507c6a13f3fbb373a6e43b. Workflow42387120450 succeeded. Public installer attachment exactly matches the locally checked file. Final packed source/PNG and all career/competition payload checks passed. Temporary transfer branch removed.

Source f4e30b6407d16c7953026dba22e8dfbc1899c3e7; World1026934, existing debug upgrade certificate, API36/min26 arm64. Contracts and16 illustrated purchases, ageing/retirement, stochastic authoritative aim, revised budgets, club/league prestige, favourite-club offers, career records and additive owner-run bastion installer. Dashboard/coach/title celebrations and crowd refinements. Preserve physics, aliases and unrelated WIP.

418 core cases/3 existing skips,220 native cases and9 final expansion cases passed.396 responsive cases/zero findings; fixed catalogue header height. Screenshot review caught Continue behind the stadium: move retained button canvas above the new scene, native assertion/touch and refreshed screenshot confirm the correction. Rebuilt actual APK and verified package/version/signature,118 ELF16KB andZIP16KB; packed source/data checks recorded separately. Physical Android playtest pending. Five-season official final tables remain incomplete:499 game identities matched,301 five-season results-derived presets; deductions/phases/tie-break verification remains. Installer hashes/syntax verified, server not deployed from cloud.

## 2026-11-06 — World0.9.33 retro scenes and collective titles

Source70214d938564416786c716f9c58b5bd855715449; World APK1026933, existing debug upgrade certificate, API36/min26 arm64. Original ball/fan/trophy sprites, performance-based frozen attendance and top-down home/away filling. Eleven-player own-supporter trophy celebration followed by persistent once-only coach talk; merge due weekly focus choices. Preserve physics, approved player/keeper art, training gates and unrelated WIP.

407core/3existing skips,211native,4clean-staged World scene cases,231responsive/0findings and54nine-language special-talk layouts/0findings. Actual APK compiled modules and scene PNGs, packed title reload,118ELF16KB,ZIP16KB,package/version/certificate verified. Software-renderer measurement:1953visible fans/two meshes/~1.85ms update/zero texture allocations during300updates; no handset performance claim. Physical Android test pending. Public QA APK HTTP200/attachment/109591271bytes/SHA256174072446e131e0f99bb80e6368149b0e19659ecb15b2e1eaca2552060916adf matched the tested binary; delivery workflow42307217085 succeeded; temporary transfer branch removed.

### 0.9.25 public attachment verified

Workflow42123459717 succeeded. Unauthenticated public download matched all
107486979 local APK bytes and SHA256d946c4d1404c3f1e2cfa5306cefdf4f7bba1909f370275368ddd3891cc6cb406.
Content-Disposition is attachment. Public club/stadium audit,990-case responsive
report and saved suggestion list also matched the reviewed local bytes.
Evidence:RELEASE_0.9.25_download.json. Physical handset acceptance remains pending.

## 2026-11-05 — World 0.9.25 club cards and home-ground supporters

Removed the baked-in splash by clemir credit using an image edit; logo, tagline
and existing splash fonts/flow retained. Added coloured club tiles to normal and
compact hubs, with a secondary-colour stripe and readable foreground. Touch opens
founded year, ground/capacity, sourced historical titles and separately observed
career trophies (excluding personal Golden Boots). Facts follow stable club UID,
not editor aliases.15 references have no verified historical honours: show Not
available, never invent a zero or championship. Unknown fictional identities show
unavailable facts and use an explicitly separate bounded venue model.

Added378 source/revision-pinned club profiles: foundation, stadium and capacity
all covered;363 have parsed/reviewed historical records.26 supporter group names
verified against source articles; elsewhere the away banner uses the club display
name, without asserting that no fan group exists. Supplementary local-language
honours and two venue capacity references are pinned in reviewed overrides.
The build parser excludes runner-up/promotion/individual records and ambiguous
bare Winners labels; preserves genuine Promozione league titles. Exact offline
rebuild checked against the cached source snapshot. No source prose/network at
runtime. Public profile JSON explicitly allowed in staging and tested bytewise.

Home fixture UID controls venue capacity and both supporter palettes, including
when the player is away. Stand rows scale with capacity, with a separate curved
upper deck and concourse strictly above40000. Lower behind-goal screen-left block
contains away supporters and a group/club banner; all other seats use home colours.
Mesh batches carry home/away tags, with at most56 batches, cache invalidation on
fixture/kit/banner changes, and no draw of fans/banner during training. Goal report
hooks cover player and AI goals; only the scoring side jumps for2.35seconds.
Same-side skin/shirt motion, expiration and duplicate-goal guards tested.

384 core cases passed. Full native suite ran190 cases: two old52dp minima exposed
new compact club tile at48dp; raised header/tile to52dp. Nine affected/new tests
passed on rerun; initial16 targeted scene/navigation/kit/geometry cases passed.
19 final parser/profile/staging/edition checks passed, including JSON staging guard.
Expanded30-view responsive matrix:990 cases, zero findings. Club/hub66 cases rerun
after final card/stripe/height changes, zero findings. Actual1280x591 hub/card,
one/two-deck venues, banner and separate goal previews inspected. Physical Android
acceptance pending; no physics, scoring budget, save schema or server change.

First candidate lacked club_profiles.json due explicit staging allowlist; actual
APK check caught it. Added public asset to allowlist and staging regression, then
rebuilt from a fresh stage with fail-fast shell. Final actual APK source/data/font/
image checks, profile/40k rule, saves, competitions, safety, DEBUG upgrade signing
and118 ELF/ZIP16KB checks passed. Unrelated root WIP excluded.

### 0.9.24 public attachment verified

Workflow42091290777 succeeded. Unauthenticated public APK download matched all
107428595 local bytes and SHA25603657e56bcef65904c71297ebd6a5540fc2f0404ab5d3afd5501e71da0b1c5a8.
Attachment headers, public378-club colour audit and saved suggestion list were
verified. Evidence:RELEASE_0.9.24_download.json. Physical handset acceptance pending.

### 0.9.24 actual candidate verified

All actual APK checks passed:378 UID-bound palettes and explicit Vitória red/black,
exact runtime/data/font/artwork bytes, competition/progression/save/safety smokes,
existing DEBUG signature, API36/arm64 and118 ELF libraries/ZIP16KB alignment.
Initial verification failed creating a temporary directory (container ENOSPC).
Removed only generated0.9.22/0.9.23 stage/dev scratch archives after their committed
source/public delivery, preserving evidence and deliverable APK copies; full
candidate verification then passed. APK107428595bytes; SHA256
03657e56bcef65904c71297ebd6a5540fc2f0404ab5d3afd5501e71da0b1c5a8.

## 2026-11-05 — World 0.9.24 club-colour coverage repair

Confirmed Vitória BA UIDf9554f2ce1ab5ff99892 was absent from club_kits.json and
world_clubs.json, so kit_for_club fell through to a name-hashed generic palette.
The current0.9.10 names pack has378 identities but the historical colour file
covered only352. Audited all378 UID/name/provenance associations: no conflicting
assignments,26 missing palettes (Spain6, Italy4, Brazil16). Added all26 from fresh
Wikipedia infobox/revision references with explicit traditional secondary-colour
simplifications for image-overlay colours. Vitória uses red shirt/black secondary,
with white shorts/socks from the referenced home kit. No kit patterns/logos copied.

Also retained a contrasting traditional secondary colour for8 existing all-one-
colour palettes (Casa Pia, Académico Viseu, Amarante, Heidenheim, Le Mans, Athletic,
Figueirense, Barra). Fresh factual source review covered these34 changed rows;
other344 records retain their earlier reviewed values. Stable UID binding remains
independent of editor aliases. Added offline builder completeness/identity guard
against the current names pack, so future extra identities cannot silently omit
colours. New tests verify Vitória in existing saves, home/away scenes and training
after an international appearance, without reimporting aliases.

18 targeted core/name-pack/edition and10 native kit/finishing tests passed.
All378 current names/colour/provenance keys match. Syntax checks passed; actual
native training preview inspected. No gameplay, physics, save or layout change.
Candidate APK and public attachment verification follow. Unrelated WIP excluded.
Physical Android acceptance remains pending.

### 0.9.23 public download verified

Workflow42088992305 succeeded. The unauthenticated public attachment matched all
107427995 local APK bytes and SHA2566ac99368c41e3c13b4d3bd1c04562b36e6b587bf81921f6dccd0e421f7c6f296.
Content-Disposition is attachment; public responsive report and saved suggestions
also matched reviewed local bytes. Evidence:RELEASE_0.9.23_download.json.

### 0.9.23 final verification

375 core tests passed. Full native182-case run:181 passed, one old five-kind
allowlist rejected long_cross. Added long_cross/corner and6.5m minimum header
distances to its regression; the complete60-fixture rerun passed in0.511s. No
runtime change required.144 translated notice combinations and real onside/
trailing actor checks passed. Expanded957-case responsive report has zero findings.
APK exact modules/data/images, seven deliveries, legal release geometry, saves,
progression/competitions, edition/safety, same DEBUG certificate and16KB ELF/ZIP
checks passed. APK107427995bytes, SHA256
6ac99368c41e3c13b4d3bd1c04562b36e6b587bf81921f6dccd0e421f7c6f296.
Physical Android acceptance remains pending.

## 2026-11-05 — World 0.9.23 opportunity and text fixes

Removed expected playing time from match notices. Replaced stacked repeated
messages with a measured compact heading/type/context panel, widened its action,
and synchronously fit the first draw so the text cannot start in an empty clipped
viewport. Tiny notices use smaller measured line spacing; long edited results
retain their scroll fallback. Footer/result text now has explicit screen bounds.

Through balls now include a defending match actor ahead of the receiver at pass
release (goal y=0, keeper is the other opponent), moving behind the runner before
reception. He remains a physical trailing opponent; only the keeper is ahead at
the finish. Penalties and training remain isolated. Added deep wing crosses
(start25m wide/20–26m from the goal line) and corners from the real33.7m/.3m
corner arc, both with animated high delivery and header reception. Seven ordinary
variants share the existing capped opportunity slots. Source/receiver visibility
chooses the mirrored orientation without moving the shot target or changing RNG.

Removed the newspaper photo caption and its reserved band. Story text flows
alongside the photo and expands to the full column immediately below it. All
observed goal minutes, player headline/summary and one-page fallback are retained.

Targeted23 core and18 native tests passed; the added144-case all-nine-language
notice matrix passed after a tiny-screen spacing fix. Initial layout audit flags
were also corrected to compare ScrollView children in window coordinates. Native
1280x591 previews of Portuguese notice, passing defender, deep cross, corner and
caption-free newspaper inspected. Full core/native suites, expanded29-view layout
audit and actual candidate APK verification are running at this source checkpoint.
Physical Android acceptance remains pending. Unrelated root WIP excluded.

### 0.9.22 public download verified

Delivery workflow42083196774 succeeded. Unauthenticated public download matched
all107424967 local APK bytes and SHA25655b0a72984c3d8378c50561d4038ee78d2d30423003094d5306707fa008fc034;
Content-Disposition is attachment. Public responsive report and six-point list
also matched the reviewed local bytes. Evidence:RELEASE_0.9.22_download.json.

### 0.9.22 final verification

Final full native suite:179/179 passed in220.528s; core373/373. Final924 responsive
cases have zero findings, including33 coach cases rerun after compact changes.
Candidate APK checks passed for exact runtime modules/font/image bytes, saves,
progression, competitions, publishing/edition safety, upgrade signature and16KB
ELF/ZIP alignment. Initial APK smoke assertion expected ScorerPressPixel.ttf;
updated verifier to ScorerRetro.ttf and reran successfully. No runtime change was
needed for this obsolete check. QA APK107424967bytes; SHA256
55b0a72984c3d8378c50561d4038ee78d2d30423003094d5306707fa008fc034.
Physical Android acceptance remains pending.

## 2026-11-05 — World 0.9.22 font implementation

Created Scorer Retro as a 645-character TTF with distinct cases, Latin accents,
monospaced digits and licensed symbols. Global label/input/popup/canvas selectors
and newspaper use it; splash fonts and main-menu image remain original. CJK/native
script fallback retained. Unioned contours fix rendering seams seen in the first
native preview. Original font source, licence and generated coverage committed.

Syntax and 373 core tests passed. Initial 178-case native run exposed two tiny
coach layout failures and one obsolete newspaper font assertion. Updated the
assertion and fitted coach headers/paragraphs for tiny viewports; the 12 affected
coach/readability tests passed. New real-widget test verifies labels, editable
names, native fallback and splash/logo exceptions. Full final suite rerun ongoing
at this source checkpoint. Responsive matrix: 924 cases, zero findings; its 33
coach cases were rerun after the final compact adjustment. Actual menu/training/
player/help previews inspected. Android packaging and delivery evidence follow.
Physical handset acceptance remains pending. Unrelated root WIP excluded.

## 2026-11-05 — World 0.9.21 UI simplification

Owner requested values only in Training/Coach Trust, one objectives panel for the
player, and focus controls only within Training. Moved all narrative mechanics to
justified Help (twelve dynamic pages using existing nine-language strings).
Replaced the development/skills tabs with direct player objectives and standalone
trust values, preserving saved trophies/progression and name controls. Training
focus is a context-only stat/selection popup. Trust uses the existing hub value;
compact hubs add its action in an available grid slot.

30 focused core checks passed. Full native178 ran; stale four-page help/compact
button-count assertions corrected, then all9 affected cases passed. Final165-case
changed-view matrix: zero findings. Native touch tests exercise both normal and
compact trust access and focus confinement/locking. Visual English inspection of
player/training/trust/focus/Help. Actual APK source/data, progression/save/competition,
signing and16KB checks passed. Physical Android pending; unrelated root WIP retained.

Delivery note: an abbreviated release target was rejected (422), and the workflow
token could not create the new release (403). The authorized CLI created it using
the full reviewed commit; the failed job was rerun successfully. Public APK bytes,
digest, attachment header, layout report and saved-list downloads were verified.

## 2026-11-05 — World 0.9.20 objectives, focused growth and coach trust

Suggestion points1/2/3 implemented as optional bounded development save extension,
legacy current-season seeding, seasonal objectives/archive and lifetime tracked
milestones. Four focused practice types, persisted partial focus and on-focus XP,
level cap10 and explicit bounded match control effects. Trust changes role/actual
minute windows and chance frequency, retaining trained/morale floors and3maximum.
Corrected no-goal penalties so mandatory practice does not hide prolonged poor form.
Focus/save/XP and transfer failure rollback, once-only completion, neutral new-club
trust, no invented past-season progress, no extra routine coach meetings.

Full core370 passed; final24 focused progression/localisation checks include the
added legacy recognition test (371 unique core cases validated). Full native178
had one stale random-penalty assumption in the division aiming comparison; normal
chance type now fixed in that comparison, final10 affected tests pass. Initial
compact training and large-font Japanese coach fit failures corrected and22
screen checks rerun successfully. Final924-case matrix has zero findings (132
final changed-screen cases merged). New English screens inspected visually.
Actual APK focus/XP/reload/idempotence/role checks plus compiled module/data,
competition, edition, save, signing and16KB checks passed. Physical Android pending.
Unrelated main/test helper/mode WIP kept outside tested APK source.

## 2026-11-05 — World 0.9.19 opportunity sequences

Saved the six-item improvement list; Google Drive unavailable, no upload claimed.
Point5 adds deterministic cross/header, cutback, first-time, rebound and free-kick
plans. Animate delivery/receiver/players/keeper before freezing on exact reception;
aim/power/timer/input unlock then. Preserve chances, PK/duel slots, AI RNG, goal
budget, training isolation and physical finishing. Green receiver marker.
358 core tests passed; native171 run had two obsolete long-shot/all-hard assertions,
corrected and all five relevant cases rerun successfully; final3 sequence checks
passed after preserving defender caps. 66 match/shot responsive cases: zero
findings. 2,880 paired physical attempts all resolved; rebound subset rerun after
blocker placement. Existing 0.20 hard-chance budget remains conservative for the
five-type average. Exact APK bytes/modules/data, signing and16KB checks passed.
Physical Android remains pending. Evidence: RELEASE_0.9.19.md and associated JSON.
Preserved unrelated root main/test-helper/mode WIP.

## 2026-11-05 — World 0.9.18

English default/schema2 preference migration, compact launch notice, gameplay-only
justified help, coach closing paragraph below the portrait. Existing QA certificate,
arm64/API36 and 16KB packaging preserved. 354 core tests and 168 native cases
validated (full native run followed by corrected expectation reruns); 891 responsive
cases plus 33 final Help reruns, zero findings. Physical Android remains pending.
See RELEASE_0.9.18.md and RELEASE_0.9.18_artifacts.json for scope and APK digest.

## 2026-11-04 — World0.9.7: integrated schedules and verified APK

Owner paused country research and requested the APK. Integrated real regular capacities/legs and executable splits for38 countries/76 divisions in NEW careers. Old careers pin their original model and retain fixtures/history/UIDs. Smaller new rosters archive identities; larger rosters add deterministic fictional clubs without consuming reserves. Rank-locked split groups, one-time half points, unequal group endings, Finland final-round venue allocation, undrawn calendar dates, Sweden3v4 access, South African three-club promotion and China/Vietnam direct exchanges are implemented. Broader access/licence/tie clauses remain documented limitations; no full-country certification. Unrelated root WIP excluded.

296core+126nativeKivy=422 tests passed;12 final runtime tests passed. Final APK exact bytecode/data, compiled Austrian split/half-points/save/reload and old-layout load verified alongside prior brackets/call-ups/notice/editor/SAF/352palettes. Same DEBUG certificate, package com.clemir.scorerworld, version0.9.7/code1026907, API36/min26/arm64-v8a, zip16KB and118ELF16KB checks passed. No ads/billing DEX SDK markers. No physical-phone, Play, production signing or server deployment claimed. Exact artifact details: RELEASE_0.9.7_artifacts.json. GitHub delivery run41805028475 succeeded; public attachment downloaded withHTTP200 and exact74118391-byte/SHA256 match (RELEASE_0.9.7_download.json).

Initial tests exposed three historical name/presentation fixture assumptions about original rosters; historical generators/fixtures now explicitly select the original layout. An initial half-point reload fixture overwrote its own save when constructing a helper career; corrected to instantiate without signing/saving, then full and targeted checks passed. Added pending calendar dates before final rebuild. All evidence refers to the final APK, not the earlier build.

## 2026-11-04 — primary rules for Ghana/South Africa and further division reviews

Expanded132→144 records and86→92 countries. Independently downloaded/hash-pinned official NSL Handbook (approved2December2025), both GFA regulations (approved1July2025), current GFA group/date announcements and Zone1A fixture chart. Confirmed South African16/16 home-away leagues and three-club access competition; detailed playoff rules remain separately required. Ghana48-club structure uses8/8/16/16 playing groups but three promotion zones, differing28/30-game schedules, geographic additional relegation, and interim versus final ranking criteria. Added Czech qualified-only title/survival groups and second tier, dated Cypriot29-game second-tier structure, Nigerian20-club top tier/proposed34-club lower field, Algerian32-club partial record, and partial Mongolian/Sri Lankan transitional phases. No unverified proposal or secondary contradiction is marked complete.

Validation:18 targeted tests passed; deterministic generator --check, syntax and git diff --check passed. New regressions cover three-club South African access, Ghana playing groups versus promotion zones/variable demotions, qualified rank cardinalities, pending group counts and Mongolian transition totals. Original GFA fixture image exceeded safe image-decoding dimensions; kept protection enabled and inspected the publisher’s1024px derivative instead. Search results unavailable for one query were not interpreted as absence of rules. No game/career source, APK/version, backend/policy or Play changes. All runtime flags remain not_integrated and global review remains incomplete. Existing unrelated root WIP preserved.

## 2026-11-04 — expanded real-format research checkpoint

Expanded the catalogue to132 records in86 countries; all212 country slots remain indexed. Added Asian, African, American and island structures, current transition exceptions and dated historical structures with explicit current-season review requirements. Primary CPL announcement independently confirms four-team2026 playoffs. Downloaded/hash-pinned FRMF regulations; article15 delegates seasonal playoff details, and the secondary ranking citation does not match primary article53. New sourced second-tier absence exceptions for Gibraltar/San Marino; no under23 or reserve-only league silently becomes a senior Division2. Continued country-source discovery is evidence collection, not completed league review.

Schema now represents qualified-only group stages, unbalanced regular schedules, best-of-three MATCH WINS, directed winner/loser paths, and explicit pending review. Peru2026 second-tier repechage is preserved; all32 outcomes produce two distinct promoted clubs. Colombia’s different Apertura/Finalizacion structures, Uruguay’s Competencia and averaging, Ecuador’s6/4/6 split, MLS wildcard/best-of-three, Canada’s new four-team bracket, Sweden’s3v4 access eliminator and current Asian expansion/contraction clauses remain distinct. No generic playoff is created for an unknown rule. Some sources are contradictory or sparse; those clauses remain unresolved and all runtime flags remain not_integrated. A full blank result grid was found insufficient as schedule evidence, so Kazakhstan’s unverified regular format was downgraded to partial.

Validation:14 targeted tests passed, generator --check and Python syntax passed. Initial conference-model generation exposed a research-helper total of zero for the new scheduled_league type; corrected stored totals, then checks passed. A missing Ethiopian season reference was rejected before writing that batch; retained only the actual pinned general reference and dated the definition accordingly. No app/career source, APK, game version, server/policy or Play changes. Unrelated root badge/mode WIP remains excluded. Full worldwide real-format definition and runtime integration are still incomplete.

## 2026-11-03 — real domestic format definitions

Added a research-only catalogue with62 league records in32 countries (61 regular structures reviewed,1 partial),212 indexed country slots and a sourced no-domestic-league exception for Liechtenstein. Exact seasons and revision/hash-pinned evidence; corrected false discovery identities including defunct leagues, women’s competitions, awards/broadcasters and Ireland/Northern Ireland confusion. Current structures distinguish Wales6/4/6, Finland unequal split legs, Northern Ireland37games, Switzerland/Scotland38, Argentina grouped regular stages, Paraguay rolling relegation averages, Chile’s seven-entrant promotion ladder and Japan’s cross-year season. Norway’s access ladder refined. Unresolved tie/licensing/movement clauses remain explicit; official NIFL retrieval returned403 and was not treated as verified primary evidence.

Validation:7 targeted regression tests passed, deterministic generator --check passed and Python syntax checks passed. Tests reject missing evidence, incorrect totals, overlapping split ranks and lost knockout entrants, and check absence/unknown/runtime separation. No game source, saves, APK, version, policy/server or Play change. Unrelated root badge/mode WIP preserved. Country-wide real-format implementation remains incomplete.

## 2026-11-02 — World0.9.4 universal two-tier model

Owner requested two active divisions worldwide,10 rotating third-tier reserve names, free signing when the player's club exits Division2. Implemented FIFO queues, frozen3-club boundaries, free-agent persistence/offers/signing, calendar stop/native Agent routing, new-season cup eligibility, legacy save migration/backup, hidden UID archives, two-tier country browsing and updated names JSON.245core+119nativeKivy unique passes; details RELEASE_0.9.4.md. Actual0.9.3 fixture files preserve history and first-write backup. Initial test failures exposed stale multi-tier expectations and then an actual calendar loop assuming club.uid after release; fixed and covered through the real UI Play flow. Fixed won/drawn/lost rollover reset. Rebuilt final debug APK and verified compiled release/export/signing flow, exact source/data, package/key/118ELF16KB. No real handset, Console or backend deployment. Unrelated badge/mode WIP excluded.

## 2026-11-02 — corrected real-name division mapping

Owner reported real club names in the wrong divisions. Root cause: old pack generator cycled a historical reference catalogue; it never checked current league membership, and repeated clubs across slots. New offline generator uses a revision/hash-pinned manifest of792 real teams across29 divisions, European2026/27 and Brazil/Argentina2026.494 unique represented clubs are selected within the actual tier; current game capacity and saved progression stay unchanged. Reserve/homonym identity is explicit. Matching top leagues independently to OpenFootball passed for seven countries. Source rosters remain July2026; stale aliases from the entire previous combined pack are replaced/reset, never left attached to another club.

Five targeted tests passed: all494 initial UID/tier mappings and unique identities; concrete regression cases and distinct San Martín/reserve clubs; old-pack upgrade, real importer/apply/backup/reload with only display_aliases changing and player fallback resets; ambiguous alias rejection; deterministic output when club lists are reversed. Exact artifact details: docs/data/name-packs/division-validation.json. Native Android not newly tested; World0.9.3’s existing v1 editor supports the pack. A reproducibility check exposed initial club-list order dependence in the offline generator; slot assignment now uses the pinned catalogue order and an independently rebuilt file matches byte-for-byte. No APK, game/physics, policy/backend or unrelated WIP changes.

## 2026-11-01 — World0.9.3 direct leaderboard and menu cleanup

Removed main/start Privacy and scorer Global buttons. Public leaderboard reads without guardian/legal detour; publication remains separate. Report/block open for viewers. Help > Settings retains career export/import. JSON names attachment published through a manual repo workflow after local release upload credentials failed; first workflow assumed a release existed after the failed CLI creation rolled it back. Corrected create-before-upload and verified final attachment disposition/hash. No secrets read or sent.

232 unique core +116 unique native Kivy passes, including initial expected-button-count updates and deterministic domestic-rollover fixture correction; details in RELEASE_0.9.3.md. Actual debug APK/source/labels/notice gate/competition reload/118ELF16KB verified. Live read-only scoped records endpoint200/schema3/zero rows. No device/Play or live policy deployment claimed. Unrelated badge/mode WIP excluded.

## 2026-11-01 — World 0.9.2 translated agreement actions

Owner correction: Portuguese startup buttons CONCORDO / NÃO CONCORDO, equivalent translated agreement actions in all nine UI languages. Matching notice/policy wording; disagree still immediately exits, agree continues. Existing client-request removal, editor and gameplay retained. 52 targeted tests passed (25 localization/public pages,6 editions,13 publication safety,8 native Kivy including Portuguese button/exit layouts and all notice translations). APK debug rebuilt; actual compiled source/labels/Portuguese catalogue, usage gate, competition reload, signing/package and118ELF/16KB checks. No real handset, Console or live server deployment claimed. Unrelated WIP excluded.

## 2026-11-01 — World 0.9.1 startup/editor/height balance

Owner superseded the previous client privacy-request workflow: launch notice only, OK continues, NOT OK immediately exits/discards pending unsent counts. Direct hub editor and top import action. Keeper height balance corrected in matches and training; physical aim/ball/goal/collider dimensions and competition engine preserved. See RELEASE_0.9.1.md and data/shot_heights_0.9.1.json.

Validation: 232 core + 114 unique native Kivy UI = 346 passing tests. First core run used a venv missing fontTools/cryptography; rerun with installed host dependencies passed. First UI run had two new test-fixture/assertion failures (mandatory flag overridden by isolation fixture; wrong expected editor route); corrected and both targeted tests passed. 1,800 paired actual fixed-step shots per build. Android debug package built; actual compiled source/modules, notice gate/rejection, career/competition reload, package/code/certificate, 118ELF/16KB verified. Removed privacy_requests module absent from APK. No real Android/Play acceptance or live server deployment claimed. Unrelated badge/mode-state WIP excluded.

# Build log

## Packaging snapshot, 23/10/2026
- Google Drive v006 used as baseline.
- Verified local `python3 -m py_compile` succeeds.
- Android SDK/NDK and APK/AAB compilation: **not executed or verified**.
- Hardware smoke tests: **not executed**.

## Next run
Codex should append the exact commands, logs, test results and blockers for each task.

## 2026-10-23 — phase 1, source candidate 0.6.1

Read AGENTS.md, README.md, ROADMAP.md and FIRST_CODEX_TASK.md before edits.
Validated archive paths and baseline/main SHA256 against SOURCE_CHECKSUM.txt.
Imported starter in commit 957f7c5; retained Scorer history and a recoverable
Git bundle outside the checkout at /workspace/scorer-before-striker.bundle.

Changes: moved original simulation/career definitions into a headless career.py;
main.py keeps the original Kivy UI and imports its required core symbols. Added
private Android saves, legacy migration, atomic writes with visible error,
generic default Alex Silva, 13 regression/security tests, pinned host dependencies,
workspace Buildozer cache helper and candidate API 36/arm64/NDK28c settings.
No baseline changes; existing saved names remain unchanged.

Commands/results:
- `python3 -m py_compile main.py career.py tools/build_android.py`: PASS.
- `python3 -m unittest discover -s tests -v`: 13 tests PASS, none skipped.
  Covers imports without Kivy, career training/match progress, restart, v1/v2
  saves, invalid JSON, unknown migration versions, no-overwrite migration,
  write failure preserving previous save, private Android path via simulated App,
  FREE boundary, provider failure and save tampering unable to unlock WORLD.
- Installed Buildozer 1.5.0, Kivy 2.3.1, Cython 0.29.37 in external venv.
- `buildozer -v android debug`: FAILED on missing distutils with Python 3.12.
  Installed setuptools 75.8.2, retried: FAILED on read-only ~/.buildozer.
- `python tools/build_android.py -v android debug`: cache corrected; FAILED
  prerequisite check: Java compiler (javac) not found. Retried after spec update,
  same confirmed prerequisite. No native compilation or APK/AAB generated.
- `apt-cache policy ...`: system metadata has no candidates for checked build
  packages; system locations are read-only. Full build image still required.
- Kivy desktop smoke: initial KIVY_HOME parent missing, created parent and retried.
  App opened with SDL2/Mesa llvmpipe, ran event loop and stopped via Clock after
  two seconds, exit 0 and UI_STARTUP_OK. Not an Android/touchscreen test.
- `pyflakes main.py career.py tests tools`: initial unused imports cleaned.
  Remaining diagnostic is original UI local variable `score` assigned but unused;
  no undefined-name diagnostics. Full lint is therefore not a clean pass.
- Read-only upstream p4a clone at pinned commit: NDK recommendation 28c, AGP
  8.11.0, Python recipe 3.14.2, Kivy 2.3.1. Compatibility and 16 KB compliance
  remain UNVERIFIED until native build/output/device tests.

Security audit: no payments enabled; FREE remains fail closed. Baseline excluded
from APK sources to avoid shipping its personal default name. Original optional
Wikipedia badge fetch/image URLs and generated sound/cache paths require follow-up
review. Static reference manifest does not prove actual package policy. No secret
or signing key created. This is not a complete security certification.

Next task: provide full Android build prerequisites, generate debug APK, verify
manifest/ELF alignment and install on real Android hardware before ad-board work.

## 2026-10-23 — resolve cloud toolchain blockers (0.6.1 tooling revision)

No game logic, baseline, payments or advertisements changed in this revision.
The managed Docker daemon was healthy (28.4.0, vfs). Prepared a Docker toolchain
instead of requiring writes to the read-only host system. Added tools/android/
Dockerfile, setup.sh, install_sdk.sh and run.sh; tools/build_android.py now omits
environment values on failures. Added a security regression test for that behaviour.

Evidence and corrections:
- Pulled Python 3.12 Bookworm image with verified Docker digest; pinned digest
  14a4933e6cef421424f7a66d89a3f4eafcbd0d90e0a822251f298e05132dc735.
- Docker build initially needed writable buildx state: BUILDX_CONFIG moved under
  /workspace/striker-android-build/buildx, preserving registry configuration.
- Built image with JDK 17.0.20.1, autoconf 2.71, cmake 3.25.1, compilers and tools.
  Verified executable presence and `pip check` (no broken requirements).
- Mounted session/system CA bundles; refreshed Java trust store outside image.
  Git initially failed TLS trust; added GIT_SSL_CAINFO/CURL_CA_BUNDLE and reran
  with verification enabled. Python user installation initially tried /.local;
  set PYTHONUSERBASE to writable cache and added its scripts directory to PATH.
- Retrieved official SDK metadata using TLS and verified package archives against
  published checksums. Owner accepted Android SDK licence explicitly in chat.
  Latest command line tools changed --licenses semantics; used pinned CLI 19.0.
  Installed API 36, build-tools 36.0.0, platform-tools 37.0.1 and NDK r28c.
  sdkmanager install exited 0. A repeat run of `bash tools/android/setup.sh`
  completed with exit 0, including all 14 tests passing and SDK already installed.
- Buildozer's initial automatic update also installed build-tools 37.0.0. Disabled
  future broad automatic updates via APP_ANDROID_SKIP_UPDATE. No claim that
  native/Gradle build tool selection has been verified.
- Native preparation advanced to SDL2_image/libjxl recursive submodules. Build
  FAILED: proxy CONNECT 403 for https://skia.googlesource.com/skcms. No APK/AAB.
  Partial libjxl submodules need `git submodule update --init --recursive` after
  policy activation; do not silently skip this just because directory exists.
- Current tests: `python3 -m unittest discover -s tests -v`: 14 PASS, no skips.
  Shell syntax checks and Python compilation of build wrapper PASS.
- Saved additive custom network domains (preserving presets): drive.google.com,
  drive.usercontent.google.com, www.openssl.org, openssl.org,
  download.savannah.gnu.org, maven.google.com, skia.googlesource.com.
  These are DRAFT settings, not proven enforced. User review/save/publication
  is required before the blocked operation can be retried meaningfully.
- Drive download still returned 403 before policy activation. No Drive connector,
  runtime identity or secrets are configured. A network allowlist cannot provide
  private-account access; no OAuth credentials were requested or invented.

No hardware USB devices or /dev/kvm are exposed by this machine. Android hardware
acceptance, final manifest checks, ELF 16 KB alignment, signed release generation
and Drive upload remain pending. See ANDROID_BUILD.md for exact resume commands.

Additional tool verification:
- NDK clang 19.0.1 executes; sdkmanager --list_installed confirms the package
  versions above. `adb devices -l` initially failed because numeric Docker user
  had no writable account home. Added an unprivileged passwd account in the
  image with home /work/cache/user (without setting HOME). Retest exited 0;
  daemon started and device list is empty.
- A setup rerun overlapped an in-progress edit of install_sdk.sh and exited 2
  while reading the changing script. Validated the stable script with bash -n
  and reran the installer successfully. Final full setup rerun is recorded in
  /workspace/striker-android-build/cache/setup-final.log.
- The SDK setup now checks the SHA256 of the licence text accepted in this chat;
  changed licence terms stop setup for owner review rather than being accepted
  silently. This is a licence-change guard, not an artifact checksum override.

## 2026-10-23 — after user publication: real debug APK build

Runtime status now reports configuration revision 2 and the published custom
hosts. Actual Git read to skia.googlesource.com/skcms succeeded (exit 0); the
network policy state itself is reported unknown, so readiness is based on that
specific successful operation. Completed libjxl's pinned recursive submodules.
No second publication was required for the previous network blocker.

Native build completed host Python 3.14.2, libffi, OpenSSL, Python arm64, SDL,
pyjnius and Kivy. Source build fallback warnings about missing prebuilt wheels
were expected and did not establish failure. Actual later failures and fixes:
- Isolated pip lost certificate environment variables. Added a supported pip
  cert configuration at cache/user/.config/pip/pip.conf, preserving other options.
  Test without PIP_CERT/SSL_CERT_FILE/REQUESTS_CA_BUNDLE successfully fetched the
  setuptools index. No trusted-host flag or TLS bypass used.
- Gradle Java did not consume HTTP_PROXY/HTTPS_PROXY. Added Java proxy properties.
  First derived them outside Docker, where hostname proxy is outer-only; that
  failed UnknownHostException. Corrected derivation inside Docker using its
  reachable inherited proxy. Gradle then downloaded and built successfully.
- Added four configuration/security tests: pip settings preserved/repeatable,
  invalid pip config preserved, Java uses managed proxy, and proxy credentials
  are rejected without disclosure. Total: 18 PASS on Python 3.12 and built
  host Python 3.14.2; no skips.

First generated APK failed static native checks: chardet 7.7.0 bundled 17 Linux
x86_64 extensions (e_machine 62), also with insufficient 16 KB alignment. Rejected
that artifact. Pinned chardet==5.2.0 (pure Python) in buildozer.spec. A naive
rebuild retained the stale distribution because p4a matches recipe names, not
versions. Removed only the generated dist and stale chardet target files while
retaining native build caches. Packaging venv then exposed two pip versions
(25.3/26.2.2 metadata) and failed BuildDependencyInstallError import; recreated
only that generated venv. Rebuild exited 0, producing corrected debug APK.

Final artifact:
- bin/striker-0.6.1-arm64-v8a-debug.apk (20,761,765 bytes)
- SHA256 00211bb14422a9eeff5b4ab6ba3ea227b2e174c490fee7dbfdca215b61586a2b
- `apksigner verify --verbose`: PASS, v2, one debug signer.
- `zipalign -c -P 16 4`: PASS.
- tools/android/verify_elf_alignment.py: PASS, all 118 ELF files AArch64 and
  LOAD alignment >= 16 KB, including extensions inside compressed libpybundle.so.
- chardet 5.2.0 import and ASCII detection in built host Python: PASS.
- aapt: package com.clemir.striker, version 0.6.1, min SDK 26, target/compile 36,
  native arm64-v8a, landscape, no requested permissions.
- Generated debug manifest has debuggable=true and allowBackup=true. The reference
  release policy is not merged; backup/release policy remains a release gate.
- Earlier repeat packaging warnings about SDL Java patches were checked using
  reverse patch dry runs: both succeeded, proving patches already applied.
- App private payload has 4 entries (career/main/sitecustomize bytecode and p4a
  environment settings); no baseline/tests/tools packaged.

Game logic/baseline unchanged in this revision. No Android device installation,
touch gameplay, lifecycle persistence or 16 KB device execution was performed.
No AAB, release signing, public publication, payments or sponsor work performed.
Next: install corrected debug APK on real Android hardware and execute the
functional acceptance checklist before considering release or ad-board work.

## 2026-10-23 — 0.6.2 responsive menus and exit

Owner reports 0.6.1 runs on an Android phone without crashes; menu text overflow
was observed. This is owner feedback, not a full automated hardware acceptance.
Owner clarified product: FREE has exactly one division, funded exclusively by
stadium advertising; World is a separate paid app with fictional defaults and a
local name editor/importer. Updated AGENTS/ROADMAP and docs/PRODUCT_MODEL.md.
No payments, paid artifact, advertisements or remote name downloads added here.

Changes:
- Added menu_ui.py: native Kivy layouts for offers/hub/training/standings/scorers/
  calendar/agent/world, wrapped labels, adaptive columns, vertical/horizontal
  scrolling, 52 dp touch buttons and fixed navigation header. Compact hub puts
  Play/actions before statistics. Menu tree is retained between frames and only
  rebuilt when career/view state changes. Stadium, simulation and career logic
  remain the original Python/Kivy implementation.
- main.py routes real widget touches before game shooting, adds save/exit modal,
  prevents simulation advancing while exit confirmation is open, and saves on
  Android pause/stop. A failed explicit save prevents exit. Menus can fit portrait
  windows; gameplay retains landscape. No claim about all possible device/notch
  configurations without device tests.
- career.py reports save success/failure and fixes the pre-existing current_club
  reference in the local rename method. Tests prove edited names/progress survive
  restart. New FREE career division displays fictional Divisão Striker; existing
  saved/custom names remain compatible. FREE menu/action guard hides paid editor
  and World actions; save edits still cannot unlock World.
- buildozer.spec 0.6.2, excludes ui_tests from APK. Development requirements add
  pinned pytest for Kivy's real touch-test helpers. Baseline unchanged.

Validation:
- `python3 -m unittest discover -s tests -v`: 20 PASS, no skips.
- `KIVY_HOME=/workspace/striker-runtime/kivy /workspace/striker-venv/bin/python
  -m unittest discover -s ui_tests -v`: 8 PASS, no skips. Includes 7 menu views
  across 640x360, 800x360, 960x540, 1280x720, 360x800 and 320x240 (42 layout
  combinations), system font scale 1.6, native touch navigation, training/game
  transition, visible Play button, cancel exit, save-before-stop ordering and
  remaining open after save failure. Numeric cells stay within their rows.
- Initial GUI test dependency pytest was missing; installed/pinned it, then reran
  real tests successfully. A first Widget.export_to_png capture did not represent
  live rendering, so inspected actual App event-loop Window screenshots instead.
  Corrected table minimum width to account for cell spacing/card padding so
  trailing numeric columns are reachable by horizontal scrolling.
- Live Linux SDL2/Mesa app opened and produced reviewed screenshots at 960x540,
  640x360 and 360x800. These are desktop renders, not Android store screenshots.
  UI result logs/screenshots: /workspace/striker-runtime/menu-tests/.
- Python syntax, pyflakes on menu_ui/ui_tests/changed career tests and diff
  whitespace: PASS. No claim that all legacy main.py lint warnings were fixed.
- `bash tools/android/run.sh python tools/build_android.py -v android debug`:
  PASS, actual native APK, final log cache/build-0.6.2-final.log.
- Actual final APK: signature v2 PASS, `zipalign -c -P 16 4` PASS; all 118 bundled
  ELF libraries AArch64 with LOAD alignment >=16 KB PASS. Development signing
  certificate matches 0.6.1; package/application ID retained for in-place updates.
- APK private payload includes career/main/menu_ui/sitecustomize bytecode and p4a
  environment file, with no tests/baseline/tools.

Artifact: bin/striker-0.6.2-arm64-v8a-debug.apk (20,774,313 bytes)
SHA256: 87b55632503d132a357fec2c3583d29715d2d3b23d02b9c51623b9859327b387
Copy: /workspace/deliverables/Striker-0.6.2-arm64-debug.apk

Limitations: new APK not yet tested on the owner's phone. No release APK/AAB,
public distribution, real advertisements or paid World application. Existing
World simulation has full-depth European pyramids but only one tier in many
other countries; a true worldwide all-divisions product and safe name importer
remain future tasks. Next: owner tests update-in-place, scrolling/text, exit and
career recovery; then offline fictional stadium advertising.

## 0.6.3 — SCORER, splash e auditoria de UI/persistência

Pedido do proprietário: Sair exclusivamente no menu principal, corrigir texto
sobreposto do resultado, splash com jogador a rematar/crédito clemir e auditoria.
Nome corrigido pelo proprietário para SCORER, texto do splash em inglês.

Ficheiros: `main.py`, `menu_ui.py`, `career.py`, `buildozer.spec`,
`assets/splash.png`, testes de carreira e Kivy, README e relatório
`docs/AUDIT_0.6.3.md`. Motor e baseline preservados.

Validação: py_compile dos três módulos, 21 testes de carreira/build/segurança e
10 testes Kivy aprovados. Captura da janela Kivy 1280×589 inspecionada após
corrigir a configuração inicial do tamanho da janela do capturador (primeira
captura tinha viewport de 800 px). Não confundir com teste Android.
Compilação real: `bash tools/android/run.sh python tools/build_android.py -v android debug`.
Assinatura v2 debug, ZIP 16 KB e todos os 118 ELF AArch64 alinhados a 16 KB.
Mesmo certificado e applicationId da beta 0.6.2. Sem permissões solicitadas.
Logs completos no ambiente: `/workspace/striker-runtime/build-0.6.3-final.log`,
`verify-0.6.3.log`; próxima tarefa é validar esta atualização no telemóvel,
percorrendo splash, menu, treino, oportunidade, resultado e gravação/reabertura.
Sem validação física de 0.6.3, sem AAB ou assinatura release nesta etapa.

## 0.6.4 — menu sem scroll, caixas compactas e ícone

Feedback do proprietário: caixas demasiado grandes, menu principal com scroll,
crédito clemir insuficiente; pedido adicional de ícone profissional.

Alterados `menu_ui.py`, `ui_tests/test_menus.py`, `assets/splash.png`, novo
`assets/icon.png`, `buildozer.spec`, README, AGENTS e `docs/UI_0.6.4.md`.
Main menu passa a dashboard sem ScrollView, com seis ações simultaneamente
visíveis. Painel final dimensionado ao conteúdo, botão de largura limitada.
Splash e ícone originais gerados para esta aplicação; splash inclui a assinatura
«SCORER by clemir» com destaque. Simulação, baseline e saves não alterados.

Verificação: py_compile; 21 testes sem interface e 11 testes Kivy aprovados.
Novo teste cobre seis combinações de ecrã/densidade, limites dos botões,
alvos de pelo menos 48 dp, ausência de sobreposição e ausência de ScrollView.
Capturas reais da janela Kivy 1280×589/densidade 1,64 inspecionadas: identificada
e corrigida concatenação de linhas de estatísticas e ordem dos campos durante
mudança de dimensões. Última captura do menu: `scorer-064-hub0003.png` no
runtime; captura do painel: `scorer-064-match0001.png`. Não são capturas Android.

Build real: `bash tools/android/run.sh python tools/build_android.py -v android debug`.
Assinatura v2 debug válida, mesmo certificado das betas anteriores; ZIP e 118 ELF
AArch64 com alinhamento 16 KB verificados. API 36/mínimo 26, mesmo applicationId.
Hashes dos recursos reais Android `res/mipmap/icon.png` e presplash e respetivos
assets privados conferem com as imagens fontes. Nenhuma chave de assinatura
incluída no APK. SHA-256 do APK:
`de061bd542b89488ede8f4161be609ed2e8a85caaec6409f2fe7d83d2bef1363`.
Logs locais `build-0.6.4.log` e `verify-0.6.4.log` em
`/workspace/striker-runtime`. Próximo: instalar atualização no telemóvel e validar
menu, ícone, splash e transições treino/oportunidade/resultado. Sem AAB ou build
release de loja nesta etapa; teste físico de 0.6.4 pendente.

## 0.6.5 — splash persistente, novo/carregar e FREE explícito

Feedback: splash desaparecia na rotação, faltava escolha de carreira ao abrir,
nome «England Division 4» sugeria várias divisões e menu precisava de redesign.

Alterados: main.py, career.py, menu_ui.py, assets/menu_stadium.png,
buildozer.spec, suites core/Kivy, README, AGENTS e docs/UI_0.6.5.md.
Detalhes e referência visual consultada (imagem de menu FIFA 2000) no relatório.
Não foi integrado código ou material de outros jogos. Novo fundo original.

25 testes sem interface + 15 Kivy aprovados (40). Comandos:
`python3 -m py_compile career.py main.py menu_ui.py`;
`python3 -m unittest discover -s tests -v`;
`KIVY_HOME=/workspace/striker-runtime/kivy /workspace/striker-venv/bin/python -m unittest discover -s ui_tests -v`.
Logs core/UI em `/tmp/scorer-065-core-final.log` e
`/tmp/scorer-065-ui-final.log`. Cobrem persistência do splash através de tempo,
rotação e toque real, carregamento explícito, ausência de autogravação antes da
escolha, confirmação/cancelamento/backup atómico, saves inválidos, transferência
FREE e duas épocas mantendo uma única liga, migração do nome sem perder progresso.

Capturas reais da janela Kivy 1280×589/densidade 1,64 inspecionadas: menu,
entrada e splash, em `/workspace/striker-runtime/scorer-065-*.png`.
Não equivalem a capturas nem testes Android. Baseline SHA-256 permanece
fed211d2ec63fe0275390b13ed4a1bcfcd18fa61238460b04b67d80ebca6205b.

Build real: `bash tools/android/run.sh python tools/build_android.py -v android debug`.
Logs `build-0.6.5.log` e `verify-0.6.5.log` no runtime. Assinatura v2 debug válida,
mesmo certificado, versão 0.6.5/API 36/mínimo 26/arm64. ZIP alinhado a 16 KB e
118 ELF AArch64 verificados. Ícone, presplash e assets (incluindo fundo novo)
conferem com fontes; sem saves, backups ou chaves de assinatura no pacote.
SHA-256 APK: 2334c6447665e711edf91d2f6cd70bd34b9acd360f824ec130adce21b2dca7e4.

Próximo: testar no telemóvel rotação/espera sem tocar no splash, toque para
Novo jogo/Carregar jogo e carregamento da carreira anterior, nome Liga Scorer e
navegação do menu. Sem teste físico desta versão, AAB ou assinatura release.

## 0.6.6 — nome do jogador, relevo e redução de scroll

Pedido: explicar/remover a imposição de Alex Silva, diminuir by clemir na mesma
posição, botões arredondados com efeito 3D e menos scroll nas páginas do jogo.

Alterados `career.py`, `main.py`, `menu_ui.py`, `assets/splash.png`,
`buildozer.spec`, testes, README, AGENTS e `docs/UI_0.6.6.md`.
Novo jogo exige nome antes do contrato; botão Jogador altera carreira existente
sem reiniciar. Renomeia também o marcador, valida nomes/colisões e reverte se a
gravação falhar. Botões partilham cantos arredondados, base, face elevada, brilho
e estado premido. Classificação, marcadores e calendário usam páginas sem
ScrollView, incluindo salto para clube/jogador e alternância de dados, sem
ocultar/remover registos. Cards compactados e propostas em duas colunas.

Verificação: py_compile dos três módulos; 27 testes core/build/segurança e 18 Kivy
aprovados (45). Primeira verificação detetou acesso errado a `.y` numa instrução
RoundedRectangle (API correta é `pos[1]`); corrigido no teste e no brilho do botão.
Suite final e capturas reais da janela Kivy inspecionadas: menu, classificação e
formulário, 1280×589/densidade 1,64. Não são capturas/testes Android.
Logs: `/tmp/scorer-066-core-final.log`, `/tmp/scorer-066-ui-final.log`.

Compilação real: `bash tools/android/run.sh python tools/build_android.py -v android debug`.
Logs runtime `build-0.6.6.log` e `verify-0.6.6.log`. Assinatura v2 válida e mesmo
certificado; versão 0.6.6/API 36/mínimo 26/arm64, ZIP 16 KB e 118 ELF AArch64
alinhados a 16 KB verificados. Ícone, presplash e novo código de perfil/listas
confirmados dentro do APK; sem saves, backups ou chaves privadas incluídos.
SHA-256: fae82e4dea96a491a66fef31cb31f081400a11016938a4208f6f3b7d884ba4b8.
Baseline mantém fed211d2ec63fe0275390b13ed4a1bcfcd18fa61238460b04b67d80ebca6205b.

Próximo: atualizar no telemóvel, alterar nome através de Jogador e verificar a
persistência ao reabrir, teclado, feedback dos botões e navegação por páginas.
Validação física desta versão pendente. Sem AAB ou assinatura release nesta etapa.

## 0.6.7 — alinhamentos e marca tipográfica

Pedido a partir de quatro capturas do proprietário: alinhar textos e melhorar a
fonte de SCORER by clemir. Marca nativa partilhada em Barlow Condensed ExtraBold
Italic + Barlow Regular, incluídas offline com licenças SIL OFL. Ajustados alinhamento
da entrada, identidade/indicadores e números/legendas da época; oportunidade e
resultado centrados. Face/rebordo dos botões alinhados com o centro do texto.
Seta não renderizada na energia do treino substituída por «para».

Ficheiros: menu_ui.py, ui_tests/test_menus.py, assets/fonts (2 TTF e 2 licenças),
buildozer.spec, README, AGENTS e docs/UI_0.6.7.md. Sem alteração do motor, carreira,
saves, arte do splash ou ícone. Fontes originais obtidas do repositório oficial
Google Fonts e redistribuídas sem modificações com a licença.

Verificação: py_compile; 27 testes core/build/segurança + 18 Kivy aprovados (45).
Suite Kivy final em `/tmp/scorer-067-ui-final.log`; core em
`/tmp/scorer-067-core.log`. Inspecionadas capturas reais da janela Kivy de entrada,
menu, treino concluído e oportunidade em 1280×589/densidade 1,64, runtime
`scorer-067-*.png`. Não são capturas Android.

Compilação real com `bash tools/android/run.sh python tools/build_android.py -v android debug`.
Logs `build-0.6.7.log` e `verify-0.6.7.log` em `/workspace/striker-runtime`.
Assinatura v2 válida, mesmo certificado, ZIP alinhado a 16 KB e 118 ELF AArch64
alinhados a 16 KB; Android API 36, mínimo 26. Confirmados hashes de ambas as fontes
e licenças dentro de assets/private.tar; novo BrandMark no bytecode e presplash
inalterado. Sem saves ou chaves privadas no pacote.
SHA-256: 0177f4bb804474b341b02a8b208aa2f8289acf5d30655bdb4e64ffead7297910.

Próximo: validar no telemóvel alinhamentos e renderização das fontes nos quatro
ecrãs enviados pelo proprietário. Versão beta debug, sem teste físico desta
versão, AAB ou publicação de loja.

## 0.6.8 — alinhamento, splash e treino semanal

Jogar alinhado às margens de Marcadores em landscape; ícone S seguido de CORER.
Splash gerado/revisto com pé esquerdo apoiado, direito recuado e bola no chão.
Uma sessão de treino por semana da carreira, reservada e gravada ao começar;
reabrir/abandonar não permite repetir. Bónus único, rollback em falhas de save,
compatibilidade com saves v2 anteriores, nova semana/época desbloqueia.

Ficheiros: career.py, main.py, menu_ui.py, assets/splash.png, buildozer.spec,
tests/test_career.py, ui_tests/test_menus.py, README, AGENTS, docs/UI_0.6.8.md.
Baseline preservado (SHA-256 fed211d2ec63fe0275390b13ed4a1bcfcd18fa61238460b04b67d80ebca6205b).

Verificação: 31 testes core/build/segurança + 22 Kivy passaram (53); py_compile
e git diff --check. Logs /tmp/scorer-068-core-final.log e
/tmp/scorer-068-ui-final.log. Corrigidos durante testes posição de Jogar em
retrato, dimensões antigas após mudança de densidade e resumo de treino cortado.
Capturas Kivy reais do menu e treino inspecionadas; não são capturas Android.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
Logs build-0.6.8.log e verify-0.6.8.log em /workspace/striker-runtime.
Assinatura v2 válida, mesmo certificado SHA-256
84c17cdf31e2ee7c6e9c082bde539df6822bf48267a0603de9814d6e2846ef49; ZIP alinhado
a 16 KB, 118 ELF AArch64 alinhados a 16 KB. API 36, mínimo 26, versão 1026608.
Confirmados splash/presplash, ícone, fontes/licenças e bytecode atualizado no APK.
Sem permissões declaradas, saves ou chaves privadas incluídas.
APK: 29 433 977 bytes. SHA-256:
44d3fe975b34e96f7095a426cb68f0d3b8fe69bd5d03bc18828941787557a4e2.

Próximo: atualizar no telemóvel e verificar alinhamento, splash e treino semanal
após reabrir/avançar semana. Beta debug, sem validação física desta versão,
AAB ou assinatura release para loja.

## 0.6.9 — base do nome alinhada com o ícone

Pedido: alinhar CORER com a parte inferior do S do ícone. O cabeçalho agora
agrupa ícone e palavra numa mesma linha, com altura partilhada e crédito
by clemir por baixo alinhado com o texto. Mantida a altura total do cabeçalho.
Ficheiros: menu_ui.py, buildozer.spec, README.md e este log.

31 testes core/build/segurança + 22 Kivy passaram (53), py_compile e
git diff --check. Captura real da janela Kivy em 1280×589/densidade 1,64
inspecionada em scorer-069-hub0001.png; bases visuais do S e CORER alinhadas.
Sem alterações à carreira ou aos seus saves. O primeiro comando de captura
falhou por xvfb-run não instalado; usado SDL_VIDEODRIVER=offscreen com sucesso.

APK beta debug 0.6.9 realmente compilado. Assinatura v2 válida, mesmo certificado
e identificador Android; ZIP e 118 ELF alinhados a 16 KB. Código atualizado
confirmado no pacote, sem saves/chaves privadas incluídos.
Logs build-0.6.9.log e verify-0.6.9.log em /workspace/striker-runtime;
testes /tmp/scorer-069-core.log e /tmp/scorer-069-ui.log.
SHA-256: 6fb5c0fe24463bbc1371a332201ccb195a68baef08625f61e88b4691e1eeaff0.
Próxima tarefa: confirmar alinhamento no telemóvel. Validação física desta
versão pendente; sem AAB/assinatura release nesta correção visual.

## 0.6.10 — jogo em inglês

Traduzidos menus nativos e Canvas, confirmação de saída/novo jogo, perfil,
erros de nome/save, contratos, agente, transferências, treino, jogo, datas,
tabelas, calendário e acesso World. Liga automática passa a Scorer League;
nomes personalizados não são traduzidos. Saves v2 anteriores mantêm progresso:
Liga Scorer migra, calendário histórico atualiza campos gerados e mensagem
transitória ao carregar passa a Career loaded. Esta edição permanece em inglês
independentemente da língua do Android; seleção automática não implementada.
Estratégia futura documentada em docs/UI_0.6.10.md.

Ficheiros: career.py, main.py, menu_ui.py, buildozer.spec, tests/test_career.py,
ui_tests/test_menus.py, AGENTS, README e docs/UI_0.6.10.md. Baseline preservado.

32 testes core/build/segurança + 23 Kivy passaram (55), py_compile e
git diff --check. Novo teste cobre meses em inglês e migração de feedback,
calendário e liga sem perda de nomes/progresso. Novo teste Kivy percorre sete
menus e valida feedback de nome. A primeira execução deste teste começou no
splash, pelo que o carregamento foi corretamente recusado e faltou MY POSITION;
corrigida a preparação para entrar em Start antes de carregar, sem relaxar
a asserção. Logs /tmp/scorer-0610-core.log e /tmp/scorer-0610-ui-final.log.
Capturas reais Kivy do menu e treino concluído inspecionadas em 1280×589,
densidade 1,64; textos visíveis. Não são capturas Android.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 versão 0.6.10, versionCode 1026610, API 36/mínimo 26.
Assinatura v2 verificada com o certificado anterior, ZIP e 118 ELF alinhados
a 16 KB. Strings inglesas conferidas no bytecode do APK. Sem permissões
declaradas, saves ou chaves privadas incluídos. Logs build-0.6.10.log e
verify-0.6.10.log em /workspace/striker-runtime.
Tamanho: 29434161 bytes. SHA-256: d1fd7b3614e2e26793bef67da4aa0d47b09ba8d5f7e24853f6f510865113f9e6.

Próximo: validar a versão inglesa no telemóvel, incluindo partida e diálogos.
Validação física desta versão pendente. Sem AAB/assinatura release nesta etapa.

## 0.6.11 — marcador fixo, flash de golo e intervalo

Marcador único no canto superior esquerdo, equipas em duas linhas, resultado
por linha e relógio à direita. Mesma geometria na simulação, aviso de oportunidade
e remate; barra inferior de tempo/data/competição removida. Avisos e contador
de remate posicionados abaixo do marcador. Flash verde local de um segundo
a cada golo simulado ou do jogador. Resultado do jogador atualiza no instante
do golo, com guarda por remate para não duplicar ao continuar.

Primeira parte termina aos 45 + descontos (1–4), com HALF-TIME e SECOND HALF.
Pausa mantém relógio parado; retoma aos 45:00. Mantidos descontos finais (1–8).
Timeline inclui ambos os descontos; apresentação desconta os da primeira parte
na segunda. Corrigido processamento de golos futuros antes de uma oportunidade
anterior: limitar avanço à oportunidade/limite da parte antes de processar eventos.

Ficheiros: main.py, menu_ui.py, buildozer.spec, ui_tests/test_menus.py, AGENTS,
README e docs/UI_0.6.11.md. career.py, saves e baseline preservados.

32 testes core/build/segurança + 27 Kivy passaram (59); py_compile e
git diff --check. Novos testes: pausa/retoma/descontos, oportunidade no limite
do intervalo, ordem de eventos, flash e contagem única do golo, desenho idêntico
em três resoluções/densidades e separação do contador de remate.
Uma execução expôs uma diferença de arredondamento de 0,000008 píxel na
asserção do contador, deixando densidade alterada para testes seguintes.
Aplicada tolerância de 0,0001 píxel e cleanup de densidade/janela no teste.
Suite final /tmp/scorer-0611-ui-final.log; core /tmp/scorer-0611-core.log.
Capturas Kivy reais de oportunidade, remate e intervalo inspecionadas em
1280×589/densidade 1,64, scorer-0611-*.png. Não são capturas Android.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.11, versionCode 1026611, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior, ZIP e 118 ELF alinhados a 16 KB.
Código do marcador/intervalo confirmado no APK; sem saves ou chaves privadas
incluídos, sem permissões declaradas. Logs build-0.6.11.log/verify-0.6.11.log
em /workspace/striker-runtime. Tamanho 29434861 bytes.
SHA-256: d80a2eed88c29460672f35671f054ac9365236611e71aef4176c06ea5392c64b.

Próximo: testar no telefone golo a favor/contra, oportunidade e retoma após
intervalo. Validação física desta versão pendente; sem AAB/assinatura release.

## 0.6.12 — marcador compacto e treino obrigatório

Marcador reduzido de 360×64 para 280×46 dp; First half / Second half em vez
de 1H/2H. Mantido flash, relógio, intervalo e posição nas oportunidades.
Training movido para a esquerda de Play. Play cinzento/desativado até concluir
os três remates da semana; validação também em start_career_match. Data junto
a NEXT MATCH e quatro ações secundárias. Sessão de treino interrompida pode
ser retomada com contagem/golos persistidos após cada remate, sem novo bónus.
Campos opcionais v2 training_shots_taken / training_session_goals; reservado
legado sem contagem inicia com zero remates registados, sem bloquear a carreira.

A falha de oportunidade relatada não foi reproduzida no teste inicial. Mudado
o redesenho para manter MatchNotice na árvore de widgets, restaurando apenas
o Canvas, sem remover/repor o painel a cada frame. Teste de toque com cinco
frames entre pressionar/soltar cobre três oportunidades, incluindo descontos,
sem saltar nem consumir remate. Causa original ainda não confirmada no telefone.

Ficheiros: career.py, main.py, menu_ui.py, buildozer.spec, tests/test_career.py,
ui_tests/test_menus.py, AGENTS, README e docs/UI_0.6.12.md. Baseline preservado.
33 testes core/build/segurança + 29 Kivy passaram (62); py_compile e
git diff --check. Logs /tmp/scorer-0612-core.log e /tmp/scorer-0612-ui.log.
Testes novos verificam bloqueio/desbloqueio/rebloqueio semanal, contagem parcial
ao reabrir, rollback de gravação, bónus único, botões lado a lado e toques.
Capturas Kivy reais do menu e oportunidade inspecionadas em 1280×589/densidade
1,64. Não são capturas Android.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.12, versionCode 1026612, API 36/mínimo 26.
Assinatura v2 válida com mesmo certificado, ZIP e 118 ELF alinhados a 16 KB.
Código atualizado conferido no APK; sem permissões declaradas, saves ou chaves
privadas incluídos. Logs build-0.6.12.log e verify-0.6.12.log em
/workspace/striker-runtime. Tamanho 29436361 bytes.
SHA-256: 43988e5279b11f0812ad3843156d531f269c7fcb8dc530e57d6e5392996086fb.

Próximo: atualizar telefone, confirmar dimensões, completar treino e abrir
todas as oportunidades. Validação física e confirmação da falha reportada
pendentes. Sem AAB/assinatura release nesta etapa.

## 0.6.13 — dificuldade de finalização e logótipo

Pedido: reduzir facilidade excessiva, no máximo uma oportunidade fácil por
jogo e restantes difíceis; logótipo baseado no ícone, sem by clemir no menu.
Oportunidades pessoais limitadas a 0–3 consoante energia/moral. Uma oportunidade
fácil é atribuída em 60% das partidas, nunca mais de uma. Restantes remates
a 16,5–21 m e ângulo de 4,5–8 m, quatro defesas/barreira, menos tempo e GR
mais rápido. Penáltis/cabeceamentos/livres mantidos. Golos decididos pela física,
sem falhas impostas ou inflação de marcadores rivais. Totais antigos preservados.
Novo assets/menu_logo.png gerado com imagegen a partir do ícone original,
transparente, SCORER marfim/verde. Usado no hub e entrada sem crédito; ícone
e splash originais mantidos.

Ficheiros: main.py, career.py, menu_ui.py, assets/menu_logo.png, buildozer.spec,
tests/test_career.py, ui_tests/test_menus.py, tools/balance_shots.py, AGENTS,
README e docs/UI_0.6.13.md. Baseline preservado.
34 testes core/build/segurança + 31 Kivy passaram (65); py_compile e
git diff --check. Cobertura nova de 60 alocações sem dois lances fáceis,
posições/oposição/tempos, tipos de remate, reação do GR, treino e logótipo.
Uma asserção de visibilidade expôs inicialmente tamanho de widget não assentado;
fixado viewport explícito no teste. A execução seguinte confirmou recorte
real de ângulos extremos em landscape mais estreito. Reduzido o intervalo e
espelhado o mesmo ângulo para o lado visível quando necessário; suite final
aprovada em /tmp/scorer-0613-ui-final.log. Core /tmp/scorer-0613-core.log.

Ensaio físico reproduzível tools/balance_shots.py: 240 remates por perfil,
720 total, potência 0,85 e destinos amostrados com as mesmas seeds. Gerador
anterior: 109 golos/100 defesas/31 falhas (45,4%); fácil: 177/63/0 (73,8%);
difícil: 62/104/74 (25,8%). Todos resolvidos até 15 s simulados. Log
/tmp/scorer-0613-balance-release.log. Ensaio não mede habilidade humana,
classificação ao longo da época ou desempenho Android. O primeiro comando
do utilitário encontrou conflito dos argumentos com Kivy; corrigido com
KIVY_NO_ARGS antes da importação. Usa saves temporários isolados.
Capturas reais Kivy do menu, entrada e livre difícil inspecionadas em
1280×589/densidade 1,64; não são capturas Android.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.13, versionCode 1026613, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior; ZIP e 118 ELF alinhados a 16 KB.
Logo e código de equilíbrio confirmados dentro do APK; ícone e splash
conferidos por bytes. Sem permissões declaradas, saves ou chaves privadas
incluídos. Logs build-0.6.13.log e verify-0.6.13.log em /workspace/striker-runtime.
Tamanho 30206997 bytes. SHA-256: ff747656022880c3d11cd0cf027c09babdf60f93f357eaa87b4824f9adb726c6.

Próximo: jogar várias partidas no telefone e avaliar conversão dos lances
difíceis. Validação física/equilíbrio humano pendentes. Sem AAB/assinatura release.

## 0.6.14 — contador agregado e iniciais do jogador

TIME TO SHOOT integrado numa faixa de 22 dp colada por baixo do marcador,
com a mesma margem esquerda e largura. Barra de progresso fina; duração,
dificuldade e cronómetro da partida não alterados.
Nome do jogador passa a ter inicial maiúscula em cada componente separado
por espaços ao guardar perfil ou carregar carreira. Mantidas grafia interna
e letras acentuadas. Migração da chave de marcadores acompanha o nome, sem
apagar golos. Colisão com outro marcador num save antigo mantém ambos os
registos intactos; editar perfil permite escolher nome sem ambiguidade.

Ficheiros: main.py, career.py, buildozer.spec, tests/test_career.py,
ui_tests/test_menus.py, AGENTS, README e docs/UI_0.6.14.md. Baseline preservado.
36 testes core/build/segurança + 31 Kivy passaram (67), py_compile e
git diff --check. Logs /tmp/scorer-0614-core.log e /tmp/scorer-0614-ui.log.
Cobertura de nomes acentuados, maiúsculas internas, migração com golos,
colisões, rollback e geometria do contador em três densidades.
Captura real Kivy scorer-0614-shot0001.png inspecionada em 1280×589/densidade
1,64. Contador agregado visível; não é captura Android.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.14, versionCode 1026614, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior; ZIP e 118 ELF alinhados a 16 KB.
Código atualizado confirmado no APK; sem permissões declaradas, saves ou chaves
privadas incluídos. Logs build-0.6.14.log/verify-0.6.14.log em
/workspace/striker-runtime. Tamanho 30207473 bytes.
SHA-256: eb9af3189e0a6f835d2ea768051b3cc408f6d0448b19b571ec9d03a03e74111c.

Próximo: validar contador e nome no menu/marcadores no telefone. Validação
física desta versão pendente; sem AAB/assinatura release nesta etapa.

## 0.6.15 — oportunidades dependentes do adversário

Quantidade e probabilidade de oportunidade fácil passam a depender do rating
e posição do adversário na liga dele. Energia/moral mantidas. Perfil definido
ao início do jogo com o adversário correto, em casa ou fora. Adversário muito
forte: no máximo uma oportunidade, sempre difícil; forte: máximo duas, 15% de
atribuir uma fácil; restantes: máximo três, probabilidade fácil até 60% a descer
com a pressão. Zero oportunidades continua possível.
Classificação tem peso gradual até cinco jogos; uma tabela sem jogos não
conta. Elite ou top-15% após cinco jogos força o perfil muito forte. Taças
consultam a liga do adversário; seleções/sem tabela usam apenas rating.
Simulação de resultados, física, treino, UI e progresso existente não alterados.

Ficheiros: career.py, main.py, buildozer.spec, tests/test_career.py,
ui_tests/test_menus.py, AGENTS, README e docs/UI_0.6.15.md. Baseline preservado.
38 testes core/build/segurança + 32 Kivy passaram (70); py_compile e
git diff --check. Novos testes cobrem qualidade/posição, 500 amostras pareadas
fraco/forte, liga própria do adversário de taça, seleções, tabela sem jogos e
integração em casa/fora. Teste genérico de tipos de remate usa perfil fraco
explícito para isolar a regra de no máximo uma chance fácil. Sem falhas novas
na execução. Logs /tmp/scorer-0615-core.log e /tmp/scorer-0615-ui.log.
Sem mudanças visuais; não foram produzidas novas capturas de ecrã nesta etapa.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.15, versionCode 1026615, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior; ZIP e 118 ELF alinhados a 16 KB.
Perfil e uso do adversário confirmados no bytecode empacotado. Sem permissões
declaradas, saves ou chaves privadas incluídos. Logs build-0.6.15.log e
verify-0.6.15.log em /workspace/striker-runtime. Tamanho 30208805 bytes.
SHA-256: f99019b28fe69cb43bd657a6af5c647d59cd98b41378d38da2ba308a1dd3841f.

Próximo: comparar partidas contra líderes, equipas intermédias e fracas no
telefone. Validação física/equilíbrio humano pendentes; sem AAB/assinatura release.

## 0.6.16 — correção de jogos sem oportunidades após treino

Relato: carreira nova com zero chances nos primeiros dois jogos apesar de
3/3 em cada treino. Causa: o sorteio introduzido em 0.6.15 tinha limite inferior
zero, mesmo após treino obrigatório, e os golos do treino só ajudavam por
energia/moral. Corrigido chance_count: treino concluído garante no mínimo
uma oportunidade, incluindo em saves anteriores. Golos da sessão da semana
adicionam 0,15 cada à média (máximo 0,45), sem exceder limites do adversário.
Muito forte mantém exatamente uma oportunidade, sempre difícil. Não altera
física, golos históricos ou classificação; golos do treino não contam na liga.

Ficheiros: career.py, buildozer.spec, tests/test_career.py, ui_tests/test_menus.py,
AGENTS, README e docs/UI_0.6.16.md. Save v2 e baseline preservados.
40 testes core/build/segurança + 33 Kivy passaram (73); py_compile e
git diff --check. Regressão integrada percorre as primeiras duas semanas
com 3/3 em cada treino e abre uma chance em cada partida. Core testa 500
sorteios por força do adversário, treino guardado/recarregado, legado e
efeito do bónus. Sem falhas novas. Logs /tmp/scorer-0616-core.log e
/tmp/scorer-0616-ui.log. Sem alteração visual ou novas capturas nesta etapa.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.16, versionCode 1026616, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior; ZIP e 118 ELF alinhados a 16 KB.
Código do bónus/treino verificado no APK; sem permissões declaradas, saves
ou chaves privadas incluídos. Logs build-0.6.16.log/verify-0.6.16.log em
/workspace/striker-runtime. Tamanho 30208941 bytes.
SHA-256: 9c2e0f6776a1cadefd46ef58ad35d42f599fc1cf456aa31f1531f1f10ad5441b.

Próximo: atualizar sem desinstalar e confirmar oportunidades nas próximas
partidas após treino. Não é preciso recomeçar a carreira. Validação física
desta versão pendente; sem AAB/assinatura release nesta etapa.

## 0.6.17 — investigação e calibração de golos

Investigadas três épocas completas de League Two/Premier League (2022/23–
2024/25) em openfootball/england e duas épocas de remates (2017/18–2018/19)
no espelho público FootballData. Fornecedor direto devolveu 403; usados
repositórios públicos com revisões e hashes fixados. League Two: 4316 golos
em 1656 jogos, média 2,606. Remates: 2867 golos/24377 remates/9373 enquadrados
(~11,76% e ~30,59%). Fontes, distinções e limites em docs/REALISM_0.6.17.md
e docs/data/real_football_reference.json; nenhum pack real/nome oficial no APK.

Auditoria: toque direto permitia repetir cantos quase infalíveis; velocidade
e limite de voo aceleravam remates longos. Ajustada dispersão física de saída
por pressão/condição/potência, velocidade horizontal 18–26 m/s e máximo de voo
1,15 s em jogo; treino conserva comportamento original. GR hard passa a reação
0,14–0,22 s e melhor deslocação. Golos mantêm-se decididos pela física.
Orçamento de golos simulado 1,43/1,18 (total 2,61), dividido por força/posição;
a contribuição esperada do jogador é reservada antes de sortear colegas.
Corrigida dupla atribuição de golos pessoais a NPCs, exclusão de taça da
classificação da liga e uso do contador correto no UI. Distribuição NPC passa
de uniforme a papéis ponderados, sem criar golos extra e com identidade pelo
clube completo. Papéis são hipótese do modelo, não medição dos CSVs.
Progresso e golos históricos preservados; defeitos históricos não reconstruídos
sem dados suficientes. Mínimo de participação após treino e adversários mantidos.

43 testes core/build/segurança + 36 Kivy passaram (79), py_compile e
git diff --check. Novos testes de conservação/taça/reload, orçamento de golos,
papéis, velocidades, dispersão sem resultado pré-determinado, treino intacto e
reserva de golos em casa/fora. Logs /tmp/scorer-0617-core-final.log e
/tmp/scorer-0617-ui-final.log. Não houve falhas de implementação nas suites;
a validação física revelou o limite de voo antigo e motivou repetição dos
ensaios afetados/compilação após a correção. Sem alterações de geometria/arte.

Ensaios reproduzíveis com saves temporários e baseline da3db00 isolada:
- 100 épocas/55200 jogos: 2,720 para 2,620 golos/jogo; 5+ golos 13,97% para
  12,58%; líder de marcadores médio 13,82 para 29,31 com os mesmos golos
  redistribuídos por papéis (não é comparação com jogadores reais).
- 240 remates físicos por perfil/estratégia: canto hard 85,8% para 30,0%;
  canto easy 100% para 48,3%; alvos variados hard 18,3%, easy 50,8%.
- 100 partidas completas com bot instantâneo aos cantos: 3,64 para 2,81
  golos/jogo, 190 para 67 golos pessoais, 28% para 13% jogos com 5+ golos.
  Outros 100 jogos com alvos variados: 2,85 golos/jogo e 37 golos pessoais.
Resultados/condições em docs/data/simulation_0.6.17.json. Bots não são testes
humanos/Android, amostras são limitadas e sequências de épocas divergem.
Ferramentas tools/analyse_football_data.py, calibrate_goals.py,
calibrate_playable.py e balance_shots.py permitem reprodução.

Ficheiros alterados: career.py, main.py, menu_ui.py, buildozer.spec, testes
core/Kivy, ferramentas acima, AGENTS, README e relatório/dados. Baseline imutável
continua fed211d2ec63fe0275390b13ed4a1bcfcd18fa61238460b04b67d80ebca6205b.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.17, versionCode 1026617, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior; ZIP e 118 ELF alinhados a 16 KB.
Código final de golos/voo/dispersão confirmado no APK; arte conferida por bytes.
Sem permissões declaradas, CSVs brutos, saves ou chaves privadas incluídos.
Logs build-0.6.17.log e verify-0.6.17.log em /workspace/striker-runtime.
Tamanho 30210325 bytes. SHA-256: 542314cb93bf31ef0509c6fbf249395aebf37f06d1e9fa884510a625d2d9b5e5.

Próximo: jogar várias partidas no telefone, avaliar justiça da mira e frequência
de golos. Validação física/equilíbrio humano pendentes. Modelo FREE calibrado
para League Two, sem alegar que todas as ligas mundiais foram calibradas.
Sem AAB/assinatura release nesta etapa.

## 0.6.18 — alternância casa/fora no campeonato

Corrigida orientação dos emparelhamentos: antes a paridade da jornada era
aplicada a todos os pares e podia criar longas sequências casa/fora. Versão 2
fixa a paridade por par, alternando o primeiro, e reordena a segunda volta
(inversão com desfasamento de duas jornadas). Cada equipa tem no máximo uma
quebra de alternância por volta, incluindo transição para a segunda; nunca
três jogos seguidos na mesma condição. Adversários uma vez em cada volta com
local invertido; 24 equipas: 46 jogos, 23 casa e 23 fora. Pausas corrigidas para
casos ímpares de teste. Taças conservam sorteio independente.

Novo campo opcional schedule_version no save v2. Saves antigos migram já apenas
se todos os jogos realizados mantiverem adversário/local (normalmente 0–1
jornadas em FREE). Épocas antigas incompatíveis mantêm o calendário inteiro
até terminarem e mudam na época seguinte. Preservados resultados/progresso;
sem pedir novo jogo ou substituir retroativamente jogos realizados.

47 testes core/build/segurança + 37 Kivy passaram (84), py_compile e
git diff --check. Verificação completa de campeonatos com 2–32 equipas, pares
únicos, locais invertidos, contagens iguais, regra por volta/transição e ausência
de triplas. Hashes dos calendários legados 5/24 equipas preservados. Testes de
save/load com 0/1/2 jornadas, histórico/pontos/golos, mudança de época,
recarregamento e rejeição transacional de versão desconhecida. Kivy confirma
o mesmo próximo jogo no calendário, menu e lançamento.
Primeiro teste Kivy herdou viewport minúsculo onde o resumo é ocultado de
propósito; preparação corrigida para 960×540 com cleanup, sem mudar o UI.
A análise inicial da transição entre voltas encontrou uma quebra adicional
para duas equipas; corrigida ordenação da segunda volta e adicionada asserção
que também conta essa fronteira. Logs /tmp/scorer-0618-core-final.log e
/tmp/scorer-0618-ui-final.log. Sem alterações de arte/geometria ou novas capturas.

Ficheiros: career.py, buildozer.spec, testes core/Kivy, AGENTS, README e
docs/UI_0.6.18.md. Baseline preservado (fed211d2ec63fe0275390b13ed4a1bcfcd18fa61238460b04b67d80ebca6205b).
Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.18, versionCode 1026618, API 36/mínimo 26.
Assinatura v2 válida, mesmo certificado; ZIP e 118 ELF alinhados a 16 KB.
Código do calendário/migração confirmado no APK. Sem permissões declaradas,
saves ou chaves privadas incluídos. Logs build-0.6.18.log/verify-0.6.18.log
em /workspace/striker-runtime. Tamanho 30211485 bytes.
SHA-256: 385892f68d4706661128d35160e3e838daee2f0bc82dfe76ec8ce50355a05697.

Próximo: verificar calendário do campeonato em época nova/compatível no telefone.
Época legada incompatível preservada até à seguinte. Validação física desta
versão pendente; sem AAB/assinatura release nesta etapa.

## 0.6.19 — caixa YOUR PLAYER

A partir da captura do proprietário, removida a linha decorativa do painel
que atravessava o campo. Campo do nome arredondado, com contorno de foco e
texto centrado verticalmente. Margens alinhadas, menos espaço vazio e painel
com altura pelo conteúdo. Ajuste compacto de margens/espaçamento mantém
controlos de 52 dp. Sem mudar validação, capitalização, saves ou jogabilidade.

Ficheiros: menu_ui.py, buildozer.spec, AGENTS, README e docs/UI_0.6.19.md.
47 testes core/build/segurança + 37 Kivy passaram (84), py_compile e
git diff --check. Cobertura funcional/layout existente usada nesta alteração
visual: perfil novo/editar, validação, gravação e limites em ecrãs de telefone.
Logs /tmp/scorer-0619-core.log e /tmp/scorer-0619-ui-final.log.
Captura real Kivy scorer-0619-profile0002.png em 1280×589/densidade 1,64
inspecionada. Primeiro ensaio visual mostrou cor do contorno a afetar texto;
adicionado reset de Color e contraste explícito, captura final conferida.
Não é captura Android. Baseline preservado.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.19, versionCode 1026619, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior; ZIP e 118 ELF alinhados a 16 KB.
Código do campo confirmado no APK; sem permissões declaradas, saves ou chaves
privadas incluídos. Logs build-0.6.19.log/verify-0.6.19.log em
/workspace/striker-runtime. Tamanho 30212625 bytes.
SHA-256: b9ff9b7e011a0f651da9c9181627a84ea64b07ebf62915a25f7cf43b556a825c.

Próximo: atualizar sem desinstalar e verificar caixa/teclado no telefone.
Validação física desta versão pendente; sem AAB/assinatura release nesta etapa.

## 0.6.20 — requested training/balance/presentation revision

Changes/evidence/limits: docs/UI_0.6.20.md; seeded results in
 docs/data/balance_0.6.20.json. Files: career.py, main.py, buildozer.spec,
 tools/balance_shots.py, core/Kivy tests, AGENTS, README and these docs.

49 core/build/security + 38 actual Kivy tests pass (87 total), syntax and
 git diff --check pass. Initial expected-contribution regression correctly failed
 after moving the reserved hard-shot mean from .18 to .20; updated its explicit
 expected totals, reran both suites successfully. Headless desktop lacks optional
 xclip/xsel clipboard executables; Kivy fallback runs, all UI tests pass.

240 seeded uniform attempts/profile before and after: hard 44 -> 49 goals;
 training 131 -> 75; clear unchanged at 122. Corner strategy final hard 97/240.
 100 complete playable matches: 2.46 total goals/match, 59/224 personal shots.
 Desktop scoreboard/catch screenshots rendered and inspected. Not device tests.

Actual build tools/android/run.sh python tools/build_android.py -v android debug
 passed. Signature v2 and existing certificate verified, ZIP16KB and 118 ELF
 alignments pass. Actual package versionCode1026620, target36/min26, no requested
 permissions. Payload inspected for saves/signing keys. APK30,215,905 bytes,
 SHA256 d2d938c1f8331a81db65f037b652a65c1632b8a4ad8282932a67bd4a1f008114.
 Logs build-0.6.20.log and verify-0.6.20.log in /workspace/striker-runtime.
 Next: actual phone training, hard shots, keeper catch/fall, scoreboard and flags.

## 0.6.21 — complete fixtures and progressive cup draws

Changes: docs/UI_0.6.21.md. Files: career.py, menu_ui.py, buildozer.spec,
core/Kivy tests, AGENTS, README and docs. 51 core/build/security tests and
38 real Kivy tests pass (89). Syntax/whitespace and baseline hash pass.
An initial UI regression from calling the removed detail view was fixed by
a safe no-op for tables without details; all UI tests rerun successfully.
Full schedule and 35-result persistence/reload tested; cup draws stable through
all eight rounds/final with no repeated eliminated opponent.

Actual Android build: build-0.6.21-final.log. Static verification: signature v2
with existing debug certificate, ZIP16KB and all 118 AArch64 ELF alignments,
package com.clemir.striker/versionCode1026621, target36/min26, no permissions.
Payload checked: no saves or signing keys. verify-0.6.21.log retained outsideGit.
APK 30217021 bytes, SHA256 77e8f0c8ce4e3c842ecb101164cd5ff381c251efbc3f575808d48a992043713b.
Desktop fixtures screenshot inspected; current APK not tested on a phone.
Next: phone fixture pages, save/load, cup progression and weekly training.

## 0.6.22 — AdMob native SDK, TEST only

Owner supersedes no-AdMob restriction by requesting immediate network revenue;
no account exists, general audience includes minors. Real production revenue is
blocked by account/IDs/readiness, not represented as achieved. Full instructions
and data/permission implications: docs/ADMOB_SETUP.md. Implementation/evidence:
docs/UI_0.6.22.md. Added advertising.py, Java ScorerAds bridge, manifest removals,
Gradle SDK pins, main/menu hooks, controller and actual Kivy integration tests.

56 core/build/security and 41 actual Kivy tests pass (97). Early failures: exact
menu counts changed by Privacy; new test had not loaded its career. Corrected
expectations/setup, retained geometry/overlap assertions, reran full suites.
Syntax, git whitespace and immutable baseline checks pass. Real desktop entry,
hub and privacy screenshots inspected. No actual Android ad has been displayed.

Actual Android build build-0.6.22-banner.log successful, GMA25.5.0/UMP4.0.0 and Java
bridge in DEX verified. APK version1026622, target36/min26, same debug signaturev2,
ZIP16KB + 118 AArch64 ELF alignments pass. Manifest sample App ID and DEX official
TEST ad unit checked. AD_ID and all three AdServices permissions absent; network,
wake-lock, foreground-service and AndroidX signature receiver permissions remain.
No saves/private keys in APK. APK37,175,750 bytes,
SHA256 28b4abdaf13cebdb3a75df32c895c352366b416d4ae6058f5be705db2ff75cc7.
Native presentation/UMP/rotation/offline/performance still need phone validation.
No production IDs, no payments, no Play publishing, no revenue claimed.

Owner additionally requests ads after splash: added native TEST banner in the
entry menu only, separate 64dp footer and safe-size suppression. Removed on
navigation, never delays splash/menu or appears during play. Controller visibility
transitions and actual Kivy button/footer separation added to the passing suite.

## 0.6.23 — first post-match ad and optional morale RewardedAd

Owner reports 0.6.22 banner displayed, no post-match ad. Old 3-match/180s gate
can explain this, no device error log available. First final CONTINUE now eligible
if ready, subsequent fullscreen minimum60s. Prefetch earlier and separate Privacy
status for break/reward failures. Optional training +1 morale capped20/once-weekly,
SDK earned callback only, native private receipt, atomic save + idempotent ack.
Files/evidence: docs/UI_0.6.23.md; four production IDs needed in ADMOB_SETUP.md.

59 core/build/security and 42 real Kivy tests pass (101). Includes save failure,
replay/reload, stale contexts, no reward on request/early close without SDK record,
first-match/cooldown and existing full suites. Initial UI caught 8px overflow;
compacted training spacing/removed duplicated energy line, all UI rerun passed.
Desktop training capture at density1.64 inspected. Actual 0.6.23 ad load/show/earned
callback/rotation/early close still need Android phone validation.

Real build build-0.6.23-final.log successful. SDK RewardedAd/receipt and all TEST
IDs in DEX verified, Python advertising.pyc in payload; no saves/private keys.
Same debug signaturev2, package com.clemir.striker/version1026623, target36/min26,
ZIP16KB +118 AArch64 ELF alignments pass, AD_ID/AdServices permissions still absent.
APK37,181,442 bytes, SHA256
5477d0272298ae493294f22cf40bf83c64eaffc338e9618043840b5715754dcd.
Static log verify-0.6.23.log; no production revenue or paid IDs activated.

## 0.6.24 — Help, locale starts, World test edition and names editor

Full change/test/build/limitation report and hashes: docs/WORLD_0.6.24.md.
67 core/build/security +44 actual Kivy tests pass (111), syntax/whitespace and
baseline hash pass. New coverage: locale/one Free division, World table reload,
World access not save-unlockable, alias import/rollback/UID/scorer preservation,
same-name cross-country isolation, promotion swap and all cup rounds before
short-league season end; Help/Upgrade/navigation/editor and prior layout suite.

Initial UI action-count expectations updated from9 to11, preserving geometry/
48dp targets. Audited/fixed original promotion duplication and local Free season
switch-to-England hazard. Aliases originally used ambiguous global name matching;
now direct UID/country context with regression. Compacted initial contracts/editor
after real desktop screenshots showed avoidable scrolling. No physical phone test
of the new edition/SAF/companion launch yet. World simplified international model
and fictional pyramids explicitly documented; no paid release claimed.

Two actual final builds successful, Free com.clemir.striker and World test
com.clemir.strikerworld.preview. World distribution first failed due to mixed
packaging pip files; preserved/recreated disposable venv, native caches retained.
Both signaturesv2 (same prior certificate), ZIP16KB and 118 ELF alignment checks
pass, target36/min26/version1026624. Compiled edition.pyc flags checked using
built hostPython3.14: Free false, World true. World DEX LocalNameFiles present,
Google Ads absent, no Internet/Billing permission. Free AdMob TEST remains, no
Billing/AD_ID/AdServices. No private saves/keys in either private archive.
Logs: build-0.6.24-{free,world}-final.log / verify-0.6.24-{free,world}.log.
Next: install alongside Free, test locale/English contracts, Help/Upgrade, World
season/transfer, document export/import and alias persistence on Android.

## 0.6.25 — single-app World purchase and Play preparation

Owner correction supersedes 0.6.24: a single com.clemir.striker application with an
optional one-time World/editor/ad-free upgrade, not a second paid app. Play account
is under verification; no owner AdMob IDs/public policy/support details or production
signing/service credentials are available. This revision performs no Play upload,
real purchase, payment activation, service deployment or public store rollout.

Changes: native Google Play Billing 8.0.0 bridge, SKU scorer_world_upgrade, real price
query/checkout readiness, pending/cancelled/already-owned handling, Restore on request
and resume, fail-closed Python ownership snapshot, transactional same-app career
upgrade and private backup. BillingConfig.ENABLED remains false in source/rehearsal.
World removes the ad backend; expired/unverified World progress is retained for
restore. Historical companion launch/package query removed from shipping code.
Native SAF name-file bridge now accompanies the same application.

Server-only verifier checks package/product/token with Android Publisher API,
rejects pending/cancelled/consumed/test production purchases, acknowledges completed
purchases and signs installation/nonce-bound RSA SHA256 licences with seven-day
expiry. Client verifies signatures and bounds before private caching. No private key,
ADC credential, career/player name or payment card enters the APK or verification
request. Backend is prepared, not deployed or tested against a real Google purchase.
Deployment controls, licence testers/refunds/expiry and device tests remain required.

Release staging/public-config validation, actual bundle inspector, 16KiB audit and
env-only signing helper added under tools/play. Production template correctly exits2
for missing owner identity/contact/policy/AdMob/Billing configuration. Rehearsal uses
TEST ads and disabled purchases, fixed numeric versionCode1026625, API36/min26 ARM64,
backup=false, cleartext=false, release not debuggable. Server/config/saves/key material
excluded. Privacy screen describes local storage/purchase data and can link the final
policy/contact once configured. Draft listing (EN/PT), policy, Data Safety inventory,
server deployment guide and Console handoff in docs/play and server/README.md.

Verification of the final source:
- `python -m unittest discover -s tests -v`: **79 PASS**, 11.780s.
- Actual Kivy suite: **46 PASS**, 46.344s. Total **125 tests**. New tests exercise
  production gating, manifest restrictions, no state change from an unverified Buy,
  provider snapshots, same-app progress/UID/table/training preservation, failed-save
  preservation, invalid/pending/refunded/consumed/test receipt rejection, signing/tamper,
  acknowledgement, bounded request schema, redacted service failures and disabled UI.
- `python -m py_compile` changed/new modules, `bash -n` wrappers and
  `git diff --check`: PASS. Immutable baseline tests retained.
- Actual final `android release` AAB generated from isolated staging at
  /workspace/Scorer-play-qa-0625-final, log build-0.6.25-play-final.log.
  Unsigned rehearsal AAB: **34,722,073 bytes**, SHA256
  `4836b8f689cc1d4e2e131911950948dd0eba47733ee7b143d768cfa9a7824240`.
- Official bundletool1.18.1 validates the actual AAB. Manifest inspector PASS:
  com.clemir.striker, versionCode1026625, target36/min26, no debuggable/backup/cleartext,
  Billing/Internet present, no AD_ID/AdServices/storage/location/camera/microphone or
  legacy World companion query. SDK browser/billing intent queries are retained.
- Bundle config PAGE_ALIGNMENT_16K; **118 ELF LOAD alignments >=16KiB** pass,
  including Python extensions inside the compressed bundle. Native Billing, ad and
  SAF bridges and Python modules found; no saves/private signing/server files.
- bundletool generated a universal **DEBUG-signed inspection APK**, 35,045,477 bytes,
  SHA256 `391a78b5335fe608468991439e2a74ac90957ccdc1528eb8cabb5d7a15d53246`.
  apksigner v2/v3 and zipalign16KiB pass. Compiled edition flag false; javap of the
  actual compiled BillingConfig confirms ENABLED=false, empty verifier/public key.
- Signing helper first found only a JRE on the outer host, then passed inside the
  full-JDK build container using the **existing public DEBUG key only** on a separate
  clearly labelled test copy. This proves the helper, not production signing. The
  delivered rehearsal AAB stays unsigned; self-signed debug warnings are expected.

Issues resolved: Buildozer passes shell-wrapped XML through an argv list, causing
invalid application attributes in release manifests. Fixed only those two XML argv
wrappers in WorkspaceBuildozer, tested without shell evaluation, then rebuilt
successfully. The first audit incorrectly rejected all queries (including legitimate
Google SDK intents); refined it to reject the old companion package and added tests.
An old test asserted a literal Android status message; retained its actual fallback
contract (nonempty readable status/no blocking ads) after generalising production text.
One UI assertion found changed charge wording; restored the explicit “does not charge”
explanation. Final suites pass. No physics/career balance changes in this revision.

Logs outside Git: /tmp/scorer-0625-{core,ui}-final.log,
/workspace/striker-runtime/{build-0.6.25-play-final,verify-0.6.25-play-final}.log.
Actual audit files are in bin/play-audit-0.6.25; public readiness/hashes are recorded in
docs/play/READINESS_0.6.25.json. APK/AAB inspection is not phone or Play execution.

Next: finish account/public metadata/AdMob setup, agree price and approve a configured
licence-test candidate; deploy verifier with protected server keys/Google permissions,
configure Play product/upload signing, then perform real Play tests and current Android
screenshots/pre-launch/16KiB device checks before asking for publication approval.
Existing debug beta certificates differ from a future production Play signing key;
do not uninstall beta/private saves without a tested preservation/transfer plan.

## 0.6.26 — Free country choice removed; separate Free/World saves

Owner corrections: new Free games have no country selector, and a Free career
is available only in Free. World starts its own career inside the same application.

Changes:
- New Free careers go directly to Scorer League (internal England|4), ignoring
  phone locale. No country buttons or start_country route in Free; core rejects
  foreign-country selection. Only World retains local/England Division4 choices.
- Existing legacy Free careers keep their current single league/progress.
- Explicit Free/World save slots: striker_career.json and striker_world_career.json.
  World never auto-imports Free; a copied Free payload is rejected by World load.
  World ownership cannot turn the Free slot into World or enable its editor.
- Verified owners can select modes from the entry/menu, then explicitly New/Load.
  First World entry has a new player/contracts, zero goals/matches, not Free stats.
  Switching saves the active career first; a failed save blocks switching.
  Previous-game/editor backups remain slot-specific. Inaccessible World remains
  stored; return to Free never copies its data. Ads/reward buttons are suppressed
  for owners in either mode. Purchase remains disabled in this beta.
- Updated Help, Upgrade, store/privacy drafts, packaging exclusions and instructions.

Files: career.py, main.py, menu_ui.py, world_ui.py, version/config/exclusion files,
core/UI tests, Play artifact inspector and product/release documentation.

Tests: **82 core/security PASS** (12.072s), **48 actual Kivy PASS** (48.853s),
**130 total**. Includes legacy Free preservation, paid Free restrictions, independent
World goals/player/files, mode save failure, copied-Free rejection, unknown slot/path
rejection, hidden/guarded country actions and unauthorised World route rejection.
An initial UI snapshot compared a loaded career with its pre-load status message;
normalised the selected state by saving before the isolation comparison. Final pass.
Syntax and git diff --check pass. No match balance or physics changes.

Actual debug APK built, com.clemir.striker, versionCode1026626, target36/min26 ARM64.
Existing DEBUG certificate matches previous betas. apksigner/zipalign16KiB and all
118 ELF LOAD alignments pass. Compiled WORLD_PREVIEW=false; billing stays disabled.
Size: 37,593,779 bytes. SHA256: `e68ffdedd3d1e168a532a2690a31e83f28d0f01da7f674b0135937927003d69b`.
This is a beta, not a production-signed release; device/Play purchase tests remain pending.
No AAB was rebuilt for 0.6.26: the 0.6.25 rehearsal AAB/report are historical; regenerate
and validate from the final selected source before any store submission.

Logs: /tmp/scorer-0626-core.log, /tmp/scorer-0626-ui-final.log,
/workspace/striker-runtime/build-0.6.26-free-final.log and verify-0.6.26-free.log.
Next: owner validates Free new-game offers and existing career on Android; configure
and explicitly approve Play licence testing before testing live World ownership/modes.

## 0.6.27 — World aim, morale floors, club presentation and JSON guide

See [full revision report](WORLD_0.6.27.md): 88 core/security + 51 Kivy = 139 PASS;
actual Free and same-package owner QA APKs built and statically verified. World
presentation uses unchanged canonical UIDs, 9896 display rows, real city/local forms
and available colour references. Coverage limits and licences are documented.
New morale floors supersede old opponent quantity caps without creating easy elite
chances or adding simulated goals on top of the reserved budget. JSON FORMAT uses
valid selected IDs and does not modify saved aliases. QA opens World only for owner
testing with Billing disabled; no paid ownership or Google Play release claimed.

## 2026-10-24 — official regulation collection, research batch

Research-only batch; see [collection index](regulations/README.md) and
[reviewed sections](regulations/REVIEW_NOTES.md). Selected catalogue: 31 sources;
10 complete PDFs cached outside the app; 100 retrieval attempts including errors;
coverage matrix includes all 212 existing game regions, none marked fully verified.
Partial primary-source review covers Portugal professional progression, MLS 2026,
OFC Champions League 2026, OFC Professional League 2026, AFCON provisions adopted
in 2023, historical CAF club-document warnings and UEFA 2026/27 season calendars.

Validation PASS: JSON parsing, unique IDs/regions, all coverage source references,
stored source bytes and SHA-256 hashes, PDF signatures and relative Markdown links;
`git diff --check` passed. Zero cache metadata mismatches. HTTP 200 EFL navigation
and UEFA JavaScript shells explicitly do not count as regulation text. Incomplete
RFEF PDF download and blocked document hosts are recorded. Supplemental file-host
allowances saved in environment draft; tool requires environment review/save and
Publish to apply them. No game code changed by this research batch, no new APK,
gameplay regression or Android device testing claimed. Pre-existing gameplay work
in the checkout remains separate and uncommitted.

Next: retrieve blocked primary documents after network configuration applies;
verify full current-season rules, eligibility, tiebreakers and amendments by country
before implementing or labelling any model an exact reproduction.

## 2026-10-25 — scoped fallback model and priority research

Owner scope: Europe/Brazil/Argentina/Mexico require national-source research;
other World countries use two active divisions with three direct promotions and
relegations. Implemented ranked six-club exchanges, active-only browsing/offers,
standings P/R zones and versioned legacy-tier/name-pack preservation. New World
has 450 active divisions/6200 clubs. Free's single league stays intact.
Android locale selection now prefers system configuration over a possible
app/runtime English default. No complete Portuguese interface is claimed.

PASS on the exact staged source snapshot: 102 core/security and 52 actual Kivy
tests (154 total), plus syntax/static whitespace checks. Eight new domestic tests
cover exact exchanges, identity/count conservation, legacy season-boundary
migration, alias archives and damaged metadata; six new locale tests cover
Portuguese system/English runtime, API23, empty lists and missing bridge fallbacks.
One new Kivy test verifies two league choices and exactly three P/R zones.
Logs: /tmp/scorer-priority-reviewed-core.log and
/tmp/scorer-priority-reviewed-ui.log. Validation snapshot:
/tmp/scorer-priority-review-20261025. It excludes separate pre-existing unfinished
World tournament/one-way-mode changes in the working tree. An earlier full working
tree UI run had one old mode-switch test expecting a return to Free; that conflicts
with the owner's later one-way decision and belongs to that separate integration.
No new APK/AAB, Play upload, payment activation or physical Android locale test.

Research: 55 UEFA association pages retained; 53 linked publisher sites identified;
75 follow-up requests recorded. CBF returned503, Mexican/legacy Argentinian and
most European publisher destinations returned proxy403. See
docs/regulations/PRIORITY_STATUS.md. Do not call those priority regulations
extracted/implemented. The saved environment network draft needs user review/save
and Publish; this session has no Publish tool. Source checksum/reference checks
passed; no full third-party documents are bundled.

## 0.6.28 — separate Free/World APKs and stadium promotion

Owner decision supersedes single-app purchases: Free com.clemir.striker, World
com.clemir.scorerworld, separate private careers. No runtime in-app billing/mode
switch, no AdMob SDK or Internet permission in World. Free has11 local World
promotion board surfaces outside pitch boundaries, four cached message textures,
25second rotation, no touch/collision/tracking behaviour. World info explains
separate installation/career and disables the store link until an actual listing.

PASS:108 core/security +53 actual Kivy=161 tests on the scoped source snapshot;
syntax checks; both real arm64 debug APK builds; actual manifest/package/SDK
checks; Python3.14 evaluation of actual bundled edition flags; same existing debug
certificate; ZIP16KB and all118 ELF LOAD alignments >=16KB in both. Logs and full
behaviour/device test checklist: docs/TWO_APPS_0.6.28.md. Screenshot is desktop Kivy,
not Android. Initial World cache-directory mismatch and mirrored board text were
found and corrected before final artifacts. No physical device, paid purchase or
store release claimed. Separate unfinished tournament work remains preserved.


## 0.6.29 — Free English / World nine languages

Owner language request implemented without changing careers or simulation.
Free remains fixed English and stages no extra fonts/catalogues. World adds
nine complete offline209-message catalogues,212 localized country/region labels,
phone/manual selection and private atomic preferences. Canonical names, JSON,
custom aliases and editable input remain opaque. Official pinned regional Noto
CJK fonts/OFL and Babel/Unicode data licences are retained in World only.

PASS:118 core/security +61 Kivy=179 tests. An initial UI run exposed an incorrect
standings game reference; fixed before the complete passing suites. Deferred
layout locale loss was found and fixed/tested for paginated tables. Actual desktop
Japanese Help, Korean hub and Chinese picker renders were visually inspected.
Separate unfinished World tournament code is preserved outside the release
snapshot. See docs/LANGUAGES_0.6.29.md for build evidence and device limitations.

Both real APK builds PASS, version0.6.29/code1026629. Actual manifest/SDK checks,
Python3.14 bundled edition evaluation, catalogue/font byte verification, existing
debug certificate, ZIP16KB and118 ELF alignments per APK PASS. Free37,515,186bytes;
World71,431,971bytes. SHA256 in LANGUAGES_0.6.29_artifacts.json. No physical device
language test or production upload claimed.

Integration check: the main checkout with its preserved unrelated World WIP also
passed the same118 core/security and61 Kivy tests after the three-way merge.


## 0.6.30 — distinct launcher icons and labels

Owner request: two installed applications named Scorer and Scorer World.
Free label changed from SCORER Free to Scorer, retaining original S icon. World
uses Scorer World and a generated blue globe/WORLD companion icon. Separate
packages, signatures, private saves, language behaviour and SDKs are unchanged.
The existing staging test now verifies exact launcher labels and icon paths/bytes
and World-art exclusion from Free. No gameplay changes. See LAUNCHER_0.6.30.md
for actual build verification and physical phone checks still required.

PASS:118 core/security +61 Kivy=179 tests; both actual0.6.30/code1026630
APK builds. aapt2 confirms launcher labels Scorer and Scorer World on the
launchable activity and application. Actual launcher resource bytes exactly
match their corresponding different source icons. Same debug certificate,
separate packages, ZIP16KB/118 ELF alignments perAPK, correct bundled editions,
language resources and SDK exclusion checks PASS. No physical launcher test.


## 0.6.31 — World name, nationality and starting country

New World player form has independent nationality and starting country selectors,
localized offline search/paging, draft preservation and small-screen layout.
Existing canonical nationality/league fields persist after the first contract;
no schema or Free creation change. All nine languages cover the new UI.

PASS122 core/security +65 Kivy=187 tests, plus final catalogue checks after label
punctuation refinement. Initial missing form game reference and a pre-contract
save test assumption were corrected. See PLAYER_CREATION_0.6.31.md for actual
APK evidence and device checks still required.

Both real APKs PASS actual version/package/launcher art/signature checks,
Python3.14 bundled edition evaluation, actual configure_new_player/PlayerCountryPicker
bytecode presence, language/font/SDK checks, ZIP16KB and118 ELF alignments each.
World carries218 messages per language; Free has no extra language assets.
The merged main checkout with preserved unrelated WIP also passes122 core and65
Kivy tests (187). No physical device run was performed.


## 0.6.32 — Free entry removes Scorer World

Removed only the post-splash World action; New Game fills the row. Existing entry
button-set assertion updated. PASS122 core/security +65 Kivy=187 tests; actual Free
APK build, bundled EntryScreen bytecode, package/icon/signature/SDK, ZIP16KB and118
ELF checks. Actual desktop render inspected. See ENTRY_MENU_0.6.32.md and artifact
hashes. No physical phone or Play test. Latest World APK remains0.6.31.


## 0.6.33 — Free main menu removes World action

Removed from regular header and compact hub, preserving all ten Free actions and
offline stadium promotion. Existing responsive UI test updated for ten actions
and no WORLD button at six density/size combinations. See FREE_HUB_0.6.33.md.
World0.6.31 remains unchanged; no career/schema/gameplay/SDK changes.

PASS122 core/security +65 Kivy=187 tests; real Free APK build, signature/icon/edition/SDK/bundled UI, ZIP16KB and118 ELF alignment checks. Desktop render inspected; no phone test claimed.


## 0.6.34 — cleaner menu copy

Removed small entry edition/test-ad tagline, normal hub prose footer, generic
profile helper, redundant training-ad footnote and privacy SDK diagnostics.
Kept actual errors, core labels/statistics, Help, privacy/consent and ad actions.
Fixed dashboard hero insertion after footer removal. PASS122 core/security +67
Kivy=189 tests; both real APK builds and actual package/icon/signature/edition/UI,
SDK/font/language checks plus ZIP16KB and118 ELF alignments perAPK. Two desktop
renders inspected. No phone/production test claimed; see CLEAN_MENUS_0.6.34.md.


## 0.6.35 — compact new-career confirmation and top-left World logo

Replaced oversized fixed-height popup with wrapped content-sized opaque themed
ModalView. Shared MenuLogo aligns original art left and adds World product text;
entry logo now belongs to screen top left. Banners hide for confirmations and
stay hidden through rotation/profile transition. Cancel/backup semantics retained.
PASS122 core/security +71 Kivy=193 tests; four focused modal/brand/ad regressions.
Old52dp-only entry assertion updated to compact48dp minimum. Visual translucency
was found and fixed before final renders/rebuild. See START_LAYOUT_0.6.35.md.

Both final APKs PASS actual package/version/icon/signature/edition, bundled
CareerStartDialog/MenuLogo/main modal ad guard and opaque-panel keyword checks,
language/font/SDK payload checks, ZIP16KB and118 ELF LOAD alignments each. The
merged main checkout with unrelated WIP also passes122 core and71 Kivy tests.
No physical Android test was performed.


## 0.6.36 — World lettering matches Scorer artwork

Replaced the mismatched native Barlow WORLD caption with unified transparent
SCORER WORLD artwork, shared by entry/regular/compact menus. Free art is unchanged
and World-only PNG is stripped from Free staging.193 tests PASS (122 core+71
Kivy); World APK genuinely built, actual signature/manifest/edition/UI/PNG/SDK/
language/font contents, ZIP16KB and118 ELF checks PASS. Desktop render inspected;
phone test still required. See WORLD_WORDMARK_0.6.36.md.


## 0.6.37 — World standings P/PO/R eligibility zones

Read-only current-game zones across all active World standings/browser tables,
green/amber/red plus codes/ranges and full localized rule key. Highest/lowest-tier
limits and owner two-tier/no-playoff fallback retained. Priority-country model
and its35% hero playoff outcome remain provisional/simulated, with explicit UI
notice; no season engine, NPC movement or knockout fixtures implemented here.
125 core/security +75 Kivy=200 tests PASS. Narrow touch targets corrected; neutral
hero highlight avoids promotion-colour ambiguity. World actual APK build/content/
signature/SDK/font/language/ZIP16KB/118 ELF checks PASS. See STANDINGS_0.6.37.md.

Integration check: the merged checkout with preserved unrelated World WIP also
passes125 core/security and75 Kivy tests (200). No physical phone run claimed.


## Free0.6.38 — optional aggregate statistics and own collector

143 core/security +79 Kivy=222 PASS. Default-off opt-in, fixed counters only,
atomic local state/withdrawal, offline expiry, no career upload or identifiers.
Own localhost collector ingestion and email preview tested; deployment/SMTP not
active. Actual Free arm64 APK built, certificate/package/API36/payload/16KB checks
passed. Endpoint empty, therefore no developer uploads in this beta. World no-op
staging verified by tests; no new World APK. See ANONYMOUS_STATS_0.6.38.md.


## Free0.6.39 — owner start/end session email preference

Nine fixed counters including normal-stop completion; no pause-based fake end,
no force-stop guarantee, explicit in-flight follow-up, no identifiers. Server-only
new-total session notice preview/checkpoint/SMTP command, no daily schedule needed.
148 core/security+80 Kivy=228 PASS; actual Free APK/package/signature/API36/content/
ZIP16KB/118ELF checks passed. No live hosting/SMTP or device testing, endpoint
empty and collection default-off. See SESSION_NOTICES_0.6.39.md.

## Apps Script connection preparation — 2026-10-26

Owner selected Google Workspace and requested connection. Runtime/tool discovery
found no authenticated Google identity or Apps Script deployment capability, so
no Google project, trigger, deployment or mail was created. Added Code.gs and
minimal manifest plus exact owner setup/client follow-up requirements. Script
validates strict9-counter Free schema, discards non-session counters, aggregates
start/end pending counts without player records, defaults off, fixes recipient
server-side, uses minute polling/60-notice daily cap and bounds pending retention.
Node functional/security tests with mocked Google services PASS: off/PII/wrong
app/bool/negative/overflow, no request-triggered email, aggregate send/clear,
minute guard, SMTP-provider failure/quota/cap and private response/header guards.
No real mail or Google authorization/redirect validation claimed. Existing
APK0.6.39 remains empty-endpoint and does NOT support the Apps Script URL or
response redirect yet; actual URL/account activation is the next dependency.
No game/save/app code was changed; unrelated World WIP preserved.
See server/apps_script/README.md. Next: owner account deployment URL, bounded
Apps Script transport/client tests and actual device beta, then live validation.


## Explicit Exit notice ordering — source-only follow-up

Owner requested another notice when Exit is used. Confirmed SAVE AND EXIT now
records sessions_ended before the explicit nonblocking flush and app.stop, after
successful career save. Failed save, cancel and background do not signal Exit.
The existing on_stop guard prevents counting the same ending twice. Default-off
consent and World no-op remain unchanged. A new real Kivy case checks failed-save
suppression, end-event presence at flush/stop and duplicate-stop protection.
148 core/security+81 Kivy=229 tests passed. Apps Script mocked security/functional
checks also passed. No app version bump/new APK/real email is claimed for this
source-only change; current APK0.6.39 and empty endpoint remain unchanged. The
receiving service is still not deployed/configured. Next: actual owner-hosted URL,
client transport validation and configured APK/device test before enabling mail.

## Windows Free first desktop candidate — 2026-10-28

Original Kivy Free only, one division/English/fictitious clubs. Added launcher
with persistent per-user saves independent of executable/temp resource path and
save/cancel title-bar close handling. Native PyInstaller single-file staging/
requirements/spec and Windows2022 build/frozen smoke workflow. Desktop Privacy
and training omit Android ad claims/reward videos; Android behaviour retained.
154 core/security+83 real Kivy=237 tests PASS; Apps Script mocked checks PASS.
Real Linux source Kivy smoke PASS: splash/new career/offer/training/save/reload,
fixed Free/no SDK/default-off local stats; not a Windows binary test. Initial new
save test incorrectly expected a no-club menu state to create a save; corrected
the test to start a career first, preserving existing no-empty-save behaviour.
Windows native workflow is the next build gate; no EXE or Windows functionality
is claimed at this point. No Android APK rebuild/version/store/payment changes.
See docs/WINDOWS_FREE.md. Unrelated World/career WIP remains preserved.

Windows run40665092529 stopped before build: Kivy[base] constrains Pillow<11,
conflicting with the explicit11.3.0 image-tool pin. Use core Kivy2.3.1 (its normal
Windows SDL2/ANGLE/GLEW dependencies remain included) and separately pinned Pillow
for icon conversion; no unused base extra. Repeat native build before claims.

Windows run40665288718 resolved dependencies but caught two test path assertions:
Windows expands RUNNER~1 short paths to the same runneradmin directory. Resolve
expected paths too; keep the correct canonical persistent path in production.
Enable UTF8 consistently for Windows tooling and rebuild on Windows-test changes.
No application save or gameplay change was needed for this test correction.

Windows run40665514334 passed all6 native staging/save tests but remained in
PyInstaller analysis. Kivy's GL initialisation can show a blocking Windows modal
when default OpenGL is unsupported. Cancelled this run to use ANGLE consistently
in the build-hook subprocesses as well as frozen smoke. Windows launcher defaults
to bundled ANGLE too (explicit user backend override retained). Re-run native
build/smoke; no successful executable is claimed from the cancelled run.

Windows run40666480471 successfully built and launched the frozen AMD64 EXE;
6 native checks and career/training/save/reload flow PASS, and PE/archive checks
passed on the downloaded41,547,717byte file. However the immediate post-mutation
capture was black. Do not use that capture as visual evidence. Schedule capture
after another frame and add an actual nonblank rendered-image gate, plus native
window-close confirmation/cancel check. Linux source smoke of this delayed flow
PASS. A new Windows frozen run is required for the final delivered artifact.

Windows run40667096800 again passed frozen functional flow, including window-close
confirmation, but the stricter image check rejected its black screenshot. SDL's
Kivy screenshot helper reads GL_RGB after buffer swaps; that is not portable to
ANGLE/GLES. Smoke capture now reads guaranteed RGBA before on_flip swaps/discards
the backbuffer, then stops on the next Clock tick. This affects automation only;
keep the visual gate and require a new native run rather than claiming a render
from a black image. Initial window config now precedes Window creation too.

Final Windows run40667690804/source0c33da6 PASS:6 native staging checks, built
frozen AMD64 EXE, new career/training/save/reload/exit confirmation and nonblank
rendered hub image (visually inspected). Downloaded artifact PE/archive boundary
checks PASS;41,548,924bytes SHA256 eac0b07abf836ee876e6af73ff0ea1a269e42fe0b272a7cd03afd9bf72744e56.
237 source core/Kivy tests remain passing, plus isolated Pillow-enabled source
RGBA capture smoke. No full manual Windows match/audio/resize/human validation,
code signature, Microsoft Store/public release or Android rebuild claimed.
Single-file QA distribution branch/windows guide/artifact preserve evidence.


## Windows0.6.39-win.2 — matchday/league leaders dashboard

Exact current league pairings/highlight left, saved scorer leaders right, compact
hero/season footer, original Training/Play gate and all navigation retained.
No main scroll or RNG/save/schedule changes; scoped Windows signature refresh and
small-window fallback, Android original dashboard retained.158core/security+
87Kivy=245 PASS. Source staged Windows-profile smoke includes engine match finish,
NPC scorers, save/reload,12visible games and close/cancel; actual root FBO render
avoids stale ANGLE framebuffer/modal capture. Native Windows build is the next
gate; no final EXE claimed yet. See WINDOWS_MATCHDAY.md for cases/limits.

Windows native run40729867510/sourcef842a66 PASS. Frozen EXE displays12current
league pairings/highlight and9leading scorers in1280x720; root-canvas capture
visually inspected. Automated engine match/career/training/save/reload/window
close-cancel pass. PE/archive fixed-Free/no backend/keys/save/World art checks
PASS;41,561,488bytes SHA256 bfcb4170c299c71f607e484cde5de36ac799f505e4263dd28bab4ebf1b32189a.
Source158core/security+87Kivy=245 PASS, plus6 native Windows staging checks.
Windows0.6.39-win.2 direct EXE preserves save folder and schema. No Android rebuild,
manual full-match/audio claim, code signing, production ads/payments or server
activation. WINDOWS_MATCHDAY.md and artifact/capture retain evidence.


## Windows0.6.39-win.3 — larger goal/depth fix/local sponsor copy

Single per-game Windows geometry +12%width/+10%height, consistent frame/net/physics/
aim and unchanged Android dimensions. Depth bug removed active-state branch;
resting net balls stay behind frame/keeper, between-plane and held-ball cases
handled. Rounded shaded goal tubes, cleaner translucent net, proportional far
ball and4bounded local English sponsor/World messages.161core+92Kivy=253PASS.
Paired80hard shots/profile:18/80original vs26/80Windows,0unresolved at15s; not a
human goal rate. Source staged hub/engine/save smoke and static goal/depth render
pass. Native Windows build/visual verification pending before delivery. See
WINDOWS_GOAL.md and WINDOWS_GOAL_CALIBRATION.json. Unrelated WIP preserved.

Native Windows run40740304128/sourcef9b6f05 PASS: frozen8.1984x2.684goal/depth,
12fixture hub, real engine match/save-reload/exit-cancel and hub+static-goal render
checks. Goal capture visually inspected. PE/archive confirms profile module,
no active-state term in frozen depth helper, fixed Free/no keys/career/backend.
41,565,437byte EXE SHA256 0dd70a7f7f2e5c1def7aad62351e492ea34007cf6aeebc2fd028728937107eac.
253source cases +6native Windows checks. Direct unsigned QA candidate0.6.39-win.3;
manual human shot/audio/full-game and code signing remain pending. Career schema/
folder unchanged, Android no new artifact; public sponsor/server/store inactive.
See WINDOWS_GOAL_artifact.json and actual static Windows capture.

## Windows0.6.39-win.4

# Windows Free 0.6.39-win.4

Windows only: goalkeeper pose, reach/collision volumes and rendered thickness
reduced14%; shot flight duration divided by1.22 (22%higher horizontal velocity)
with gravity recomputed to retain aim destination. Includes headers and ordinary
shots, normal training/match code. Original Android scale, speed/clamps and crowd
remain exact under the default profile. No Android APK rebuilt. Shared constants,
career schema, goal dimensions, aim dispersion and NPC results unchanged.

Windows training hides only crowd mesh draws; real stand geometry remains.
Match crowds return automatically without invalidating caches. Sponsor boards stay.

Paired80-seed hard-shot bot calibration: original18goals/37saves/25misses;
previous Windows26goals/34saves/20misses; current37goals/19saves/24misses.
All resolve through physical code. Bot corners/instant aim are not human rates;
owner should play a full match before accepting difficulty. No automatic goals.

Validation: core/security161 pass; actual Kivy93 pass (including6 focused profile/render checks) including unchanged
Android profile and crowd call checks; native Windows run40743617913 PASS:6 staging checks, frozen career/training/match/save-reload/close and nonblank hub/goal/empty-training FBO renders.
Files: main.py, desktop_launcher.py, tools/windows/verify_smoke.py,
ui_tests/test_goal_geometry.py. No new dependencies, network uploads or secrets.
Next: Windows human mouse/keyboard match/training test and save/reload.

Unsigned Windows x64 EXE: 41566939bytes. SHA256 `e515818e052573f7f0c76f271a3246085ba19ae93ed07c51ad9c18209c98e529`.
[Download win.4](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/windows-beta-0.6.39-4/Scorer-Free.exe).
Static training capture reuses the test result state (SHOT4/3), not a playable fourth training attempt. No claim of full human match validation.

Core/security161 and Kivy93 PASS. Initial core attempt used Kivy venv missing fontTools/cryptography; repeated with existing system dependencies, all pass. Focused test typo STATE_AIM corrected to STATE_AIMING. Pre-existing WIP patch preserved byte-for-byte. No Android build or production services activated.

## Scorer0.6.40


## Verified artifacts

166core/security +96Kivy tests PASS. Added30real engine crossed-shot cases inside
one regression.5actual local HTTP/client tests,2Kivy online UI cases included.
Windows native run41115421830/sourcef688333 PASS:6staging checks, real frozen
career/training/automated engine match/save-reload/close, fullscreen true,
1024x768hub/goal/empty-training FBO renders. Human full-match still owner test.
Android Free/World0.6.40 code1026640 both actually compiled; signatures preserve
prior debug certificate, ZIP16KB and118ELF LOAD16KB checks PASS. World verifier
initially assumed a single bool constant; fixed to verify named WORLD_BUILD and
WORLD_PREVIEW assignments instead. No APK binary change required for verifier fix.
Existing source regression expecting random target dispersion now asserts fixed
marker target, bounded compensated speed and original training distances. Initial
run failed obsolete expectation; final complete suite passes. No failures hidden.

Static training screenshot reuses final smoke state SHOT4/3; it is a render fixture,
not a playable fourth shot. Existing careers/WIP retained; no release signing/Play
store activation, remote destination or human Android device testing claimed.

See ONLINE_0.6.40.md and artifact JSON for exact evidence. Own-host laptop service remains uninstalled pending access/owner terminal commands; existing Cloudflare Tunnel avoids static-IP/router configuration.

## Scorer0.6.41 — owner-hosted integration

167core/security and97Kivy checks PASS; actual public submit/read/withdraw and
private totals denial PASS; one technical session counter accepted by owner server.
Three builds configured with public HTTPS origin, no administrator credentials.
Shared default-off usage factory now covers World per owner request; existing
legacy app discriminator keeps aggregate protocol compatible with installed server.
Android real bytecode/CAasset checks, old upgrade signature and16KB ZIP/118ELF
PASS. Initial4-column _arrange caused fifth footer action to wrap and test failed;
fixed5columns, reran whole UI suite PASS. Root unrelated WIP preserved with targeted
merge of test helper's existing world parameter and new network isolation patches.
Native Windows evidence/download recorded after build; physical phone/human match
not claimed. See CONNECTED_0.6.41.md.

Native Windows41123889956 PASS; actual archive/CA/endpoints and main button validated. Source74c07af, see CONNECTED_0.6.41_artifacts.json. Prior setup/cache-stalled41122999548 cancelled; no gameplay change. Normalized Windows text CRLF for public CAcontent comparison. Both APKs verified, no human phone test claimed.

## Scorer0.6.42

174core/security+98Kivy PASS, focused4rerun after sparse-row anchor correction. Final native41132392263/source4339c88 PASS with records render; old artifact discarded. Both final APKs rebuilt and signature/16KB/bytecode PASS. Additive local server/legacy migration HTTP tests PASS. Public v2 last probe404, laptop upgrade still required. New consent2 needed for player names/team; usage unchanged. Unrelated World/career WIP retained. See SEASON_RECORDS_0.6.42.md and artifact JSON.

## Scorer0.6.43 ad-free / official Google Play review

176core/security+98Kivy PASS, native6staging+frozen Windows41192102865/sourceb1ac79f PASS with adfree_release and empty sponsor cache. Actual Free/World DEX forbids GMA/UMP/Billing/custom bridges; permissions only Internet/network-state, original debug upgrade signature and ZIP16KB/118ELF checks PASS. Actual native stadium capture inspected, no panels. New production gates remove obsolete mandatory ads/same-app billing; deliberate IDs/enabled billing now rejected. API36 fits current official requirement. Rewrote listing/privacy/Data Safety drafts and recorded remaining public-policy/contact, Families/social/UGC, release-AAB and account closed-test work. Email inaccessible and owner explicitly waived it; reviewed official sources, no claim of reading email. No production AAB, store submission, cloud/laptop/DNS/mail change, real payments or human phone test. Unrelated WIP preserved. See POLICY_REVIEW_0.6.43.md and artifact JSON.

## Scorer0.6.44 foreground session counting

179core/security+99Kivy PASS, local HTTP collector SUM sessions=2 for two openings. Old splash-only/per-process flag missed warm reopen; lifecycle start/pause/resume now increments each opening exactly once locally, persists before send and retries pending every10s. Native41241589273/sourceb4137e3 PASS with minimize/restore callbacks count2 and default-off actual game consent restored. Both actual APKs signed/16KB/bytecode/ad-free verified. No manual owner counter/server/credential change; old missed counts not invented. Protocol unchanged, remote ACK ambiguity/offline delay remains documented. See SESSIONS_0.6.44.md/artifactJSON; real phone owner test pending.

## Scorer0.6.45 automatic usage

Owner confirmed second session received then required no off switch. Actual app factory mandatory, old Off ignored, controls/actions removed; splash and Privacy disclose automatic aggregate counters. Public records remain optional. 180core+99Kivy PASS; native Windows41248241931/source52db76ad frozen automatic disclosure/session smoke PASS plus6staging checks. Both actual APKs bytecode/signature/16KB/ad-free verified. Fake QA transport installed before startup; no manual historical-total or laptop changes. See AUTOMATIC_0.6.45.md and artifact JSON for limitations.

## Google Play audit —2026-10-31

Reviewed current0.6.45 source/artifacts against12official pages fetched200; recorded source URLs/text hashes and objective checks under docs/play/evidence. Three production-config/manifest regression checks PASS. Public read-only health/v2 return200, unauthenticated totals404; no synthetic events, public names or owner credentials used. Missing identity/support/privacy confirmed, production staging CLI gap, UGC/moderation/adult controls, automatic collection legal/disclosure basis, World notice translations, final store assets/AAB signing/device/Console gates documented. Replaced obsolete Play README that still instructed single-app AdMob/Billing; corrected version headers. Full audit PUBLISHING_AUDIT_2026-10-31.md. No app behavior, server, payment, upload or rollout changes.

## Scorer0.6.46 publication preparation —2026-11-01

Owner confirmed active/verified account, Gonçalo Pereira/goncalo@clemir.com public, minors included, World FREE. Implemented detailed pre-send notice without usage toggle, adult-managed social access/local PIN lockout, explicit terms and v3 pre-publication review, public report/block IDs, private moderation pagination/actions, safe edition-bound career transfer/Android SAF/desktop chooser, periodic retention/aggregate-only backups, public policy/terms/deletion page implementation, production staging/review and certificate gates,9language publication messages, store-size art/listings. Corrected obsolete Free Help ads claim. Original WIP preserved unstaged.

193core/security+105Kivy PASS (298unique), backend13 and mandatory-usage independence focused checks PASS. Actual native Windows41254289408/sourceceeeb0a6staging+frozen PASS, no owner QA traffic. Both debug APKs preserve original certificate, actual compiled safety/factory/SAF inspected; both NEW unsigned release AABs bundletool/static/derivedAPK/16KB/118ELF PASS. No production signing/Play/physical Android claim. Publichealth200/v3/privacy404: owner laptop deployment pending. Policy default moved to public /opt/scorer/public.json, preserving root-only /etc/scorer for admin secrets. Precise source/backend commits, hashes and limits in docs/play/RELEASE_0.6.46_artifacts.json.

## Public policy next step —2026-11-01

Owner screenshot confirms server schema3, health and maintenance timer installed; policy example refused because empty legal/provider/minor/transfer fields. Prepared full PT/EN policy proposal with current public Cloudflare/Google references (5official HTTP200 sources/hashes), clear draft marker/noindex and no inferred account settings or approved legal basis. Public terms/removal depend only on verified identity/contact. Missing policy status defaults draft. Added narrow transactional installer: stop/start only scorer-online, update2public renderer/config modules+public.json, verify3loopback documents, restore prior files on failure; refuse published/complete legacy policy downgrade and symlinks before reads. No token/SQLite/tunnel/timer/career manipulation, no change to client APKs or production review flags.13new focused+3existing backend checks PASS; --check PASS. Exact pinned laptop commands and previews in POLICY_NEXT_STEP_2026-11-01.md. No cloud SSH or actual deployment claimed.

## World 0.6.47 — 1 November 2026

World-only free Play scope, no ads/IAP, editor retained. Final English public policy/terms/removal and listing; owner Tunnel/proxy report and legal exceptions recorded. Privacy-request suspension is real and survives offline/restart; no case ID in usage or aggregate backups. 216 core/security + 108 Kivy = 324 unique tests passed. Actual matching-debug-cert APK and unsigned rehearsal AAB passed compiled-source equality and 118 ELF/16KB/static/bundletool checks. Existing unrelated root WIP preserved. No physical Android, production signing, laptop deployment or Play upload claimed. See RELEASE_0.6.47_artifacts.json and SERVER_0.6.47.md.

## World 0.6.48 — competitive difficulty

Owner requests averages above one goal/match to be difficult. Progressive opponent-tier keeper reactions/footwork/height-directed high and low saves and pre-aim central/far-side marking implemented. Existing physical target/goal/collider geometry, training and morale opportunity floors retained; no score cap or recent-goal adjustment. 218 core + 111 Kivy = 329 tests pass. 6,400 paired physical shots each before/after; synthetic season evidence and limitations in DIFFICULTY_0.6.48.md/data JSON. Native high/low save captures inspected. World debug APK versionCode1026648 retains upgrade certificate, exact compiled modules and 118 ELF/16KB verified. No physical Android or Play-production claim. Unrelated root WIP preserved.

## Release numbering: 0.9 testing, 1.0 public launch

Owner selected 0.9 for the next test and 1.0 for publication. Edition staging reads names/codes from world-launch.json; separate production public config defaults to code1030000, above test1026900 and delivered1026648. Production rejects reused/lower test codes and still requires review assertions/signing. 33 focused edition/publication/release tests pass, including actual 0.9 staging and 1.0 default/custom production staging under synthetic test-only review flags. No new APK produced. Current readiness documented in ROAD_TO_1.0.md: live policy remains draft/bilingual, delivered international competition progression is simplified, real Android and actual production/Console checks remain. Existing gameplay and unrelated root WIP preserved.

## Scorer World0.9 — World competition implementation

Owner requested closing launch point1. Integrated/reviewed existing competition WIP and completed actual fixture/group/Swiss/knockout/qualification simulation, domestic cups, national qualifiers and World Cup104fixture finals, Nations game leagues, played promotion playoffs and balanced global club movement. StableUIDs/aliases, future qualification snapshots, compact membership, elapsed-save migration and mid-run-in final-table persistence retained. Distinct within-week World slots avoid chronology reversing at rollover. New paged World competition views and nine-language messages. Unrelated badge cleanup/mode preference WIP remains excluded.

233core +114nativeKivy =347tests PASS. Three seeded seasons:148controlled player-team fixtures,9reloads, actual World Cup/Libertadores/Copa/qualifiers,3archives; no repeated fixtures or backward calendar dates. Current fixtures/tables captured natively. APK0.9/code1026900 built and exact compiled source plus compiled competition/save smoke checked using matchingPython3.14;118ELF/16KB and existing debug upgrade cert verified. These are host/engine QA checks, not physical Android or Play-production approval. Point2(real handset acceptance),point3(actual final-policy/server operation) andpoint4(production signing/Console) remain. Source/proof in WORLD_COMPETITIONS_0.9.md and data/world_competitions_0.9.json.

0.9 final UI acceptance additionally checks imported aliases across countries in international fixture lists and calendar rows, resolving club names by stableUID and national team names through the country catalogue. World history carries sideUIDs for unambiguous presentation after rename/promotion. Final candidate validation totals233core+115Kivy=348unique checks.

## 2026-11-02 — 0.9.5 built-in club home colours

- Added 352 offline UID palettes matching the current eight-country real-name
  pack (272 active clubs plus 80 reserves), with factual source revisions and
  explicit representative-colour overrides. Names import is independent.
- Training resolves the current club instead of stale international participants.
  Existing World palette fallbacks follow UID after canonical edits too.
- Core suite: 249 passed. Native SDL/Kivy suite: 121 passed. Final delivery checks:
  15 passed (edition staging, kit movement/import/save/fallback and presentation).
  Syntax compilation passed. Native tests are host tests, not a physical phone.
- Initial tests correctly exposed two obsolete presentation expectations; updated
  fallback tests to remove both data sources and Porto to its new palette. A new
  transfer fixture initially lacked an actual agent offer; corrected the fixture.
- First APK source/data verification rejected a missing club_kits.json: staging
  allowed only the older world_clubs.json. Added the new data to the explicit
  staging allowlist and a byte-for-byte staging regression assertion. Rebuilt in
  a fresh staging directory; distribute only the final verified candidate.
- Source/ELF/signature and compiled-behaviour APK evidence is recorded separately
  in RELEASE_0.9.5_artifacts.json. Annual patterns/away kits, real palettes for
  unsupported countries and researched national competition formats are not
  claimed complete by this release. Public version remains 1.0.

## 2026-11-03 — redone0.9.6playoff/call-up iteration

- Implemented persistent access brackets, conditional standings zones, neutral
  finals, aggregate/extra-time/rank/shootout decisions and variable reserve
  movement. French ladder, Championship six-team field, Brazil independent ties,
  Italian points thresholds and B-team exclusions have behavioural coverage.
- Replaced the national selection gate with positive-goal competition rank1–3 in
  any current first division, independent of morale/form and club country.
  Window selections persist; caps/goals remain separate from club counters.
- Pinned FIFA April2026PDF window ranges2025–2030 and known final ranges. Fixed
  Friday national games preempting Thursday club games, and Nations League
  membership being discarded during a season without that tournament.
- Core suite:266passed. Final native SDL/Kivy suite:124passed. Final targeted
  backend delivery:46passed; native playoff/zone/relegation delivery:10passed.
  Syntax checks passed. This is390unique host tests, not physical-phone testing.
- Earlier verification exposed a country-variable shadow during rollover and
  stale three-up expectations. Fixed the variable and made promotion-test heroes
  explicitly eligible instead of accidentally choosing Portuguese B clubs. Added
  a native test that the actual match AI calls the neutral-venue goal-budget
  helper; a backend-only neutral test did not establish that wiring.
- Final APK verification records exact bytecode/data, actual compiled French
  playoff progression and call-up gate, upgrade certificate,118ELF16KB and release
  payload checks in RELEASE_0.9.6_artifacts.json. No server change or Play upload.
- Owner expanded scope to real formats in every country. Research now indexes
  candidates for212countries across608retrieved articles. Full group/split/period
  models and real capacities remain OPEN;0.9.6is an access/calendar iteration,
  not a completed worldwide real-format release. See RELEASE_0.9.6.md.

- Distribution follow-up: direct large Git pushes timed out (HTTP408). Source
  commits were pushed successfully. The exact tested APK was transferred as
  checksummed parts through the GitHub API, reassembled and hash-checked in
  Actions run41693874115, then published as the single uncompressed APK attachment
  in prereleaseqa-0.9.6. Public download independently verified74105187bytes and
  SHA256`646cbcc046db50b2bb8dde880c06ae5931e1dccbcace435b2bb4f6ca2e766886`.
  No binary rebuild or alteration occurred during transfer.

## 2026-11-04 — 0.9.8 decisive match moments

Implemented live-score late opportunities, actual final/playoff context, thirteen
UID-bound derby pairs and close direct-relegation run-in context. Retime only an
existing final chance using independent RNG after AI events are sampled; never
alter shot physics, chance counts/clear index or goal budgets. Persist one actual
moment outcome in fixture history and render it in nine languages.

Initial core suite:302 passed; additional survival-boundary test and targeted
localisation suite passed. Native suite initially129/130: retained match notice
did not refresh the headline when changing language. Added language to the
notice signature; the four targeted integration tests passed. Final full native
suite and APK evidence are recorded in RELEASE_0.9.8_artifacts.json. A repeated
staging invocation correctly refused a non-empty output directory; the final
build uses a fresh staging directory. Unrelated root badge/UI WIP is retained.
No physical-device, production signing, Google Play or live-server validation.

Final0.9.8 validation:304 core +130 native Kivy =434 passing. Actual APK compiled
source matches commit6cc2436; API36/code1026908/arm64,118ELF16KB, ZIP alignment,
existing upgrade certificate and compiled competition/save/publishing checks pass.
Public attachment SHA256/bytes independently verified; see download evidence.
The initial delivery dispatch used the preceding branch revision and was cancelled.
The current dispatch initially could not create a release with its integration
identity; release metadata was created using the configured owner CLI and the
same workflow rerun successfully uploaded the checked APK. No credential or key
was changed. Local direct upload remains unsupported by that CLI identity.

## 2026-11-04 — 0.9.9 weekly coach meetings

Added mandatory saved weekly coach meetings before training/play, including
week jumps, new clubs/seasons and both hub layouts. Stable club personalities,
three-game drought feedback spaced by appearances, decisive-performance and
strong-form feedback; brief routine meetings otherwise. Store bounded optional
coach state without changing physical gameplay, RNG or career identity.

Initial core suite313 passed, with nine dedicated coach tests. Legacy migration
was then tightened to retain training progress but require the meeting before
resuming; dedicated coach and localisation tests passed. Initial native suite
identified existing fixtures that skipped the new mandatory step, the extra
hub action count and a test that searched the wrong button subclass. Updated
those tests to use meetings and assert the new disabled state explicitly; the
four dedicated native coach tests passed. A tenth core coach test verifies that
national-team appearances do not alter club feedback. Final suite/APK evidence is recorded
in RELEASE_0.9.9_artifacts.json. Window screenshot readback was black in this
host; widget export also lacked complete text. Neither is device visual validation. Unrelated root WIP remains excluded.

Final0.9.9 validation:314 core +134 native Kivy =448 passing. Actual APK compiled
source matches commit e83a9da; API36/code1026909/arm64,118ELF16KB, ZIP alignment,
existing upgrade certificate and compiled coach-gate/save, competition and
publishing checks passed. Public download evidence records the actual bytes and
hash. Temporary GitHub push HTTP500 errors were resolved using the same remote
with HTTP/1.1; no credentials or signing keys changed.

## 2026-11-04 — 0.9.10 conditional coach meetings and newspaper

Owner correction: remove routine weekly meetings; only droughts and actual key
matches create requests. Only a pending request blocks training/play. Preserve
coach personalities and save-before-unlock. Added key-match reviews after poor
performances and same-week repeated key fixtures; ordinary strong form and
missed late chances no longer force meetings.

Added offline SCORER DAILY with a paper layout, serif text, factual result-based
headlines, observed/conserved goal chronology, conditional personal mentions,
negative-performance streak and five original generated rotating photographs.
Assets/provenance/font licence are documented in NEWSPAPER_ASSETS.md. The latest
report/rotation persist; legacy history gets score-only reporting. No invented
player statistics, quotes, events or photo attribution. Existing root WIP stays
excluded from reviewed source and APK.

Initial core324 and native139 passed. Added goal-clock/conservation checks after
that run; final core/native and exact APK evidence follow in release metadata.
No physical-device, production signing, Google Play or live-server validation.

Final0.9.10 validation:326 core +140 native Kivy =466 passing. Actual APK compiled
source matches commit df26ae8; API36/code1026910/arm64,118ELF16KB, ZIP alignment,
existing upgrade certificate, bundled photo/font bytes and compiled conditional
coach/newspaper/competition/save/publishing checks passed. Public download
attachment bytes/hash were independently checked; see download evidence.

## 2026-11-04 — regenerated real-name JSON downloads for0.9.10

Added an offline current-capacity pack:378 clubs/16 leagues/2403 player aliases,
including26 added clubs and120 added sourced player names. All previous club/
player aliases are preserved. Added a352-club compatible variant for older
career layouts, which retain old capacities and reject unknown expanded UIDs.
Both files pass actual editor validation; apply/private backup/reload preserves
progress and competition state. Real initial tiers and country/team uniqueness
are checked against the reviewed registry. Players remain the July2026 snapshot;
missing source squads stay fictional. No app/UID/physics change or APK rebuild.
Six dedicated generation/import tests passed; related regression checks follow.
Related regressions:5 division-pack and8 two-division tests also passed,19 total.
Published uncompressed JSON attachments through the conditional names-delivery
job; six dedicated tests also passed in GitHub Actions. Both public downloads
returned HTTP200 with attachment disposition and exact checked bytes/SHA256.
See docs/data/name-packs/current-downloads.json. No APK rebuilt or game changed.

## 2026-11-04 — 0.9.11 page layout, coach portraits and World editor

Replaced the newspaper scroll reader with a measured single-page layout. Use
full/concise editorial text, stable facts and conditional personal mentions,
responsive columns and a smaller illustration on tight screens. Back48dp;
body>=12sp in tested cases. Ten original generated coach-at-desk portraits are
bundled and saved with bounded club/index identity. Actual transfers always
change the face, with no match RNG use. Editor moved from all main hubs into
World's search row; Back/Escape return to World. No IDs/rules/physics changes.

Core336 passed. Targeted UI tests exposed old thumbnail-size assumptions and
an extreme56-character CJK club-name overflow at320×240. Tightened the compact
edition (remove repeated result prose, use a score-led heading and put photo/
score in the masthead). The worst-case Latin/CJK tests then passed. Final full
native and actual APK checks follow in release evidence. The first full native
run passed143/144; one historical test still expected direct main-menu editor
access. Updated it to assert absence in the hub and follow World > Names Editor. Original image hashes
are documented in COACH_PORTRAITS.md; no physical Android validation claimed.

Final0.9.11 checks:336 core +144 native Kivy =480 passing. A final conservative
fractional-width measurement adjustment was rechecked by the6 newspaper UI tests;
all passed and the APK was rebuilt from a fresh staging directory. Actual compiled
source matches commit4f372ba; API36/code1026911/arm64,118ELF16KB, ZIP alignment,
existing upgrade certificate, all ten portrait bytes and compiled appearance/save/
competition/publishing checks passed. Public attachment evidence follows.

## 2026-11-04 — 0.9.12 folded newspaper and full goal reporting

Rebuilt the reader as an inset, folded-paper window on a dark background with
shadows, crease, reverse-sheet print and paper grain. Added original display and
pixel news fonts with source/OFL licensing. Photo participates in actual text
flow beside/below it and across columns. Long reports can turn leaves without
scrolling, truncation or omitted words; typical four-goal phone report fits one
leaf. Capture screenshots use the real desktop Kivy main loop and were visually
inspected at1280×720 and1280×591/density1.4; they are illustrative host renders.

All recorded goals now get minute/team/running-score narrative, plus a factual
comeback/draw/margin/penalty summary. Unknown historic clocks remain explicitly
unknown and use team totals. No invented scorers or changed personal-mention
criteria. No model/UID/physics changes. Core340 passed; font, article and locale
targets passed after singular-wording cleanup. Initial full native runs exposed
tests that assumed an unbroken player name/empty-message phrase in one label.
Updated them to inspect the complete flowed text across leaves. Final full native
and actual APK evidence follow. Unrelated root WIP remains excluded.

Final0.9.12 validation:340 core +147 native Kivy =487 passing. After the last
compact-header adjustment all9 newspaper UI tests also passed. Actual compiled
source matches commit7fd0e42; API36/code1026912/arm64,118ELF16KB, ZIP alignment,
existing upgrade certificate, original TTF/licence bytes and compiled four-goal/
summary/competition/publishing checks passed. Public APK/preview byte checks are
recorded in the release download evidence. No physical Android validation.

## 2026-11-04 — World 0.9.13 fair finishing and training/coach feedback

Owner asked to remove scoreboard badges, ease finishing, stop keeper arm stretching,
keep aim scorable, improve practice information/remove practice opponents and add
coach feedback. Source 2fabe132965363a2ef7a6da74eab0e101b89ebcf stages only these
changes; unrelated badge implementation cleanup/mode state WIP remains unstaged.

Final clean-source core: 340 passed (130.793 s); native: 153 passed (170.571 s).
A targeted 7-test repeat confirms compact 800x360 training and fair finishing;
its viewport setup was corrected to restore Window.size and avoid test-order
coupling. Earlier runs caught a training attribute typo, old shot-time assertions
and excess small-window content. Fixed before final verification.

Built World 0.9.13/code1026913 arm64 DEBUG APK with existing upgrade certificate,
API36/min26. Android candidate, exact compiled source/data, actual competition
load/rollover, rehearsal payload and publishing-module checks all passed. All118
ELF files and ZIP layout retain16KB alignment. No physical handset, production
signing, Play upload or live server changes. Runtime evidence:
/workspace/striker-runtime/0913; metadata/limits in RELEASE_0.9.13.md and artifactJSON.

Delivery: workflow41869386481 succeeded. Public APK and both Portuguese preview
attachments returned HTTP200 with Content-Disposition attachment and exact local
SHA256/byte matches. APK107333547B, SHA25617d2d9617ac2b2810737b022b963fd284dd4f7ffb76818323c1c424c7aa1a104.
Temporary qa-upload-0.9.13 transfer branch removed after public verification.

## 2026-11-04 — World0.9.14 every goal, wide aim and per-match training

Source6abc1876235913a2581181822707aaa0bd7e3694. Every personal goal gets a
headline and article mention; ordinary goals are not falsely called decisive.
Aim now sweeps both posts and slightly beyond. World same-week fixtures exposed
that the weekly training flag stayed valid after cup/national matches; every
completed appearance now consumes the session. Completion requires three saved
shots and rewards use saved goals. Old gate-less completed sessions reset once;
partial sessions retain progress. Source/clean archive excludes unrelated WIP.

Final core345 passed in121.386s; native154 passed in163.778s, total499. Targeted
four core gate tests and seven native finishing/Play tests passed. Core covers
World same-week club/cup and national consumption/reload, incomplete sessions,
authoritative goal credit and migration. Native covers actual Play throughout
partial training/reload plus 28,800 aim positions crossing both posts. Initial
existing340/153 suites also passed; new core fixture setup corrected its legacy
save-slot argument before final full runs.

World0.9.14/code1026914 DEBUG arm64 APK built and verified: exact compiled source,
actual three-shot/same-week national gate/headline-after-defeat, competitions,
upgrade certificate, API36/min26,118 ELF/ZIP16KB, ad-free rehearsal payload.
Portuguese newspaper screenshot is desktop Kivy with a synthetic recorded goal,
1280x591/density1.4, one paper leaf. No physical Android, production signing,
Play upload or live-server changes. Evidence /workspace/striker-runtime/0914.

Delivery: raw chunk downloads timed out twice in run41874249294. Updated the
transfer step to read the same immutable Git blobs through the authenticated
GitHub API with bounded retries, retaining all byte/hash checks; YAML/embedded
Python parsed successfully. No APK changes. Workflow41874991893 succeeded in38s.
Public APK and preview returned HTTP200, attachment headers and exact local
size/SHA256 matches. APK107335455B,
SHA2565d9cd7422ea4662203db1df1a6fba6d72287e980f3b117731bcc3d4d477a1770.
Temporary qa-upload-0.9.14 branch removed after public verification.

## 2026-11-04 — World0.9.15 post-match flow and trophy cabinet

Source95ba884d12d48b82883d82f64477da77ef01f12f adds persisted result→newspaper→
requested coach→hub flow, removes hub news/coach buttons, shortens World's editor
button and greys/guards Agent outside windows (free agents retain signing access).
Observed participation/actual winners populate saved personal cup/league/national
trophies and positive joint league Golden Boot. Optional honours state is bounded;
no unverifiable old trophy reconstruction. Player cabinet scrolls independently
with golden cup icons and fixed name/actions, tested down to320x240. Unrelated
root badge-helper/mode WIP remains unstaged and excluded from the APK source.

Core350 passed in130.323s; native158 in169.323s, total508. Targeted honours5 passed
in2.984s; post-flow/menus18 passed in32.435s. Initial native expectations for old
hub buttons, editor wording and direct return to hub were updated for the new
sequence. Native checks include restart/back/save failure, optional meeting,
agent-window controls, trophies/reload and profile bounds. Actual league/cup-final
awards, Golden Boot, deduplication and transfer persistence are covered in core.

Built World0.9.15/code1026915 DEBUG arm64 APK,107342435B,
SHA256b2d2b2524c024abf8cbca4f87040beed098d2b625f8824e4cc598ec5a9475268.
API36/min26, same upgrade certificate,118ELF/ZIP16KB alignment and ad-free payload
verified. Exact compiled honours/gameplay/UI source and unchanged assets verified;
actual compiled cup final awards/reloads a personal trophy and newspaper queue.
Desktop Kivy preview uses synthetic awards, not an owner's save or handset capture.
No physical Android, production signing, Play upload or live-server changes.
Evidence /workspace/striker-runtime/0915 and RELEASE_0.9.15*.json/md.

Delivery: public APK and Portuguese trophy preview returned HTTP200 with attachment
headers and exact local SHA256/size matches. Delivery run41878748227; public-byte
verification is recorded independently of delayed run-status reporting. Download
proof is RELEASE_0.9.15_download.json. Temporary qa-upload-0.9.15 branch removed
after the attachment checks; no APK or career changes during delivery.

## 2026-11-04 — World0.9.16 penalties, clear chances and one-screen UI

Source5847d481f6abf2c93bdda15e7ee3fe81db268bc0. More clear chances (.35elite,
.65medium, .73–.90low pressure), one-clear/three-total limits retained. Penalties
preselected at18% when chances exist, replacing a slot, announced in the notice;
11m origin and no outfield players. AI reservation includes .65 modeled penalty
conversion and single-slot overlap; team baseline/physical scoring are unchanged.

Newspaper is one leaf with measured full/concise reports and all recorded goal
minutes, no scrolling/leaf controls. Coach uses a dedicated no-scroll portrait/
feedback/completion screen, with full or concise three-paragraph text. Notice
paragraph justified. Root handles first delivered splash touch before child layout.
Name is the player button; World's three header actions align to season panel.
Hub-only viewport rebuild fixes stale initial compact layout while preserving
profile input widgets/drafts. Identity row corrected from36dp to52dp after full
geometry checks. Caption measurement prevents photo-caption/story overlap.

Core353 passed in120.699s. Native165 passed in191.306s (518 total). Final targeted
22 screen/penalty/coach/paper tests passed in49.968s; layout8 in32.117s; final
hub-resize/profile-draft test1 in1.782s; locale/font10 in2.023s. The final change
restricting structural resize rebuild to the hub was verified by the final
profile-draft smoke; other screens retain normal size bindings. Initial runs
caught stale elite/PLAYER/leaf assumptions, caption fit, header callback and the
undersized name button. All observed64 goal minutes fit on320×240 and640×360;
min6sp occurs in the tiny/high-score stress case, not a general readability claim.

Final World0.9.16/code1026916 arm64 DEBUG APK107353911B,
SHA256a7e54615f514c6393006f80d58c2ba4fbfa6e24dd05c97863294122a320a7d12.
API36/min26, same upgrade certificate,118ELF/ZIP16KB and ad-free payload verified.
Exact compiled changed modules plus all9catalogue bytes verified. Compiled smoke
also checks elite clear chances, penalty budget and concise minute conservation.
The five Portuguese previews are native desktop Kivy at1280×591/density1.4 with
synthetic stats/fixture; no handset validation. OS/native-loading first-touch
behaviour remains a device check. No production signing/Play/server changes.
Unrelated root badge-helper/mode WIP remains unstaged/excluded.

Delivery: run41924917321 completed successfully. The public APK and all5previews
returned HTTP200 with attachment headers and exact local SHA256/size matches;
proof in RELEASE_0.9.16_download.json. Temporary qa-upload-0.9.16 transfer branch
removed after these checks. No APK changes during delivery.

## 2026-11-04 — World0.9.17 responsive audit and corrections

Owner requested confirmation that all screens fit phone sizes. Ran a native
Kivy audit of27 views ×11 pixel/density/text-scale configurations ×3languages
(pt/de/ja):891 cases.0.9.16 flagged16 cases: coach fixed-height font clipping
and German Back controls above the viewport with130% text. Source
c1b341e48dc8c2474c6f2bce15344381d226f578 measures coach header/status heights and
fits non-hub headers to content. The corrected891-case report has zero findings,
stored in docs/data/responsive_0.9.17.json; reusable tool in tools/audit_responsive.py.
The diagnostic's initial parent traversal was corrected to handle Window's
self-parent cycle before collecting the complete before/after audit.

Core353 passed in138.111s; native167 in215.668s (520 tests). No gameplay or save
schema changes. Final APK107354451B,
SHA25607baf14165aca89b8d15095600c6787291881e5c5f48b1002eab5bdae9936deb.
Exact compiled changed source/all9catalogues, API36/min26, existing DEBUG
certificate, arm64,118ELF/ZIP16KB and ad-free payload verified. No physical phone,
production signing, Play upload or live-server changes. Landscape geometry audit
is not universal device/cutout/OS certification. Unrelated root WIP preserved.

Delivery run41933942390 succeeded. Public APK and891-case report returned HTTP200
with attachment headers and exact local byte/SHA256 matches. Proof recorded in
RELEASE_0.9.17_download.json; temporary qa-upload-0.9.17 branch removed after checks.

## 2026-11-05 — approval-only retro sprite lab, phase 1

Inspected the Kivy procedural actors, ball, delivery/shoot paths, keeper pose
and shared collision skeleton before editing. Recovery branch
`recovery/sprites-phase1-2026-11-05` at 51d2ef9, plus local worktree patch,
snapshots and 589-file SHA manifest under striker-runtime/sprites-phase1/recovery.
Existing uncommitted main.py/.gitignore/UI-test work and career_mode_state.py
were preserved. All 589 initially tracked files matched their initial worktree
hashes before this intentional log append; no runtime/game asset/version change.

Added original 32x40 nominal pixel bodies in fixed padded canvases: 168 indexed
transparent PNG frames, 24 sheets, 16 clips; player front/back, long-sleeve keeper,
role palette recolouring, metadata/joint/contact anchors. Independent Kivy viewer
shows both, animation/individual/sheet modes, all actions, speed, pause, stepping,
mirror, scale and kit controls. No game imports, bindings or main-game replacement.

Validation: 2 asset/clock test cases pass (168 frames, unique minimum counts,
alpha/palette/no clipping, atlas equality and clock/event contract); compileall
passes. Real Kivy2.3.1 SDL2/Mesa offscreen smoke checks every frame, filters,
controls, views and modes; 960x640/1280x800/1440x900 layouts pass. 2,000 warmed
updates created zero additional textures; 120 actual rendered frames completed.
See docs/sprite_lab/validation.json for measured desktop timings/memory.
An initial head mask, read-only texture UV assignment and palette variable
collision were corrected; small-window assertion was adjusted to its actual
130px minimum stage, keeping integer fitting. Optional clipboard provider
warnings do not prevent execution. Animated preview, contact sheets, screenshot,
inspection/recovery report and run instructions are in docs/sprite_lab/.

Stops at owner-requested visual approval boundary (task sections 9 and 11).
No integration, Android build/device test, physics regression claim or Play action.

## 2026-11-06 — sprite lab reference revision 2 (still awaiting visual approval)

Owner supplied two screenshots and requested closer proportions/style. Preserved
first proposal at recovery/sprites-before-reference-revision-2026-11-06 (4bf8932).
Redrew all168 frames/24 sheets with fuller shoulders/limbs, original9x9 heads,
short necks, separate shorts/bare thighs/socks, blue-white stripe preview kit;
keeper green shirt/dark shorts/yellow socks, wide low ready stance, outward
knees and two-handed low gather. Expanded run/dribble strides and arm alternation.
Canvas sizes, anchors, state counts and existing presentation clock retained.
Ground-level knee bend now chooses the alternate solution if a knee would sink
below the floor. Added fixed-bone-length check; it exposed a coincident-target
IK degeneracy, fixed with a stable unit direction instead of collapsing limbs.
These are sprite-lab-only changes; game physics/keeper collision skeleton intact.

3 asset/clock/articulation cases pass across all168 frames. Pixel/alpha/palette,
transparent margins, sheet equality and uniqueness pass; compileall passes.
Real Kivy SDL2/Mesa smoke again traversed all frames, modes and views at the
three previous window sizes; 2,000 warmed updates upload zero new textures.
All589 initially tracked files compared with pre-phase1 hashes: only this expected
documentation log differs. Existing untracked career module also byte-identical.
Updated animated preview, compact reference pose board, full sheets, viewer
screenshot, validation metrics and report. Android/device integration is still
explicitly deferred until owner's visual approval; no game version/APK changed.

## 2026-11-06 — owner-approved sprites integrated, World QA 0.9.26

Owner explicitly approved art revision2. Recovery branch
recovery/sprites-approved-before-integration-2026-11-06 and initial WIP patch/
main snapshot retained in striker-runtime/sprites-integration. Integrated exact
approved PNGs through retro_sprites; shared root clock/texture modules now serve
both game and viewer without Android imports from excluded tools. Production
cache bounded at24 recoloured textures, nearest filtering, existing team kits.
Only3 existing drawing methods changed plus lazy renderer accessor; all135 other
existing methods compared by AST with initial workspace, including physics,
control/update, collisions/keeper skeleton, held-ball attachment and scoring.
Root-motion compensated at diving hips; held gloves align to independent ball;
recovery only after inactive/unheld completed result. Existing build-up block
animates TACKLE, no invented tackle/fall gameplay. Wind-up before actual launch,
contact frame starts at the real immediate kick/header event.

385 core cases:382 passed/3 skipped in126.256s. All192 native Kivy cases passed
in253.538s, including2 integration cases; all3 sprite asset/clock/IK cases pass.
compileall and staging payload guard pass. Main drawing cannot mutate physics
snapshot, all keeper states and opportunities render, training has only2 actors,
warmed repeated draws upload no textures. 1280x591 aiming/build-up/shot/dive/
held-ball fall/training screenshots inspected. Same-process Mesa comparison:
35.081ms/frame sprites vs34.895 baseline; CPU draw11.446 vs11.850ms. An earlier
concurrent-load sample104.916ms/frame is retained to show variance. Desktop
measurements are not Android performance claims; training source RGBA buffers
421200B,3 warmed textures; full-process peak RSS includes app/Mesa, not sprites only.

Built actual World APK from clean committed source a68b469, excluding initial
unrelated WIP. Explicit staging manifest allowlist covered by a new regression.
Actual compiled main/renderer/clock/texture source and all168frames/24sheets
match; no developer sprite tools in APK. Existing DEBUG certificate retained,
versionCode1026926, API36/min26, arm64, ZIP16KB and all118ELF alignments pass.
Existing APK edition/ad-free metadata/saves/competitions/training/newspaper
verification passes. Physical Android install/playtest still pending. No Play
submission, new signing key, save schema, server or balancing change.

Initial setup redundantly tried to add staging's existing platform symlink;
stage already correct, build succeeded. Direct release binary upload returned401
on uploads.github.com; use the existing authenticated Actions delivery pipeline
with immutable8MiB chunks/digest checks, not a new login or credential workaround.
Old generated QA bin APKs0.9.12–0.9.17 removed to free build space; latest0.9.25
and all source/caches/careers retained. Optional host audio warnings due to no
sound device do not affect passing Kivy tests. Initial user's .gitignore/main/
UI-test work and untracked career_mode_state.py remain separate and preserved.

### Final Android texture recovery candidate — World QA 0.9.27

Final code review found custom recoloured Texture.create buffers need explicit
Kivy reload observers after Android graphics-context recreation. Added bounded
CPU payloads for the existing24-entry LRU, exact RGBA re-upload/nearest filters
and removal of observer/payload on eviction. Real Kivy regression clears GPU
pixels, invokes recovery and checks exact restored pixels and bounded eviction.
Targeted3 cases pass; final full native suite193/193 passed in269.562s. Asset/
clock/IK3 cases and staging payload1 case rerun successfully; compileall passes.
Physics/drawing selection and approved PNG art unchanged by this final fix.

Bumped the final upgrade to0.9.27/versionCode1026927, superseding the intermediate
0.9.26 QA candidate. Clean source ce315b3. Actual rebuilt APK again passes exact
compiled code/168frames/24sheets, same DEBUG certificate, API36/min26, arm64,
118ELF and ZIP16KB alignment, edition/ad-free/safety/competition/save checks.
No physical phone/resume validation claim. The recovery simulation tests only
the reload path; installation and actual background/resume remain device checks.
Final cache retains one RGBA recovery copy per live cached texture in addition
to source buffers; no per-frame upload. Performance measurements retained from
initial integration are explicitly labelled0.9.26, not rebranded as device data.

Initial final build ran out of workspace space while copying generated app
assets; freed802MiB of re-downloadable old QA APKs/app staging caches and rebuilt
successfully. Source, careers, native toolchain and pre-task0.9.25 APK retained.
Actions delivery still uses digest-checked immutable chunks; direct uploads
remain unavailable through the local upload-host credential binding.

Final delivery run42182967744 attempt3 succeeded. Actions could not create the
release with its integration token (403); the source tag and QA release were
created through the already-authorized repository connection, then the runner
uploaded the digest-checked files. No permissions expansion or new login.
Public0.9.27 APK returns HTTP200 with attachment filename,107575587B and SHA256
370d3302017cff8c7f727b2444c22bef3873d459a6ba70df44f15c115d632951,
matching the locally tested APK exactly. Proof: RELEASE_0.9.27_download.json.
Temporary qa-upload-0.9.26 and qa-upload-0.9.27 transfer refs removed after
successful delivery; source branch/tags and release attachments retained.

## 2026-11-06 — crowd revision, banner removal and mixed kit colours

Removed supporter-banner drawing and name-dependent context. Existing home/away
sectors and scorer-only celebrations remain. Club primary/secondary shirt colours,
small shade variants, skin tones and jump groups use a deterministic per-seat
32-bit avalanche hash seeded by fixture club UIDs. No shared gameplay RNG, repeated
linear stripe patterns, redraw flicker or extra palette/mesh-batch growth.
9 native stadium/club/celebration tests pass in4.829s, including no banner/text draw,
colour mixing/stability/RNG isolation. Captured 1280x591 grounds at2500/10000/
40000/70000 seats; main edits limited to banner import/call removal. Initial
unrelated worktree edits preserved. Small-ground occupancy change is awaiting
clarification of whether "only a corner" describes a problem or desired behaviour;
no stadium geometry change, version bump or new APK is claimed at this stage.

## 2026-11-06 — clarified visitor sectors, stewards and 1.80m reference, QA0.9.28

Owner clarified small VISITOR clubs only occupy the corner; larger visitors also
occupy the next behind-goal bay to its first staircase. Own visitor stadium
capacity drives this model (<=20k corner-only, >20k extended); actual HOME capacity
still drives rows/tiers. Not a real ticket-allocation claim. Cleared both flanking
stairs, two files of neon-green stewards per stair/tread, separate static mesh
that never celebrates. Training remains empty. Prior banner removal and stable
random per-seat kit colours included. Mixed colours do not consume gameplay RNG.

All actor roles now use1.80m upright world reference, calibrated to40px outfield/
39px keeper ink, relative to unchanged2.44m goal, instead of multiplying by the
old physics scales. Crouched keeper/animated poses keep natural heights. Existing
low1.31m headers meet the ball with the approved crouched contact frame, no jump
above it or delayed launch. Approved PNGs unchanged; metadata calibration only.
Main AST comparison: only3 drawing methods changed in this step; solver, hitboxes,
ball attachment, controls, scoring and saves unchanged. Shared texture recovery
from0.9.27 retained. Unit/staging checks cover new pure supporter_layout module.

Full core387 cases in131.655s (3 skipped) and native197 in255.899s exercised. One
failure each was an obsolete assertion: pinned QA0.9.25 and old high-header frame.
Updated version guard to authoritative launch JSON and header pose contract.
Affected edition6 cases then pass(.479s), sprite integration4 pass(2.298s).
All10 stadium/club/celebration cases pass(5.014s); all4 dedicated asset/clock/IK/
calibration cases pass(.104s), compileall passes. Sector geometry checks verify
small-corner/large-first-bay, no upper visitors, no fan-stair overlap, four steward
files, neon colour, fixed guards during celebrations and empty training. Height
checks cover all roles at multiple depths and immediate low-header launch.

1280x591 small/large visitor fixtures, training, low header and height ruler were
visually inspected. Capture's first diagnostic attempt used an unsupported ruler
colour argument; fixed capture only, no product change. Synthetic5000/60000 visitor
capacities share a70000-seat host in the comparison; no real club facts changed.
Calibration actor/ruler is capture-only, not added to the game.

Clean build input4a8288b. Final source9c7e397 differs only in the two excluded test
files fixing stale expectations, verified by Git diff. Same runtime and assets.
Actual APK compiled main/stadium/layout/renderer/clock/textures and approved168PNG
frames/24sheets match. Existing DEBUG certificate, versionCode1026928, API36/min26,
arm64,118ELF and ZIP16KB checks pass; edition/ad-free/safety/saves/competitions
checks pass. No physical device validation, Play submission or server change.
Initial unrelated .gitignore/main/UI-test WIP and untracked career module preserved.
Duplicate downloaded/generated0.9.27 copies and old0.9.27 app staging cache cleared
for build space; latest pre-task0.9.27 APK and recovery source retained.

Delivery42195662697 succeeded on first attempt using the existing authenticated
Actions transfer route and pre-created source tag/release. Public0.9.28 APK
returned HTTP200 with attachment filename,107578487B and exact local-tested SHA256
4b963a7d328586053349cb1e93e3e4092c8567aea431dfb3955a6afd78122ec0.
Proof in RELEASE_0.9.28_download.json. Temporary qa-upload-0.9.28 ref removed.
Additional dive/held-ball-fall captures at the new scale inspected; no pixel-art
redraw or change to ball physics. Physical Android playtest still pending.

## 2026-11-06 — individual supporters and player goal celebrations, QA0.9.29

Recovery branch before-goal-celebrations-0929 plus initial WIP patch/main snapshot
in striker-runtime/celebrations-0929. Unique deterministic per-seat jump frequency,
height, phase and reaction delay, perspective-scaled height and varied fade. Head/
body share offsets, only scorer side moves, exact base-y restoration, static
stewards. Precomputed profiles and palette14-batch meshes replace4 shared wave
groups/56 batches; no per-person draw calls or gameplay RNG. New presentation-only
celebrations module: original striker position to own home/visitor section,
3 staggered teammates embrace, decisive observed late lead runs/slides on knees
facing supporters, gets up then hugs. No future scores read. Clock stays paused;
auto result waits, normal tap skips, reset/new shot clears state. Goal counter and
all launch/ball/field/keeper collision methods untouched; no new gameplay actor
positions or colliders. Original168 PNGs byte-identical.40 new CELEBRATE/KNEE_SLIDE/
HUG frames,6 sheets, total208/30; calibrated1.80m and original team palettes retained.

390 core cases in142.771s:387 pass/3 skip. All201 native Kivy cases pass in293.083s,
including4 new integration cases.3 new pure trajectory/decisive/slide cases pass;
all4 asset/clock/IK/calibration cases pass(.099s). compileall/staging guards pass.
Tests cover unique traces, no RNG changes, head/body coherence, no opponent/guard
movement, exact reset, own supporter targeting, preserved start anchor, slide
deceleration/recovery/hug, immediate single score, clock/auto-advance/tap and
training isolation. Normal/decisive run, slide and embrace screenshots inspected.
Standalone Kivy viewer extended to11 outfield actions:208 frames/PNG/sheet modes,
960x640/1280x800/1440x900 pass,2000 warmed updates with zero texture uploads.
Initial imported test helper class duplicated discovery; moved import inside helper
before final suite. A temporary fade variable placement was corrected before tests.

Clean committed source9ebc071. Combined real Android build/verification succeeds:
compiled main/stadium/layout/celebrations/renderer/clock/textures and208frames/30
sheets exact; DEBUG upgrade key unchanged, API36/min26, versionCode1026929, arm64,
118 ELF+ZIP16KB, edition/ad-free/safety/competition/save guards pass. No physical
phone validation, new permissions, Play action, save schema or server changes.
Duplicate/old generated APK/app staging and clean old dev worktrees removed for
space; latest pre-task0.9.28 APK and source recovery commits retained. Initial
unrelated main/.gitignore/UI-test changes and untracked career module preserved.

Delivery42206733292 succeeded on its first attempt. Public0.9.29 APK returns
HTTP200/attachment filename,107602219B and SHA256
7e34595d39e223087b2e1de66bad888b15097a7540b89fda496b506d47903262,
exactly matching the tested APK. Proof: RELEASE_0.9.29_download.json. Temporary
qa-upload-0.9.29 ref removed; release, source tag and source branch retained.


## 2026-11-06 — continental competitions0.9.30

Recovery branch: recovery/before-continental-0930. Preserve unrelated root badge,
mode-state and menu-test WIP. Add Sudamericana with Libertadores thirds/playoffs,
CAF Confederation Cup, AFC Champions League Two and AFC Challenge League.
Twelve continental club fields, seven national finals overview, Copa regional
places, persistent secondary qualification snapshots and additive old-book upgrade.
National same-week matches now sort by full date before fixture ID.
Core discovery before the date correction:395 tests,3 skips, no failures.
Focused expansion/date and competition suites, native UI, multi-season replay and
actual Android build/bytecode checks are being completed. An initial Sudamericana
fixture-count expectation was corrected (141 including playoffs); lifecycle caught
the same-week national ordering bug. No physics/art/control changes.
Official portal checks do not certify current access regulations: see
WORLD_COMPETITIONS_0.9.md for modeled baselines and excluded regional feeder cups.
Physical Android playtest remains pending.


Final0.9.30 evidence: all7 expansion/date and15 competition regression cases
passed;202 native Kivy cases passed. Three-year controlled lifecycle:218 matches,
13 reloads,3 archived seasons, nondecreasing dates, no repeated fixtures. The
prior0.9.29 baseline lifecycle also passed; the new Copa field exposed the latent
same-week lexical ordering error, now covered by a focused date regression.
Build succeeded; initial post-build ELF check ran out of container temporary
disk. Removed3421MiB of obsolete generated staging app/bin copies, retaining
sources, native toolchain and current APKs. Rechecking the identical APK passed:
existing debug signature, ZIP16KB,118 ELF alignments,208 original sprite frames/
30 sheets and exact compiled rendering source, edition/safety/no-ad checks,
actual secondary competition results/transfers/snapshot reload and legacy career
flows. APK107606951bytes; SHA256
c8f0e438d85b9a455d3c42b00b9d6461763fb4a4dec3a26391ea69f4a0e5c511.
Code source55d506fa39c9f9a68fbf8e09d0f9974aec69f60b; World0.9.30/code1026930.
Physical Android playtest pending; no production1.0/Play/server changes.

Public delivery verified: GitHub Actions run42214598925 succeeded; qa-0.9.30
attachment returned HTTP200 with Content-Disposition attachment, exact107606951
bytes and matching tested SHA256. Temporary QA transfer branch removed after
verification. Download evidence: docs/RELEASE_0.9.30_download.json.


## 2026-11-06 — involved standings and contextual help0.9.31

Recovery: recovery/before-standings-help-0931. Preserve unrelated root badge/
mode-state/menu-test WIP with partial patches. World Standings selects all current
club competitions, observed current-season former club/league campaigns and
eligible/called-up/observed national campaigns. Eliminated entries remain visible.
Groups have a selector; knockout phases show fixtures/results/penalties rather
than invented points. Membership reading consumes no RNG and does not advance cups.
Help now opens as a context-specific modal from normal game/menu screens (splash
art remains unchanged). No normal global manual navigation. Training alone owns
focus/XP guidance; confidence owns role/trust explanations; profile owns objectives.
Help preserves drafts/post-match gates and freezes elapsed time, ball, shot timer,
match progression and shooting/key shortcuts; Close/Back resumes the same screen.
New gameplay help button also works above the opportunity notice, with narrow
scoreboard clearance. Add13 translated guidance paragraphs in all9 languages.
Core discovery:400 tests,3 skips, no failures.297 native responsive cases
(9 changed menu views ×11 profiles ×en/de/ja) have zero findings. First full native
suite:208 cases,3 stale expectations (group now opens on actor's group, notice
adds Help, language returns to underlying hub); updated expectations. All7 focused
new native cases pass, including actual touch through a match notice. Final native
rerun and Android build/bytecode verification in progress. Screenshots visually
inspected after EventLoop.idle (initial FBO captures missed pending font uploads).
Physical Android playtest pending. No solver, scoring, save format or server change.


Final0.9.31: all209 native Kivy cases pass in263.217s. The second run's sole
failure was a remaining obsolete help_back step after modal Language navigation;
the test now follows the actual flow (modal dismisses before language screen,
Back returns to hub); all8 language cases pass and the full209 rerun is green.
All400 core cases (3 skips),7 focused native cases and297 responsive cases remain
passed. Android APK compilation and checks pass: debug signature, ZIP16KB,
118 ELF files,208 sprites/30 sheets, exact compiled main/menu/coach/newspaper/
contextual_help/standings_ui/competition_views sources, edition/ad-free/safety,
actual APK read-only involved membership and prior competition/career flows.
World0.9.31/code1026931; source9453841c1531f638bbe40f0b1a1bc8131366e236.
APK107632111 bytes, SHA256
4ba1cf550c318ef9aa85f6d915806e484cbc665d80d22f358e825b94db106079.
Physical Android playtest pending; no physics/save/server/production changes.

Public0.9.31 delivery: Actions run42220873368 succeeded. Download verified HTTP200,
attachment filename, exact107632111bytes and matching tested SHA256. Evidence:
docs/RELEASE_0.9.31_download.json. Temporary verified transfer branch removed.


## 2026-11-06 — weekly locker-room team talks0.9.32

Recovery: recovery/before-team-talk-0932. Remove gameplay Help and restore the
scoreboard's original available width. Other contextual help remains. Coach talk
is compulsory once per club/season/week, including the first week; transfers and
season changes bind a new talk. Read collective feedback from actual club results
(including shootouts), individual recent form and coach personality. Exactly two
deterministic focus offers, no gameplay RNG consumed; UI requires a choice before
completion. Save weekly choice, acknowledgement and post-match queue atomically,
rollback all on failure; no attribute rewards. Same-week extra fixtures retain the
focus and defer feedback to the next talk. Training has stats/progress only and no
focus chooser/action. Old partial drills keep their original focus/XP; the chosen
weekly focus applies to following sessions. A new week clears a stale development
session so its old focus/reward flag cannot override the new choice.
New original locker-room scene (image generation), retain10 saved coach faces as
cropped avatars. One screen, no scroll: collective + named individual feedback,
room photo, two choices and fixed finish/help actions. Prefer concise complete
sentences over tiny full text.21 new strings ×9 languages; focus guidance moves
to coach Help. Initial398 core cases pass/3skips,11 coach regressions and5 native
coach tests pass;231 responsive cases +33 final coach cases have zero findings.
Legacy conditional-meeting/training-focus UI tests adapted to the new weekly
contract; unrelated fixtures explicitly acknowledge their setup week's talk.
Final full suites and actual Android build verification in progress. Preserve
root badge/mode-state/menu-test WIP with partial staged patches. Physical Android
playtest pending; no shot solver/collision/save-envelope/server/Play changes.


Final0.9.32:399 core cases/3skips pass in168.287s; all207 native cases pass in
303.254s. All11 coach core and5 coach UI cases pass.231 responsive cases and33
final coach checks have zero findings. Original full-suite failures reflected
obsolete conditional-meeting/focus-picker assumptions; final unrelated fixtures
acknowledge their setup week, club-change fixture acknowledges the new coach,
finishing-only geometry fixture explicitly uses placed finishing.
Actual APK build/checks pass: debug signature, ZIP16KB,118 ELF alignments,
208 approved sprite frames/30 sheets, exact compiled main/coach/progression/UI/
help modules and locker-room PNG; actual saved weekly choices, no extra same-week
talk, next-week gate, focused XP, competitions/standings/legacy career flows.
Source8448aebd78dd97700124119eda026b6ed375c898. World0.9.32/code1026932.
APK109566131bytes; SHA2568c75a0dcfe53d4796a23835caa7bf87f963e026423374ef8f52bec6a6fdb9f6f.
Physical Android playtest pending; no solver/collider/server/production change.

Public0.9.32 delivery verified: Actions run42301240855 succeeded; public attachment
HTTP200, expected filename,109566131bytes and exact tested SHA256. Evidence:
docs/RELEASE_0.9.32_download.json. Temporary QA transfer branch removed.


## 2026-11-09 — Play policy audit of World1.0 candidate

Read official User Data/Families/UGC/IP policies (HTTP200); privacy endpoint403
from cloud, not proof of universal failure. Audited matching0.9.39 source;13
publication safety tests passed in5.910s. Initial policy retrieval script failed
because system Python has no requests; retried successfully with stdlib urllib.
No runtime changes. See docs/play/POLICY_AUDIT_1.0_2026-11-09.md for unresolved
policy accuracy, live access/moderation, minors/data treatment and rights evidence.
No compliance declaration or Console submission performed.


## 2026-11-09 — optional usage and World policy remediation0.9.40

Owner clarified clubs are fictional and confirmed live privacy still says test
version on the phone. Added versioned, default-off optional usage, separate adult
PIN opt-in, no-PIN stop/erase, translated safety reminder and matching English
Season/Career/local-purchases/feedback policy. Combined bastion installer has
source checks, rollback and local policy/v3/v4 verification; not executed remotely.
Preserved pre-existing badge-deletion/test-helper WIP and career_mode_state.py.

First full runs:433core with1stale policy-text assertion,235native with1stale
Windows-label assertion. Updated those assertions for optional statistics. Final
clean indexed-source core:436tests passed(3existing skips). Focused public policy
15passed; installer3passed including failed-verification rollback/symlink rejection;
statistics20passed. Final clean native run and APK delivery evidence follow in
RELEASE_0.9.40_artifacts.json when completed. Responsive165cases/zero findings.

Initial plain Buildozer call missed the shared native distribution; retry used
existing tools/build_android.py correctly. Initial APK bytecode inspection used
container Python instead of the matching hostpython and exited139; retry uses
the packaged Python compiler version. This was an inspection-process failure,
not an Android app run. Signature, package/code/API,16KB ZIP and118ELF checks passed.
No production signing key, Console declaration, public server update or submission.

Final0.9.40 indexed-source evidence:436core/3skips and235native Kivy passed;
165responsive cases/zero findings. APK bytecode verified using matching hostpython:
actual default-off factory, versioned opt-in, stop/erase and safety text all passed.
Public standalone installer HTTP200/download hash verified. Owner must execute on
bastion; latest live phone report is still the OLD draft/test policy.


## 2026-11-09 — independent public legal pages0.9.41

Prepared5public-only static files and separate minimal Pages workflow. Existing
service untouched. Initial Pages activation API403; later reads confirmed enabled
site, but legacy dynamic build and retry failed without jobs/logs. Custom workflow
uses existing Pages environment/gh-pages branch policy and normal minimal scoped
Pages permissions, no protection bypass. Public availability verification pending.

Site generator2tests, public policy15tests, release staging14tests, editions6tests
and native policy-link1test passed. Gameplay unchanged from0.9.40; no redundant
full gameplay run. Changed release_settings/examples/compiled metadata check to
canonical GitHub Pages privacy URL. Unrelated WIP remains excluded.

Public policy host closure: custom workflow42673061046 succeeded; Pages built.
All3canonical anonymous HTTPS URLs returned200, final English HTML and expected
identity. Direct Chromium got the managed proxy CA error (no TLS checks disabled);
render/navigation checked using exact TLS-verified live HTML on localhost. First
local browser selector matched both header/footer navigation links; fixed the probe
to choose the first link. See live/browser evidence under docs/data/policy_0.9.41.
Bastion and old policy/service remain untouched; no operator-review flags asserted.

Final0.9.41 APK: package com.clemir.scorerworld/code1026941/API36/min26/arm64,
existing DEBUG signature, ZIP16KB and118ELFs verified. Matching hostpython bytecode
inspection confirms new public policy URL and edition/channel metadata. No physics
or save-format changes; game regression baseline remains0.9.40. Physical Android
and Play production signing/review remain pending.

0.9.41 delivery workflow42674141359 passed. Anonymous APK HTTP200,118312875bytes
and SHA2561bfe5414c26e811a2a277f44d89ba7a3fa9932615702db9a0854dc616f73c108
verified. Transfer commit creation initially preceded pushing its source parent;
pushed source and reconstructed the tree from existing uploaded blob hashes,
without re-uploading/rebuilding APK. Site recheck: all3final HTTPS pages200;
Pages reports built/HTTPS enforced. No bastion access or Play submission performed.


## 2026-11-09 — real online acceptance and actual upgrade rehearsal

Read-only real HTTPS using app UA: health200/v3schema3; v4JSON404; unauthorized
private queue404. Own disposable zero-goal pending canary: terms400, submit204,
not publicly visible, report204/invalid-reason400, withdrawal204. First repeat
withdrawal got503; cleanup owner/reporter204. Complete paced second run passed
including idempotency and report-target absence after withdrawal; both credentials
cleaned,0600 recovery files removed. No user records or usage counters changed,
no live admin approvals or queue access. Original503 evidence preserved.

New isolated rehearsal exports actual qa-0.9.33 v3 modules into temporary source/DB,
seeds unrelated approved record and aggregate42, applies the actual standalone
0.9.40 installer and restarts with new sources.20checks passed: migration, both
pending/approved categories, invalid terms/private admin, reports, local block,
bans, withdrawals and preservation. First harness run lacked root import path for
client-block module; fixed the probe path, reran successfully. No runtime game
code changed. Existing publication safety13tests and installer3tests passed.

Service update not applied remotely: no SSH/admin credential and owner lacks
bastion access. Live v4/human moderation gate stays open. Prepared honest physical
Android acceptance checklist; version/install confirmation requested asynchronously.


## 2026-11-09 — visible build version0.9.42

Owner reports all3requested physical0.9.41 smoke checks work (startup/policy,
training/single-tap/unlock, match/save/reload), device/Android details unspecified.
Added small version footer to entry and version in Help>Settings; reserve footer
space, retain48dp controls. Main hub, splash/wordmark and gameplay unchanged.
Staging emits VERSION_NAME from actual package versionName; production fixture
asserts1.0, rehearsal metadata matches spec. No hardcoded UI version string.

Focused editions6/release14/publication13tests passed; native start dialog4passed;
66responsive entry/settings cases, zero findings. Native screenshots visually
checked. Headless clipboard reports absent xclip/xsel providers, unused by these
screens; captures complete. Initial command addressed a clean checkout before
it existed; reran from source, then tested/staged the clean index successfully.
APK build/signature/metadata verification and delivery evidence follow separately.
No server update, signing key creation, production assertion or Play submission.

Final0.9.42 package/signature/API/code and ZIP16KB passed. Initial container ELF
probe could not create a temporary directory due to writable-layer disk space;
archived only generated older staging/index snapshots to /tmp, preserving them,
then118ELF and matching-hostpython metadata checks passed. Actual APK prints
Displayed version:0.9.42, matching Android versionName/code1026942.
No APK rebuild or gameplay change was needed after verification.

0.9.42 QA delivery workflow42680414361 succeeded. Anonymous attachment download
HTTP200/118313343bytes/SHA25675193fca9d47a72177fefb32b736c7067be0ef7dbcfc3fbb2007ca3749cf64a6
verified against the tested APK. Temporary transfer branch removed after proof.


## Backend repair1 — missing privacy dependencies on bastion

Owner journal shows ImportError server.privacy_cases, then systemd StartLimitHit,
after old standalone installer rollback. The old payload omitted privacy_cases.py
and its root privacy_requests.py dependency; prior20-check rehearsal started from
a complete v3 checkout and did not exercise the damaged deployment. Acknowledged
installer packaging defect. Old immutable0.9.40 download is retained as historical
evidence, not the repair recommendation.

Repair payload includes explicit server package and complete startup modules,
legacy privacy reference dependency, aggregate validator, record helpers and admin
HTML. Preflight isolated Python import/Collector initialization/public-policy render
uses ONLY bundled files and a disposable DB before service stop. Start clears
systemd failed/start-limit state. Rollback error preserves original failure too.
Initial local repair preflight caught a missing sys import in the new helper; fixed
before publishing. --check now passes,22real isolated migration/moderation/deletion
checks pass with privacy modules deliberately removed/reproduced failure,6installer
tests pass including missing-import preflight and reset-failed ordering. Python3.12
locally; owner host journal shows3.13, not available for local execution. No remote
service modification performed here, no secret read/printed, no APK/game changes.


##2026-11-10 — owner backend repair succeeds, public v4 accepted

Owner applied pinned Repair1: checksum/preflight/installation pass, systemd active,
public schema4. Independent HTTPS health200, v3schema3 and v4schema4 confirmed.
Own disposable pending Career fixture passed full safe lifecycle (terms, private
unapproved submission, report, invalid reason, withdrawal, idempotency, removed
report target), both owner/reporter cleanup204, no retained recovery credentials.
No real user records, usage counters or live admin approval changed. First probe
ran cleanup then lacked old /tmp report directory; repeated with persistent path
and recorded passing evidence. No game/APK modifications. Deployment blocker closed;
operator availability, production signing/Console/Play checks not inferred.


## Upload-key preparation on owner bastion

Owner authorized upload-key/AAB preparation. New-app status was already confirmed;
no production key in cloud. Hardened standalone key helper: hidden double password
prompt,12+ASCII rule for PKCS12 compatibility, no password argv/history,4096RSA
SHA256/10000days, private directory/0600 key, exclusive no-overwrite commit, public
PEM/SHA256 export. Does not change permissions of existing non-private directories;
rejects them rather than altering an unrelated directory.

3tests passed: no overwrite of existing key/certificate, invalid secret rejected
without key creation, real disposable JDK PKCS12 generation/export/fingerprint/
permissions and no secret in argv. All test identities removed with temp directory.
No production key generated, no AAB signed/submitted, no publication flags faked.
Asked who operates moderation before declaring that production readiness field.


## World1.0 unsigned release candidate

Owner created private upload key on bastion and sent PUBLIC SHA256 screenshot;
no private key/password received. Pin stored as owner-reported, not Console-enrolled.
Owner explicitly confirmed Gonçalo Pereira operates moderation. Recorded engineering
data/Families/provider review with published policy and live backend evidence; no
external legal counsel or Google approval claim. Production gate accepts the actual
review config, example placeholders unchanged. Clean indexed source excludes WIP.

Built release AAB world1.0/code1030000; original has no signature entries. First
static audit failed an obsolete fixed9896club count. Actual source/stage/bundle
all have10598entries and identical SHA2569a308fcaaf885f832c4dd817d9a26afffe9308dbfa33d3915f41ae5c13c6e1f7.
Replaced fixed count with exact reviewed-source hash+schema validation,2regression
tests pass. Re-ran full unsigned inspection: bundletool, production manifest,
forbidden SDK/permissions/private-data checks,118ELF16KB,16KB ZIP request, matching
hostpython edition/channel/version1.0 and derived DEBUG inspection APK pass.
No AAB production signature or Play upload performed.

New owner-side signing helper: pin unsigned SHA and expected public certificate,
hidden existing password, JDK env selectors, no overwrite, signed-JAR verification
and actual certificate comparison, exclusive final commit.2tests passed with full
JDK and disposable signing-only fixture (not runnable Android), no secret argv,
wrong input/cert/already-signed/output refusal. Tests use no real production key.
Archived only known generated QA artifacts/source snapshots to /tmp for space;
originals preserved, no user work or signing material moved.

Unsigned1.0 delivery workflow42882040459 succeeded; anonymous AAB116946453bytes
SHA2562d44aa9197c3d97f37cad8569ed70ce1c5333882852276e7d44ef34283cc9730 and
standalone signing helper5492d1fa8de0e3072960a0c34eaf05548cdaaa51c84f154d8ef579c885fa6761
HTTP200 verified. Signature still pending owner-side hidden password input. No
production key/certificate enrollment or Play upload was performed by the cloud.

##2026-11-10 — owner-reported real names / creation captions,1030001

Acknowledged shipping-identity defect in1030000. Source equality gate was
insufficient: World overlay/profile/status reference labels shipped. Build now
creates fictional-only UID-identical presentation, strips real profile metadata,
retains capacity/palettes/patterns/rating gameplay. Actual1030000 AAB regression
fails new gate.25 focused release/catalogue/kit checks pass;5 clean-source native
creation tests pass,90 full-caption measurements at5 sizes/densities/3 languages.
Staged runtime8888active names canonical, saves and explicit aliases preserved.
Rendered English form screenshot visually checked. Rebuild first completed before
UI steering; final rebuild first attempt failed ENOSPC in disposable Docker layer.
Preserved old generated1.0 staging/source under/tmp/scorer-signing-archives and
restarted final build. No real keys in workspace; Play suspension owner-operated.
Final1030001 rebuilt successfully after preserving old generated staging. Actual
AAB static gate passes fictional data, package/code1030001, nondebug, noad/billing,
118ELFs16KB, bundletool/16KBZIP config/derivedAPK checks and compiled metadata1.0.
Actual archive contains10598canonical fictional identities,352sanitized profiles
and new CreationTile bytecode. Direct hostpython invocation outside container
failed to locate stdlib (not used for results); container-native metadata audit
passed.3standalone download/signing coordinator safety tests pass. Final signing
remains on owner bastion; new Play installation pending.
Delivery prepared with original upload cert pinned and fresh output path. Existing
registered apk-delivery.yml is used on review branch because GitHub does not
register workflow_dispatch for a new off-default workflow (404); no default-branch
settings changed. Historical editor-name attachment job retained. Source7f70966.
Delivery42913734812 succeeded. Anonymous full downloads independently verified:
AAB116837994bytes SHA256e0dda65b3f97ca2ff684595be8b31f7870cf070d3bb20449290823b12774eabc;
coordinator2336bytes SHA256f378c524f2376eccd11b770b289373874fc2aee6143b7a5974f1d113cbb3e509;
unchanged signing helper4668bytes SHA2565492d1fa8de0e3072960a0c34eaf05548cdaaa51c84f154d8ef579c885fa6761.
AllHTTPS200. Original flawed GitHub candidate marked SUPERSEDED with corrected link.
Owner still must sign and replace internal release; no Play changes claimed.

##2026-11-10 — local fictional names and centred season heading,1030002

1030001was culturally wrong for Portugal: English canonical fallback. Replaced
with immutable10736UID local-name registry, explicit212country naming conventions,
normalized known-reference/uniqueness checks. Full real-format runtime revealed
138active UID gaps beyond old10598catalogue; first partial build stopped, coverage
expanded to actual current+legacy. All8888current display names exactregistry,
UIDs/save/custom aliases retained.378profile capacity/pattern+499rating rows covered.
29focused tests pass;6clean-sourceKivy tests pass including90caption measurements
and YOUR SEASON centre at2sizes. Old generated partial stages preserved under/tmp.
Build1030002final running; signing/Play acceptance still owner-operated.
Final native hub screenshot showed a long Portuguese name being ellipsized by the
existing fixture label. Allowed full two-line wrapping in that fixture panel;
added a real UI regression alongside centred YOUR SEASON check. No buttons moved.
Final packaging rerun includes this small readability fix; previous partial builds
were not delivered. No keys or credentials in source.
Final1030002AAB compiled and inspected: bundletool, nondebugmanifest, target36/min26,
118ELFs16KB/ZIP16KB, derivedinspectionAPK, compiledWorld/production/version1.0 pass.
Actual archive matches reviewed10736local labels+registry,378sanitized profiles,
499strengthrows.32focused checks (29core+3coordinator) and6native tests pass.
Input117177209bytes SHA2562e30020eef7ddf264839221bc6ec74364908fc08490a40ed3c687aa814d8cd53.
Original AAB unsigned; owner bastion signing/Play install remain pending.
Delivery42923329696success. Independent full anonymousHTTPS200 downloads verified:
AAB117177209bytes SHA2562e30020eef7ddf264839221bc6ec74364908fc08490a40ed3c687aa814d8cd53;
coordinator2344bytes SHA25642f755e3c785cc2bd4b06d23c9449552c162bfc9b4a9f5c9e71e48ef92503f6e;
signer4668bytes SHA2565492d1fa8de0e3072960a0c34eaf05548cdaaa51c84f154d8ef579c885fa6761.
1030001GitHub candidate marked superseded. Older generated AABs preserved in/tmp
archive for disk headroom. User still signs only on bastion and uploads new
internal Play release; no remote Play changes or physical acceptance inferred.

##2026-11-11 — selected city/colour style,1030003

Owner explicitly selected city+colour aliases. Current378real club/name/city/kit
identity checked against UID-bound home palettes;133old-reference conflicts must
not set modern names. Chosen examples match, incl VitóriaBA SalvadorVermelho-Preto.
All10736entries covered; 40extra representative palettes,10318geographic/existing
palette rows remain explicitly NOT fully real-kit verified. RGB/patterns unchanged.
33focused tests pass.6prior native tests pass; new four-club palette/label native
case passes after fixture setup acknowledges coach (first setup redirected to
CoachScreen). Citycolournative menu capture uses actual staged data. Real AAB
built; static inspection/download and owner-only signing pending below.
1030003final inspection passes bundletool/nondebug/target36/min26,118ELFs16KB,
16KBZIP, derivedinspectionAPK and compiledWorld/production/version1.0. ActualAAB
matches all4reviewed city-colour datasets.33focused+3coordinator safety+7native UI
checks passed (sixexisting+newfourclub case). Screenshot actual staged hub shows
PortoAzul/LisboaVermelho and correct red clubbutton/centred YOURSEASON.
AAB117212326bytesSHA25614a143d6f879d2bc11def5cf35d32fc5e8fe11fefb2112baf7690d26edf076bb.
Owner-only signing/Play install remain pending. Transfercommitf38cd05bf564c2d67043c301a8d05a760551f01f.
Delivery43002791031succeeded. Full anonymousHTTPS200 downloads verified:
117212326byteAAB SHA25614a143d6f879d2bc11def5cf35d32fc5e8fe11fefb2112baf7690d26edf076bb;
2352bytecoordinator SHA2569960b8b6349e0b9ea68f633db5e852252f2bc85fa1caa536b5acc74e03a979a1;
4668bytesigner SHA2565492d1fa8de0e3072960a0c34eaf05548cdaaa51c84f154d8ef579c885fa6761.
1030002candidate marked superseded by owner-selected city/colour1030003. Owner
signs only on bastion; existing certificate pinned; no key generation or Play
upload by cloud. Actual phone/Play update still pending. Reference colour coverage
limits (378current+40extra vs10318existing-game palettes) explicitly retained.

##2026-11-11 — owner-authorized bastion→Play internal automation

Prepared standalone stdlib/OpenSSL/JDK publisher. FixedScorerpackage/internaltrack,
1030003payload digest+owner cert pins, Google version/SHA validation, private
credential install/nooverwrite,0700SFTPsetupdir/0600key, private snapshot of verified
AAB, lock, resumable8MiB upload with offset recovery, edit validate/commit. Existing
P12/password never leave bastion; no service key received by this cloud.
Google live discovery contract confirms resumable path and2026commit review flags;
ERROR_IF_IN_REVIEW+changesNotSentForReview=true never silently removed. Noproduction,
listing,tester,financial or user-management writes. Uncertain commits not blindly
retried.23scenarios locally covered: host22pass/1JDKskip; fullJDKcontainer22pass/1
approved-AAB-pathskip. Together cover RSAJWT signature, actual JDK fixture signing,
approved real AABpayloadpin, transaction/recovery/security/idempotency boundaries.
Owner screenshot confirms ScorerPublishing project/APIEnabled. Service account,
Play per-app read/testing grant, privateJSONinstall, live --check/first --publish
remain pending. Game/APK/AAB unchanged1030003; preserve unrelated WIP.
Public automation delivery43006706958succeeded with CI fixtures (23cases, portable
source skips approved-AAB localpath only). Independent anonymous downloads of
public script/docs/SHA file match localbytes (HTTPS200). Publisherfile SHA256
1c20d328ceaaeb97f063e926d3203fa4e125eaf3f85d64d6ce6d388b373b455a.
Owner screenshot confirms serviceaccount scorer-play-uploader@scorer-publishing.iam.gserviceaccount.com
created/enabled. Guided owner to Play Users/permissions, Scorer-only read/testing
release permissions, no Admin/production. Grant, privateJSON/SFTP install, live
--check and first realpublish still pending. No API credentials received here.

##2026-11-11 — owner live upload success, Google automatic-review commit400

Owner --check authenticated and read internal1030002; serviceJSONinstalled privately
on bastion. First --publish localcert/payload checks, full resumable upload and
Google validation passed. Finalcommit rejected400 with explicit instruction NOT
to set changesNotSentForReview because this app sends review changes automatically.
Prepared uploader1.1: omit that unsupported optional flag; retain ERROR_IF_IN_REVIEW
(no review cancellation), internal-only track+same limited accountpermissions and
all existing code/hash/signature guards. No fallback retries after review errors.
Existing signedAABandGoogle/P12keys reused.24local tests:23pass,1unchanged JDKcrypto
fixture skipped onhost (previous fullJDKfixture pass); new regression simulates
exact automatic-review400 and reuses uploaded matching bundle without upload.
Commit/Play delivery still pending owner rerun. No credential received in cloud.
Uploader1.1delivery43022476258passed CI24cases (portable source lacks approved-AAB
localpath only). Independent anonymousHTTPS200 script/docs/SHA downloads match
source; publisherSHA2564547252192d2ee1fe70c661fe8699882541655ba90c4cae92e9becf8e60f3476.
Public update preserves existing private JSON/P12/signedAAB; owner rerun required.
No successful commit or Play install inferred from this fix/delivery.

## 2026-11-13 — simulation-only deeper cloth deformation and compliant ties

Owner correction: keep all turf points fixed, increase interior net deformation,
and let rear suspension cords yield only slightly at the net while their pole
ends remain fixed. Added a lab-only cloth subclass with extra suspended sag,
softer link transmission/larger stretch reserve and three elastic rear ties
limited to 12 cm displacement. Rendered cords follow the actual cloth support
particles; fixed external ends are marked. Square/hexagonal matrices preserve
three speeds and three impact heights at 50% playback. No production integration,
Android compilation, version increment, signing or upload.

Validation: `python -m unittest tests.test_rolling_net_experiment -q` — four tests
passed. Covers all nine speed/height trajectories, exact turf pins, immutable
external tie endpoints, bounded net-end displacement and nonzero elastic yield.
`python -m py_compile tools/net_lab/rolling_contact.py tools/net_lab/rolling_demo.py`
and `git diff --check` passed.

## 2026-11-13 — broad draped pocket based on owner reference stills

Simulation-only reference profile: extra hanging fabric, distributed normalized
contact load across neighboring welded side/back vertices, stronger tensile
propagation and less local link extension. Preserved hard turf/front pins and
existing 12 cm bounded rear ties with fixed pole endpoints. Added a same-shot
before/after capture and square/hexagonal 3x3 height/speed captures at 50% speed.
No production net code, version, Android compilation, signing or upload changes.

Validation: six rolling-experiment tests passed (48.529 s), including all nine
reference trajectories, exact hard pins/cord endpoints, bounded tie yield and a
broad-patch regression (58 vs 23 vertices displaced at least 15 cm in the fast
mid-net case). A seventh focused test passed for normalized contact load shared
across both sides of the welded seam. Syntax compilation and diff whitespace
checks passed. Before/after frame inspection confirms a broad rounded pocket in
place of the previous narrow spike; stills guide shape rather than calibrated
physical timing.

## 2026-11-13 — isolated hard side-first hexagonal-net replay

Added lab-only `--side-shot` capture: 68 km/h at mid height, first left-sheet
contact .125 s, then back .192 s, descending into the pocket and rolling to rest
inside. Focused trajectory/anchor regression passed (1.753 s). Existing cloth,
material and renderer physics retained. No Android build or production change.

## 2026-11-13 — World 1.0 / 1030018 in-game draped nets

Owner approved the side-first hexagonal shot and requested a fresh Android test
build. Promoted the identical lab solver into net_drape.py; the lab imports that
shared runtime implementation. The game creates a separate presentation sphere
only after its original legal-goal/net collision. Broad side/back folds, fixed
turf points and compliant rear ties apply to both stadium mesh patterns; cord
rendering follows its actual net attachment. Original ball, collision, goals,
training progression and saves are never written by this adapter. Reset clears
the display trajectory. Veil structure uses its own upper-support depth.

Eight pure rolling tests passed (36.609 s); 24 native net/training/seat tests
passed (31.816 s), including paired authoritative-ball equivalence across styles
and the new in-game side-first regression. Syntax/diff checks passed. First
build failed on Docker disk pressure; removed only reproducible temporary frame
captures and old downloaded build copies, preserving committed previews/videos,
research, saves and signing materials. Retry produced unsigned 1030018 AAB,
118192605 bytes, SHA256 05e9635ec0e452e346ef6c31ae7f385e578316eb80e7135cdc8388a5e7852b70.
Full Android static audit and owner Play/phone acceptance recorded separately.
Primary workspace main.py/.gitignore/menu-test/mode-state WIP excluded by using
an isolated clean worktree and production staging.

1030018 full audit passed: bundletool validation, com.clemir.scorerworld/version
1030018, INTERNET/ACCESS_NETWORK_STATE only, 118 aligned ELF libraries and 16 KB
ZIP request, unsigned owner-signing candidate, and exact compiled runtime source
(including net_drape/net_presentation/goal_nets). All original 248 sprite frames /
35 sheets matched staged bytes. Publisher fixtures: 25 cases, 24 passed and the
existing host-JDK fixture skipped. No Google Play API called from cloud. Existing
safety settings and update-gate behaviour retained. Bastion handoff pins the new
bundle/payload and original upload certificate; public minimum must stay zero
until intended testers actually receive this build through Play.

Delivery complete: GitHub uploader workflow43441065999 and AAB workflow43441193408
both succeeded on codex/net18-in-game. Anonymous HTTPS downloads of the full
118192605-byte AAB, pinned bootstrap, signing helper, metadata, owner guide and
uploader matched local SHA256 bytes. Temporary aab-upload-1.0-1030018 transfer
branch removed after release verification. Public uploader SHA256:
333f3a7a4c99978aa27a32c14e8be0af1818f6b9e894c9a98e12a60f70d9831a.
Cloud did not invoke Google Play, sign with an owner key or activate a mandatory
minimum; those exact existing-bastion commands are in the delivered guide.

## 2026-11-13 — correct unloaded side-net shape after owner feedback

1030018's rest shape stacked three outward offsets: side midpoint ~60.75 cm
outside its undeformed plane, giving an unloaded goal a permanent impact pocket.
Reference rest geometry now uses one downward-only world-space field, with the
same front/turf pins and upper cord supports. X/Y coordinates stay on the unloaded
panels; gravity droops the top edges between supports without preforming a ball
pocket. Shared roof/side seams use the same field. Broad impact coupling retained.

Preview before/after uses the previous rest field as an explicit lab fixture,
90 frames without a ball/contact and then the same strong side-first shot at
50% playback. Eight existing pure rolling tests passed (33.766 s); new rest-shape
regression passes for box/veil and full/mobile grids. Initial native recovery
check exposed microscopic ground/net overlaps keeping the veil awake after a
stopped ball; the presentation adapter now lets the cloth recover separately
once the display sphere has genuinely settled at turf level. All seven native
net tests passed (23.294 s), including physical-state equivalence and reset.
Syntax/whitespace checks pass. No Android build, version increment, signing,
public release or update-policy change for this visual correction yet. Existing
main/menu/badge/mode-state WIP preserved unstaged.

## 2026-11-13 — World 1.0 / 1030019 build requested

Owner requested a new Android version after approving the unloaded-shape
correction. Fresh isolated source/worktree excludes unrelated main/menu/mode WIP.
Production staging bumps only versionCode to 1030019, retaining package, original
signing handoff, saves, fixed anchors and post-goal-only presentation. Runtime
changes are the downward-only unloaded rest field and settled-ball cloth sleep
fix committed in fb78e1c. Build/audit/test/delivery results follow below.

1030019 results: 9 pure rolling/rest-shape tests passed (29.626 s), 24 native
net/training/seat tests passed (41.168 s), 25 publisher fixture cases with 24 pass /
one existing host-JDK skip. Actual unsigned AAB: 118193176 bytes, SHA256
a4b2bd5b884aca7527996fba0cbba9eb1ee97de2696654b2cb88fb6524f8bc27.
Bundletool/static audit passed for com.clemir.scorerworld/version1030019, only
INTERNET/ACCESS_NETWORK_STATE, 16 KB ZIP request and 118 aligned ELF libraries.
Owner signing/Play/phone acceptance remain pending. No owner credentials entered
cloud; public uploader pins original certificate and this exact payload. Code
preserves the existing update gate; minimum stays zero until Play availability.

1030019 exact-source/sprite audit completed successfully: actual packaged
bytecode matches staged source including both corrected net modules; 248 sprite
frames/35 sheets unchanged. No simulator UI, reference captures, signing keys or
service-account credentials in the Android package. Physical phone test remains
the owner's next step after internal Play delivery.

1030019 delivery complete: uploader workflow43445374100 and AAB workflow43445536170
succeeded. Anonymous HTTPS downloads of full118193176-byte AAB, pinned bootstrap,
signing helper, metadata, handoff and uploader match local SHA256 bytes. Uploader
SHA256 ec1404c13051b6faa41f7e03d81663a7a09651bc1163d8a40c29bf6ab4df5649.
Temporary aab-upload-1.0-1030019 branch removed after verification. No live Play
API, owner key/signature or version-policy change performed by cloud. Owner's
existing-bastion upload and after-availability mandatory activation commands are
included in the public handoff. Primary unrelated WIP remains preserved.
