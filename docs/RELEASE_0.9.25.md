# Scorer World 0.9.25 — club cards, home grounds and supporters

The splash artwork no longer has the by clemir credit. The existing logo,
tagline, splash fonts and touch flow remain; the main-menu logo is unchanged.

The club name in normal and compact hubs is a button in the club's primary and
secondary colours. It opens foundation year, stadium, capacity, historical honours
and separately observed career trophies with that club. Golden Boots remain
personal awards. Facts and colours follow the club UID through aliases/transfers.
All existing career/save formats remain compatible.

The offline snapshot contains378 identified real clubs, all with sourced founding
year, stadium and capacity;363 have available historical title records and15
explicitly show Not available. No missing history is invented or called zero.
Sources/revisions and supplementary venue/local-language facts are included in
the audit.26 supporter-group names are verified; an unverified primary group uses
the club's display name on the banner, without asserting that no fan group exists.
Other fictional/unmapped club identities keep unavailable factual history and a
separate bounded game model for their ground capacity.

Match grounds use the actual home fixture's capacity and colours, including when
the player is away. Generic stand geometry scales its rows with capacity. A
separate curved second deck/concourse is added strictly above40,000 spectators.
This is a capacity-based representation, not an exact architectural stadium model.
Training uses the player's club ground and remains empty of fans/visiting banners.

The lower deck behind the goal, on the screen-left side, holds the away section
in visiting colours, with its verified group/club banner. Other spectators wear
home colours. Home/away mesh batches are separate and cached by fixture/palette/
banner. Player and AI goal events trigger only the scoring side's fans for2.35s;
repeat-goal guards and expiration prevent duplicated/permanent celebrations.

Validation:384 core tests passed. Full native suite ran190 cases; two compact
club tiles were48dp rather than the project's52dp minimum. Raised them to52dp and
reran9 affected/new cases successfully.19 final profile/parser/staging/edition
checks passed, including the new public JSON asset's byte-for-byte staging guard.
The30-view responsive matrix passed990 cases across11 screen/density/font-scale
profiles and Portuguese/German/Japanese. Club/hub66 cases were rerun after final
adjustments, zero findings. Actual1280x591 card/hub, one/two-deck grounds, visiting
banner and separate celebrations were visually inspected.

Initial candidate verification caught the missing profile JSON in the explicit
asset allowlist. Fixed the allowlist, added its staging regression and rebuilt
from a fresh stage. Final actual APK checks passed for exact compiled code/data/
artwork/fonts, club/40k rules, saves/competitions/safety, existing DEBUG upgrade
certificate, API36/arm64 and118 ELF/ZIP16KB alignment checks.

World DEBUG QA upgrade; public1.0 unchanged. Physical Android installation and
playtesting remain pending. No shot physics, goal budget, save-schema or server
behaviour was changed.
