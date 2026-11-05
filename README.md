## Scorer World 0.9.21 — compact player and training screens

[Download World 0.9.21 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.21/Scorer-World-0.9.21.apk)

Player objectives share one panel. Training and coach confidence contain values
and controls; all explanations are in justified Help. Skill selection is confined
to Training. Tap the green hub trust value (or compact Coach Trust action) for
confidence stats. Existing careers, skill progress and trophy data are retained.

30 focused core checks,178 native cases with corrected navigation/count reruns,
and165 targeted layout cases validated. Actual APK/signing checks passed.
Physical Android acceptance remains pending; DEBUG QA.
[Scope and validation](docs/RELEASE_0.9.21.md) · [APK evidence](docs/RELEASE_0.9.21_artifacts.json).

## Scorer World 0.9.20 — objectives, skills and coach trust

[Download World 0.9.20 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.20/Scorer-World-0.9.20.apk)

Player name > Player Development opens Objectives, Skills and Coach Trust.
Training Focus selects low/placed finishing, headers or penalties for the next
three-shot session. Persisted experience improves bounded match controls.
Club trust controls status, availability and chance frequency while preserving
training/morale minimums; scoring and training allow recovery. Existing careers,
trophies, names and post-match flow remain compatible.

549 core/native cases validated with final targeted reruns; 924 responsive cases
have no findings. Exact APK code, upgrade certificate and16KB packaging verified.
Physical Android acceptance is pending; this is DEBUG QA, not Play approval.
[Rules and validation](docs/RELEASE_0.9.20.md) · [APK evidence](docs/RELEASE_0.9.20_artifacts.json) ·
[Saved six-point list](docs/GAMEPLAY_IMPROVEMENTS.md).

## Scorer World 0.9.19 — watch the move, then finish

[Download World 0.9.19 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.19/Scorer-World-0.9.19.apk) ·
[Six saved gameplay suggestions](docs/GAMEPLAY_IMPROVEMENTS.md)

Crosses, cutbacks, first-time finishes, rebounds and direct free kicks now have
visible preparation. The ball reaches the striker before the scene pauses and
aim/power/full countdown appear. Existing through-ball duels and announced
penalties retain their slots; training stays striker+keeper only.

358 core/171 native cases validated with corrected obsolete assertions; 66 targeted
layout checks have zero findings. 2,880 paired physical attempts are documented.
DEBUG QA upgrade; physical Android acceptance remains pending.
[Changes and limits](docs/RELEASE_0.9.19.md) · [APK evidence](docs/RELEASE_0.9.19_artifacts.json).

## Scorer World 0.9.18 — English default and compact screens

[Download World 0.9.18 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.18/Scorer-World-0.9.18.apk)

English starts by default; saved language choices and phone-country contracts remain
independent. Compact justified launch notice retains the automatic usage disclosure.
Help has justified gameplay instructions. Coach closing feedback starts below the
portrait and spans the panel width. Existing career-transfer Settings remain accessible.

354 core and 168 native Kivy tests validated; 891 layout cases have no findings,
including 33 repeated Help cases after the final Settings-access adjustment.
Exact APK source and upgrade signing checks are documented with the release.
Physical Android handset validation remains pending; this is DEBUG QA, not Play approval.
[Changes](docs/RELEASE_0.9.18.md) · [APK evidence](docs/RELEASE_0.9.18_artifacts.json).

## Scorer World0.9.17 — responsive layout audit and corrections

[Download World0.9.17 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.17/Scorer-World-0.9.17.apk) ·
[891-case layout report](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.17/responsive_0.9.17.json)

27 views across11 resolution/density/text-scale configurations and Portuguese,
German and Japanese:891 native layout cases, zero findings after corrections.
Coach headings/status use actual font heights; navigation headers fit enlarged
Back controls. Cases cover16:9,18.5:9,19.5:9,20:9, foldable/compact viewports and
130% text. These are landscape desktop Kivy checks, not universal physical-device
or cutout/OS certification. Android handset validation remains outstanding.

520 host tests passed (353 core +167 native Kivy). Exact compiled source,
existing QA certificate, API36/arm64 and16KB alignment verified. Gameplay,
careers, single-screen news/coach and penalty rules retained. DEBUG QA;
public launch remains1.0.
[Scope](docs/RELEASE_0.9.17.md) · [APK evidence](docs/RELEASE_0.9.17_artifacts.json) ·
[Public download check](docs/RELEASE_0.9.17_download.json).

## Scorer World0.9.16 — more duels, penalties and one-screen reading

[Download World0.9.16 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.16/Scorer-World-0.9.16.apk) ·
[Menu preview](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.16/0.9.16-menu-pt.png) ·
[Penalty preview](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.16/0.9.16-penalty-pt.png)

More one-on-one opportunities, including against elite teams. Penalties are
announced before playing the chance and replace existing slots. Newspaper and
coach fit one screen with concise fallbacks; all observed goal minutes and three
feedback parts are retained. Notice text is justified. Root splash touch handling
works before child layout. The player name is the button, with three aligned
World header actions; viewport rebuild preserves profile typing.

518 host tests passed (353 core +165 native Kivy), with final targeted viewport/
locale checks. Exact compiled gameplay/UI/coach source and all nine catalogues,
penalty budget, existing QA certificate and16KB alignment verified. Previews are
desktop Kivy with synthetic fixtures. Physical Android first-touch/reading checks
remain outstanding. DEBUG QA; public launch remains1.0.
[Scope](docs/RELEASE_0.9.16.md) · [APK evidence](docs/RELEASE_0.9.16_artifacts.json) ·
[Public download check](docs/RELEASE_0.9.16_download.json).

## Scorer World0.9.15 — post-match newspaper/coach flow and player trophies

[Download World0.9.15 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.15/Scorer-World-0.9.15.apk) ·
[Player trophy preview](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.15/0.9.15-trophies-pt.png)

