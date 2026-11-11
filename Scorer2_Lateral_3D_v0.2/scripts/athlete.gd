extends Node3D
## A character made out of anatomical 3D meshes and a procedural joint hierarchy.
## The scene can be replaced with licensed .glb skinned humanoids later.

var team_id: int = 0
var motion_phase: float = 0.0
var animation_speed: float = 0.0
var rig: Node3D
var left_thigh: Node3D
var right_thigh: Node3D
var left_shin: Node3D
var right_shin: Node3D
var left_arm: Node3D
var right_arm: Node3D
var left_forearm: Node3D
var right_forearm: Node3D
var shirt_color: Color
var skin: Color
var goal_celebration: float = 0.0

func setup(number: int, jersey: Color, shorts: Color, side: int) -> void:
    team_id = side
    shirt_color = jersey
    var skin_palette: Array[Color] = [Color("#d3a076"), Color("#ba7956"), Color("#f0c6a3"), Color("#85543c"), Color("#ba8a71")]
    skin = skin_palette[number % skin_palette.size()]
    var hair_palette: Array[Color] = [Color("#151a23"), Color("#3c271f"), Color("#221a14"), Color("#7d4f2f")]
    rig = Node3D.new()
    rig.name = "AthleteRig"
    add_child(rig)
    _ellipsoid("Pelvis", Vector3(0, 0.91, 0), Vector3(0.29, 0.19, 0.19), shorts, rig)
    _taper("Jersey", Vector3(0, 1.35, 0), 0.295, 0.235, 0.62, jersey, rig)
    _ellipsoid("Shoulders", Vector3(0, 1.54, 0), Vector3(0.34, 0.13, 0.21), jersey, rig)
    _ellipsoid("Collar", Vector3(0, 1.67, 0), Vector3(0.137, 0.07, 0.135), Color("#e7e7dd"), rig)
    _taper("Neck", Vector3(0, 1.76, 0), 0.085, 0.081, 0.17, skin, rig)
    _ellipsoid("Head", Vector3(0, 1.995, 0), Vector3(0.176, 0.228, 0.160), skin, rig)
    _ellipsoid("HairTop", Vector3(0, 2.175, 0.012), Vector3(0.178, 0.080, 0.164), hair_palette[number % hair_palette.size()], rig)
    _ellipsoid("LeftEar", Vector3(-0.175, 2.00, 0), Vector3(0.037, 0.065, 0.041), skin, rig)
    _ellipsoid("RightEar", Vector3(0.175, 2.00, 0), Vector3(0.037, 0.065, 0.041), skin, rig)
    _ellipsoid("EyeL", Vector3(-0.065, 2.028, -0.151), Vector3(0.025, 0.015, 0.013), Color("#151f2c"), rig)
    _ellipsoid("EyeR", Vector3(0.065, 2.028, -0.151), Vector3(0.025, 0.015, 0.013), Color("#151f2c"), rig)
    _taper("JerseyStripe", Vector3(0, 1.35, -0.186), 0.041, 0.041, 0.52, Color.WHITE if team_id == 0 else Color("#ffdcb6"), rig)
    var digits: Label3D = Label3D.new()
    digits.name = "ShirtNumber"
    digits.text = str(number)
    digits.font_size = 48
    digits.pixel_size = 0.006
    digits.outline_size = 0
    digits.modulate = Color("#f6fbff")
    digits.position = Vector3(0, 1.37, 0.204)
    rig.add_child(digits)

    left_thigh = _joint("LeftHip", Vector3(-0.155, 0.86, 0), rig)
    right_thigh = _joint("RightHip", Vector3(0.155, 0.86, 0), rig)
    _ellipsoid("LeftShort", Vector3(0, -0.095, 0), Vector3(0.154, 0.22, 0.158), shorts, left_thigh)
    _ellipsoid("RightShort", Vector3(0, -0.095, 0), Vector3(0.154, 0.22, 0.158), shorts, right_thigh)
    _taper("LeftThigh", Vector3(0, -0.285, 0), 0.115, 0.14, 0.40, skin, left_thigh)
    _taper("RightThigh", Vector3(0, -0.285, 0), 0.115, 0.14, 0.40, skin, right_thigh)
    left_shin = _joint("LeftKnee", Vector3(0, -0.48, 0), left_thigh)
    right_shin = _joint("RightKnee", Vector3(0, -0.48, 0), right_thigh)
    _ellipsoid("LeftKneeCap", Vector3.ZERO, Vector3(0.12, 0.13, 0.115), skin, left_shin)
    _ellipsoid("RightKneeCap", Vector3.ZERO, Vector3(0.12, 0.13, 0.115), skin, right_shin)
    _taper("LeftSock", Vector3(0, -0.25, 0), 0.106, 0.125, 0.42, jersey, left_shin)
    _taper("RightSock", Vector3(0, -0.25, 0), 0.106, 0.125, 0.42, jersey, right_shin)
    _ellipsoid("LeftBoot", Vector3(0, -0.455, -0.092), Vector3(0.14, 0.09, 0.255), Color("#171a20"), left_shin)
    _ellipsoid("RightBoot", Vector3(0, -0.455, -0.092), Vector3(0.14, 0.09, 0.255), Color("#171a20"), right_shin)

    left_arm = _joint("LeftShoulder", Vector3(-0.335, 1.57, 0), rig)
    right_arm = _joint("RightShoulder", Vector3(0.335, 1.57, 0), rig)
    left_arm.rotation.z = -0.16
    right_arm.rotation.z = 0.16
    _ellipsoid("LeftSleeve", Vector3(0, -0.10, 0), Vector3(0.15, 0.19, 0.165), jersey, left_arm)
    _ellipsoid("RightSleeve", Vector3(0, -0.10, 0), Vector3(0.15, 0.19, 0.165), jersey, right_arm)
    _taper("LeftUpperArm", Vector3(0, -0.26, 0), 0.090, 0.103, 0.28, skin, left_arm)
    _taper("RightUpperArm", Vector3(0, -0.26, 0), 0.090, 0.103, 0.28, skin, right_arm)
    left_forearm = _joint("LeftElbow", Vector3(0, -0.40, 0), left_arm)
    right_forearm = _joint("RightElbow", Vector3(0, -0.40, 0), right_arm)
    _taper("LeftForearm", Vector3(0, -0.15, 0), 0.077, 0.093, 0.31, skin, left_forearm)
    _taper("RightForearm", Vector3(0, -0.15, 0), 0.077, 0.093, 0.31, skin, right_forearm)
    _ellipsoid("LeftHand", Vector3(0, -0.32, 0), Vector3(0.088, 0.105, 0.083), skin, left_forearm)
    _ellipsoid("RightHand", Vector3(0, -0.32, 0), Vector3(0.088, 0.105, 0.083), skin, right_forearm)
    _build_shadow()
    set_meta("shirt_number", number)

