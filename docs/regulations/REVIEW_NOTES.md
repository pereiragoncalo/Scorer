# Reviewed competition provisions

Read on 2026-10-24. Source IDs resolve to URLs/checksums in
[source_catalogue.json](source_catalogue.json). These are partial research notes,
not claims of completed game implementation. Later amendments must be checked.

## Portugal: professional divisions, 2026/27

Source: `portugal-competition-2026-27`; articles 21, 22, 25, 26 and 31.

- Both professional divisions have 18 teams.
- Liga 2's top two eligible clubs are promoted directly; Liga 1's bottom two
  clubs are relegated directly.
- Liga 1's 16th faces the next eligible Liga 2 club outside the direct promotion
  places, excluding B teams, in a two-leg playoff. Venue order is drawn.
- The playoff uses aggregate goals, then 30 minutes of extra time in the second
  leg and penalties if necessary. Article 31 does not prescribe away goals.
- Liga 2 also relegates its bottom two directly and its 16th contests a playoff
  against the Liga 3 representative indicated by the FPF. Liga 3 supplies two
  direct promotions, subject to eligibility.

Pending: FPF Liga 3/Championship of Portugal group structures, licensing/B-team
exceptions, complete tiebreakers, cup formats, dates and continental access.

## United States/Canada: MLS, 2026

Source: `usa-mls`; sections **Conferences**, **MLS Regular Season** and
**Audi 2026 MLS Cup Playoffs**. The source explicitly identifies the 2026 season.

- 30 clubs, two conferences of 15. Each club has 34 regular-season matches:
  28 against conference opponents, plus six different cross-conference opponents;
  17 home and 17 away. Points: win 3, draw 1, loss 0.
- Conference places 1–7 enter Round One directly; 8–9 contest a single Wild Card
  match hosted by the higher seed. A tied Wild Card goes straight to penalties.
- Round One is best of three, first to two wins. Higher seed hosts games 1 and,
  if needed, 3; lower seed hosts game 2. Drawn games go straight to penalties.
- Round One pairings per conference: 1 vs Wild Card winner; 2 vs 7; 3 vs 6;
  4 vs 5. This is a series of match wins, not an aggregate-goals two-leg tie.
- Conference semifinals and finals are single matches hosted by the higher seed;
  drawn matches use extra time then penalties. The bracket is specified by the
  competition guide and must not be replaced by an arbitrary redraw.
- MLS Cup is a single match hosted by the finalist highest in the Supporters'
  Shield standings; extra time and penalties apply if needed.
- After points, tiebreakers are wins, goal difference, goals scored, head-to-head
  points then head-to-head goal difference within the same conference, fewest
  disciplinary points, away goal difference, away goals, home goal difference,
  home goals, then coin toss/drawing lots. Reapply the source's tie procedure to
  clubs still tied. Points-per-game contingency applies to cancelled schedules.

Pending: full disciplinary/roster implementation, continental qualification and
the separate domestic pyramids of the US and Canada. MLS evidence alone does not
verify either country's complete model.

## Oceania: OFC Men's Champions League, 2026

Source: `ofc-champions-2026`; articles 14.2, 16 and 17.

- Championship stage: eight clubs, two groups of four, single round robin within
  each group (three matches per club), points 3/1/0.
- Top two in each group advance. Semifinals cross A1–B2 and B1–A2; semifinal
  winners play the final. Knockout matches use extra time then penalties.
- Group ranking starts with all-group points, goal difference and goals scored,
  then the corresponding head-to-head criteria, conduct score, then coin toss or
  OFC drawing of lots. The conduct weights are explicitly prescribed in 16.3.4.
- Matches are 90 minutes; extra time is two 15-minute periods.

Pending: qualifying stage, allocation/club eligibility, draw restrictions and
edition-specific withdrawals. Do not confuse this tournament with the new OFC
Professional League below.

## Oceania: OFC Professional League, 2026

Source: `ofc-pro-competition`; article 8, particularly 8.4–8.9.

