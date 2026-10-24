# SCORER 0.6.27 — World aim, morale opportunities and club presentation

## Behaviour

World match aim now increases at each modelled promotion: tier5 1.55, tier4 1.90,
tier3 2.30, tier2 2.75, tier1 3.25 (base phase speed). International World is 3.65.
Existing cup/hard multipliers and physical shooting remain; Free aim is unchanged.

Both modes apply strict morale floors: **>10 gives at least2 chances; >15 at least3**.
At exactly10 the training floor applies; exactly15 still guarantees2. Current maximum
remains3. Floors override opponent quantity caps, while elite opponents still allow
no clear chance and all shots remain physically simulated. Expected interactive goals
are still reserved from the team budget before sampling teammate goals; no goals
are forced or rival scorer totals inflated. Mandatory weekly training still gates Play.

Free keeps its fictional names/generic kits and one fixed new-career league. World
gets a World-only offline presentation overlay: real city names, locally appropriate
prefixes/suffixes, and reference palettes where known. Original canonical names and
club UIDs are untouched; tables, fixtures, scorer identities and saved progress keep
their keys. Explicit user aliases win over new defaults. Country-scoped replacement
prevents same-name clubs in other countries receiving another team's alias. Promotion
keeps the same presentation/colour identity via UID. Legacy explicit canonical edits
are not overwritten. Missing/corrupt local presentation data falls back to old names.

The editor now has **JSON FORMAT**, showing a compact valid example for the selected
club/league/player role. It explains Export > edit right-hand values > Import > preview
> Apply, UTF-8, fixed IDs, limits and partial packs. It is read-only and does not open
a keyboard. [Player instructions](NAME_PACK_FORMAT.md). Existing validation, private
backup, preview/confirmation and atomic rollback remain unchanged.

## Reference coverage and limits

The overlay covers **9,896 game club IDs / 212 football regions**. Source club/city
records cover **91 regions / 4,160 game entries** (references can be reused to fill
fictional tiers). Other clubs use actual geographic cities and local naming forms;
**193 regions** have multiple city candidates. This is a fictional football model,
not a certified current-season real club roster or complete real regional pyramid.

**92 entries** have a known representative reference palette; other kits remain
generic. These are plain club colours, not reproduced official shirts/crests or a
claim to current-season kit accuracy. Existing away-colour clash handling remains.
No official club images, names pack, external assets, scripts or runtime downloads
were added. Raw source-reference names are recorded only in excluded documentation,
not the shipped presentation catalogue or exported default name pack.

Build sources pinned in assets/data/world_clubs.json and the unshipped
[reference provenance](data/world_club_provenance.json):
- openfootball/clubs, CC0: club/city reference data.
- annexare/Countries, MIT: country metadata/capital fallback.
- datasets/world-cities, GeoNames CC BY4.0: geographic city candidates.
- jokecamp/FootballData: historical EPL colour facts; explicit representative colour
  supplements for the existing top-club reference groups. Brand colours are not
  presented as licensed current kit artwork.

Data licences/attribution are bundled; Privacy credits the geographic sources and
modifications. Country labels from the geographic CSV are only offline join keys;
the game's pre-existing country identifiers remain authoritative.

Rebuild metadata with the four pinned checkouts:

```sh
python tools/build_world_clubs.py --clubs PATH_OPENFOOTBALL --countries PATH_ANNEXARE --football-data PATH_FOOTBALLDATA --cities PATH_WORLD_CITIES
```

The tool reads passive text/CSV/JSON only. It does not execute reference code. A
mistyped initial repository name returned not-found; used openfootball/clubs. A
country without a capital field (Macau) required the explicit Macao city fallback.
Removed hierarchical county suffixes from source city fields and included Monaco
club references in France. Broader GeoNames cities avoid assigning every fallback
club to a capital. Existing IDs/default canonical names were never regenerated.

## Builds and checks

- **88 core/security tests PASS**, 12.736s; **51 actual Kivy tests PASS**, 49.549s:
  **139 total**. New checks include strict morale boundaries/elite floors, actual
  World match aim integration, unchanged Free presentation/aim, all9896 stable IDs,
  unique country names/city containment, promotion/alias/colour persistence, corrupt
  asset fallback, valid read-only JSON guide and source-safe same-app QA staging.
- Older tests asserting elite maximum1 at morale20 were adjusted to test the opponent
  cap at morale10, with separate tests proving the new floor overrides. World alias
  tests now compare the actual default presentation rather than canonical engine keys.
- Python syntax, shell syntax, git diff checks and public rehearsal config PASS.
- Actual Free APK and same-app World QA APK compiled, target36/min26 ARM64,
  versionCode1026627. Both keep com.clemir.striker and the existing DEBUG certificate.
  apksigner/zipalign16KiB and all118 ELF LOAD alignments pass for each APK.
- Actual private archives contain the World module, all9896 presentation rows and
  licences; no saved careers, server code/keys or raw provenance file. Play staging
  explicitly allows this one public JSON asset while continuing to exclude other
  JSON/config/key files. Actual compiled BillingConfig confirms ENABLED=false.
- Desktop GL captures of the editor and JSON guide inspected at1280x589/density1.64;
  the four actions and six-line JSON example fit. An initial manual-clock capture
  read an undrawn framebuffer; recaptured using the actual Kivy event loop. These
  are desktop captures, not Android screenshots or device validation.

Logs: /tmp/scorer-0627-core-final.log, /tmp/scorer-0627-ui-final.log and
/workspace/striker-runtime/{build,verify}-0.6.27-{free,world-qa}.log.

## One-app QA, not paid ownership

The repository and normal Free build keep WORLD_PREVIEW=false. A separate generated
**test binary**, prepared with tools/prepare_world_qa.py, enables the deliberate test
entitlement so the owner can test Free and World in the **same installation/package**.
It does not create a second paid app, claim a verified purchase or enable Billing.
It replaces the previous debug beta; the Free save stays Free, World uses its own slot.
Return to Free with the entry-menu FREE button or MODES. No auto-copy or cross-slot load.

Production/rehearsal candidates must keep the test entitlement false and pass the
production gate. This QA must never be submitted as a paid/ownership-verified release.
No Google Play upload, real payment, ad revenue activation or production signing.
No new AAB produced in this revision. Physical-device feel, import/export and live
Play testing still pending. Next: owner checks the World progression/aim and name
editor on the phone; extend reference/colour coverage without re-keying identities.
