# Striker Android — repository instructions for Codex

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
- Default player is fictional (Alex Silva). Preserve existing user names and saves; ship no official club assets or real name packs.
- Preserve privacy (no hidden analytics or external upload), fictitious clubs and original content, safe input handling. No secrets or signing keys in source/repo.
- Target Android API 36 or newer. Debug APK 0.6.1 was genuinely built and the owner reports it runs without crashes. Every subsequent APK needs its own build/static checks and device validation. The reference manifest in docs is not automatically merged by Buildozer; release gates still apply.
- APK and AAB must be genuinely generated and tested on Android, not claimed ready based solely on Python syntax compilation. Test landscape orientation and touchscreen usability.
- Menus must wrap text, keep touch targets at least 48 dp, scroll instead of overflowing, and provide save-before-exit confirmation. Test real Kivy layouts across phone aspect ratios; do not treat geometry checks as screenshots or device validation.
- Work in small reviewable commits; never overwrite the baseline or mark tasks DONE without test evidence. Log tests and failures in `docs/BUILD_LOG.md`.
- On every change, run available syntax/static checks, add tests for changed logic, and report limitations honestly.
- Never submit to Google Play, turn on real payments, buy ads, or contact sponsors without explicit human approval.

## Workflow
1. Read `README.md`, `ROADMAP.md` and `FIRST_CODEX_TASK.md`.
2. Start with `FIRST_CODEX_TASK.md` only, not the entire 14-day backlog.
3. Verify assumptions in code, make focused changes, run tests, document results.
4. Then proceed task by task from the roadmap and request approval at release boundaries.
