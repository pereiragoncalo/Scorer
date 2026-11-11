# Scorer 2 technical separation

- Independent Godot 4 project, **never import Scorer 1 Python code**.
- Direction of play is left-to-right on screen. Pitch long axis = world X. Width = world Z. Up = world Y.
- Camera is ortho `Camera3D` from +Z looking across the pitch. It follows only the X position, with no change in azimuth.
- `scripts/match.gd`: game controller, controls, rules and camera.
- `scripts/athlete.gd`: self-contained procedural 3D character, with simple manually animated limb joints.
- `scripts/crowd.gd`: MultiMesh crowd for low mobile draw-call cost.
- `scripts/net.gd`: 3D goal mesh and shader deformation on scored goal.
- `scripts/ball.gd`: standalone ball flight model.
- No server and no external AI inference.

## Next milestones

1. Device verification of side camera and FPS.
2. Replace procedural characters with original/appropriately licensed skinned GLB avatars and AnimationTree motion sets.
3. Refine goal geometry, real contact/physics and mesh deformation.
4. Expand crowd from repeated meshes to varied animations and LODs.
5. Add complete career as a separate simulation module.
