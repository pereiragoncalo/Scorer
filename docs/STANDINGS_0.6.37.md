# Scorer World 0.6.37 — standings eligibility zones

Owner requested who goes up/down and whether playoffs exist in World standings.
Previously only the owner's simplified two-tier fallback had P/R suffixes. Now
all active World leagues use an immutable, read-only eligibility model in
 domestic_rules.table_zones. Own standings and the World browser both show P,
PO and R next to positions, with green/amber/red backgrounds and position text.
The hero's independent highlight is neutral blue/white outside zones, avoiding
confusion with promotion. Paging and the stats toggle retain row-zone meaning.

The Rules bar gives exact current place ranges; '-' means none, '*' identifies
the simulated playoff. Tap it for full translations and no-up/no-down/no-playoff
statements. A bounded modal keeps Back outside the potentially scrollable text;
the table itself never scrolls vertically or horizontally. A redundant in-table
league title is omitted (the screen header retains it). Compact/narrow controls
wrap where needed and preserve48dp touch targets, with pagination based on actual
remaining height. Colour is supplemented by text codes/ranges.

## Exact scope and limitations

These are CURRENT GAME eligibility rules, not a completed national-regulation
implementation. No season resolver, fixture, migration, club ID or save schema
was changed. Priority Europe/Brazil/Argentina/Mexico still use the existing
provisional career model:3 direct promotion places,4–7 simulated promotion
playoff eligibility,2 relegation places, each requiring an available adjacent
division. The existing resolver samples a35% promotion outcome for the hero in
playoff places; this is NOT a newly implemented knockout competition. Broader
NPC movement and exact country-specific formats remain unfinished. The rules
modal explicitly states simulated outcomes/no playoff matches and pending
country-specific regulations. Do not claim this completes those earlier requests.

Owner-selected fallback countries keep exactly2 active divisions:3 up from tier2,
3 down from tier1, no playoffs. Highest tier cannot promote; lowest active tier
cannot relegate. Compatibility archives show their special move to tier2 instead
of ordinary movement zones. Codes show current places, not mathematically clinched
final-season outcomes. Original standing_zone/exchange_three remain compatible.

## Validation and files

125 core/security +75 actual Kivy tests PASS (200); four focused final UI tests
also pass after neutral hero-colour refinement. Core cases cover pyramid limits,
fallback, archive, count/range/disjointness, no mutation of active tiers. UI cases
cover Portugal tiers1/2/4, fallback both tiers/no playoffs, paging/stats, colours,
read-only RNG/save/league state, Free isolation, responsive layouts and rules Back
at1280x640,640x360,360x640 density1.6. Existing movement/save/locale tests pass.
An initial narrow control was just below48dp; explicit grid column minima fixed
it before the final checks. Earlier green hero highlighting was corrected to
avoid semantic conflict with promotion zones.

Files: domestic_rules.py, menu_ui.py; nine catalogues (229 messages each);
 tests/test_standing_zones.py, ui_tests/test_standing_zones.py, updated existing
fallback UI assertion; buildozer.spec/tools/prepare_editions.py0.6.37/code1026637;
docs. Free has no new zones/rules control; latest Free APK remains0.6.35. Source
profile version is staged for future Free builds, not a newly built Free artifact.

Actual World arm64 debug build passed package/version/launcher/icon/signature,
bundled UI/TableZones/Portuguese rule messages/neutral hero colour, existing
wordmark PNG/font/language/SDK, ZIP16KB and118 ELF alignment checks. Exact hashes
in STANDINGS_0.6.37_artifact.json. No real device, release signing, Play upload,
payments, ad activation or certified regulation implementation is claimed.

[Desktop promotion/playoff view](captures/zones-up-0637.png),
[relegation places](captures/zones-down-0637.png),
[full rule key](captures/zones-rules-0637.png) are actual Kivy renders, not Android
screenshots. Logs: /workspace/striker-runtime/zones-core-final.log,
zones-ui-final.log, zones-ui-focused-final.log, build-0637-world-final.log.
Separate unfinished World competition WIP was preserved outside the APK snapshot.

Next: install World over0.6.36, check your league's markers, open Rules, page to the
bottom/stats and confirm saved career data remains intact on a phone. Accurate
national competition/knockout implementations remain a separate pending stage.

Integration check: the merged checkout with preserved unrelated World WIP also
passes125 core/security and75 Kivy tests (200). No physical phone run claimed.
