# Scorer World0.9.30 — continental competitions

Four playable club competitions have been added: CONMEBOL Sudamericana,
CAF Confederation Cup, AFC Champions League Two and AFC Challenge League.
Together with the existing principal cups, twelve club competitions cover all
six confederations. Qualification fields are disjoint at the initial draw.
Sudamericana has eight group winners entering the last16 and eight runners-up
playing the eight Libertadores group thirds over two legs. Transfer and waiting
states persist without duplicate draws. CAF's secondary final has two legs;
AFC Two/Challenge keep West/East apart until their single final.

Competitions now permanently shows the next edition of FIFA World Cup, European
Championship, Copa America, Africa Cup of Nations, AFC Asian Cup, Concacaf Gold
Cup and OFC Nations Cup. Active editions open their qualifying or finals draw.
All seven finals complete in a four-year engine cycle; the World Cup has48 teams
and104 finals fixtures. Copa America's modeled field reserves10 South American
and6 Concacaf places. Existing top-three first-division call-up criteria, separate
international goals/caps, post-match news, training gate and observed trophy
awards are retained. Same-week national fixtures now sort by actual date before
lexical fixture IDs, fixing a backwards June2028 Copa sequence.

Old books acquire only missing cups and simulate elapsed rounds without personal
credit. Existing scores/draws, club UIDs, edited names and old qualification
snapshots remain valid. New secondary fields survive qualification snapshots,
export/reload and next-season draws. No shot physics, sprites, controls, public
server, monetization or production1.0 change. Existing unrelated WIP is excluded.

Validation:395 core discovery cases completed,3 skipped; all202 native Kivy
cases passed. After the date correction, all7 expansion/date regression cases
and15 competition cases passed. The three-season controlled-score lifecycle
completed218 matches with13 reloads,3 archived seasons, no repeated fixture and
nondecreasing dates. A separate secondary-cup test plays through and wins the
Sudamericana without automatic simulation of protected personal fixtures.
The initial fixture-count assertion was corrected to141 (including playoffs).
The first Android verification exhausted temporary disk; obsolete generated
staging copies were removed. Rechecking the identical APK passed: signature,
ZIP16KB, all118 ELF files, exact compiled rendering/runtime source,208 sprite
frames/30 sheets, edition/ad-free/safety and actual compiled competition/career
checks, including secondary snapshot reload and Libertadores transfers.

World DEBUG QA upgrade, same package and existing debug upgrade certificate,
versionCode1026930, API36/min26, arm64. Physical Android installation/playtest
remains pending; this is not a Play submission or production1.0.

Scope: access allocations, some phase baselines and match dates remain game
models. This is not a certification of current2026/27 regulations. Regional
Concacaf feeder cups and the OFC professional league are outside this iteration;
no fictional Europa equivalent is created for those confederations. See
[format details](WORLD_COMPETITIONS_0.9.md).

[Download APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.30/Scorer-World-0.9.30.apk).
