# SCORER 0.6.21 — full league fixtures and progressive cup draw

## Changes

- Fixtures no longer has a STATS action or alternate detail submenu. Date,
  match, competition and result/round appear together in the existing paged table.
  Standings retains its own statistics action.
- New careers shuffle the league club order once using a separate deterministic
  season RNG. The complete double round-robin is thereby fixed at creation,
  retaining alternating home/away, the one-repeat-per-leg limit and reversed
  return venues. Saved club order retains the draw after reopening. A new season
  draws a new order. Existing in-progress club order and schedule versions stay.
- Calendar no longer truncates upcoming fixtures to eight: all 46 FREE league
  fixtures are accessible through pages from the start. Results remain visible
  for the season: stored history grows from 20 to 128 entries (sufficient for the
  league, cup and international appearances). Previously discarded results from
  old saves cannot be reconstructed; existing retained results are preserved.
- Reserve cup weeks regardless of elimination, keeping future league dates fixed.
  When eliminated, unused cup weeks are skipped automatically without a match or
  consuming another training session. Normalisation also handles loaded saves.
- Only the current cup round has a drawn opponent, with a stable seeded draw
  shared by Fixtures and the actual match and retained on reload. Advancing
  reveals the next round; no future opponent is displayed prematurely. Defeated
  opponents cannot be drawn again. After the final the cup is closed. This keeps
  the original player-career cup system, not a new full-world tournament engine.

## Verification

51 core/build/security tests and 38 actual Kivy tests pass (89 total). Added:
full 46-match calendar, stable future dates across 35 played fixtures including
cup elimination, retaining those results, save/reload equality, every cup draw
through the final, no repeated defeated opponent and no premature future draw.
Existing home/away calendar tests and layout/touch/page coverage pass. Fixtures
explicitly has no STATS label. Syntax, whitespace and immutable baseline pass.

The initial UI regression found the test calling toggle_detail on a table with
no details; the callback now safely does nothing in that case. The full Kivy
suite was rerun after that fix. Actual desktop screenshot inspected:
/workspace/striker-runtime/scorer-0621-fixtures0001.png. Not an Android screenshot.

Actual APK build and static checks are recorded in docs/BUILD_LOG.md. Device
validation of this version is pending. Next: install as an update and check all
fixture pages, cup progression, reload and training around reserved cup weeks.
