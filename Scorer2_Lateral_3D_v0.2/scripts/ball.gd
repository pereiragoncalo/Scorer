extends Node3D
## Bola experimental de atualizacao manual. Em versoes futuras usar fisica e animacao dedicadas.

var velocity: Vector3 = Vector3.ZERO
var flying: bool = false
var spin: float = 0.0
const RADIUS: float = 0.23

func _ready() -> void:
    var model: MeshInstance3D = MeshInstance3D.new()
    model.name = "Football"
    var mesh: SphereMesh = SphereMesh.new()
    mesh.radius = RADIUS
    mesh.height = RADIUS * 2.0
    mesh.radial_segments = 24
    mesh.rings = 12
    model.mesh = mesh
    var white: StandardMaterial3D = StandardMaterial3D.new()
    white.albedo_color = Color("#f9fbfc")
    white.roughness = 0.72
    model.material_override = white
    add_child(model)
    for offset in [Vector3(0, RADIUS, 0), Vector3(0, -RADIUS, 0), Vector3(RADIUS, 0, 0), Vector3(-RADIUS, 0, 0), Vector3(0, 0, RADIUS), Vector3(0, 0, -RADIUS)]:
        var patch: MeshInstance3D = MeshInstance3D.new()
        var patch_mesh: SphereMesh = SphereMesh.new()
        patch_mesh.radius = 0.067
        patch_mesh.height = 0.134
        patch_mesh.radial_segments = 8
        patch_mesh.rings = 4
        patch.mesh = patch_mesh
        var black: StandardMaterial3D = StandardMaterial3D.new()
        black.albedo_color = Color("#121c29")
        patch.material_override = black
        patch.position = offset * 0.85
        add_child(patch)

func kick(direction: Vector3, power: float, lift: float = 1.9) -> void:
    var planar: Vector3 = Vector3(direction.x, 0, direction.z).normalized()
    if planar.length() < 0.01:
        planar = Vector3.FORWARD
    velocity = planar * power + Vector3.UP * lift
    flying = true

func tick(delta: float) -> void:
    if not flying:
        return
    velocity.y -= 18.0 * delta
    position += velocity * delta
    if position.y < RADIUS:
        position.y = RADIUS
        if velocity.y < -1.0:
            velocity.y = -velocity.y * 0.33
        else:
            velocity.y = 0.0
        velocity.x *= maxf(0.0, 1.0 - delta * 1.65)
        velocity.z *= maxf(0.0, 1.0 - delta * 1.65)
    if absf(position.z) > 29.0:
        velocity.z = -velocity.z * 0.45
        position.z = clampf(position.z, -29.0, 29.0)
    rotation.x += velocity.z * delta * 1.9
    rotation.z -= velocity.x * delta * 1.9
    if velocity.length() < 0.65 and position.y <= RADIUS + 0.02:
        flying = false
        velocity = Vector3.ZERO

func attach_to(position3d: Vector3) -> void:
    flying = false
    velocity = Vector3.ZERO
    position = Vector3(position3d.x, RADIUS, position3d.z)