- Eight clubs; initial double round robin of 14 matches per club, delivered over
  five circuit-series rounds.
- Split into Leaders (initial places 1–4) and Challengers (5–8), each playing a
  single round robin of three matches per club. **Points reset to zero.**
- Leaders' top three enter the semifinals. Leaders' fourth plays Challengers'
  first in a single semifinal playoff; extra time and penalties apply.
- Semifinals: Leaders' first vs playoff winner; Leaders' second vs third.
  Single-match semifinals and final use extra time and penalties if needed.

Pending: complete tiebreakers, licensing eligibility, circuit venues/dates and
continental representation. The separate `ofc-pro-licensing-2026` PDF is retained
but not yet reviewed. This is a regional professional competition, not a national
promotion/relegation division.

## Africa Cup of Nations: adopted 18 November 2023

Source: `caf-afcon`; articles 73–75 and adoption article 121.

- Finals: 24 teams in six groups of four; points 3/1/0.
- Each group's top two plus the four best third-placed teams qualify for the
  round of 16 (75.3). The knockout bracket must account for the qualifying
  third-place combination, using the mapping in 75.6.
- Article 74 distinguishes two-team from multi-team ties. Head-to-head criteria
  precede overall goal difference/goals, with explicit reapplication for clubs
  still tied and eventual drawing of lots.

Pending: edition-specific amendments, qualifiers, full best-third-place matrix,
calendar and player eligibility. The 2023 adoption date is not proof that every
clause remains unchanged for all subsequent tournaments.

## CAF club tournaments: historical document warning

Sources: `caf-champions` and `caf-confederation`. Both documents' adoption clauses
identify 17 July 2019, despite their being linked from the current CAF portal.

The Champions League PDF describes four groups of four, quarterfinals with group
winners against runners-up from other groups, and two-leg quarterfinals and
semifinals. It also retains away-goals rules and a single-match final (III.28).
These clauses require checking against subsequent amendments and season-specific
rules. They must not silently override a current-season two-leg final model.

## UEFA: 2026/27 official season calendars

Sources: `uefa-champions-format-2026`, `uefa-europa-format-2026`,
`uefa-conference-format-2026`. These are official guides, not the full regulations.

| Competition | League matchdays | Last league matchday | Final |
| --- | --- | --- | --- |
| Champions League | 8 | 27 January 2027 | 5 June 2027, Madrid |
| Europa League | 8 | 28 January 2027 | 26 May 2027, Frankfurt |
| Conference League | 6 | 17 December 2026 | 2 June 2027, Istanbul |

The guides also list qualifying and knockout dates and warn that dates may
change. The full 2026/27 regulation links are confirmed by each official About
page, but the retrieved document-portal HTML is only a JavaScript application
shell. Article-level review, access lists, league ranking and draw constraints
remain pending; a successful portal request does not verify them.

## Located documents awaiting bodies or current editions

- Premier League: exact 2026/27 handbook PDF linked by official Governance page;
  file-host download blocked.
- Germany: DFB 3. Liga statute and July 2026 match/implementation rules linked;
  file-host downloads blocked.
- France: 2026/27 general, Ligue 3, national championship and Coupe de France
  PDFs linked by the FFF; file-host downloads blocked.
- Italy: FIGC NOIF articles 47–70, updated via CU209A of 6 May 2026, located in
  official page data; file-host download blocked.
- Spain: general competition framework PDF located, incomplete download. The
  readily linked competition-bases portal is explicitly **2022/23**; finding
  those documents does not establish 2026/27 formats.
- Concacaf: Champions Cup 2026, Nations League 2026/27 and Gold Cup 2025 English
  PDF links confirmed on official regulation pages; file-host downloads blocked.
- EFL: the attempted pages return navigation without readable regulation bodies.
  Earlier HTTP 200 observations must not be interpreted as completed EFL review.
- FIFA: portal located, individual competition and nationality/call-up rules
  still need retrieval and review.
