# Striker Android — repository instructions for Codex

## Absolute scope
- This project is the original Python/Kivy Android app. **Do not use or port the Striker HTML/web version** and do not rewrite the game in another engine.
- `main.py` is an exact copy of the verified Drive baseline `Striker-P0-05-v006.py` as of 2026-10-23. Keep `baseline/` untouched and version future changes in git.
- Preserve the existing **striker career** gameplay: goal/shot simulation, player career, team offers, agent, training, competitions, fictitious club names, FREE/WORLD entitlement boundary, automatic saves.
- IMPORTANT: this v006 game is a striker's career game, NOT a club-share trading simulation. Do not falsely market unimplemented share-purchasing features or silently change the game's genre.

## Immediate release goal
By 2026-11-06 produce a tested signed APK for direct distribution and a tested Android AAB candidate for Google Play review, where feasible. Play Store publication is gated by Google approval and account testing requirements.

## Commercial model
- FREE to install and play, one division; WORLD is one-time unlock **only after native Play Billing is fully verified**, otherwise remain FREE.
- Monetisation V1: unobtrusive in-stadium ad boards rendered within Kivy Canvas. Use **locally bundled fictional placeholder brands only** until direct sponsors and cleared artwork exist. No internet requirement. Rotation every 20-30s only if it doesn't distract or hurt FPS. No click traps.
- Do not attempt to embed/reshape AdMob ads as textures; no AdMob integration in v1.
- Sponsor artwork belongs in replaceable asset/config slots; forbid external scripts, unknown tracking or suspicious remote URLs. Premium/billing work is separately gated.

## Safety and technical rules
- The current save path is near `__file__` and may be unwritable inside an installed Android package. Fix to Kivy `App.user_data_dir` / Android app-private storage while supporting migration and desktop testing. Protect compatible saves.
- Current game defaults to a real personal player name; replace any personal default with a generic fictional name before public release.
- Preserve privacy (no hidden analytics or external upload), fictitious clubs and original content, safe input handling. No secrets or signing keys in source/repo.
- Target Android API 36 or newer. Existing `buildozer.spec` is only a static starting point; successful compilation and device tests have NOT been verified. The reference manifest in docs is not assumed automatically merged by Buildozer.
- APK and AAB must be genuinely generated and tested on Android, not claimed ready based solely on Python syntax compilation. Test landscape orientation and touchscreen usability.
- Work in small reviewable commits; never overwrite the baseline or mark tasks DONE without test evidence. Log tests and failures in `docs/BUILD_LOG.md`.
- On every change, run available syntax/static checks, add tests for changed logic, and report limitations honestly.
- Never submit to Google Play, turn on real payments, buy ads, or contact sponsors without explicit human approval.

## Workflow
1. Read `README.md`, `ROADMAP.md` and `FIRST_CODEX_TASK.md`.
2. Start with `FIRST_CODEX_TASK.md` only, not the entire 14-day backlog.
3. Verify assumptions in code, make focused changes, run tests, document results.
4. Then proceed task by task from the roadmap and request approval at release boundaries.
