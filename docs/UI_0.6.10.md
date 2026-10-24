# SCORER 0.6.10 — English edition

All generated player-facing text now uses English: entry, profile, first
contract, main menu, training, standings, scorers, fixtures, agent, match
notices, timers, editor, confirmations, career feedback and save errors.
Dates use English month abbreviations; tables use P/W/D/L/GF/GA/GD/PTS.
The existing English splash and fictional club names are retained.

## Existing careers
The automatic league title becomes Scorer League. Previous automatic titles,
including Liga Scorer, migrate without resetting progress. User-created player,
club and competition names remain unchanged. Historic automatic Liga Scorer
fixture labels and Jornada statuses migrate. Loading replaces a transient
saved feedback message with Career loaded, preventing Portuguese notifications
from returning. Save format remains v2 and the weekly training rule is unchanged.

## Device language
This edition deliberately stays in English, regardless of the phone language.
Automatic localisation is possible later: read Android's ordered locale list,
select a supported translation and use English for unsupported languages or
missing entries. This requires bundled, reviewed translations of the interface,
career messages and artwork text. It does not require internet access, a
translation service or additional permissions. No automatic translation or
locale switching is implemented in this build.

## Files and verification
Changed career.py, main.py, menu_ui.py, buildozer.spec, tests/test_career.py,
ui_tests/test_menus.py, AGENTS.md, README.md and documentation. Original baseline
and simulation preserved. Validation and actual APK checks are in BUILD_LOG.
Kivy screenshots are desktop window captures, not Android device screenshots.
Next: update the phone without uninstalling and check English text in normal
play and error dialogs. Physical validation of this beta remains pending.
