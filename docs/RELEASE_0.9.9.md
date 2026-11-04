# Scorer World 0.9.9 — weekly coach meetings

World QA update. Save and Exit, install over World QA and Load Game. Existing
careers are retained. Public launch remains 1.0.

## Meeting, training, match

A Coach Meeting action is available on the normal and compact main menus,
including the Windows dashboard. Training and Play are disabled until the
player opens and finishes the current week's meeting. Opening it or going Back
alone does not complete it. Training remains required after the meeting.
Direct training/play callbacks also enforce the gate, including when the next
fixture advances the career into another week. Club and season changes require
a new meeting. Free agents continue through Agent rather than a coach screen.

Completing the meeting saves before unlocking progression. Reopening an
already completed meeting shows the same conversation; it grants no attribute
reward and consumes no match RNG. A failed save keeps the meeting locked and
allows retry. All text is translated into the existing nine UI languages.

## Feedback and personality

Each club has a stable fictional coach approach: Encouraging, Demanding or
Balanced. Encouraging coaches praise major performances; demanding coaches
acknowledge them and insist on focus. Different wording is available for
prolonged droughts and decisive performances, with brief routine check-ins in
weeks without special feedback.

- A drought is three consecutive played club matches without a personal goal.
  After a drought conversation, another special warning requires three more
  club appearances; empty calendar weeks do not repeat it. A goal resets it.
- A decisive performance is at least two personal goals in a match with a
  recorded decisive moment, or a scored late equaliser/lead opportunity in a
  match the player's team did not lose. This feedback waits for the next
  meeting even if another club match occurs first in the same week.
- Five personal goals across the last three club matches trigger strong-form
  feedback. International appearances do not alter the club coach's streaks.

These criteria describe actual played results and physical goals, not scripted
success. Feedback does not promise a trophy or guaranteed survival.

## Persistence and checks

Coach state is a bounded optional save extension. Legacy careers seed only
known recent club form. Existing training shots, completion, stats, names and
competition state remain intact, with a meeting required before continuing.
Damaged coach data resets only the optional coach state, not the career.

Validation covers model gates, persistence, failed writes/retry, week/season/
club boundaries, drought frequency, personality/wording, major performances,
legacy partial-training preservation and unchanged match RNG/attributes. Native
Kivy tests cover the visible actions, both hub layouts, direct callback guards,
calendar jumps, nine languages and reachable controls down to320×240. These
are host tests, not physical Android device validation.

The actual APK is checked for API36/arm64, existing DEBUG upgrade certificate,
16KB ELF/ZIP alignment, exact compiled source, competition/save flows and
ad-free publishing payload. No production signing, Play upload or live-server
change is included.