Full-time Continue opens the newspaper, then a requested coach meeting, then the
career menu. That queue survives reload; newspaper/coach hub buttons are removed.
Player shows saved league/cup/national trophies and Golden Boot awards from
observed campaigns in this version onward. Earlier unrecorded personal titles
are not invented from AI winner archives. The World button reads EDITOR. Agent
is grey outside transfer windows, with the existing free-agent exception.

508 host tests passed (350 core +158 native Kivy). Actual compiled honours/cup
award and newspaper queue/reload verified, with exact gameplay/UI source, existing
QA certificate, API36/arm64 and16KB alignment. Preview is desktop Kivy with
synthetic awards. Physical Android validation remains outstanding. DEBUG QA;
public launch remains1.0.
[Scope](docs/RELEASE_0.9.15.md) · [APK evidence](docs/RELEASE_0.9.15_artifacts.json) ·
[Public download check](docs/RELEASE_0.9.15_download.json).

## Scorer World 0.9.14 — every goal in the headline, wide aim, training gate

[Download World 0.9.14 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.14/Scorer-World-0.9.14.apk) ·
[Newspaper preview](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.14/0.9.14-goal-headline-pt.png)

Every personal goal earns a name headline and article mention, including a goal
in a draw or defeat. Aim now sweeps both posts and slightly outside. Three saved
practice shots are mandatory before each match; cup/national fixtures in the
same week consume training too. Abandoned practice cannot unlock Play or grant
completion rewards. Career, aliases and partial training remain compatible;
old completed-training flags reset once on upgrade to close the reuse loophole.

499 host tests passed (345 core +154 native Kivy). Actual APK compiled source,
three-shot/same-week gate, goal headline, existing QA upgrade certificate, API36
and16KB alignment verified. Preview is desktop Kivy; physical Android validation
remains outstanding. DEBUG QA; public launch remains1.0.
[Scope](docs/RELEASE_0.9.14.md) · [APK evidence](docs/RELEASE_0.9.14_artifacts.json) ·
[Public download check](docs/RELEASE_0.9.14_download.json).

## Scorer World 0.9.13 — fairer finishing, training and coach feedback

[Download World 0.9.13 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.13/Scorer-World-0.9.13.apk) ·
[Training preview](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.13/0.9.13-training-pt.png) ·
[Coach preview](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.13/0.9.13-coach-pt.png)

Scoreboard badges removed. Aim stays within the goal, hard chances allow more
time and slower aim, and keeper arms retain a fixed length for drawing/collisions.
Training is player versus keeper only, with session plan, saved shots/goals,
progress and readiness. Requested coach meetings include actual recent club form
and three feedback paragraphs adapted to the situation and coach's personality.
Nine languages and existing careers retained.

493 host tests passed (340 core +153 native Kivy). Exact compiled APK source,
existing QA upgrade certificate, API36/arm64 and16KB alignment verified.
Desktop previews are illustrative native Kivy renders; physical Android
validation remains outstanding. DEBUG QA; public launch remains1.0.
[Scope](docs/RELEASE_0.9.13.md) · [APK evidence](docs/RELEASE_0.9.13_artifacts.json) ·
[Public download check](docs/RELEASE_0.9.13_download.json).

## Scorer World 0.9.12 — folded newspaper and complete goal reporting

[Download World 0.9.12 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.12/Scorer-World-0.9.12.apk) ·
[Preview](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.12/0.9.12-newspaper-pt.png)

The paper sits in a dark reading window with a folded reverse, shadows and grain.
Original Scorer Press display/pixel fonts give the title and story a retro game
identity. Text wraps beside/below the embedded photo and into columns. Every
recorded goal includes its minute and changing score, followed by a brief factual
summary. Long reports turn leaves without scrolling or deleting words.

487 host tests passed (340 core +147 native Kivy). A real Kivy preview at the
owner's phone proportions fits the four-goal example on one sheet. The preview
uses an illustrative test fixture, not the owner's actual goal chronology or a
physical Android screenshot. Existing careers/name packs remain compatible.
Actual compiled source/fonts, upgrade certificate and16KB alignment verified.
DEBUG QA; physical Android validation remains outstanding.
[Scope](docs/RELEASE_0.9.12.md) · [APK evidence](docs/RELEASE_0.9.12_artifacts.json) ·
[Public download check](docs/RELEASE_0.9.12_download.json).

## Scorer World 0.9.11 — single-page news, coach portraits, World editor

[Download World 0.9.11 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.11/Scorer-World-0.9.11.apk)

The newspaper fits one screen with measured full/concise text and no scrolling.
Meetings show one of ten saved coach-at-desk portraits; changing clubs always
changes the previous face. The editor now lives in World > Names Editor and is
removed from the main menus. Existing careers and name packs remain compatible.

480 host tests passed (336 core +144 native Kivy), followed by6 final newspaper
checks. All nine languages and long CJK aliases tested down to320×240 with
body type>=12sp. Actual compiled source/assets, upgrade certificate and16KB
alignment verified. DEBUG QA; physical-device testing remains outstanding.
[Scope](docs/RELEASE_0.9.11.md) · [APK evidence](docs/RELEASE_0.9.11_artifacts.json) ·
[Public download check](docs/RELEASE_0.9.11_download.json).

## Scorer World 0.9.10 — newspaper and conditional coach meetings

[Download World 0.9.10 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.10/Scorer-World-0.9.10.apk)

[Download real-name editor JSON files](docs/data/name-packs/README.md): current and legacy-compatible variants for eight countries, including Brazil and Argentina. No APK update needed.

Ordinary weeks have no meeting. Only a drought or an actual key match prompts
the coach and blocks training/play until reviewed. Newspaper opens SCORER DAILY:
factual last-match coverage, recorded goal minutes, conditional player mentions
and five original rotating match photographs in a paper-style reader.
Existing careers and training progress are retained; no reset required.

