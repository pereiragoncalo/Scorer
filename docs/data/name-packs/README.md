## World0.9.10: current capacities and compatible JSON

- [Download complete current-layout JSON](https://github.com/pereiragoncalo/Scorer/releases/download/real-names-0.9.10/Scorer-World-Real-Names-0.9.10.json):378 club names, including26 added slots. Use for careers started with the new0.9.7+ capacities.
- [Download compatible JSON](https://github.com/pereiragoncalo/Scorer/releases/download/real-names-0.9.10/Scorer-World-Real-Names-Compatible.json):352 club names. Works in old and current layouts; additional new slots keep fictional names.

Both are uncompressed JSON attachments, covering Portugal, England, Spain,
Germany, Italy, France, Brazil and Argentina. Player reference remains July2026;
these are not current November rosters. Import through Editor > Import names.
No APK update or career reset. [Selection, limits and source evidence](REAL_NAMES_0.9.10.md) ·
[Import validation](current-validation.json) · [Public download verification](current-downloads.json).

## World 0.9.4: two divisions and ten reserves

[Download the JSON for the two-division model](https://github.com/pereiragoncalo/Scorer/releases/download/real-names-two-divisions-2026/Scorer-World-Real-Names-Two-Divisions-2026.json). Install World0.9.4 first.272 real active-club names plus80 real reserve-club names:10 per supported country,352 unique clubs total.16 active league names and2283 player aliases. The eight supported real-name countries remain Portugal, England, Spain, Germany, Italy, France, Brazil and Argentina; other game countries use the existing fictional local names.

Every country now has only two playable leagues and a FIFO reserve of10 clubs, not a simulated third division. The file preserves all active-club aliases from the prior corrected pack, and uses verified third-tier names for the initial reserve. Imported aliases follow the stable club UID as it moves between leagues and the reserve. Reimporting does not undo simulated promotions/relegations. Reference seasons and player-snapshot limitations below still apply. [Mapping](Scorer-World-Real-Names-Two-Divisions-2026.provenance.json) · [Validation](two-divisions-validation.json).

The generator now defaults to `--layout two-divisions`; use `--layout historical` only to reproduce the previous full-pyramid pack. For this new file use `--previous Scorer-World-Real-Names-Divisions-2026.json` so stale player aliases on the selected slots are reset safely. Hidden archived aliases are retained for old match history.

# Real club and player names for the Scorer World editor

## Current corrected pack

[Download the division-corrected JSON](https://github.com/pereiragoncalo/Scorer/releases/download/real-names-divisions-2026/Scorer-World-Real-Names-Divisions-2026.json). **Use this file instead of the older packs below.** Compatible with World0.9.3; no new APK.494 unique real clubs,29 league names and2633 player aliases (including892 fictional-slot resets to remove old wrong-club squad aliases);146520 bytes.

Club membership reference: **2026/27 for Portugal, England, Spain, Germany, Italy and France; 2026 for Brazil and Argentina.** Every selected name is assigned to a slot in its verified initial division, and no real team is repeated. The old generator merely cycled through reference clubs without validating their actual tier. This generator checks the explicit [division manifest](../real_divisions_2026.json), including separately identified reserve teams and similarly named clubs. All29 source page revisions and hashes are recorded; top divisions for the six European countries and Brazil were independently cross-checked against OpenFootball fixtures.

The game keeps its current division capacities: where these are smaller than the real competition, the pack represents a documented subset. Existing catalogue references are preferred within their verified tier, then source table order; clubs are never borrowed from a different tier to fill vacancies. Argentina tiers3/4 use the metropolitan branches. See the [mapping/omissions](Scorer-World-Real-Names-Divisions-2026.provenance.json).

Import over the old combined pack to replace all its club and player aliases; preview/apply, save, backup and reload were verified. It changes names only, not results, progress or already simulated promotions/relegations. The initial membership reference does not freeze teams against future in-game movement. Player source remains the July6,2026 snapshot; this correction does not claim current November squads. A slot without a sourced current-club name keeps/reverts to a fictional player, rather than retaining another real club’s old squad. [Validation](division-validation.json).

Source attribution: Wikipedia contributors, linked revisioned season pages (CC BY-SA; membership facts), OpenFootball fixture data, and the existing CC0 player dataset below.

## Older packs — historical reproduction only

The following July files did **not** validate real divisions and are superseded by the corrected pack above.


Download the **JSON file**, then open a World career and choose **Editor > Import names**, select the file, review the preview and confirm. No new APK is needed. The editor creates a names backup before updating a saved career. Keep your own career export too.

- [Europe + Brazil + Argentina JSON](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/main/docs/data/name-packs/Scorer-World-Real-Names-Europe-Brazil-Argentina-2026-07.json): all eight countries; 494 club-slot aliases and 1,898 player-slot aliases, 113,122 bytes. Use this for a single import.
- [Brazil + Argentina add-on JSON](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/main/docs/data/name-packs/Scorer-World-Real-Names-Brazil-Argentina-2026-07.json): 96 club-slot aliases and 492 player-slot aliases, 27,925 bytes. Import after the previous Europe pack to add these countries while preserving European names, including custom edits.
- [Europe JSON](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/main/docs/data/name-packs/Scorer-World-Real-Names-Europe-2026-07.json): Portugal, England, Spain, Germany, Italy and France; 398 club-slot aliases and 1,406 player-slot aliases, 85,269 bytes.
- [Portugal-only JSON](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/main/docs/data/name-packs/Scorer-World-Real-Names-Portugal-2026-07.json): 72 club-slot aliases and 323 player-slot aliases, 18,431 bytes. The Europe file already includes these names.

All four files use the existing version-1 editor format and fit its 256 KiB / 4,096-name limits. Import the JSON without `.provenance` in its filename. The provenance and validation files are documentation, not editor packs.

## Scope and reference date

The player's public source is **dcaribou/transfermarkt-datasets**, whose current README states that updates stopped in July 2026, with data current to **6 July 2026**. These are a downloaded reference snapshot, not a claim of verified November 2026 transfers or complete 2026/27 squads. Rows with `last_season` before 2025 are excluded. Club names come from the real references already recorded by Scorer's OpenFootball-based catalogue.

The pack changes display aliases only. It does not change the game's existing league memberships, club slots, rules, results, abilities or match simulation into real-world competition data. Some reference clubs are historical or occur in several game slots. Repeated real club references receive the same sourced names. Counts above describe alias slots, not unique real teams or people.

The editor supports 12 names per club. Eligible outfield players are selected by position (attackers, midfielders, defenders), then source market value and stable player ID. Market values and IDs are not included in the import file; this ordering only selects recognisable names for the available slots. No keeper is substituted into a scorer slot. Clubs are matched by exact normalised names within their country's source competition, plus an explicit reviewed alias table. No fuzzy city matching or invented player assignment is used. Missing/partial squad matches keep the remaining existing player names. See the corresponding provenance file for every mapping and gap.

## Sources and reproducibility

- [Transfermarkt dataset repository and update status](https://github.com/dcaribou/transfermarkt-datasets)
- [players.csv.gz](https://pub-e682421888d945d684bcae8890b0ec20.r2.dev/data/players.csv.gz)
- [clubs.csv.gz](https://pub-e682421888d945d684bcae8890b0ec20.r2.dev/data/clubs.csv.gz)
- [Dataset's CC0 licence](TRANSFERMARKT-DATASETS-CC0.txt)
- Game club references: `docs/data/world_club_provenance.json`, OpenFootball source revisions recorded there.

Downloaded on 1 November 2026. Exact compressed input hashes and per-club source matches are recorded in the `.provenance.json` files. The pack includes names only, without photos, logos, dates of birth, contact information, source profiles or executable content.

Rebuild with `tools/build_real_name_pack.py --players PATH/players.csv.gz --clubs PATH/clubs.csv.gz --output OUTPUT.json`; add `--countries Portugal` for the small pack. The generator does not download data or touch a career.

Validation used clean Scorer World 0.6.47 source `19c13b10d51e9dc49f4bbd70f34f66b82cb50ffc`: actual editor preview, apply, save, automatic backup and reload passed for all four files. Only `career.display_aliases` changed in the saved game; simulation and progress were preserved. See [validation.json](validation.json).

The Brazil/Argentina add-on was also applied after the original Europe pack: its merged aliases equal the combined file, and importing it preserves custom European names. Country-specific source matching uses BRA1 (Brazil) and ARG1 (Argentina); Botafogo RJ is not confused with Botafogo SP. The reference date and missing-player limitations above also apply to these countries.
