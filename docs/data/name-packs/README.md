# Real club and player names for the Scorer World editor

Download the **JSON file**, then open a World career and choose **Editor > Import names**, select the file, review the preview and confirm. No new APK is needed. The editor creates a names backup before updating a saved career. Keep your own career export too.

- [Europe JSON](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/main/docs/data/name-packs/Scorer-World-Real-Names-Europe-2026-07.json): Portugal, England, Spain, Germany, Italy and France; 398 club-slot aliases and 1,406 player-slot aliases, 85,269 bytes.
- [Portugal-only JSON](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/main/docs/data/name-packs/Scorer-World-Real-Names-Portugal-2026-07.json): 72 club-slot aliases and 323 player-slot aliases, 18,431 bytes. The Europe file already includes these names.

Both files use the existing version-1 editor format and fit its 256 KiB / 4,096-name limits. Import the JSON without `.provenance` in its filename. The provenance and validation files are documentation, not editor packs.

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

Validation used clean Scorer World 0.6.47 source `19c13b10d51e9dc49f4bbd70f34f66b82cb50ffc`: actual editor preview, apply, save, automatic backup and reload passed for both files. Only `career.display_aliases` changed in the saved game; simulation and progress were preserved. See [validation.json](validation.json).
