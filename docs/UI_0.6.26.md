# SCORER 0.6.26 — Free country restriction and independent careers

Owner corrections: new Free games have no country selector, and a Free career
is available only in Free. World starts its own career inside the same application.

Changes:
- New Free careers go directly to Scorer League (internal England|4), ignoring
  phone locale. No country buttons or start_country route in Free; core rejects
  foreign-country selection. Only World retains local/England Division4 choices.
- Existing legacy Free careers keep their current single league/progress.
- Explicit Free/World save slots: striker_career.json and striker_world_career.json.
  World never auto-imports Free; a copied Free payload is rejected by World load.
  World ownership cannot turn the Free slot into World or enable its editor.
- Verified owners can select modes from the entry/menu, then explicitly New/Load.
  First World entry has a new player/contracts, zero goals/matches, not Free stats.
  Switching saves the active career first; a failed save blocks switching.
  Previous-game/editor backups remain slot-specific. Inaccessible World remains
  stored; return to Free never copies its data. Ads/reward buttons are suppressed
  for owners in either mode. Purchase remains disabled in this beta.
- Updated Help, Upgrade, store/privacy drafts, packaging exclusions and instructions.

Files: career.py, main.py, menu_ui.py, world_ui.py, version/config/exclusion files,
core/UI tests, Play artifact inspector and product/release documentation.

Tests: **82 core/security PASS** (12.072s), **48 actual Kivy PASS** (48.853s),
**130 total**. Includes legacy Free preservation, paid Free restrictions, independent
World goals/player/files, mode save failure, copied-Free rejection, unknown slot/path
rejection, hidden/guarded country actions and unauthorised World route rejection.
An initial UI snapshot compared a loaded career with its pre-load status message;
normalised the selected state by saving before the isolation comparison. Final pass.
Syntax and git diff --check pass. No match balance or physics changes.

Actual debug APK built, com.clemir.striker, versionCode1026626, target36/min26 ARM64.
Existing DEBUG certificate matches previous betas. apksigner/zipalign16KiB and all
118 ELF LOAD alignments pass. Compiled WORLD_PREVIEW=false; billing stays disabled.
Size: 37,593,779 bytes. SHA256: `e68ffdedd3d1e168a532a2690a31e83f28d0f01da7f674b0135937927003d69b`.
This is a beta, not a production-signed release; device/Play purchase tests remain pending.
No AAB was rebuilt for 0.6.26: the 0.6.25 rehearsal AAB/report are historical; regenerate
and validate from the final selected source before any store submission.

Logs: /tmp/scorer-0626-core.log, /tmp/scorer-0626-ui-final.log,
/workspace/striker-runtime/build-0.6.26-free-final.log and verify-0.6.26-free.log.
Next: owner validates Free new-game offers and existing career on Android; configure
and explicitly approve Play licence testing before testing live World ownership/modes.
