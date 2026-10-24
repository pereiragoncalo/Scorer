# SCORER Android — repository instructions for Codex

## Absolute scope
- This project is the original Python/Kivy Android app. **Do not use or port the Striker HTML/web version** and do not rewrite the game in another engine.
- `baseline/Striker-P0-05-v006.py` is the immutable original. Career/simulation now live in `career.py`; `main.py` retains the Kivy game and `menu_ui.py` the responsive menus. Version changes in Git.
- Preserve the existing **striker career** gameplay: goal/shot simulation, player career, team offers, agent, training, competitions, fictitious club names, FREE/WORLD entitlement boundary, automatic saves.
- IMPORTANT: this v006 game is a striker's career game, NOT a club-share trading simulation. Do not falsely market unimplemented share-purchasing features or silently change the game's genre.

## Immediate release goal
By 2026-11-06 produce a tested signed APK for direct distribution and a tested Android AAB candidate for Google Play review, where feasible. Play Store publication is gated by Google approval and account testing requirements.

## Commercial model
- Updated owner decision: FREE is a basic app with exactly one playable division, funded exclusively by stadium advertising. No in-app purchases, subscriptions or WORLD unlock in FREE.
- WORLD must be a separate paid app, with all worldwide divisions, fictional defaults and a local name editor/importer. Do not claim worldwide depth is complete: current simulation has detailed European pyramids and one tier for many other countries. Native payments, store publication, and the separate paid artifact are not activated in the current FREE build. See docs/PRODUCT_MODEL.md.
- Monetisation V1: unobtrusive in-stadium ad boards rendered within Kivy Canvas. Use **locally bundled fictional placeholder brands only** until direct sponsors and cleared artwork exist. No internet requirement. Rotation every 20-30s only if it doesn't distract or hurt FPS. No click traps.
- Do not attempt to embed/reshape AdMob ads as textures; no AdMob integration in v1.
- Sponsor artwork belongs in replaceable asset/config slots; forbid external scripts, unknown tracking or suspicious remote URLs. Premium/billing work is separately gated.

## Safety and technical rules
- Saves now use Kivy App.user_data_dir on Android, with legacy migration and a desktop/test override. Preserve compatible saves; a failed save must not exit the app or erase previous data.
- Uppercase the first letter of each space-separated player-name component on profile save and legacy load; preserve internal spelling, accents, progress and scorer identity. Never overwrite another scorer on a formatting collision.
- Alex Silva is only the legacy fictional default. New careers must ask for a safe player name before the first contract; existing names change only through the Player action, retaining progress and scorer identity. Preserve saves; ship no official club assets or real name packs.
- Preserve privacy (no hidden analytics or external upload), fictitious clubs and original content, safe input handling. No secrets or signing keys in source/repo.
- Target Android API 36 or newer. Debug APK 0.6.1 was genuinely built and the owner reports it runs without crashes. Every subsequent APK needs its own build/static checks and device validation. The reference manifest in docs is not automatically merged by Buildozer; release gates still apply.
- APK and AAB must be genuinely generated and tested on Android, not claimed ready based solely on Python syntax compilation. Test landscape orientation and touchscreen usability.
- Match balancing: personal chance quantity and clear-chance probability depend on opponent quality and its own league position as well as player condition. Use at most three chances and one clear chance; elite teams (rating ≥84.6) or top-15% sides after five matches allow at most one chance, always hard. Use little/no ranking weight before five matches and rating alone if no domestic table exists; resolve the actual opponent for home/away and cup/international fixtures. All remaining chances use pressured long/angled shots, defenders and faster keeper reaction. Preserve penalties/headers/free kicks, physical scoring and existing career totals; never force misses or inflate rival scorers to enforce a quota.
- Main hub and entry menu use assets/menu_logo.png, generated from the original icon, without a by clemir label. Preserve the splash credit.
- Public game identity is SCORER by clemir. Native wordmarks use bundled Barlow Condensed ExtraBold Italic with a smaller Barlow Regular credit; preserve font licenses in the APK and use shared alignment. Keep the existing Android package/save identifiers for upgrade compatibility.
- Startup must retain the Kivy splash until a touch, including through rotation. Then offer New game / Load game / Exit without autoload. New game with an existing save requires in-app confirmation and an atomic private backup; never save unselected state on pause/stop.
- This version uses English throughout, regardless of device language. Preserve custom names; do not claim automatic localisation without translated resources.
- FREE displays Scorer League: migrate only automatic legacy league labels, retaining progress and custom names. Internal England|4 is a compatibility key, not four playable divisions.
- Keep the match scoreboard compact (280 × 46 dp) and use First half/Second half labels, not 1H/2H. Keep match notices attached during redraws so touches retain a stable widget tree. Match scoreboard stays at the top left in both simulation and chances, with stacked team names/scores and a clock on the right. Attach the 22 dp shot countdown directly beneath the scoreboard with identical left edge/width; keep notices below it; no bottom match-time bar. Every goal produces one local highlight, counted immediately and once. Pause at 45 plus first-half added time until Second Half; resume display at 45:00 and finish after second-half added time. Never process events beyond the next chance or half boundary.
- Training sits immediately left of Play in the main menu. Play is grey and disabled until the current career week’s three-shot session is completed, with a matching start-match guard. Persist completed shots/goals so an interrupted session can resume; never block career progress after abandonment. Training is limited to one session per career week, reserved and saved before the first shot. Abandonment/reload must not grant another session or duplicate rewards; retain compatibility with older completed-training saves. Reset for a new season.
- Buttons use rounded raised Kivy surfaces with visible pressed feedback. Standings, scorers and calendar use compact readable pages, with every row accessible and no horizontal scrolling; do not shrink touch controls below 48 dp.
- The main menu must fit on one screen without scrolling, with all six FREE actions and Exit visible. Use compact responsive columns and bounded summary text. Other lists may scroll. Keep touch targets at least 48 dp and save-before-exit confirmation. Test real Kivy layouts across phone aspect ratios; do not treat geometry checks as screenshots or device validation.
- Work in small reviewable commits; never overwrite the baseline or mark tasks DONE without test evidence. Log tests and failures in `docs/BUILD_LOG.md`.
- On every change, run available syntax/static checks, add tests for changed logic, and report limitations honestly.
- Never submit to Google Play, turn on real payments, buy ads, or contact sponsors without explicit human approval.

## Workflow
1. Read `README.md`, `ROADMAP.md` and `FIRST_CODEX_TASK.md`.
2. Start with `FIRST_CODEX_TASK.md` only, not the entire 14-day backlog.
3. Verify assumptions in code, make focused changes, run tests, document results.
4. Then proceed task by task from the roadmap and request approval at release boundaries.