466 host tests passed (326 core +140 native Kivy), including all nine languages.
Actual compiled source, bundled photo/font bytes, upgrade certificate and16KB
alignment verified. DEBUG QA; physical-device testing remains outstanding.
[Scope](docs/RELEASE_0.9.10.md) · [APK evidence](docs/RELEASE_0.9.10_artifacts.json) ·
[Public download check](docs/RELEASE_0.9.10_download.json).

## Scorer World 0.9.9 — coach meetings and feedback

[Download World 0.9.9 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.9/Scorer-World-0.9.9.apk)

Meet the coach before each week's training and match. Club coaches have stable
Encouraging, Demanding or Balanced approaches, with varied feedback on droughts,
decisive performances and strong form; brief check-ins in ordinary weeks.
Existing careers and training progress are retained.

448 host tests passed (314 core +134 native Kivy). Actual compiled source,
coach save/gates, competitions, upgrade certificate and16KB alignment verified.
DEBUG QA; physical-device testing remains outstanding.
[Scope](docs/RELEASE_0.9.9.md) · [APK evidence](docs/RELEASE_0.9.9_artifacts.json) ·
[Public download check](docs/RELEASE_0.9.9_download.json).

## Scorer World 0.9.8 — decisive match moments

[Download World 0.9.8 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.8/Scorer-World-0.9.8.apk)

Late chances to equalise or lead, actual finals/playoffs, curated derbies and
close survival run-ins now have visible context. One actual featured chance
is retained in Fixtures history. Existing careers receive the feature without
a reset; chance caps, shot difficulty and AI goal budgets are unchanged.

434 host tests passed (304 core +130 native Kivy). The built APK's compiled
source, upgrade certificate and 16KB alignment were verified. DEBUG QA;
physical-device testing remains outstanding. [Scope](docs/RELEASE_0.9.8.md) ·
[APK evidence](docs/RELEASE_0.9.8_artifacts.json) ·
[Public download check](docs/RELEASE_0.9.8_download.json).

## Scorer World 0.9.7 — domestic schedules and split tables

[Download World 0.9.7 APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.7/Scorer-World-0.9.7.apk)

New World careers use sourced regular capacities/splits in38 countries/76 divisions,
including Spain20/22 and Brazil20/20. Split membership, points and different group
endings persist. Save and Exit, install over the existing World QA app, and Load
Game to keep your current career’s original model. Start New Game (with the normal
confirmation/private backup) to use the new structures. No automatic career reset.

[Scope and upgrade instructions](docs/RELEASE_0.9.7.md) ·
[Verified APK](docs/RELEASE_0.9.7_artifacts.json) ·
[Public download verification](docs/RELEASE_0.9.7_download.json).
422host tests passed; actual compiled source/data, splits/legacy reload, upgrade
certificate and118ELF16KB verified. DEBUG QA; public launch remains1.0.

## Scorer World 0.9.4 — two divisions everywhere

