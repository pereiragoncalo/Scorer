# Domestic model development — 2026-10-25

This source change implements the owner's simplified fallback. It is not an APK
release or a claim that the priority national regulations have been implemented.

## Behaviour

- Europe (the existing 55-region set), Brazil, Argentina and Mexico remain the
  priority for national-format research. Existing placeholder depths there are
  retained pending verified replacements, not presented as exact regulations.
- Other World countries have two active divisions. At the season boundary the
  bottom three in division one exchange places with the top three in division
  two. There are no playoffs and no further division above/below that pair.
- Movement uses the actual tables for all six clubs, rather than exchanging only
  the hero with a low-rated club. Club objects/UIDs, country and division sizes are
  preserved; division metadata changes together. All activated fallback countries
  are processed when the career season ends.
- Standings use `P` for the three promotion places and `R` for the three relegation
  places, with an explanation in the title. The World browser, starting contracts
  and transfer offers exclude retired third/fourth divisions.
- New World careers currently contain 450 active divisions and 6,200 clubs across
  212 regions. The older 9,896-entry name catalogue is deliberately retained as a
  superset for historical identities and aliases.
- Free retains its single Scorer League and ownership restrictions.

## Existing saves

An older World career in a retired third/fourth division continues its current
season. At its season boundary the hero is moved into division two by exchanging
an existing club, keeping identity and club counts. Retired objects remain as
inactive save archives; they do not become new playable destinations.

Older World saves can include name packs for unvisited retired divisions. Preserve
those identities too, rather than rejecting or deleting aliases during loading.
`domestic_model_version` and bounded `legacy_domestic_depths` metadata make this
explicit on subsequent saves. Invalid archive metadata fails without replacing
the current career. These fields never grant World ownership.

## Language versus country

The interface remains English because that is the previously requested version's
language and its strings are written in English. A Portuguese phone locale cannot
translate those strings automatically. This change does **not** claim complete
Portuguese UI or enable a partially translated interface.

`device_locale.py` now reads Android's primary **system** locale, with API-23 and
Java-default fallbacks, instead of relying first on `Locale.getDefault()`, which
may reflect an app/runtime override. In World, `pt-PT` suggests Portugal and `pt-BR`
suggests Brazil. Free intentionally ignores locale for its starting league, and
an existing saved career keeps its country.

`language_from_locale()` prepares selection of `pt` or `en`; translated resources
and coverage of all screens/messages are still required before automatic UI
language switching can be advertised. Country suggestions, UI language and saved
nationality are separate concerns. No IP/GPS access or new permissions were added.

## Validation

The exact staged change was exported to an isolated plain directory (not a Git
worktree) for verification, excluding separate unfinished changes already in the
working checkout.

- 102 core/security tests passed, including eight new fallback/migration tests
  and six Android-locale tests with a mocked Java bridge.
- 52 actual Kivy interface tests passed, including two-division browsing and
  exactly three `P`/`R` places.
- Existing full-season fixtures, save/entitlement boundaries, editor identity,
  advertising, shot balancing and UI geometry checks remain covered by those
  suites. Syntax/whitespace checks passed.
- Logs: `/tmp/scorer-priority-reviewed-core.log` and
  `/tmp/scorer-priority-reviewed-ui.log`.

No new APK/AAB was built in this step and no real Android device locale test was
performed. Broader pending World tournament/one-way-mode work must be integrated
and separately validated before a new distributable is produced.

## Next dependency

Finish current-season primary-source retrieval for the priority countries, then
implement each verified country profile and its progression tests. See
[priority research status](regulations/PRIORITY_STATUS.md). The current fallback
must remain labelled a game design choice, never a real-country regulation.
