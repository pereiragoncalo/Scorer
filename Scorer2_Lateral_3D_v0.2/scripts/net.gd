extends Node3D
## Physical-looking 3D net made from a single line mesh, with shader-driven impact ripple.

var net_material: ShaderMaterial
var time_after_hit: float = 100.0
var event_strength: float = 0.0
var scoring_side: float = 1.0
var impact_local: Vector3 = Vector3.ZERO

func setup(goal_x: float, direction: float, half_width: float, goal_height: float) -> void:
    position.x = goal_x
    scoring_side = direction
    var verts: PackedVector3Array = PackedVector3Array()
    var depth: float = 2.8
    var steps_z: int = 21
    var steps_y: int = 9
    var steps_x: int = 9
    # Back face, two side walls and roof; the front is left open for the ball.
    for row in range(steps_y):
        var y: float = goal_height * float(row) / float(steps_y - 1)
        _segment(verts, Vector3(direction * depth, y, -half_width), Vector3(direction * depth, y, half_width))
    for col in range(steps_z):
        var z: float = -half_width + 2.0 * half_width * float(col) / float(steps_z - 1)
        _segment(verts, Vector3(direction * depth, 0, z), Vector3(direction * depth, goal_height, z))
        _segment(verts, Vector3(0, goal_height, z), Vector3(direction * depth, goal_height, z))
    for col in range(steps_x):
        var x: float = direction * depth * float(col) / float(steps_x - 1)
        _segment(verts, Vector3(x, goal_height, -half_width), Vector3(x, goal_height, half_width))
        for z in [-half_width, half_width]:
            _segment(verts, Vector3(x, 0, z), Vector3(x, goal_height, z))
    for row in range(steps_y):
        var yy: float = goal_height * float(row) / float(steps_y - 1)
        for z in [-half_width, half_width]:
            _segment(verts, Vector3(0, yy, z), Vector3(direction * depth, yy, z))
    var arrays: Array = []
    arrays.resize(Mesh.ARRAY_MAX)
    arrays[Mesh.ARRAY_VERTEX] = verts
    var mesh: ArrayMesh = ArrayMesh.new()
    mesh.add_surface_from_arrays(Mesh.PRIMITIVE_LINES, arrays)
    var visual: MeshInstance3D = MeshInstance3D.new()
    visual.name = "AnimatedNetMesh"
    visual.mesh = mesh
    var shader: Shader = Shader.new()
    shader.code = """
shader_type spatial;
render_mode unshaded, cull_disabled, depth_draw_never;
uniform float hit_energy = 0.0;
uniform float time_since_hit = 100.0;
uniform vec3 impact_point = vec3(0.0, 1.2, 0.0);
void vertex() {
    float radius = distance(VERTEX, impact_point);
    float decay = exp(-max(time_since_hit, 0.0) * 3.4);
    float pulse = sin(radius * 5.8 - time_since_hit * 18.0);
    VERTEX.x += hit_energy * pulse * decay * exp(-radius * 0.6) * 0.62;
}
void fragment() {
    ALBEDO = vec3(0.85, 0.94, 1.0);
    ALPHA = 0.78;
}
"""
    net_material = ShaderMaterial.new()
    net_material.shader = shader
    visual.material_override = net_material
    add_child(visual)

func _process(delta: float) -> void:
    if event_strength <= 0.0:
        return
    time_after_hit += delta
    net_material.set_shader_parameter("time_since_hit", time_after_hit)
    if time_after_hit > 3.0:
        event_strength = 0.0
        net_material.set_shader_parameter("hit_energy", 0.0)

func impact(hit_point_global: Vector3) -> void:
    impact_local = to_local(hit_point_global)
    time_after_hit = 0.0
    event_strength = 1.0
    net_material.set_shader_parameter("impact_point", impact_local)
    net_material.set_shader_parameter("hit_energy", 1.0)
    net_material.set_shader_parameter("time_since_hit", 0.0)

func _segment(target: PackedVector3Array, a: Vector3, b: Vector3) -> void:
    target.append(a)
    target.append(b)
