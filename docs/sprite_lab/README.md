# Scorer original retro sprite lab — phase 1, art revision 2

**Art revision 2 was approved on 2026-11-06 and is now integrated in World 0.9.26.**

This page records the phase-1 preview. For the integration, APK checks and remaining device test, see [release report](../RELEASE_0.9.26.md). The standalone viewer remains available.

[Reference-style pose board](reference-revision-2.png) · [Animated preview](animations.gif) · [Actual Kivy viewer screenshot](viewer.png) · [All field-player frames](players-all-frames.png) · [All goalkeeper frames](goalkeeper-all-frames.png)

## Run the viewer

Use Python 3.10 or newer on a desktop with an OpenGL-capable display:

```sh
python -m venv .venv-sprites
# Linux/macOS
. .venv-sprites/bin/activate
# Windows instead: .venv-sprites\Scripts\activate
python -m pip install Kivy==2.3.1
python tools/sprite_viewer.py
```

Run from the repository or the extracted standalone bundle. The entry point also resolves resources correctly when launched from another directory. Pillow is **not** needed to run the viewer. Recommended window: 1440×900; layouts checked at 960×640, 1280×800 and 1440×900. This is a separate desktop inspection tool, not a new game or an Android APK.

Both characters animate simultaneously on a pitch-green background. Choose any animation independently. Pause/play and previous/next frame apply to both characters; stepping pauses playback. Speed changes the playback rate; pixel scale selects integer enlargement and automatically fits the available panel. Mirror changes facing without moving the anchor. Front/back views are available for the outfield player. The goalkeeper is shown from the front, with lateral movement and both dive directions.

Animation uses cached sheet regions. **Frames** displays the individual PNG files; **Sheet** displays the actual atlas. All three views use the delivered resources, not substitute artwork. Frames and Sheet place frames in reading order. A tiny window may crop a sheet rather than interpolate pixels; use the tested sizes above. Yellow outlines and crosses expose the fixed canvas and ground anchor; toggle **Anchors** to hide them. **Repeat / hold** switches preview replay of one-shot actions; holding still loops the naturally looping idle/run clips.

The five hexadecimal fields configure shirt, secondary trim, shorts, socks and gloves. Apply validates the values; presets make colour changes quick to inspect. The outfield preview starts in blue/white stripes, with blue shorts and pale socks. The keeper starts in a bright green long-sleeved shirt, dark shorts, yellow socks and visible gloves, matching the colour vocabulary of the user-supplied references. Presets are viewer-only; existing team data is neither loaded nor rewritten. A future integration must supply the existing team's exact kit values.

## Reference revision — 2026-11-06

The supplied screenshots requested fuller footballers than the first thin silhouettes. Revision 2 redraws the bodies with wider shoulders, tapered kit shapes, stronger limbs, distinct bare thighs, short sleeves and larger original 9×9 heads with short necks. Blue/white torso stripes and shorts are independent palette roles. Run/dribble use wider strides and bent, alternating arms. The goalkeeper now waits in a wider, lower crouch; lateral steps and the low save share that stance, with outward knees and a two-handed ground gather. Dives still progress through take-off, extension, contact and landing.

These are original redraws, not extracted pixels from the screenshots. All 168 frames and 24 sheets were regenerated; the visualizer uses them directly. Canvas sizes, ground anchors, frame counts, state names and the approval boundary remain unchanged. Bone lengths remain fixed; a grounded knee solution that would sink through the ground is replaced by its alternate bend. There is no ball painted into the sprites. The compact pose board centres cropped silhouettes for presentation only; the animated preview and viewer retain the actual fixed anchors.

Recovery point for the first proposal: `recovery/sprites-before-reference-revision-2026-11-06`, commit `4bf8932`. The main game remained unmodified during both sprite proposals. Integration was subsequently approved by the owner and is documented in the release report.

## Delivered artwork

Original indexed pixel art drawn with Pillow on a hard pixel grid. Inspired by the proportions, articulation and limited-colour vocabulary of ZX Spectrum football games; no sprites or graphics from those games were copied or downloaded. No external model or copyrighted game assets are required.

