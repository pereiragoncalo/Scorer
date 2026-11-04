# Scorer World0.9.15 — post-match news/coach flow and player trophies

World DEBUG QA update. Save/Exit, install over existing World QA and Load Game.
Package, upgrade certificate and career identity are unchanged. Public1.0 stays
separate; no Play or live-server changes.

After the full-time result, Continue opens the newspaper. Its Continue action
opens the requested coach meeting, if any, and then returns to the career menu.
Ordinary matches have no meeting. The newspaper/coach queue is saved with the
result and survives loading the career. Android Back follows the newspaper's
Continue route; it cannot dismiss a required meeting. A failed queue save keeps
the current step available for retry. Main menus no longer contain Newspaper or
Coach Meeting buttons in normal, compact or inherited Windows layouts. Existing
coach requests remain reachable automatically instead of stranding a career.

The Player screen now includes a scrollable trophy cabinet with original golden
cup icons, seasons, competition titles and clubs, keeping name/save controls
reachable on small screens. Observed personal participation is tracked separately
from AI winners. Actual league/cup/national champions award trophies; qualifying
or promotion-playoff results do not award a championship cup. A player tied at
the positive final league scoring maximum receives a Golden Boot. Duplicate
collection is idempotent, and trophies persist across saves, seasons and club
changes. Optional malformed honour data is bounded/discarded independently.

Historical limitation: earlier saves did not record a personal trophy cabinet or
complete competition-participation history. Unprovable old personal titles are
not reconstructed from AI-winner archives. The cabinet records verified played
campaigns and resulting awards from this version onward; an empty cabinet says
that no trophies have been recorded. Existing career stats/results remain intact.

The World submenu button now reads EDITOR, with existing import and navigation.
Agent is visibly disabled outside the transfer window, and direct Agent/Refresh
actions are guarded too. The existing free-agent exception remains: a released
player can seek/sign a contract outside windows, avoiding a stuck career.

Validation:350 core +158 native Kivy tests (508 total), plus an18-test targeted
native run. Added tests cover post-match order, optional meetings, saved queue,
Back, failed saves, both hub sizes, agent windows, small Player layouts, actual
league/cup-final awards, Golden Boot, deduplication, transfers and reload. The
initial native run exposed old expectations for removed buttons and skipped
post-match steps; these were updated to follow the new flow before the final run.

The APK's actual compiled honours/career/UI modules match reviewed source. A
compiled smoke fixture awards a personal cup trophy and reloads the newspaper
queue. API36/min26, arm64, existing DEBUG certificate,118 aligned ELF files/16KB
ZIP alignment, previous competition invariants and ad-free publishing payload
also pass. Physical Android validation and production signing remain outstanding.
The Portuguese preview is a desktop Kivy render with synthetic demonstration
awards, not the owner's career or a physical Android screenshot.
