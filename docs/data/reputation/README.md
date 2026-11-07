# Status inputs and unfinished factual coverage

Official FIFA men's national ranking snapshot:20July2026, queried from the public
FIFA rankings API. Official UEFA association coefficient:five seasons2022–2026,
updated3July2026. Exact URLs/hashes are included in assets/data/league_status.json.
FIFA ranks national teams, not domestic leagues. UEFA ranks associations. Neither
is an official worldwide division ranking. The five league-status bands and72%
second-division scaling are explicit game adaptations. Northern Mariana Islands
has an explicit unranked game fallback, not a fabricated FIFA position.

Club presets use football-data.co.uk completed results over2021/22–2025/26 in
split-year countries and2021–2025 in calendar-year countries.175 country/tier/year
requests are recorded in coverage.json. Some feeds do not cover all those seasons.
The source matches use exact normalised club names and a reviewed abbreviation
map within each country; no fuzzy matching. Game UIDs and existing aliases remain
unchanged. Source points, matches, goals and reconstructed positions are retained.

**This is not complete official final-table verification.** Disciplinary points
adjustments, head-to-head tie-break rules and some multiple-phase final orders
are not applied.499 game identities have matched results;301 have five seasons.
These identity counts can include repeated legacy references, not unique clubs.
The3687 other referenced identities have no matched table in this source set;
additional fictional identities have no real-world history. They retain an
explicit country-scaled deterministic game baseline. No invented historical
seasons or official positions are attached to them. Source reconstruction and
unmapped gaps must be checked before claiming the owner's complete five-year
official-classification request is finished.

Rebuild: `python3 tools/reputation/build_status.py`. Official ranking snapshots
are checked in here. Result CSVs download to a temporary cache; set
SCORER_REPUTATION_CACHE to select another cache. Public results are factual
inputs; betting-odds columns are not retained in the game data.
