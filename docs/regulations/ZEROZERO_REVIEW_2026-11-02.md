# Zerozero and domestic-data review — 2026-11-02

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
