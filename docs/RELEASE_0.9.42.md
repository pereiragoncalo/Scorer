# Scorer World0.9.42 QA — visible version

The New Game/Load Game entry screen now shows v0.9.42 in a small footer at the
bottom right. Help → Settings also displays the version. Splash and logo artwork
are unchanged. The label uses generated build metadata from the same versionName
as the Android package; production staging displays1.0 automatically.

Career hub controls, finishing, competitions, saves, public policy destination
and optional statistics remain unchanged from0.9.41. Owner reports the requested
0.9.41 phone smoke checks passed: startup/policy, training/single-tap/unlock,
completed match/save/exit/reload with progress retained. Device model and Android
version were not supplied; full extended/Play acceptance remains pending.

This is a DEBUG-signed QA APK. The public v4 Career service still needs its bastion
update; this UI-only release does not deploy it or create a signed Play1.0 AAB.
