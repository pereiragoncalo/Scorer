# Real names for Scorer World 0.9.10

Two uncompressed, UTF-8 editor JSON files are available. No APK update is needed.
Both cover Portugal, England, Spain, Germany, Italy, France, Brazil and Argentina.
They rename displays only; they do not move clubs, change results or reset saves.

## Choose the file for your career

- **Scorer-World-Real-Names-0.9.10.json**:378 club aliases, including298 active
  slots and80 reserve slots;16 league aliases and2403 player aliases. Use for a
  career started with the new capacities introduced in0.9.7 or later.
- **Scorer-World-Real-Names-Compatible.json**:352 club aliases,16 league aliases
  and2283 player aliases. Imports in both older and current career layouts;
  additional clubs introduced in new careers keep their fictional names.

An installed APK version does not identify the saved career layout. Old careers
retain their original capacities when upgrading. The complete file uses26
additional club UIDs that do not exist in that older model, so the editor correctly
rejects it there. Use the compatible file if continuing such a career.

Download the JSON attachment, open **Editor > Import names**, select it, review
the preview and confirm. The app makes a private names backup. Import does not
undo simulated promotions/relegations: aliases follow stable club identities.

## Reference and limitations

Initial division membership follows the reviewed Europe2026–27 and Brazil/
Argentina2026 registry retrieved2 November2026. Existing352 UID assignments and
all their player aliases are preserved. Only26 newly available current slots are
filled, using unused verified clubs from the same real division. There are no
guessed clubs, duplicates, cross-tier substitutions or canonical-ID changes.
Argentina's game capacities still represent a subset of the real competitions.
The reserve retains ten names per supported country.

Player source remains the6 July2026 CC0 snapshot used by the preceding packs;
this is not a November transfer/squad update. The complete file includes1858
sourced real player-slot names plus the preceding pack's fictional reset aliases.
Where no exact unique source squad exists, unsourced new player slots remain
fictional. This is a12-slot scorer-name mapping, not full licensed team rosters.
Other countries retain their existing fictional names.

Membership sources/attribution and per-slot player evidence are retained in the
[provenance](Scorer-World-Real-Names-0.9.10.provenance.json). Existing dataset
attribution is in TRANSFERMARKT-DATASETS-CC0.txt. Build offline with:

```
python3 -m tools.build_current_name_pack --players PATH/players.csv.gz --clubs PATH/clubs.csv.gz --output docs/data/name-packs/Scorer-World-Real-Names-0.9.10.json --compatible-output docs/data/name-packs/Scorer-World-Real-Names-Compatible.json
```

## Verification

Validation covers complete supported current/reserve slots, source-division
membership, real-identity uniqueness, preserved previous aliases, bounded editor
schema, legacy compatibility, atomic backup, apply/reload with career progress
and competitions unchanged, sourced new player slots and generation independent
of league/reserve shuffle order. File hashes/bytes and public download checks are
recorded separately. No physical Android import or new APK build is claimed.
