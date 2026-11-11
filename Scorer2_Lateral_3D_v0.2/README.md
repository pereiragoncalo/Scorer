# Scorer 2 — Opportunities v0.3.1 camera correction

This experimental Godot application keeps the Scorer 1 match-opportunity loop.
**There is no free player movement**, and no controls for dribbling or passing.

## Fix from reported Android screenshot

- Corrects camera placed inside a grandstand at Z=-46, with a foreground blue supporter flag obscuring the goal.
- Moves camera to the clear sideline at Z=+32, at an elevated diagonal angle.
- Uses a fixed orthographic view to include the shooting player and near goal on a landscape phone.
- Removes all waving flags, camera-side safety rail and foreground ad boards that can cover the pitch.
- Shot aiming, match timeline, goalkeeper AI and goals are unchanged.

Temporary Android package: `com.clemir.scorer2.opportunities.camfix`
(Separate from both Scorer 1 and the previous v0.3 test build, so Android installation is not blocked by the test signing key.)

This is not a FIFA-level graphical product and has only placeholder procedural player meshes.
The Scorer 1 code and `main` branch have not been altered.

# Scorer 2 — Lateral 2.5D (Godot 4.7.2)

**Independent prototype** — entirely new Godot 4 GDScript code, without using Scorer 1 Python/Kivy source. Android prototype package: `com.clemir.scorer2.lateral`.

## Vertical slice v0.2

- Locked **side-on** orthographic tracking camera. Forward play is left to right, with depth towards/away from camera.
- 3D modelled athletes built from articulated rounded anatomical forms, with procedural running, diverse skin tones, hair, shirt numbers, team kits and goal celebration.
- Physical-looking 3D posts and net mesh (sidewalls, back panel and roof) with animated impact ripple on goals.
- Low-cost 3D stadium with **1,400 individual spectator bodies and heads**, supporter flags, lighting pylons and ad boards.
- Stadium/pitch, pass, shot, sprint, rudimentary opponent AI, goalkeeper, goals, controls and scoreboard.
- Landscape Android touch controls; keyboard: WASD/arrows, Space to shoot, F to pass, Shift sprint, R reset.

## Reality check

Not FIFA/PES quality, and not a complete game. The people are procedural placeholder meshes rather than motion-captured rigged humans. To approach modern console fidelity we will need licensed fully rigged player characters, high-quality stadium meshes, ball/net contact physics, recorded animation and mobile optimization.

## Isolation

The Scorer 1 main branch, Python/Kivy files and Android package are untouched. This experiment is a fully separate folder with its own scene and scripts. It can be moved into an entirely independent GitHub repository.

## Build

Import `project.godot` with Godot 4.7.2 and export the Android preset after installing Android SDK/JDK and export templates. A debug APK generated in GitHub Actions uses an ephemeral signing key, so install it separately from previous experimental builds (a dedicated package name is used here).
