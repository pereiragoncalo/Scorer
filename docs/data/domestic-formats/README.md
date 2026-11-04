# Real domestic format catalogue

This research catalogue defines first/second-tier structures independently of the released game's compact league capacities. It is not loaded by the application. All game countries have explicit review slots; unknown slots have no invented team count, phases or promotion quota.

- `source-index.json`: revision-pinned secondary source identities, content hashes and current-identity exclusions. A candidate is not an approved format. The BBC Wales report adds independent contemporary evidence.
- `reviewed.json`: reviewed structures, season, phases, access rules where evidenced, unresolved clauses and the sourced Liechtenstein exception. A tier may contain several regional competitions (for example Cymru North/South).
- `catalogue.json`: deterministic generated country/tier index. `structure_reviewed` means the regular structure has been reviewed, not that all tie-breakers, licensing clauses or cross-tier access rules are complete. `partially_defined` keeps contradictory or incomplete structures open.
- `../../regulations/DOMESTIC_FORMAT_DEFINITIONS.md`: generated coverage report and outstanding division slots.

Rebuild with `python3 tools/build_domestic_format_catalogue.py`; check reproducibility with `--check`. Run `python3 -m unittest discover -s tests -p test_domestic_format_catalogue.py`.

Each definition cites source IDs, gives an explicit season and records unresolved rules. Wikipedia references point to exact revisions rather than a mutable current page; the hashes identify the researched wikitext, not rendered HTML. No full third-party article is bundled. General league articles can establish a stable regular structure; they cannot settle a contradictory current-season regulation. Excluded historical or women's competitions remain in the evidence index so that exclusions can be audited.

Round-robin phases record group sizes, legs, point carry and regular match counts. Split phases partition finishing ranks exactly once. Knockouts conserve entrants and explicit byes; unknown tie decisions stay `unresolved`. External playoffs describe cross-tier entrants or condition-dependent stages without guessing an unsupported bracket. Regular-game totals exclude knockout and cross-tier matches. Apertura/Clausura titles and annual aggregate tables must remain separate; three-year relegation averages must not become annual-table positions.

## Review limits and next integration work

All records remain `not_integrated`; all country implementation flags remain false. Exact ranking/tie procedures, professional licences, B-team exclusions, promotion eligibility, averaging denominators and lower-tier replacements require their recorded further review. In particular Bulgaria's14-club2026/27 field conflicts with the older16-club generic format; no guessed split is supplied. England's six-club Championship playoff announcement requires later2026 detailed rules. Argentina's full reduced-tournament seeding is still open.

Northern Ireland's current official Championship PDF and announcement returned HTTP403 during this review:

- https://www.nifootballleague.com/media/21084/nifl-championship-rules-2026-27.pdf
- https://www.nifootballleague.com/news/2026/may/championship-format-confirmed-for-202627-season/

Their contents are not claimed as independently verified. Current secondary references support the16-club30+7 schedule; detailed access/tie clauses remain unresolved. The Wales35/33/35 split is also checked against the BBC report included in the source index.

Runtime integration needs variable team capacities, phase/group-specific tables and fixture generation, persistent phase transitions, rolling relegation averages, cross-tier eligibility and save/UID migration. Existing compact0.9.6 access profiles must not be labelled as these complete real formats. No APK/version change accompanies this research-only catalogue.

## Extended phase models (4 November2026)

`qualified_round_robin` records matches played by a subset of clubs, with explicit participant count and selection. Those matches must not inflate the universal season total for eliminated clubs. Bonus points are explicit in Peru’s championship phase. `scheduled_league` records sourced fixed match counts for unbalanced/conference schedules; it is not converted into a full round robin by arithmetic. MLS best-of-three rounds use individual match wins (two required, up to three games), with no aggregate score.

`bracket_graph` supports winner/loser paths such as Peru’s separate title, repechage and second-promotion playoff. Inputs must refer to seeds or earlier matches. Exhaustive tests of all32 outcome paths verify that the four-club Peruvian graph produces two distinct promoted clubs. Exact unconfirmed semifinal seed allocation remains open before scheduling.

`pending_review` is explicitly not a confirmed playoff. Half-point rounding can remain unresolved only in a partial definition. `no_competition_at_tier` records sourced absence of a separate senior second tier (Gibraltar, San Marino); it must not manufacture under23 competitions as Division2. Country-level absence remains separately recorded for Liechtenstein.

The catalogue includes explicitly dated older-season structures where those are the last sufficient references; their unresolved list requires current-season confirmation. Counts of records/countries never mean that all current regulations or runtime integrations are complete. A blank result-grid template is not proof that every possible home/away pair will be played.

Additional primary evidence retrieved: the CPL31March2026 announcement confirms four playoff clubs, two-legged semifinals1v4/2v3 and a single-match final at the higher seed. FRMF2025 competition regulations confirm the16-club maximum per professional division and delegate playoff details to a seasonal circular (article15). The secondary ranking citation to article53.2 does not match the retrieved primary PDF’s article53; it remains flagged rather than treated as verified.