| Character | Animation | Frames | Native fps | Behaviour |
|---|---|---:|---:|---|
| Field player | IDLE | 2 | 4 | loop |
| Field player | RUN | 8 | 12 | loop |
| Field player | DRIBBLE | 8 | 10 | loop |
| Field player | PASS | 6 | 10 | one shot |
| Field player | SHOOT | 8 | 12 | one shot |
| Field player | TACKLE | 8 | 11 | one shot |
| Field player | HEADER | 8 | 10 | one shot |
| Field player | FALL | 8 | 10 | one shot, includes getting up |
| Goalkeeper | READY | 4 | 5 | loop |
| Goalkeeper | MOVE | 8 | 11 | loop |
| Goalkeeper | LOW_SAVE | 6 | 10 | one shot |
| Goalkeeper | DIVE_LEFT | 8 | 12 | one shot |
| Goalkeeper | DIVE_RIGHT | 8 | 12 | one shot |
| Goalkeeper | HIGH_SAVE | 8 | 11 | one shot |
| Goalkeeper | CATCH | 6 | 9 | one shot |
| Goalkeeper | RECOVER | 8 | 10 | one shot |

There are **168 individual PNGs and 24 sheets**: 56 field-player frames in each of two views, plus 56 goalkeeper frames. Every animation meets or exceeds the requested minimum of distinct frames. Source images are transparent, indexed PNGs with a maximum of 16 palette entries and binary alpha. The source kit colours are recorded separately for each character in the manifest, so recolouring preserves independent shorts/socks roles even when their colours look similar.

A nominal **32×40** body uses padded, constant-size frame canvases: **65×57** for outfield players, **97×65** for the goalkeeper. The larger transparent margins accommodate kicks, jumps and fully extended dives without resizing the frame. Anchors, measured from the top left, are **(32.5, 52)** and **(48.5, 58)**. Mirroring around the canvas centre preserves these anchors exactly. Airborne offsets and the gradual dive travel inside the canvas are deliberate pose motion. Scale the nominal 40-pixel body to the existing world height in a future integration, not the padded canvas height.

The manifest contains views, sheets, individual frame paths, timings, loop flags, contact-frame metadata and joint reference positions. The ball is absent from the character images and animation clock. It must remain the existing independent physics object, including during catches.

## Inspection and recovery

The original implementation uses Python/Kivy 2.3.1. `main.py:StrikerGame` draws projected world-space articulated characters using canvas lines, triangles and ellipses. `career.py:FieldPlayer` stores player positions/team/phase; `career.py:Ball` owns physical ball state. There were no existing character sprite resources to reuse. Other art consists of backgrounds, logos, coach/newspaper photographs, fonts and team data.

Relevant existing integration points, deliberately unchanged:

- `main.py`: `_start_opportunity`, `_update_buildup` — delivery sequence before aiming; `_field_player_position`, `_draw_field_players`, `_draw_player` — field-player motion/rendering.
- `shoot`, `_update_ball` — kick progression, launch and fixed-step ball physics.
- `_goalkeeper_pose`, `_goalkeeper_world_pose`, `_draw_goalkeeper` — keeper articulation and drawing. The same pose feeds limb collisions, so replacing this physics skeleton would change gameplay.
- `_collide_field_players`, `_collide_goalkeeper` — swept body/limb tests. These must continue to use the existing hitboxes, never a sprite rectangle.
- `opportunity_sequences.py` — visual pass/delivery planning. There is no independent tackle action state to connect automatically; a future adapter must respond to real existing actions rather than introduce a new gameplay action.

Current world dimensions: 7.32 m goal width, 2.44 m goal height, 2.65 m depth; ball radius 0.115 m; physics step 1/120 s; pitch half-width 34 m. Player, field-player and keeper scale constants are 0.76, 0.72 and 0.80. Field collision centres are 0.43/1.08/1.73 m high with radii 0.25/0.34/0.22 m, multiplied by field-player scale. Keeper arm segments remain the original 0.68 × scale. The existing oblique camera is at (-46, 52.5, 9.5), targeting (0, 5, 1), with 17° vertical FOV. The outfield back/three-quarter and keeper front/profile views are intended for this perspective; their in-game projection still requires the later approved integration.

