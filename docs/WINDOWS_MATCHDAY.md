# Scorer Free Windows0.6.39-win.2 — matchday dashboard

Owner request: replace the Windows hub's oversized one-fixture/season cards with
all upcoming league matchday games on the left (own game highlighted), league
scorers on the right. Shared original Kivy game; no Android UI/engine rewrite.

## Behaviour

WindowsDashboard reuses the existing responsive header/action strip, Training and
Play gate, errors and compact fallback. Left displays exact current league
pairings in their saved order, alternating row backgrounds and a green/bold own
fixture. Round12games fit in a normal1280x720 or1366x697 client viewport. Only
smaller views need fixture paging, with48dp controls; no main-menu scroll view.
If the window falls below780x520dp it restores the original compact dashboard,
then returns to tables on enlargement, without changing the career.

Next date/opponent/competition remain in a compact line. On cup weeks this line
identifies the cup fixture, while the table explicitly remains the upcoming
LEAGUE matchday; no fictitious whole-cup round or wrong league date is invented.
A completed league does not repeat its final round. Fixture data comes only from
current_league.pairings, not new draws/calendar reshuffles.

Right displays saved league scorers, sorted identically to the full scorer table,
with rank, player, club and goals; hero row highlights when among visible leaders.
It shows as many leaders as fit; TOP SCORERS still opens the full paged ranking.
A persistent YOU rank/league-goals footer retains the hero when outside the top
rows. Season matches/all-competition goals are separate compact footer values,
not substituted for league scorer totals. Fresh careers cannot invent other
scorers/goals to fill the empty state. Labels are bounded/plain text, no markup.
Training remains left of Play; Play remains disabled until weekly training.

Pure dashboard_data copies counts and resolves display names; no save/write,
RNG advance, simulation, calendar change, unlock or network request on browsing.
The Windows menu signature includes round/scorer data so live totals refresh.
Android continues to instantiate the original MainDashboard; its header, touch
controls, layouts and version are unchanged. No new Android APK was produced.

## Validation

158 core/security +87 real Kivy tests (245) pass. Four new core cases cover exact
pairings/highlight, unchanged RNG/save, cup-vs-league distinction, end-of-season,
league-vs-career goal totals and tied ranking. Four new UI cases cover full12-game
1366x697 layout, highlight, no ScrollView, leader list/hero footer, read-only paging,
800x600/1024x600/1920x1080/1366x768 resizes,48dp actions and compact/restored mode,
and Android isolation. Existing weekly training/save/score/edition tests pass.
Initial harnesses had not loaded the saved club before checking its highlight;
corrected that setup. Tests also exposed stale totals when only the scorer map
changed; the scoped Windows signature fix resolves it. No gameplay RNG change.

Source staged Windows-profile smoke passes startup/new career/weekly training,
one automated engine-finished match/real NPC scorer generation, save/reload,
new dashboard,12visible fixtures and window exit-confirmation/cancel. This is
an automated flow, not a physically played full match. Render now exports the
actual Kivy root canvas to an RGBA FBO, avoiding stale/discarded ANGLE window
backbuffers or a ghost of a just-dismissed modal. Cancellation additionally
asserts the popup really left Window.children. Render code is smoke-only.

Native Windows EXE build/frozen test and final hash must be recorded before
claiming delivery. Manual mouse/keyboard/full match/audio/resize checks remain
pending on the owner's PC. No digital signature/store/publication/payment or
stats-server activation. Existing private Windows career directory is unchanged;
replace the EXE without uninstalling or deleting %LOCALAPPDATA%/Clemir/Scorer/Free.

Files: dashboard_data.py, desktop_dashboard.py, scoped menu_ui.py hub/signature;
desktop_launcher.py and tools/windows/verify_smoke.py automation; workflow paths;
tests/test_dashboard_data.py, ui_tests/test_windows_dashboard.py; release docs.
Next: install the new EXE, Load your existing career and check actual matchday,
own-fixture highlight, scorer order/hero rank, Training/Play gate and resizing.
