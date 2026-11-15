# International calendar correction1030036

The previous model already contained playable Euro/World Cup finals. It could
nevertheless schedule five games in the long autumn window, create qualifying
only in the finals' club season, concentrate qualifiers in one window, use
June3 finals defaults, and put club games inside release periods. Reproduction
and source investigation preceded this change; selection is still required.

New dated model:
- FIFA published windows2025–2030, maximum2matches in9days or4in16days.
  Friday/Tuesday game dates allow travel/recovery; the source calendar's Monday
  is a release day, not an extra matchday. Minimum3days between national games.
- NL A2026/27: September25/29, October2/6, November13/17; two-legged quarter-finals
  March26/30,2027; semis/finalJune9/13. B/C/D finish their promotion groups without
  fictional title finals. Lower-league promotion and future formats remain models.
- Euro/World European qualifying groups use two legs, with spring/autumn fixtures
  in the year before finals. Persistent campaigns retain draws, results, pending
  fixtures and IDs across July. Nation qualification outcomes are still simulated,
  and selection retains the first-division/top-three-scorers rule. No forced caps.
- Euro2028 spanJune9–July9,2028; World2026 spanJune11–July19. Other announced2027
  finals spans retained. Individual fictional draw matchdays within these spans
  are game dates; unannounced future finals (including2030exact days) are labelled
  projections. Qualification place allocation/other confederation formats remain
  game models, not a claim to reproduce every real playoff/host qualification rule.
- Club schedules use persisted dates through midMay with Wednesday matches when
  necessary for46round leagues. International windows and corresponding national
  finals have club release breaks. Existing opponents/home-away order are unchanged.
  Remaining dates migrate without rewriting historical results. Cup dates avoid
  release windows and same-day/adjacent-day league collisions. Promotion ties can
  use midweek capacity. Completed appearances consume their own practice as before.
- Fixture pages and next-match dashboard show the actual dated fixture, not a
  week index/Sunday proxy. Reserved training and an already chosen focus move with
  a retimed upcoming appearance; completed matches still trigger ordinary new-week
  preparation. Calendar-year salary/contract logic remains in the existing system.

Compatibility: shipped1030035 national fixture data is retained as a compressed
regression fixture (produced from cded1dd). Played scores/dates, draws/fixture IDs,
club standings, personal goals/caps and honour records are authoritative. Legacy
unplayed dates can migrate; an oversized already-started qualifying draw that
cannot fit without dropping games retains its current campaign and upgrades next
season. No fabricated old personal appearances, save reset or new backend required.

Sources inspected:
- FIFA Men's International Match Calendar2023–2030, April2026:
  https://digitalhub.fifa.com/m/3123d37097318f7f/original/Men-s-International-Match-Calendar-2023-2030_EN.pdf
- UEFA EURO2028 lowdown (17September2026), March–November2027 qualifying and
  March2028playoff period; finals9June–9July2028:
  https://www.uefa.com/euro2028/news/028f-1b599fe02d18-0c758142f5e4-1000--euro-2028-all-you-need-to-know/
- UEFA Nations League2026/27 (14November2026), league matchday spans, March
  quarter-final period and June finals:
  https://www.uefa.com/uefanationsleague/news/0298-1d6ef1acfaef-b54fcf1da859-1000--2026-27-uefa-nations-league-all-you-need-to-know/