Before adding any phase-1 files, a recovery branch was created:

```
recovery/sprites-phase1-2026-11-05
51d2ef9f6780c5e962e70515925638a4d1446c05
```

The initial worktree already contained unrelated edits. They were preserved, not committed or reset. Their binary diff, snapshots and SHA-256 manifest are stored locally at `/workspace/striker-runtime/sprites-phase1/recovery/`. The branch preserves committed source; the patch and snapshots preserve the previously uncommitted work as well. Do not blindly reset the worktree to that branch. This phase only adds the sprite lab, assets, its tests/docs, and a build-log entry.

[Source preservation evidence](source-preservation.json) records comparison with all 589 initially tracked files before the intentional documentation log append. Main game code, physics, existing graphics, kits, app version and saves were not changed.

## Animation and texture architecture

`tools/sprite_lab/animation.py` is a deterministic, dt-driven presentation clock: select, speed, pause, step, loop/one-shot and event selection. Its `event()` contract accepts RUN/PASS/SHOOT/TACKLE/MOVE/RECOVER, and DIVE plus a side. It is **not connected to the game**. Production clips can hold their final frame by disabling preview repeat. Action completion and return to idle belong to the future existing-game adapter.

`textures.py` loads a source image once, recolours its role palette once per kit and caches the resulting texture. The LRU limit is 32 recoloured textures in the viewer. Animation regions share one sheet texture; changing frame does not upload another image. Both texture filters are `nearest`. The finite source collection is retained as pixel buffers, measured in the validation report. No Pillow, OpenCV, NumPy or shaders are needed at runtime. The implementation uses Kivy APIs available on Android, but **Android compatibility and device performance have not yet been tested**.

## Rebuild and verification

Pillow is a development dependency for generation/tests/previews only:

```sh
python -m pip install Pillow
python tools/sprite_lab/build_assets.py
python -m tools.sprite_lab.build_preview
python -m unittest discover -s tests/sprite_lab -v
python ui_tests/sprite_lab/smoke_viewer.py
python -m compileall -q tools/sprite_viewer.py tools/sprite_lab tests/sprite_lab ui_tests/sprite_lab
```

The Kivy smoke uses a real SDL2/OpenGL window. On this headless Linux host it was run with `SDL_VIDEODRIVER=offscreen`, `KIVY_HOME=/tmp/scorer-sprite-kivy` and `MESA_SHADER_CACHE_DIR=/tmp/mesa-sprite`. Missing optional system clipboard tools produce Kivy provider warnings but do not prevent this viewer from running.

Checks cover all required/distinct frame counts; binary transparency; palette constraints; canvas consistency; transparent margins/no clipping; atlas/individual PNG equality; centered anchors; clock timing, pause, step, event selection and one-shot completion. The real Kivy smoke traverses all 168 frames, both views and every display mode; checks atlas crops against individual PNG bytes, nearest filters, mirroring, controls, layouts, and zero additional texture allocation in 2,000 warmed updates. It also renders 120 frames through SDL2/Mesa. [Measured results](validation.json) distinguish the CPU update loop from actual rendering; they are **desktop measurements**, not Android performance claims.

Initial validation exposed a head-stamp mask error, an unwritable texture-coordinate property, a palette-role variable collision and an overly strict small-window stage-height assertion. These were corrected before the final passing run. No main-game regression run, APK or Android-device validation is claimed because the graphics have not been integrated.

## Approval boundary

Review the run, kick, tackle, header, dive and recovery sequences in motion, including the back/front views and both facing directions. Check proportions, palette, natural limb motion and the fixed ground anchors. Phase 1 stopped for visual approval as requested in sections 9 and 11. The owner approved revision 2 on 2026-11-06. These exact resources are now connected to the existing game; see the release report for integration tests and the pending physical-device check.
