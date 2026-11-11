extends Node3D
## Stadium banks and hundreds of individually coloured 3D spectators.
## Two instanced draw calls serve the entire crowd, suitable for Android.

var phase: float = 0.0
var waving_flags: Array[Node3D] = []

func _ready() -> void:
    _create_stands()
    _create_spectators()
    _create_ads()

func _process(delta: float) -> void:
    phase += delta
    for i in range(waving_flags.size()):
        var flag: Node3D = waving_flags[i]
        flag.rotation.z = sin(phase * (1.55 + i * 0.12)) * 0.22

func _create_stands() -> void:
    _box("Track", Vector3(0, -0.22, -36), Vector3(120, 0.35, 15), Color("#333e48"))
    _box("StadiumBackdrop", Vector3(0, 13.3, -60), Vector3(125, 23, 1.0), Color("#0b1a30"))
    for row in range(14):
        var y: float = 0.65 + float(row) * 0.82
        var z: float = -32.7 - float(row) * 1.55
        var c: Color = Color("#294353") if row % 2 == 0 else Color("#1e3547")
        _box("Terrace", Vector3(0, y - 0.31, z), Vector3(114, 0.55, 1.8), c)
    _box("StandUpperRail", Vector3(0, 13.1, -55.3), Vector3(118, 0.23, 0.22), Color("#c7dce8"))
    for x in [-56.0, -37.0, -18.0, 0.0, 18.0, 37.0, 56.0]:
        _box("Stairway", Vector3(x, 6.5, -44.0), Vector3(1.2, 0.2, 24), Color("#97a2b0"))
    # Never create a camera-side rail: it occludes the field in lateral views.
    for i in range(4):
        var x: float = -50.0 if i % 2 == 0 else 50.0
        var z: float = -42.0 if i < 2 else 42.0
        _box("FloodlightPylon", Vector3(x, 9.0, z), Vector3(0.3, 18, 0.3), Color("#a8b6c6"))
        _box("LightCluster", Vector3(x, 18.4, z), Vector3(4.3, 2.0, 0.54), Color("#f0f6fc"))

func _create_spectators() -> void:
    var bodies: MultiMesh = MultiMesh.new()
    bodies.transform_format = MultiMesh.TRANSFORM_3D
    bodies.use_colors = true
    var body_mesh: CapsuleMesh = CapsuleMesh.new()
    body_mesh.radius = 0.32
    body_mesh.height = 0.78
    body_mesh.radial_segments = 8
    body_mesh.rings = 2
    bodies.mesh = body_mesh
    var heads: MultiMesh = MultiMesh.new()
    heads.transform_format = MultiMesh.TRANSFORM_3D
    heads.use_colors = true
    var head_mesh: SphereMesh = SphereMesh.new()
    head_mesh.radial_segments = 8
    head_mesh.rings = 4
    heads.mesh = head_mesh
    var crowd_count: int = 14 * 100
    bodies.instance_count = crowd_count
    heads.instance_count = crowd_count
    var palette: Array[Color] = [Color("#d5e2ee"),Color("#1f86ac"),Color("#f1c64b"),Color("#a52e48"),Color("#356b59"),Color("#283349"),Color("#e8ebf5")]
    var skins: Array[Color] = [Color("#f0caac"),Color("#cf9872"),Color("#8c6046"),Color("#b67651")]
    for row in range(14):
        for col in range(100):
            var idx: int = row * 100 + col
            var seed: int = idx * 149 + 31
            var x: float = -56.0 + float(col) * 1.12 + float(seed % 19) * 0.006
            var y: float = 1.12 + float(row) * 0.82 + float(seed % 7) * 0.021
            var z: float = -32.7 - float(row) * 1.55
            var torso_transform: Transform3D = Transform3D(Basis().scaled(Vector3(0.88, 0.89 + float(seed % 7) * 0.03, 0.91)),Vector3(x, y, z))
            bodies.set_instance_transform(idx, torso_transform)
            bodies.set_instance_color(idx, palette[(seed / 19) % palette.size()])
            heads.set_instance_transform(idx,Transform3D(Basis().scaled(Vector3(0.25, 0.29, 0.24)),Vector3(x, y + 0.62, z)))
            heads.set_instance_color(idx, skins[(seed / 11) % skins.size()])
    var material: StandardMaterial3D = StandardMaterial3D.new()
    material.vertex_color_use_as_albedo = true
    material.roughness = 1.0
    var body_instance: MultiMeshInstance3D = MultiMeshInstance3D.new()
    body_instance.name = "SpectatorBodies"
    body_instance.multimesh = bodies
    body_instance.material_override = material
    body_instance.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
    add_child(body_instance)
    var head_instance: MultiMeshInstance3D = MultiMeshInstance3D.new()
    head_instance.name = "SpectatorHeads"
    head_instance.multimesh = heads
    head_instance.material_override = material
    head_instance.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
    add_child(head_instance)
    # No giant waving flags close to the camera. Stadium props must not
    # cover the goal or shooting lane, especially on a small phone display.

func _create_ads() -> void:
    for i in range(12):
        var x: float = -55.0 + float(i) * 10.0
        var color: Color = Color("#0e5270") if i % 3 == 0 else (Color("#104c42") if i % 3 == 1 else Color("#252b4b"))
        _box("PitchAdvertising", Vector3(x, 0.58, -30.4), Vector3(9.65, 1.2, 0.22), color)
        if i % 2 == 0:
            var nameplate: Label3D = Label3D.new()
            nameplate.text = "SCORER 2" if i % 4 == 0 else "FOOTBALL EVOLUTION"
            nameplate.font_size = 64
            nameplate.pixel_size = 0.006
            nameplate.position = Vector3(x, 0.65, -30.24)
            nameplate.modulate = Color("#dcf6f7")
            add_child(nameplate)

func _box(label: String, at: Vector3, dims: Vector3, tint: Color, parent_node: Node3D = null) -> void:
    var box: MeshInstance3D = MeshInstance3D.new()
    box.name = label
    var mesh: BoxMesh = BoxMesh.new()
    mesh.size = dims
    box.mesh = mesh
    box.position = at
    var mat: StandardMaterial3D = StandardMaterial3D.new()
    mat.albedo_color = tint
    mat.roughness = 0.9
    box.material_override = mat
    if parent_node == null:
        add_child(box)
    else:
        parent_node.add_child(box)