[Download World0.9.4 APK](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.9.4/Scorer-World-0.9.4.apk) · [Download updated names JSON](https://github.com/pereiragoncalo/Scorer/releases/download/real-names-two-divisions-2026/Scorer-World-Real-Names-Two-Divisions-2026.json)

All212 countries have two playable divisions. Three clubs move between them each season. The bottom three in Division2 exchange with the front of a10-club reserve queue; relegated clubs go to the back, preserving the pool size and preventing an immediate return. A player whose club leaves Division2 becomes a free agent, with5 valid offers and signing outside normal transfer windows. World → Country shows the two leagues and10 reserve names.

Existing saves, UIDs, names and history are retained. A legacy career below Division2 moves to free-agent status without resetting personal progress. The first migrated write keeps a `.two-divisions-backup.json` copy. Old league objects remain hidden only for compatibility; no new playable destinations or league simulation below tier2. Save and Exit, install over World QA and Load Game; reimport the updated names file if wanted. [Rules and verification](docs/RELEASE_0.9.4.md). DEBUG QA; public launch remains1.0.

## Corrected real names by division

[Download JSON — Europe2026/27, Brazil/Argentina2026](https://github.com/pereiragoncalo/Scorer/releases/download/real-names-divisions-2026/Scorer-World-Real-Names-Divisions-2026.json). All494 selected club slots checked against their real division; no duplicate real teams. Reimport in Names Editor; World0.9.3 remains compatible, with no APK update. Existing game capacities and simulated movement are preserved. [Reference/validation](docs/data/name-packs/README.md).

## Scorer World 0.9.3 — direct leaderboard and cleaner menus

[Download World 0.9.3 APK](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.9.3/Scorer-World-0.9.3.apk) · [Download real names JSON — Europe, Brazil and Argentina](https://github.com/pereiragoncalo/Scorer/releases/download/real-names-divisions-2026/Scorer-World-Real-Names-Divisions-2026.json)

Privacy removed from the start and main menus; Global removed from Top Scorers. Leaderboard opens the public records table directly, without a legal/adult-control page. Adult/share confirmation applies when publishing, not viewing. Reporting/blocking/removal remain accessible; career transfer/settings are under Help → Settings. Startup agreement and 0.9.1 gameplay/editor remain. Save and Exit, install over World QA and Load Game. DEBUG test build; public launch remains1.0. [Verification](docs/RELEASE_0.9.3.md).

## Scorer World 0.9.2 — translated agreement buttons

[Download World 0.9.2 APK](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.9.2/Scorer-World-0.9.2.apk)

The launch notice now uses **CONCORDO / NÃO CONCORDO** in Portuguese, **I AGREE / I DO NOT AGREE** in English, and matching translations in all nine UI languages. Agree continues; disagree immediately exits. World 0.9.1 gameplay/editor changes and saved careers are retained. DEBUG QA; public launch remains1.0.

## Scorer World 0.9.1 — startup notice, editor and shot balance

[Download World 0.9.1 APK](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.9.1/Scorer-World-0.9.1.apk)

After each launch splash, the notice has only **OK** (continue) and **NOT OK** (close immediately and discard pending usage counts). The in-app privacy-request workflow is removed. No usage is sent before OK. World hub → **Names Editor** → **Import Names File** opens the document picker and existing import preview.

Keeper movement and visible glove reach now defend high shots and leave a fairer opportunity for low shots, in matches and training. Ball targets, goal geometry, career progress, competitions and imported names are preserved. Save and Exit, install over your existing World QA app, then Load Game. [Checks and limitations](docs/RELEASE_0.9.1.md). DEBUG QA; public launch remains 1.0.

## Scorer World 0.9 — World competitions integrated

[Download World 0.9 APK](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.9/Scorer-World-0.9.apk)

Persistent continental/national tournaments, qualifying games, domestic brackets, played promotion playoffs, ranked movement and next-season qualification. The player can inspect fixtures, groups and results under **World → Competitions**. Existing careers and imported names are retained; export a career backup before upgrading, then Save and Exit, install the matching World QA APK and Load Game.

[Game formats, save handling and verification](docs/WORLD_COMPETITIONS_0.9.md). Point 1 is implemented; actual Android acceptance and the remaining server/Play steps follow. This is a DEBUG QA candidate; public launch remains 1.0.

## Next milestones: 0.9 testing → 1.0 launch

The current Scorer World test phase is **0.9** and the public release will be **1.0**. Version staging now selects those names with increasing Android version codes. Version 0.6.48 is retained below as a historical QA build.

[Current remaining work and acceptance criteria](docs/play/ROAD_TO_1.0.md): complete intended World competition behaviour, real Android acceptance, deploy/verify final English policies and online safety, then production signing and Console checks. Developer account verification is already confirmed.

## Scorer World 0.6.48 — stronger defending

[Download World 0.6.48 APK](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.48/Scorer-World-0.6.48.apk)

More demanding goalkeepers and marking, improving with the opponent’s division. High/low saves close repeated corner exploits while physical aiming and morale opportunities remain. Existing World careers and imported names are preserved. Save and Exit before upgrading the matching QA APK, then Load Game.

[Balance measurements and limits](docs/DIFFICULTY_0.6.48.md). This is a debug QA APK, not a production-signed Play upload.

## Scorer World 0.6.47 — current Google Play launch scope

[Download Scorer World 0.6.47 APK](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.47/Scorer-World-0.6.47.apk) · [Laptop update commands](docs/play/SERVER_0.6.47.md)

Only **Scorer World** (`com.clemir.scorerworld`) will launch: **free, ad-free, no in-app purchases, local names editor included**. The nine game UI languages remain available. Earlier Free builds below are historical QA downloads, not a second Play product.

Public privacy, community rules, removal instructions and the store listing are English. [Final English policy](docs/play/PRIVACY_POLICY.md) · [World launch and remaining steps](docs/play/WORLD_LAUNCH_0.6.47.md).

This historical build included a privacy-request screen, removed in 0.9.1 in favour of the startup OK/NOT OK notice. No Play upload or rollout has been performed.

## Scorer0.6.46 — Google Play preparation

[Scorer-Free-0.6.46.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.46/Scorer-Free-0.6.46.apk)

[Scorer-World-0.6.46.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.46/Scorer-World-0.6.46.apk)

[Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.46/Scorer-Free.exe)

Both apps free/ad-free. Automatic counts wait for the first-run notice. Adult controls, reviewed public names, report/block and local career transfer added. 298unique tests passed; both new AABs validated, native Windows tested.

[Release/AABs and external production gates](docs/play/RELEASE_0.6.46.md) · [Laptop update commands](docs/play/SERVER_0.6.46.md). Backend v3/public policy are not deployed by this cloud session. These are QA candidates, not production-signed or Google-approved releases.

[Google Play: current publication audit (31/10/2026)](docs/play/PUBLISHING_AUDIT_2026-10-31.md). QA builds below are not production-ready Play releases.

## Scorer0.6.45 — automatic usage counts

[Scorer-Free-0.6.45.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.45/Scorer-Free-0.6.45.apk)

[Scorer-World-0.6.45.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.45/Scorer-World-0.6.45.apk)

[Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.45/Scorer-Free.exe)

Usage counts are automatic, disclosed on the splash and Privacy screens. Public season-record sharing stays optional. No server upgrade required. [Verification and publication limits](docs/AUTOMATIC_0.6.45.md).

## Scorer0.6.44 — every app opening counts

[Scorer-Free-0.6.44.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.44/Scorer-Free-0.6.44.apk)

[Scorer-World-0.6.44.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.44/Scorer-World-0.6.44.apk)

[Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.44/Scorer-Free.exe)

[Session-count correction and verification](docs/SESSIONS_0.6.44.md). With usage consent, startup and return after backgrounding each count once; no server upgrade needed.

## Scorer0.6.43 — no advertising

[Scorer-Free-0.6.43.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.43/Scorer-Free-0.6.43.apk)

[Scorer-World-0.6.43.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.43/Scorer-World-0.6.43.apk)

[Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.43/Scorer-Free.exe)

No adverts, ad SDK, reward videos or commercial stadium panels in any edition. Careers retained. [Google Play engineering review and remaining requirements](docs/play/POLICY_REVIEW_0.6.43.md).

## Scorer0.6.42 — completed-season records and division boards

[Scorer-Free-0.6.42.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.42/Scorer-Free-0.6.42.apk)

[Scorer-World-0.6.42.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.42/Scorer-World-0.6.42.apk)

[Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.42/Scorer-Free.exe)

[Layout, recording rules, tests and required laptop server upgrade](docs/SEASON_RECORDS_0.6.42.md). New public player-name consent required.

## Scorer0.6.41 — main-menu Leaderboard and owner usage service

[Scorer-Free-0.6.41.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.41/Scorer-Free-0.6.41.apk)

[Scorer-World-0.6.41.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.41/Scorer-World-0.6.41.apk)

[Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.41/Scorer-Free.exe)

[Validation and privacy choices](docs/CONNECTED_0.6.41.md). Optional rankings and default-off usage connect to stats.clemir.com; private owner dashboard remains /admin.

## Scorer0.6.40 — corrected aiming, empty training stands, Windows fullscreen

[Scorer-Free-0.6.40.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.40/Scorer-Free-0.6.40.apk)
[Scorer-World-0.6.40.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.40/Scorer-World-0.6.40.apk)
[Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.40/Scorer-Free.exe)

[Tests and online-service status](docs/ONLINE_0.6.40.md). Leaderboard/usage hosting prepared; no public destination configured or remote collection active.

## Windows Free 0.6.39-win.4

[Download EXE](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/windows-beta-0.6.39-4/Scorer-Free.exe) — smaller keeper, faster shots, empty training stands; Android unchanged. [Validation](docs/WINDOWS_POWER.md).

# Scorer Free Windows0.6.39-win.3 — larger goal and depth fix

[Download Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/windows-beta-0.6.39-3/Scorer-Free.exe).
Windows goal +12%width/+10%height with matching physics/net/aim, refined white
frame/translucent net and proportional far ball. Resting net balls now remain
behind the keeper. Local English boards include YOUR COMPANY HERE and World
promotion. Existing matchday dashboard/careers retained.253 core/Kivy tests,
6native Windows checks and frozen hub/goal renders PASS in run40740304128.
Unsigned QA build; human shot feel/full-match testing remains pending.
[Evidence/calibration](docs/WINDOWS_GOAL.md).

# Scorer Free Windows0.6.39-win.2 — matchday dashboard

[Download Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/windows-beta-0.6.39-2/Scorer-Free.exe).
All12 upcoming league games on the left, own fixture highlighted; saved league
leaders on the right, permanent hero rank/goals and compact season totals.
Training/Play and original navigation retained; no main-menu scroll. Small windows
use compact fallback; Android UI and saved careers unchanged.245 core/Kivy tests
and6 native Windows checks PASS; actual frozen build/render/career/training/
engine match/save-reload/exit-cancel passed in run40729867510. Unsigned QA build;
manual play/audio/resize still pending. [Evidence](docs/WINDOWS_MATCHDAY.md).

# Scorer Free for Windows — first QA executable

[Download Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/windows-beta-0.6.39-1/Scorer-Free.exe)
for Windows10/11 x64. Original Python/Kivy, English/one division, single portable
EXE, persistent per-user careers and mouse/keyboard. No Android AdMob SDK/reward
videos; local stadium promotion remains. Optional stats default off/local only.
237 core/Kivy tests plus6 Windows staging checks passed; actual frozen Windows
startup/new career/training/save/reload/exit confirmation and rendered screenshot
passed in native run40667690804. Unsigned QA build; manual full-match/audio/resize
on a user's Windows PC remains pending. [Evidence/guide](docs/WINDOWS_FREE.md).

# Scorer Free0.6.39 — start/end session notices

Owner email workflow now supports new session-start/normal-close counters instead
of a daily schedule. Default-off choice, no names/IDs/pairing, server-only SMTP;
notices may combine arrivals and force-stop may omit the end. Current APK endpoint
is empty: no developer uploads or email delivery is active.
[Details and validation](docs/SESSION_NOTICES_0.6.39.md).

# Scorer Free0.6.38 — optional usage counters

Privacy now offers explicit default-off aggregate counters. The current APK has
no receiving URL: counts stay local; no developer statistics are uploaded.
Own collector and server-only daily email digest are prepared, not deployed.
222 tests passed; actual Free APK built and statically verified. No phone/SMTP
or live HTTPS-host test is claimed. World remains0.6.37.
[Release evidence](docs/ANONYMOUS_STATS_0.6.38.md) · [Server setup](server/USAGE_SETUP.md).

# Scorer World 0.6.37 — promotion/relegation/playoff places

World standings and browsed league tables now show P/PO/R places with green,
amber and red zones. Tap Rules for complete localized meanings and explicit
no-promotion/no-relegation/no-playoffs boundaries. Markers follow the current
game format, not certified national regulations. Priority-country playoff
outcomes remain simulated; no knockout playoff fixtures were added.
200 tests passed (125 core/security +75 Kivy); actual World APK built/verified.
[Behaviour, model limitations and evidence](docs/STANDINGS_0.6.37.md).

# Scorer World 0.6.36 — matching World wordmark

SCORER WORLD is now a unified image with matching extended italic gold lettering,
rather than the original artwork followed by a different font. The shared entry,
normal hub and compact hub renderer uses this art. Free's original logo remains
unchanged; latest Free APK remains0.6.35.193 tests passed (122 core/security +71
Kivy), real World debug APK compiled and verified.
[Visual/build evidence](docs/WORLD_WORDMARK_0.6.36.md).

# Scorer 0.6.35 — compact confirmation and World branding

New-career confirmation now wraps its content in a compact themed dialog, with
no large empty block. Entry logo is at the screen's top left. World adds a native
gold WORLD word beside the existing artwork on entry and both main menu layouts.
Free keeps the original Scorer logo. Native entry banners are hidden while a
confirmation is open; backup and Cancel behaviour remain safe.
[Behaviour, screenshots and build evidence](docs/START_LAYOUT_0.6.35.md).

# Scorer 0.6.34 — cleaner menus

Removed small edition/test-ad taglines, routine main-menu prose, generic player
form helpers and the redundant training-ad footnote. Privacy keeps its disclosures
and consent action, with SDK diagnostic lines removed. Field/statistic labels,
gameplay instructions in Help and actual name/load/save errors remain visible.
Both Free and World APKs compiled;189 tests passed (122 core/security +67 Kivy).
[Build evidence and device checklist](docs/CLEAN_MENUS_0.6.34.md).

# Scorer Free 0.6.33 — no World menu button

Removed the World action from both normal and compact Free main menus.
The post-splash screen also remains without that action. Free keeps its ten
play/navigation actions and offline World promotion boards around the pitch.
World0.6.31 remains unchanged. [Evidence](docs/FREE_HUB_0.6.33.md).

# Scorer Free 0.6.32 — simpler post-splash entry

The Free entry menu now shows New Game, Load Game, Help, Privacy and Exit.
The Scorer World action was removed from this screen; New Game fills its row.
187 tests passed (122 core/security +65 actual Kivy UI), real Free arm64 debug APK
compiled and statically verified. Existing package, icon, signature and career
compatibility remain. World remains at0.6.31; no new World APK was needed.
[Build evidence](docs/ENTRY_MENU_0.6.32.md).

# SCORER 0.6.31 — World player creation

New World careers ask for name, nationality and starting country together.
Nationality and country are independent, suggested from the phone and selectable
through offline localized search/paging. England starts in Division4. Continue
shows contracts from the chosen country; accepting a contract saves the choices
with the career. Free and established World profiles keep name-only editing.
[Behaviour, evidence and Android checklist](docs/PLAYER_CREATION_0.6.31.md).

# SCORER 0.6.30 — distinct Android launcher entries

Install both APKs for two independent applications: **Scorer** (Free, original
emerald S icon) and **Scorer World** (blue globe/WORLD icon). Installing one APK
installs only its own application. Both update their matching0.6.29 package and
keep their existing private careers; no uninstall or career transfer is needed.
[Launcher identity, actual APK validation and device checks](docs/LAUNCHER_0.6.30.md).

# SCORER 0.6.29 — Free English, World nine languages

Free remains English-only. World follows the phone language or a manual choice:
English, Portuguese (Portugal), Spanish, German, Italian, Korean, Japanese,
Simplified Chinese and Vietnamese. Unsupported phone languages fall back to English.
Use Language on World's entry screen or Help page. Names/editor/save identifiers
stay unchanged; the UI language does not select or change the player's country.

**179 tests passed** (118 core/security +61 actual Kivy interface tests).
[Language behaviour, build evidence and Android test checklist](docs/LANGUAGES_0.6.29.md).
Two independent Android applications/careers remain the current product model.
Historical single-app purchase instructions below are superseded.

# SCORER 0.6.28 — separate Free and World Android applications

Latest owner decision: two independent APKs. Free retains `com.clemir.striker`
and its one-division career; World uses `com.clemir.scorerworld`, its own career,
worldwide league model and local names editor. World has no AdMob or Google Play
Billing SDK. Free promotes World on offline stadium boards outside the field.
No in-app upgrade, account linking or automatic career conversion.

**161 tests passed** (108 core/security +53 Kivy). Both arm64 QA APKs were genuinely
compiled, signed with the existing debug certificate and statically verified.
Physical Android installation/gameplay checks remain required. World country
formats and international simulation remain in development; no store/payment
activation or production-ready claim.

[Release behaviour, build commands, evidence and test checklist](docs/TWO_APPS_0.6.28.md).
Earlier single-app purchase/mode-switch instructions below are historical and
superseded. Use `tools/prepare_editions.py`; legacy single-app release CLI is retired.

# Development — 25 October 2026

The owner-selected fallback now has two active divisions with three promotions
and three relegations outside Europe/Brazil/Argentina/Mexico. Existing saves and
archived aliases are preserved; Android country detection prefers the primary
system locale. **154 tests passed on this scoped source change**; no new APK.
Interface text remains English; locale detection alone does not translate it.
[Behaviour, migration and evidence](docs/DOMESTIC_RULES_DEVELOPMENT.md).
[Priority national-regulation collection and access gaps](docs/regulations/PRIORITY_STATUS.md).

# SCORER 0.6.27 — World presentation and play balance

World aim accelerates by division. Morale >10 guarantees at least2 match chances;
>15 guarantees3 (both modes). World uses real-city/local-form fictional club names,
reference colours where known, and an in-editor JSON format example. Free names,
separate career slots and existing saves stay intact.

**139 tests passed**; Free and a same-app owner QA APK were genuinely built and
statically checked. QA temporarily opens World for testing only, with no purchases.
[Coverage, exact behaviour and test/build evidence](docs/WORLD_0.6.27.md).

# SCORER 0.6.26 — Free and World careers

Free starts directly in **Scorer League**, with no country selector. World uses
its own career/player/save inside the same application; Free progress stays in Free.
Verified owners can switch modes and choose New Game/Load Game independently.
Only World offers phone-country contracts and England Division 4.

[Changes and test results](docs/UI_0.6.26.md). Earlier 0.6.25 migration statements
below are historical and superseded. Real purchases remain disabled.

# SCORER — current preparation 0.6.25

Original Python/Kivy Android game. **One application**, com.clemir.striker:
Free plus a planned one-time World/editor/ad-free upgrade through Google Play.
This replaces the historical separate-World-app plan below.

Play Billing and the server-side verifier are prepared but **payments are disabled**.
The actual rehearsal AAB uses TEST advertising and is not signed for production.
Verification: 79 core/security tests + 46 actual Kivy tests passed. The AAB was
compiled and statically checked, not installed or purchase-tested through Play.
For backend tests in a fresh development environment, install server/requirements.txt
separately; those dependencies never belong in Buildozer requirements.

See [Play build, release gates and account tasks](docs/play/README.md) and
[verification results](docs/BUILD_LOG.md). No store upload or payment activation.

# STRIKER Android — base para trabalhar com Codex

## Estado em 23/10/2026
Código original Python/Kivy recuperado da Google Drive `Projetos/Striker/Builds/Striker-P0-05-v006.py`, com aproximadamente 6290 linhas. Reúne simulação de futebol, carreira de avançado, treino, agente, classificação e componentes FREE/WORLD. **Não é a versão web.**

- `main.py`: cópia do código-fonte v006, com o nome esperado pelo Buildozer.
- `baseline/`: cópia histórica imutável para comparação.
- `buildozer.spec`: configuração Android original já guardada na Drive; ainda não validada mediante compilação real.
- `docs/AndroidManifest.release.reference.xml`: referência estática; não implica que o Manifest final do Android já a incorpore.
- `AGENTS.md`: regras persistentes para Codex.
- `FIRST_CODEX_TASK.md`: pedido inicial para Codex.
- `ROADMAP.md`: sequência de trabalho até 6 de novembro de 2026.

## Como abrir no Codex
- Extrair este ZIP para uma pasta local.
- Abrir a pasta na aplicação Codex ou, num terminal já com Codex instalado, executar `codex` dentro da pasta.
- Fornecer o texto de `FIRST_CODEX_TASK.md` como primeira tarefa.
- Preferencialmente importar a pasta para um repositório GitHub **privado** e conceder-lhe acesso através do Codex. Não é obrigatório para executar Codex localmente.
- Revisar o diff e os resultados dos testes antes de aceitar cada alteração.

## Verificações simples já disponíveis
```bash
python3 -m py_compile main.py
```
Isto verifica apenas sintaxe. A funcionalidade Android exige um ambiente de build Linux com SDK/NDK e testes num telemóvel real.

## Critérios de lançamento
1. APK Android instalado e executado em dispositivos reais.
2. Jogo funcional, save persistente em armazenamento app-private e regresso à carreira.
3. Painéis visíveis na simulação, carregados de imagens locais e sem FPS degradado.
4. Fim de uma partida, avanço de carreira e exportação/instalação testados.
5. APK assinado disponibilizável; AAB preparado para Play (aprovação não garantida).
6. Direitos dos conteúdos e privacidade verificados antes da publicação pública.

## Fase 1 — candidato de código 0.6.1

A carreira original está em `career.py`, importável sem Kivy; `main.py` mantém a
interface. Testes: `python3 -m unittest discover -s tests -v`.
Ver [build Android e limitações](docs/ANDROID_BUILD.md) e [resultados](docs/BUILD_LOG.md).
Já foi compilado um APK debug arm64 0.6.1, com assinatura e alinhamento ELF/ZIP verificados. O proprietário confirmou que 0.6.1 abre e corre sem crashes no Android; não é uma versão de distribuição. Não foi gerado AAB.

## 0.6.2 — menus responsivos

O proprietário confirmou que 0.6.1 abre e corre sem crashes no telemóvel.
A nova interface 0.6.2 usa texto multilinha, deslocação, alvos de toque de 52 dp e
botão Sair com confirmação/gravação. Mantém a mesma aplicação/carreira.

Testes Kivy reais, além da suite sem interface:
```sh
KIVY_HOME=/workspace/striker-runtime/kivy /workspace/striker-venv/bin/python -m unittest discover -s ui_tests -v
```
A separação FREE/World e funcionalidades ainda por implementar estão descritas
em [modelo de produto](docs/PRODUCT_MODEL.md). Free tem uma divisão; a aplicação
paga separada e o editor de importação mundial ainda não são produtos entregues.

## SCORER 0.6.3 — identidade e correções

Nome público atualizado para **SCORER**, splash em inglês com crédito clemir.
Sair só no menu principal, painel final responsivo e leitura segura de saves
malformados. Mantidos identificador Android e formato de carreira para atualização.
Ver [auditoria, testes e limitações](docs/AUDIT_0.6.3.md). Suite: 21 testes sem
interface e 10 testes Kivy; esta beta ainda exige validação no telemóvel.

## SCORER 0.6.4 — menu de um só ecrã e identidade visual

Menu principal sem scroll: resumo compacto da carreira e seis ações visíveis,
com Sair apenas no cabeçalho. Listas de classificação/calendário continuam
navegáveis por deslocação. Painel final dimensionado pelo conteúdo, botão
Continuar limitado a 176 dp. Splash «SCORER by clemir» e ícone próprio Android.
Ver [verificação da versão](docs/UI_0.6.4.md).

## SCORER 0.6.5 — escolher a carreira ao abrir

O splash permanece até tocar no ecrã, inclusive depois de rodar. Segue-se
Novo jogo / Carregar jogo / Sair. Novo jogo com save existente exige confirmação
e cópia local de segurança; cancelar ou fechar antes da escolha preserva o save.
Nome legado «England Division 4» migra para Liga Scorer sem apagar progresso:
FREE permite uma única divisão. Novo menu com fundo original de estádio,
próximo jogo destacado e navegação inferior, sem scroll.
[Alterações, referência visual, 40 testes e limitações](docs/UI_0.6.5.md).

## SCORER 0.6.6 — personalização e navegação compacta

Novo jogo pede o nome do jogador. Para alterar Alex Silva numa carreira existente,
abrir **Jogador** no menu principal; o progresso mantém-se. Splash com crédito
clemir menor, botões arredondados com relevo e listas de classificação,
marcadores e calendário paginadas, sem scroll horizontal/vertical.
[Alterações, 45 testes e limitações](docs/UI_0.6.6.md).

## SCORER 0.6.7 — alinhamento e tipografia

Marca nativa com Barlow Condensed ExtraBold Italic e crédito Barlow Regular,
fontes incluídas offline com licença. Ajustados eixos de texto nos menus,
indicadores e painel de oportunidade/resultado; texto dos botões centrado na face.
Corrigida a seta em falta no resumo de energia do treino.
[Alterações, fontes, 45 testes e limitações](docs/UI_0.6.7.md).

## SCORER 0.6.8 — treino semanal e menu

Jogar alinhado com Marcadores; ícone S seguido de CORER. Splash com preparação
do remate coerente. Uma sessão de treino por semana da carreira, descontada
ao começar e persistente ao reabrir.
[Alterações, 53 testes e limitações](docs/UI_0.6.8.md).

## SCORER 0.6.9 — alinhamento da marca

S do ícone e CORER na mesma linha, com as bases visuais alinhadas.
Crédito by clemir por baixo. Ajuste apenas visual do cabeçalho principal.

## SCORER 0.6.10 — English edition

All generated game text is in English, including menus, feedback, dates and
confirmations. Existing careers retain progress and custom names. This edition
stays in English on every phone; automatic language selection requires future
translations. [Changes and localisation approach](docs/UI_0.6.10.md).

## SCORER 0.6.11 — scoreboard and half-time

Fixed top-left scoreboard with stacked teams, clock on the right and a local
goal highlight. Shared position during chances; bottom time bar removed.
Half-time pauses after 45 plus added time; SECOND HALF resumes at 45:00.
[Changes and validation](docs/UI_0.6.11.md).

## SCORER 0.6.12 — training before Play

Smaller scoreboard with First half / Second half. Training sits left of Play,
which stays grey until all three weekly shots are completed. Interrupted
training can resume; completed sessions cannot be repeated. Match notice
widgets remain attached during redraws to preserve touches.
[Changes, 62 tests and limitations](docs/UI_0.6.12.md).

## SCORER 0.6.13 — tougher finishing and new logo

At most three personal highlights per match, with at most one clear chance;
all others have harder positions, defensive pressure and sharper goalkeeping.
New icon-based SCORER logo on the main and entry menus, without by clemir.
Existing career totals remain intact.
[Changes, 65 tests and 720 physical shot samples](docs/UI_0.6.13.md).

## SCORER 0.6.14 — timer and player initials

TIME TO SHOOT is attached directly beneath the scoreboard. Player-name
initials are capitalised automatically on profile save and career load,
keeping progress and scorer identity.
[Changes, 67 tests and limitations](docs/UI_0.6.14.md).

## SCORER 0.6.15 — chances depend on the opponent

Opponent quality and league position now determine chance quantity and clear
chance probability. Very strong opponents allow at most one chance, always
hard. Energy/morale still matter and career progress is retained.
[Rules, 70 tests and limitations](docs/UI_0.6.15.md).

## SCORER 0.6.16 — participation after training

Completing weekly training now guarantees at least one match opportunity.
Training goals help earn extras within the opponent's existing limits.
Very strong opponents still allow exactly one hard chance. Existing saves
continue without starting over. [Fix and validation](docs/UI_0.6.16.md).

## SCORER 0.6.17 — researched goal realism

Calibrated scoring against three full League Two seasons and historical shot
data. Match finishing has physical pressure/accuracy; teammate goals reserve
the player's contribution. Fixed duplicate scorer attribution and cup goals
in league rankings. Existing progress and guaranteed trained participation
remain. [Sources, experiments, 79 tests and limitations](docs/REALISM_0.6.17.md).

## SCORER 0.6.18 — balanced league calendar

League fixtures alternate home/away with at most one repeated pair per leg,
no triples, reversed return venues and equal full-season totals. In-progress
legacy calendars are retained when changing them would rewrite played fixtures;
new seasons use the new rule. Cup draws remain independent.
[Rules, save compatibility, 84 tests and limitations](docs/UI_0.6.18.md).

## SCORER 0.6.19 — player name panel

Removed the stray line, rounded the name field, centred text and tightened
the panel spacing/alignment. Name handling and career progress are unchanged.
[Visual fix, 84 tests and limitations](docs/UI_0.6.19.md).

## SCORER 0.6.20 — practice and match balance

Harder practice with match ball physics; slightly more achievable hard match
shots, slower morale loss and stronger goal reward. Club-specific fictional
scorer names preserve saved totals. Standing saves hold the ball during a
forward fall; corner flags and a broadcast-style scoreboard improve presentation.
[87 tests, measured balance and Android verification](docs/UI_0.6.20.md).

## SCORER 0.6.21 — season draw and cup progression

Fixtures shows the complete league calendar without a STATS submenu. New season
league draws are fixed from the start; cup opponents appear one round at a time
through the final. League dates remain fixed after cup elimination.
[Changes, save compatibility and 89 tests](docs/UI_0.6.21.md).

## SCORER 0.6.22 — AdMob test integration

Native Google Mobile Ads + UMP compiled into Android; a test banner after the
splash on the entry menu and test interstitials at completed-match breaks, with
frequency limits and graceful offline fallback.
Privacy screen and child-directed/non-personalised request settings. No revenue
yet: owner account/app IDs, approval and phone validation remain pending.
[Setup and activation](docs/ADMOB_SETUP.md) · [97 tests and build evidence](docs/UI_0.6.22.md).

## SCORER 0.6.23 — post-match ads and morale reward

First completed match can show an available test interstitial; subsequent full-screen
ads respect 60 seconds. Training offers an optional RewardedAd for +1 morale, once
per career week, capped20. Only the SDK earned callback awards it; saves/receipts
prevent duplicate credit. Still official TEST IDs, no production revenue.
[101 tests, implementation and device checks](docs/UI_0.6.23.md).

## SCORER 0.6.24 — Help, local contracts and World preview

Help on entry/hub, informative Upgrade, phone-locale starting contracts or England
Division4; Free still has one selected playable division. Separate ad-free World
preview: 212 regions/758 fictional tiers, worldwide transfers and a local display
names editor with bounded JSON templates/import preview. No billing or automatic
career migration. [111 tests, builds and limits](docs/WORLD_0.6.24.md).