func _build_shadow() -> void:
    var disc: MeshInstance3D = MeshInstance3D.new()
    disc.name = "GroundContactShadow"
    var circle: CylinderMesh = CylinderMesh.new()
    circle.top_radius = 0.44
    circle.bottom_radius = 0.44
    circle.height = 0.006
    circle.radial_segments = 20
    disc.mesh = circle
    var mat: StandardMaterial3D = _material(Color(0, 0.04, 0.03, 0.32))
    mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
    mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
    disc.material_override = mat
    disc.position.y = 0.085
    add_child(disc)

func celebrate() -> void:
    goal_celebration = 1.8

func animate_motion(speed_ratio: float, delta: float) -> void:
    animation_speed = lerpf(animation_speed, clampf(speed_ratio, 0.0, 1.0), minf(1.0, delta * 8.0))
    motion_phase += delta * (2.0 + animation_speed * 12.5)
    var step_wave: float = sin(motion_phase) * 0.79 * animation_speed
    left_thigh.rotation.x = step_wave
    right_thigh.rotation.x = -step_wave
    left_shin.rotation.x = maxf(0, -step_wave) * 0.8
    right_shin.rotation.x = maxf(0, step_wave) * 0.8
    left_arm.rotation.x = -step_wave * 0.8
    right_arm.rotation.x = step_wave * 0.8
    left_forearm.rotation.x = -0.18 + absf(step_wave) * 0.35
    right_forearm.rotation.x = -0.18 + absf(step_wave) * 0.35
    rig.position.y = absf(sin(motion_phase)) * 0.065 * animation_speed
    rig.rotation.z = sin(motion_phase * 0.5) * 0.018 * animation_speed
    if goal_celebration > 0:
        goal_celebration = maxf(0.0, goal_celebration - delta)
        left_arm.rotation.z = lerpf(left_arm.rotation.z, -2.2, delta * 10.0)
        right_arm.rotation.z = lerpf(right_arm.rotation.z, 2.2, delta * 10.0)
    else:
        left_arm.rotation.z = lerpf(left_arm.rotation.z, -0.16, delta * 7.0)
        right_arm.rotation.z = lerpf(right_arm.rotation.z, 0.16, delta * 7.0)

func _joint(label: String, at: Vector3, parent_node: Node3D) -> Node3D:
    var n: Node3D = Node3D.new()
    n.name = label
    n.position = at
    parent_node.add_child(n)
    return n

func _material(tint: Color) -> StandardMaterial3D:
    var m: StandardMaterial3D = StandardMaterial3D.new()
    m.albedo_color = tint
    m.roughness = 0.84
    return m

func _ellipsoid(label: String, at: Vector3, size3: Vector3, tint: Color, parent_node: Node3D) -> void:
    var m: MeshInstance3D = MeshInstance3D.new()
    m.name = label
    var mesh: SphereMesh = SphereMesh.new()
    mesh.radial_segments = 16
    mesh.rings = 8
    m.mesh = mesh
    m.position = at
    m.scale = size3
    m.material_override = _material(tint)
    parent_node.add_child(m)

func _taper(label: String, at: Vector3, top_r: float, bottom_r: float, height3: float, tint: Color, parent_node: Node3D) -> void:
    var m: MeshInstance3D = MeshInstance3D.new()
    m.name = label
    var mesh: CylinderMesh = CylinderMesh.new()
    mesh.top_radius = top_r
    mesh.bottom_radius = bottom_r
    mesh.height = height3
    mesh.radial_segments = 12
    m.mesh = mesh
    m.position = at
    m.material_override = _material(tint)
    parent_node.add_child(m)
