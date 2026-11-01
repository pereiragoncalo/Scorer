# World competitions — 0.9 acceptance candidate

Point 1 is implemented as an executable, persistent game model. Tournaments now draw actual fixtures, build tables from scores, qualify teams, resolve knockout ties and archive winners. No World title is assigned by selecting a domestic leader or country as a label. The existing Kivy game, physical difficulty, career identity, local editor and online safety flows are retained.

## Formats in the game

| Competition | League/groups | Progression |
| --- | --- | --- |
| UEFA Champions League / Europa League | 36 clubs, 8 unique opponents, 4 home + 4 away | Top 8 direct; 9–24 play two-leg playoffs; round of 16 onward; single final |
| UEFA Conference League | 36 clubs, 6 unique opponents, 3 home + 3 away | Same ranked qualification and knockout structure |
| CONMEBOL Libertadores | 32 clubs, 8 groups of 4, home and away | Two qualify per group; two-leg ties; single final |
| CAF Champions League | 16 clubs, 4 groups of 4, home and away | Two qualify per group; two-leg quarterfinals, semifinals and final |
| Concacaf Champions Cup | 27 clubs; five first-round byes | Remaining 22 play two-leg ties, then a 16-team bracket; single final |
| AFC Champions League Elite | 24 clubs, separate West/East leagues, eight matches each | Eight from each region; regional two-leg last 16, then single-match final eight |
| OFC Champions League | 8 clubs, two groups | Top two, single-match semifinals and final |
| World Cup | Regional qualification games; 48 finalists in 12 groups | Top two plus eight best thirds; last 32, third-place match and final: 104 finals fixtures |
| European Championship / AFCON / Asian Cup | Qualification games, 24 finalists, six groups | Top two plus four best thirds; last 16 onward |
| Copa America / Gold Cup | Qualification games, 16 finalists, four groups | Top two; quarterfinals onward |
| OFC Nations Cup | Qualification games, eight finalists, two groups | Top two; semifinals and final |
| UEFA Nations League | Four game leagues, A/B/C/D; 16/16/16/7 nations, home/away groups | Group winners play finals; ranked group results move nations between game leagues next season |
| National cups | All eligible club identities in that country's game pyramid | Real knockout brackets with byes where needed; single-match ties |

These are the **published game formats**, not a certification of current official access lists, draw pots, country regulations or exact real-world dates. Regional/amateur football outside the game's available tiers is not represented. Initial continental entrants are seeded because an existing completed season is unavailable; subsequent entrants use completed league tables, with European cup-winner/title-holder priorities. National finalists earn places through simulated or player-participated qualification fixtures, including ranked extra places in the World Cup model.

## Promotion and relegation

Every available adjacent division exchanges the same number of clubs. All tables are captured before movement: a club cannot jump two divisions, duplicate its identity or disappear. Generic priority-country boundaries use two automatic promotion places plus a four-team playoff (third–sixth) for the third place, matched by three relegations. England uses three automatic plus one playoff winner from League Two, and one automatic plus a seeded six-team playoff from its fifth tier. The owner's simplified two-division countries retain three direct promotions/relegations and no playoffs. There is no movement beyond the available pyramid.

Playoffs have fixtures, aggregate scores and penalties where needed; the player participates when their club qualifies. Standings colours and the full rules key use the same promotion rules as the season engine. The previous independent random playoff-promotion check and rating-selected replacement are removed from the World path.

## Calendar and personal matches

Club, domestic and international games use one persistent schedule. The player inherits only their current club's remaining competitions; earlier games at a transferred-to club are simulated without adding personal goals or appearances. National participation uses the player's selected nationality, with correct home/away scoreboard attribution. National caps/goals stay separate from club-season counters and league scorer tables.

World cup matches occupy separate days within the game week instead of consuming extra league weeks. Domestic, continental and national fixtures are ordered before the week's league match, avoiding overlapping personal entries and dates running backwards at the season boundary. The last league match does not discard unfinished cups, international games or player playoffs. Those finish before results are archived, the next field is qualified and league membership is changed.

## Save, migration and recovery

The book stores draws, fixture IDs, scores, penalties, active rounds, tables, qualification paths and champions. Reopening cannot redraw a completed tie or award the same personal game twice. Run-in saves include final league tables so qualification and promotion are unchanged after a mid-playoff reload; subsequent seasons use compact global club memberships. Existing club/player IDs and name-pack aliases are retained.

Old saves acquire an elapsed external competition history without adding personal caps/goals. Existing legacy cup history remains recorded; any remaining legacy cup field is continued under the new bracket. Malformed competition state, unknown identities, duplicate fixtures, invalid scores and corrupted archives fail validation before replacing the live career. Normal career export/import carries the new optional state and retains its 8 MiB limit and backup behaviour.

## Verification and next work

Core checks cover league schedules, balanced home/away Swiss rounds, byes, aggregate ties, penalties, qualifiers, the 104-match World Cup, identity-preserving movement, future qualification, migration, duplicate result rejection, away nationality attribution, save/export/import and mid-playoff recovery. Native Kivy checks cover competition browsing, fixture pages, groups, standings, back navigation, nine languages and small phone-sized layouts. Actual APK bytecode is inspected and exercised on the build host.

`tools/check_world_seasons.py` runs three seasons with controlled player-team scores, checking repeated fixtures, nondecreasing dates, qualification, archives and repeated reloads. Controlled engine outcomes are not a human difficulty measurement. The point-1 implementation is complete for these game formats. Physical Android acceptance, actual server/policy deployment and production Play signing/Console work remain points 2–4 in [the launch checklist](play/ROAD_TO_1.0.md).
