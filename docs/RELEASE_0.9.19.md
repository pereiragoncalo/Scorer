# Scorer World 0.9.19 — animated opportunity build-ups

World DEBUG QA upgrade. Install over the previous World QA and choose Load Game.
The package, existing upgrade certificate and career saves remain compatible.
Public launch stays version 1.0.

## Gameplay

Point 5 of the owner's six-item suggestions list is implemented. Matches now plan
five distinct pressured opportunities: a high cross for a header, a byline run
and cutback, a fast diagonal pass for a first-time finish, a blocked shot falling
back to the striker, and a direct free kick with the existing four-player wall.
Existing clear opportunities use a through ball; announced penalties retain the
penalty spot, player selection and keeper-only contest.

The player sees the delivery before shooting. The ball, receiver, supporting
players and goalkeeper move during a short build-up. A green marker identifies
the striker. On exact reception the scene pauses: only then do the aiming marker,
power and full shot countdown appear. Taps and Space cannot shoot during the
build-up, and the reset shortcut cannot bypass it. First-time/rebound chances
allow a shorter reaction window; free kicks allow more time to read the wall.
Training remains three shots with only the striker and keeper, without build-up.

Delivery paths are visual choreography, not a second resolved shot or a forced
save. Rebounds replace an existing opportunity; they do not award extra attempts
following a player's miss. Actual finishing still uses the existing physical
ball, field collisions, fixed goalkeeper reach and goal geometry. No automatic
goals or forced misses were added.

Plans and delivery geometry use deterministic independent RNG keyed to the
fixture. They preserve the existing chance count and reserved penalty/clear slots,
without consuming AI result RNG or inspecting future goals. Normal slots vary
without repetition within a match. The existing 0.20 pressured-chance contribution
remains reserved from simulated teammate goals.

## Validation

358 core tests passed. The full native suite ran 171 cases; two old assertions
requiring only long shots/all-hard elite chances were updated to the current
variety/penalty/clear-slot rules. The five affected/new integration cases then
passed, as did the final three sequence tests after the defender-cap adjustment.
Tests cover blocked input before reception, untouched timer/counts/score/clock,
exact contact, frozen actor/keeper positions, live shooting after arrival,
penalties, training isolation, deterministic variety and continuous paths.

A targeted native audit ran match/shot layouts across 11 size/density/text-scale
configurations and Portuguese/German/Japanese: 66 cases, zero findings. Original
0.9.18 layouts and nine-language catalogues are retained. Representative English
frames for all five deliveries and reception states were inspected visually.

2,880 paired physical attempts cover five types plus the previous generator,
tiers 1 and 2, and uniform/low-corner/high-corner exact targets. All resolved.
Uniform exact-target conversion was 8.75–31.25% across new types, versus
11.25–12.5% for the previous generator; timing/aim movement is bypassed in this
experiment, so these are not human conversion rates or a promise about seasons.
The five-type mean remains below the existing 0.20 goal-budget reservation.
The rebound sample was repeated after keeping the total defenders at four/five.
Detailed outcomes and limitations: data/opportunities_0.9.19.json.

The actual APK passed exact compiled module/translation/data checks, delivery
module execution, World edition/competition/save/publishing smokes, existing
DEBUG certificate, API36/arm64 and 16KB ELF/ZIP alignment checks. Physical Android
installation/playtesting remains pending. This is QA, not Play production approval.

## Saved improvement list

GAMEPLAY_IMPROVEMENTS.md preserves all six suggestions and the owner's additional
build-up/reception instruction. It is versioned in the repository and attached
to the QA release. No Google Drive connector was available, so no Drive upload
is claimed.
