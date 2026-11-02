# Zerozero and domestic-data review — 2026-11-02

## Successful retry

General competition routes are now readable. Friendly edition routes and some overview child pages can still return the suspension page. Followed the links in the homepage and competition pages, using a normal anonymous session. [Collected source data](zerozero_2026_competitions.json):15complete club lists plus the French Ligue2overview, which explicitly states18teams; its regular-season table remains unavailable. This supersedes the all-unavailable status in the first attempt below.

| Country | Division1/2 confirmed on Zerozero |
| --- | --- |
| Portugal | 18/18 |
| England | 20/24 |
| Spain | 20/22 |
| Italy | 20/20 |
| Germany | 18/18 |
| France | 18/18 (Ligue2overview only) |
| Brazil | 20/20 |
| Argentina | 30/36 |

Portugal tables show the16th-place relegation playoff and17th/18th direct relegation in both divisions; Liga2also marks direct promotion/playoff zones. SportingB/BenficaB markers were retained explicitly. These raw colours are not enough to establish eligibility: B teams must not be promoted merely because their displayed row has a promotion colour. The official regulations reviewed below remain necessary. Other retrieved tables expose national differences, including the English/Spanish promotion playoffs, German cross-division playoff and Brazilian4-club relegation zones. Argentine group tables alone do not verify annual-average relegation or all promotion rules.

**No game changes in this retry.** Country-specific rules, eligibility and complete playoff procedures are not newly certified by these table legends.

## First attempt (retained log)

Zerozero was requested as the reference for clubs, division sizes and promotion/relegation. From this environment the home, competitions index and two competition pages returned HTTP200 **after redirecting to `/suspended.php`**, headed “Serviço Temporariamente Suspenso”. No Zerozero club list, count or rule was read or verified. Robots was reachable; no disallowed path or access-block circumvention was used.

The Liga Portugal2026/27 regulation PDF was downloaded again from its official publisher; its2,440,200bytes/SHA256 match the previously read copy. Articles21/25 confirm18teams in each professional division; articles22/26 provide2direct movements plus conditional playoffs. Article31 specifies the cross-division two-leg playoff, B-team exclusion, aggregate goals, extra time and penalties. The Liga2/Liga3 playoff also depends on FPF conditions. This is a partial professional-league review, not full-country certification.

[Official Portugal regulation](https://www.ligaportugal.pt/backoffice/assets/20260701_RC_2026_27_f53785bcd4.pdf) · [Detailed audit](zerozero_2026_review.json)

## Counts needing correction

The following reference counts come from the already reviewed, revisioned membership manifest, **not Zerozero**. The0.9.4 game capacities were preserved by the two-tier change and still omit68real teams across the eight supported first-two-tier reference sets.

| Country | Season | Game1/2 | Reference1/2 |
| --- | --- | --- | --- |
| Portugal | 2026-27 | 18/18 | 18/18 |
| England | 2026-27 | 20/24 | 20/24 |
| Spain | 2026-27 | 18/18 | 20/22 |
| Germany | 2026-27 | 18/18 | 18/18 |
| Italy | 2026-27 | 18/18 | 20/20 |
| France | 2026-27 | 18/18 | 18/18 |
| Brazil | 2026 | 12/12 | 20/20 |
| Argentina | 2026 | 12/12 | 30/36 |

The uniform3-up/3-down rule is a game design choice, not a verified national rule. Real profiles need separate team counts, direct and playoff places, B/reserve eligibility, parent-club conflicts, tiebreakers, group/split formats and current-season amendments. Countries without an open national promotion pyramid must not be assigned invented real rules. Retain the owner’s two-playable-tier/ten-reserve/free-agent design; explicitly map any real tier3 access into that abstract reserve rather than claim a simulated real third league.

No app source, APK, career, policy/server, or private credential changed in this research. Zerozero retrieval remains unavailable here, other country rule bodies remain unverified, and country-specific implementation is not complete.
