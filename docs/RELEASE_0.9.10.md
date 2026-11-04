# Scorer World 0.9.10 — conditional coach meetings and the newspaper

World DEBUG QA update. Save and Exit, install over World QA and Load Game.
Existing careers, names, training progress and competitions are retained.
The public release remains 1.0.

## Coach meetings only when requested

Ordinary weeks have no Coach Meeting action and do not require a meeting before
training or playing. Weekly training remains required before Play.

A coach requests a meeting after a three-game club scoring drought or a key
match. After a drought warning, another requires three more club appearances;
idle weeks do not repeat it. Key fixtures are actual finals, promotion/relegation
playoffs, derbies and survival run-ins. A scored late equaliser/lead opportunity
in a match the team did not lose also qualifies. A merely missed late chance in
an ordinary match does not create a request. Ordinary strong form alone does
not create one. An important match can prompt a review even after a poor showing.

Only requested meetings block training/play. Personality remains Encouraging,
Demanding or Balanced. Completing a request saves before unlocking progression.
A second key match can create another request in the same week. Reopening or
waiting through empty weeks never generates rewards or repeats a consumed review.

## Newspaper

The Newspaper action opens SCORER DAILY, an offline paper-style match report:
cream paper, masthead, headline, date/competition, real score, serif body text
and a miniature photo. Back stays reachable while the article scrolls. Text is
available in all nine existing languages, with CJK font fallback.

Articles use the last played fixture, not a future or simulated NPC match.
Headlines follow the actual home/away result. Goal chronology uses observed goal
minutes and is printed only when it accounts for the complete final score;
unobserved extra-time goals are not invented. Tie decisions remain in the score
record. There are no invented quotes, shots, possession, cards or assists.

The player's name is omitted from ordinary performances. It appears only for:

- Two or more personal goals, a lone goal in a win, or an actually scored late
  equaliser/lead opportunity when the team did not lose.
- At least three consecutive appearances with no personal goal despite recorded
  shooting chances. A goal or an appearance without a shooting chance resets
  this negative run. Club and national appearances both count for the paper;
  national games do not change the club coach's drought.

Five original generated football photographs rotate one per new report, persist
with that report and never reshuffle on reopening/reload. They are generic match
illustrations, not photographs of real clubs, people or this precise fixture.
A subtle caption identifies them as illustrations. No network is used to read or
write articles. Imported club aliases appear in the story without changing IDs.

New bounded optional save data retains the latest report and negative run.
Legacy played history can show a score-based report without inventing personal
performance. New careers show an empty state until the first match is played.
Malformed optional reporting data does not discard the career.

## Validation

Model and native Kivy tests cover conditional meeting gates, drought/review
frequency, same-week key matches, actual goal clocks, score conservation,
conditional player mentions, aliases, photo rotation, save/reload, malformed
optional data and legacy/empty states. Nine-language phone layouts down to320×240
keep the newspaper Back and meeting actions reachable. Host tests are not
physical Android device validation.

The actual APK is checked for API36/arm64, existing DEBUG upgrade certificate,
16KB ELF/ZIP alignment, exact compiled source and bundled photo/font bytes,
competition/save flows and ad-free publishing payload. No production signing,
Play submission or live-server change is included.
