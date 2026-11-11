extends Node3D
## SCORER 2 — lateral 2.5D, independent of the original retro Scorer game.
## Controlo: WASD/setas ou joystick tátil. Espaço / Rematar, F / Passar, Shift / Sprint.

const Athlete = preload("res://scripts/athlete.gd")
const SoccerBall = preload("res://scripts/ball.gd")
const Audience = preload("res://scripts/crowd.gd")
const Net = preload("res://scripts/net.gd")
const FIELD_HALF_X: float = 52.0
const FIELD_HALF_Z: float = 29.0
const GOAL_HALF_W: float = 3.66
const GOAL_HEIGHT: float = 2.44

var controlled
var ball
var ball_owned: bool = true
var camera: Camera3D
var bots: Array[Dictionary] = []
var elapsed: float = 0.0
var blue_score: int = 0
var red_score: int = 0
var restart_timer: float = 0.0
var status_message: String = "SCORER 2 — VISAO LATERAL 2.5D"
var joy_id: int = -1
var joy_anchor: Vector2 = Vector2.ZERO
var joy_delta: Vector2 = Vector2.ZERO
var shoot_cooldown: float = 0.0
var status_label: Label
var score_label: Label
var fps_label: Label
var joy_widget: Panel
var highlight: MeshInstance3D
var nets: Dictionary = {}
var crowd: Node3D
var previous_ball_x: float = 0.0
var goal_pause: bool = false

func _ready() -> void:
    Engine.max_fps = 60
    _build_environment()
    _build_field()
    _build_stadium()
    _build_teams()
    _build_camera()
    _build_ui()
    _kickoff()

func _physics_process(delta: float) -> void:
    elapsed += delta
    shoot_cooldown = maxf(0.0, shoot_cooldown - delta)
    if restart_timer > 0.0:
        restart_timer -= delta
        if restart_timer <= 0.0:
            _kickoff()
    else:
        _move_controlled(delta)
        _move_opponents(delta)
        if ball_owned:
            var ahead: Vector3 = controlled.global_transform.basis * Vector3(0, 0, -0.93)
            ball.attach_to(controlled.position + ahead)
        else:
            ball.tick(delta)
            if ball.position.distance_to(controlled.position + Vector3.UP * 0.23) < 1.6 and not ball.flying:
                ball_owned = true
                status_message = "BOLA RECUPERADA — PROCURA A BALIZA"
        _detect_goal()
    if is_instance_valid(highlight):
        highlight.position = Vector3(controlled.position.x, 0.062, controlled.position.z)
        highlight.rotation.y += delta * 0.6
    _update_camera(delta)
    _update_ui()

func _build_environment() -> void:
    var world: WorldEnvironment = WorldEnvironment.new()
    world.name = "StadiumAtmosphere"
    var environment: Environment = Environment.new()
    environment.background_mode = Environment.BG_COLOR
    environment.background_color = Color("#283d5f")
    environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
    environment.ambient_light_color = Color("#8fa9cc")
    environment.ambient_light_energy = 0.85
    world.environment = environment
    add_child(world)
    var sun: DirectionalLight3D = DirectionalLight3D.new()
    sun.name = "FloodlightKey"
    sun.rotation_degrees = Vector3(-57, -31, 0)
    sun.light_color = Color("#fff4de")
    sun.light_energy = 1.65
    sun.shadow_enabled = true
    add_child(sun)
    for i in range(4):
        var light: OmniLight3D = OmniLight3D.new()
        light.name = "StadiumLight%d" % i
        light.position = Vector3(-34.0 if i % 2 == 0 else 34.0, 16.0, -32.0 if i < 2 else 32.0)
        light.light_color = Color("#d3e9ff")
        light.light_energy = 0.5
        light.omni_range = 25.0
        light.shadow_enabled = false
        add_child(light)

func _build_field() -> void:
    _box("OutsideGround", Vector3(0, -0.28, 0), Vector3(160, 0.48, 95), Color("#113d30"))
    # Lengthwise view: pitch extends horizontally on screen, never along the camera axis.
    for stripe in range(20):
        var length: float = FIELD_HALF_X * 2.0 / 20.0
        var x: float = -FIELD_HALF_X + (float(stripe) + 0.5) * length
        _box("GrassStripe%02d" % stripe, Vector3(x, 0.01, 0), Vector3(length, 0.055, FIELD_HALF_Z * 2.0), Color("#257448") if stripe % 2 == 0 else Color("#1e6942"))
    var white: Color = Color("#eaf5e9")
    _pitch_line(Vector3(-FIELD_HALF_X, 0, -FIELD_HALF_Z), Vector3(FIELD_HALF_X, 0, -FIELD_HALF_Z), white)
    _pitch_line(Vector3(-FIELD_HALF_X, 0, FIELD_HALF_Z), Vector3(FIELD_HALF_X, 0, FIELD_HALF_Z), white)
    _pitch_line(Vector3(-FIELD_HALF_X, 0, -FIELD_HALF_Z), Vector3(-FIELD_HALF_X, 0, FIELD_HALF_Z), white)
    _pitch_line(Vector3(FIELD_HALF_X, 0, -FIELD_HALF_Z), Vector3(FIELD_HALF_X, 0, FIELD_HALF_Z), white)
    _pitch_line(Vector3(0, 0, -FIELD_HALF_Z), Vector3(0, 0, FIELD_HALF_Z), white)
    _field_circle(Vector3.ZERO, 9.15, white)
    for sign in [-1.0, 1.0]:
        var goal_x: float = sign * FIELD_HALF_X
        var penalty_x: float = sign * (FIELD_HALF_X - 16.5)
        var small_x: float = sign * (FIELD_HALF_X - 5.5)
        _pitch_line(Vector3(goal_x, 0, -20.16), Vector3(penalty_x, 0, -20.16), white)
        _pitch_line(Vector3(goal_x, 0, 20.16), Vector3(penalty_x, 0, 20.16), white)
        _pitch_line(Vector3(penalty_x, 0, -20.16), Vector3(penalty_x, 0, 20.16), white)
        _pitch_line(Vector3(goal_x, 0, -9.16), Vector3(small_x, 0, -9.16), white)
        _pitch_line(Vector3(goal_x, 0, 9.16), Vector3(small_x, 0, 9.16), white)
        _pitch_line(Vector3(small_x, 0, -9.16), Vector3(small_x, 0, 9.16), white)
        _field_circle(Vector3(sign * (FIELD_HALF_X - 11.0), 0, 0), 0.15, white)
        _goal(sign)

func _build_stadium() -> void:
    crowd = Audience.new()
    crowd.name = "InstancedAnimatedStadiumAudience"
    add_child(crowd)
    # Camera-side advertising boards omitted in the opportunity view.
    # Foreground props may never conceal the aiming zone or shot trajectory.

func _goal(direction: float) -> void:
    var x: float = direction * FIELD_HALF_X
    var back_x: float = x + direction * 2.8
    var post: Color = Color("#fbfbf5")
    _tube("NearGoalpost", Vector3(x, 0, GOAL_HALF_W), Vector3(x, GOAL_HEIGHT, GOAL_HALF_W), 0.085, post)
    _tube("FarGoalpost", Vector3(x, 0, -GOAL_HALF_W), Vector3(x, GOAL_HEIGHT, -GOAL_HALF_W), 0.085, post)
    _tube("Crossbar", Vector3(x, GOAL_HEIGHT, -GOAL_HALF_W), Vector3(x, GOAL_HEIGHT, GOAL_HALF_W), 0.085, post)
    _tube("BackTopNear", Vector3(x, GOAL_HEIGHT, GOAL_HALF_W), Vector3(back_x, GOAL_HEIGHT, GOAL_HALF_W), 0.045, Color("#d6e3ed"))
    _tube("BackTopFar", Vector3(x, GOAL_HEIGHT, -GOAL_HALF_W), Vector3(back_x, GOAL_HEIGHT, -GOAL_HALF_W), 0.045, Color("#d6e3ed"))
    _tube("BackBar", Vector3(back_x, GOAL_HEIGHT, -GOAL_HALF_W), Vector3(back_x, GOAL_HEIGHT, GOAL_HALF_W), 0.04, Color("#d6e3ed"))
    var net: Node3D = Net.new()
    net.name = "True3DGoalNet_%s" % str(direction)
    add_child(net)
    net.setup(x, direction, GOAL_HALF_W, GOAL_HEIGHT)
    nets[int(direction)] = net

func _build_teams() -> void:
    var blue: Color = Color("#1599cb")
    var red: Color = Color("#d84155")
    controlled = Athlete.new()
    controlled.name = "Scorer2_UserControlledAthlete"
    controlled.setup(9, blue, Color("#12314d"), 0)
    add_child(controlled)
    for i in range(4):
        var ally: Node3D = Athlete.new()
        ally.name = "BlueAI_%d" % i
        ally.setup(i + 2, blue, Color("#12314d"), 0)
        add_child(ally)
        bots.append({"node": ally, "team": 0, "home": Vector3(-22.0 + 12.0 * float(i), 0, -16.0 + 9.0 * float(i)), "speed": 4.4, "keeper": false})
    for i in range(4):
        var enemy: Node3D = Athlete.new()
        enemy.name = "RedAI_%d" % i
        enemy.setup(i + 2, red, Color("#4e1b31"), 1)
        add_child(enemy)
        bots.append({"node": enemy, "team": 1, "home": Vector3(1.0 + 12.0 * float(i), 0, -14.0 + 9.0 * float(i)), "speed": 3.6, "keeper": false})
    var keeper: Node3D = Athlete.new()
    keeper.name = "RedGoalkeeper"
    keeper.setup(1, Color("#f0b13c"), Color("#1c2449"), 1)
    add_child(keeper)
    bots.append({"node": keeper, "team": 1, "home": Vector3(FIELD_HALF_X - 1.8, 0, 0), "speed": 5.4, "keeper": true})
    ball = SoccerBall.new()
    ball.name = "Scorer2MatchBall"
    add_child(ball)
    highlight = MeshInstance3D.new()
    highlight.name = "SelectedPlayerRing"
    var ring_mesh: TorusMesh = TorusMesh.new()
    ring_mesh.inner_radius = 0.67
    ring_mesh.outer_radius = 0.74
    highlight.mesh = ring_mesh
    var ring_mat: StandardMaterial3D = StandardMaterial3D.new()
    ring_mat.albedo_color = Color("#dafa65")
    ring_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
    highlight.material_override = ring_mat
    add_child(highlight)

func _build_camera() -> void:
    camera = Camera3D.new()
    camera.name = "LockedSideProfileCamera_2point5D"
    camera.current = true
    camera.projection = Camera3D.PROJECTION_ORTHOGONAL
    camera.size = 25.5
    camera.near = 0.1
    camera.far = 180.0
    camera.position = Vector3(-15, 12.0, 56.0)
    add_child(camera)
    camera.look_at(Vector3(-15, 1.1, -2.5), Vector3.UP)

func _build_ui() -> void:
    var layer: CanvasLayer = CanvasLayer.new()
    layer.name = "MatchHUD"
    add_child(layer)
    var ui: Control = Control.new()
    ui.name = "Overlay"
    ui.set_anchors_preset(Control.PRESET_FULL_RECT)
    ui.mouse_filter = Control.MOUSE_FILTER_IGNORE
    layer.add_child(ui)
    _ui_rect(ui, Vector2(375, 18), Vector2(530, 86), Color(0.05, 0.11, 0.18, 0.84))
    score_label = _ui_label(ui, "SCORER 2", Vector2(0, 33), Vector2(1280, 46), 37, Color.WHITE)
    score_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    _ui_rect(ui, Vector2(26, 22), Vector2(248, 64), Color(0.05, 0.11, 0.18, 0.72))
    _ui_label(ui, "LATERAL 2.5D", Vector2(40, 38), Vector2(226, 40), 21, Color("#8fe5f8"))
    status_label = _ui_label(ui, "CAMARA LATERAL — FUTEBOL 2.5D", Vector2(375, 112), Vector2(530, 44), 19, Color("#e9f8fd"))
    status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    fps_label = _ui_label(ui, "", Vector2(960, 22), Vector2(280, 42), 18, Color("#c4d5dc"))
    fps_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
    joy_widget = Panel.new()
    joy_widget.mouse_filter = Control.MOUSE_FILTER_IGNORE
    joy_widget.position = Vector2(78, 482)
    joy_widget.size = Vector2(156, 156)
    var circle_style: StyleBoxFlat = StyleBoxFlat.new()
    circle_style.bg_color = Color(0.05, 0.12, 0.18, 0.45)
    circle_style.border_color = Color(0.54, 0.89, 0.96, 0.65)
    circle_style.set_border_width_all(3)
    circle_style.set_corner_radius_all(78)
    joy_widget.add_theme_stylebox_override("panel", circle_style)
    ui.add_child(joy_widget)
    _ui_label(ui, "MOVER", Vector2(122, 640), Vector2(140, 30), 18, Color("#e6edf4"))
    _hud_button(ui, "REMATAR", Vector2(1075, 525), Vector2(168, 68), Color("#e99346"), _shoot)
    _hud_button(ui, "PASSAR", Vector2(905, 608), Vector2(154, 60), Color("#4195c3"), _pass_ball)
    _hud_button(ui, "SPRINT", Vector2(1090, 615), Vector2(148, 60), Color("#54786f"), _sprint_tap)
    _hud_button(ui, "REINICIAR", Vector2(30, 23), Vector2(0, 0), Color("#1b3040"), _kickoff, false)
    _ui_label(ui, "Lateral 2.5D | 3D offline | v0.2", Vector2(408, 684), Vector2(500, 26), 15, Color("#a1bac6"))

func _hud_button(ui: Control, title: String, position2: Vector2, size2: Vector2, color: Color, action: Callable, visible: bool = true) -> void:
    if not visible:
        return
    var button: Button = Button.new()
    button.text = title
    button.position = position2
    button.size = size2
    button.add_theme_font_size_override("font_size", 22)
    button.add_theme_color_override("font_color", Color.WHITE)
    var style: StyleBoxFlat = StyleBoxFlat.new()
    style.bg_color = color
    style.set_corner_radius_all(14)
    style.set_border_width_all(2)
    style.border_color = Color(1, 1, 1, 0.26)
    button.add_theme_stylebox_override("normal", style)
    button.pressed.connect(action)
    ui.add_child(button)

func _ui_rect(ui: Control, position2: Vector2, size2: Vector2, color: Color) -> void:
    var rect: ColorRect = ColorRect.new()
    rect.color = color
    rect.position = position2
    rect.size = size2
    rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
    ui.add_child(rect)

func _ui_label(ui: Control, txt: String, position2: Vector2, size2: Vector2, font_size: int, color: Color) -> Label:
    var label: Label = Label.new()
    label.text = txt
    label.position = position2
    label.size = size2
    label.add_theme_color_override("font_color", color)
    label.add_theme_font_size_override("font_size", font_size)
    label.mouse_filter = Control.MOUSE_FILTER_IGNORE
    ui.add_child(label)
    return label

func _input(event: InputEvent) -> void:
    if event is InputEventScreenTouch:
        var touch: InputEventScreenTouch = event
        if touch.pressed and touch.position.x < 470.0 and touch.position.y > 330.0:
            if joy_id == -1:
                joy_id = touch.index
                joy_anchor = touch.position
                joy_delta = Vector2.ZERO
        elif not touch.pressed and touch.index == joy_id:
            joy_id = -1
            joy_delta = Vector2.ZERO
    elif event is InputEventScreenDrag:
        var drag: InputEventScreenDrag = event
        if drag.index == joy_id:
            joy_delta = (drag.position - joy_anchor) / 70.0
            joy_delta = joy_delta.limit_length(1.0)
    elif event is InputEventKey and event.pressed and not event.echo:
        var key: InputEventKey = event
        if key.keycode == KEY_SPACE:
            _shoot()
        elif key.keycode == KEY_F:
            _pass_ball()
        elif key.keycode == KEY_R:
            _kickoff()

func _move_controlled(delta: float) -> void:
    var x: float = joy_delta.x
    var y: float = joy_delta.y
    if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
        x -= 1.0
    if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
        x += 1.0
    if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
        y -= 1.0
    if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
        y += 1.0
    var motion: Vector3 = Vector3(x, 0, y).limit_length(1.0)
    var speed: float = 7.2 if Input.is_key_pressed(KEY_SHIFT) else 5.2
    if controlled.has_meta("sprint_time") and float(controlled.get_meta("sprint_time")) > 0.0:
        speed = 7.2
        controlled.set_meta("sprint_time", maxf(0.0, float(controlled.get_meta("sprint_time")) - delta))
    if motion.length() > 0.05:
        controlled.position += motion * delta * speed
        controlled.rotation.y = lerp_angle(controlled.rotation.y, atan2(-motion.x, -motion.z), minf(1.0, delta * 11.0))
    controlled.position.x = clampf(controlled.position.x, -50.0, 50.0)
    controlled.position.z = clampf(controlled.position.z, -27.0, 27.0)
    controlled.animate_motion(motion.length() * speed / 7.2, delta)

func _move_opponents(delta: float) -> void:
    var chase_index_blue: int = -1
    var chase_index_red: int = -1
    var closest_blue: float = INF
    var closest_red: float = INF
    for i in range(bots.size()):
        var b: Dictionary = bots[i]
        if bool(b.get("keeper", false)):
            continue
        var actor: Node3D = b["node"]
        var dist: float = actor.position.distance_to(ball.position)
        if int(b["team"]) == 1 and dist < closest_red:
            closest_red = dist
            chase_index_red = i
        if int(b["team"]) == 0 and dist < closest_blue:
            closest_blue = dist
            chase_index_blue = i
    for i in range(bots.size()):
        var b: Dictionary = bots[i]
        var actor: Node3D = b["node"]
        var target: Vector3 = b["home"]
        var is_keeper: bool = bool(b.get("keeper", false))
        if is_keeper:
            target = Vector3(FIELD_HALF_X - 1.6, 0, clampf(ball.position.z, -2.6, 2.6))
        else:
            var chasing: bool = (int(b["team"]) == 1 and i == chase_index_red) or (int(b["team"]) == 0 and i == chase_index_blue and not ball_owned)
            if chasing:
                target = Vector3(ball.position.x, 0, ball.position.z)
        var displacement: Vector3 = target - actor.position
        var direction: Vector3 = Vector3(displacement.x, 0, displacement.z)
        if direction.length() > 0.30:
            direction = direction.normalized()
            actor.position += direction * float(b["speed"]) * delta
            actor.rotation.y = lerp_angle(actor.rotation.y, atan2(-direction.x, -direction.z), minf(1.0, delta * 9.0))
            actor.animate_motion(0.72, delta)
        else:
            actor.animate_motion(0.0, delta)
        if is_keeper:
            if not ball_owned and ball.position.x > FIELD_HALF_X - 3.1 and ball.position.x < FIELD_HALF_X and ball.position.y < 1.7 and actor.position.distance_to(Vector3(ball.position.x, 0, ball.position.z)) < 1.0:
                ball.velocity.x = -absf(ball.velocity.x) * 0.60
                ball.velocity.y = 2.7
                status_message = "DEFESA DO GUARDA-REDES!"
            continue
        if int(b["team"]) == 1 and actor.position.distance_to(ball.position) < 1.08 and ball_owned:
            ball_owned = false
            ball.kick(Vector3(-1, 0, randf_range(-0.4, 0.4)), 13.0, 2.1)
            status_message = "ADVERSARIO RECUPEROU A BOLA!"
        elif int(b["team"]) == 1 and actor.position.distance_to(ball.position) < 0.96 and not ball.flying and not ball_owned:
            ball.kick(Vector3(-1, 0, randf_range(-0.4, 0.4)), 13.0, 1.6)

func _shoot() -> void:
    if restart_timer > 0.0 or shoot_cooldown > 0.0:
        return
    if not ball_owned and controlled.position.distance_to(ball.position) > 1.8:
        status_message = "APROXIMA-TE DA BOLA!"
        return
    ball_owned = false
    var to_goal: Vector3 = Vector3(FIELD_HALF_X, 0.35, 0) - controlled.position
    var forward: Vector3 = controlled.global_transform.basis * Vector3.FORWARD
    var direction: Vector3 = forward.lerp(to_goal.normalized(), 0.82)
    ball.position = controlled.position + forward * 1.0 + Vector3.UP * 0.28
    ball.kick(direction, 40.0, 3.1)
    shoot_cooldown = 0.65
    status_message = "REMATE PARA A BALIZA!"

func _pass_ball() -> void:
    if restart_timer > 0.0 or shoot_cooldown > 0.0:
        return
    if not ball_owned:
        status_message = "PRIMEIRO RECUPERA A BOLA"
        return
    var preferred: Node3D
    var closest: float = INF
    for b in bots:
        if int(b["team"]) == 0:
            var actor = b["node"]
            var d: float = controlled.position.distance_to(actor.position)
            if d < closest:
                closest = d
                preferred = actor
    if preferred == null:
        return
    ball_owned = false
    ball.position = controlled.position + Vector3.UP * 0.25
    ball.kick(preferred.position - controlled.position, 19.0, 1.8)
    shoot_cooldown = 0.45
    status_message = "PASSE PARA O COMPANHEIRO"

func _sprint_tap() -> void:
    controlled.set_meta("sprint_time", 2.0)
    status_message = "SPRINT!"

func _detect_goal() -> void:
    if ball.position.x >= FIELD_HALF_X:
        if absf(ball.position.z) <= GOAL_HALF_W and ball.position.y <= GOAL_HEIGHT:
            blue_score += 1
            status_message = "GOOOOLO! REDE EM MOVIMENTO!"
            restart_timer = 2.5
            ball.flying = false
            controlled.celebrate()
            var target_net: Node3D = nets.get(1, null)
            if target_net != null:
                target_net.impact(ball.global_position)
        else:
            status_message = "BOLA FORA!"
            restart_timer = 1.5
            ball.flying = false
    elif ball.position.x <= -FIELD_HALF_X:
        if absf(ball.position.z) <= GOAL_HALF_W and ball.position.y <= GOAL_HEIGHT:
            red_score += 1
            status_message = "GOLO DO ADVERSARIO"
            var other_net: Node3D = nets.get(-1, null)
            if other_net != null:
                other_net.impact(ball.global_position)
        else:
            status_message = "BOLA FORA!"
        restart_timer = 1.5
        ball.flying = false

func _kickoff() -> void:
    restart_timer = 0.0
    controlled.position = Vector3(-18.0, 0, 0)
    controlled.rotation.y = -PI / 2.0
    for b in bots:
        var actor: Node3D = b["node"]
        actor.position = b["home"]
        actor.rotation.y = PI / 2.0 if int(b["team"]) == 1 else -PI / 2.0
    ball_owned = true
    ball.attach_to(Vector3(-17.0, 0.23, 0))
    status_message = "AVANCA PARA A DIREITA E REMATA!"

func _update_camera(delta: float) -> void:
    if camera == null:
        return
    # Side profile only. No rotation with the player: lateral view remains constant.
    var tracked_x: float = clampf(controlled.position.x + 6.0, -28.0, 28.0)
    var desired: Vector3 = Vector3(tracked_x, 12.0, 56.0)
    camera.position = camera.position.lerp(desired, minf(1.0, delta * 2.8))
    camera.look_at(Vector3(camera.position.x, 1.25, -2.5), Vector3.UP)

func _update_ui() -> void:
    if score_label != null:
        score_label.text = "AZUL  %d   —   %d  VERMELHO" % [blue_score, red_score]
    if status_label != null:
        status_label.text = status_message
    if fps_label != null:
        fps_label.text = "%02d:%02d  •  %d FPS" % [int(elapsed / 60.0), int(elapsed) % 60, Engine.get_frames_per_second()]
    if joy_widget != null:
        joy_widget.position = Vector2(78, 482) + joy_delta * 16.0

func _box(label: String, at: Vector3, dimensions: Vector3, tint: Color) -> MeshInstance3D:
    var m: MeshInstance3D = MeshInstance3D.new()
    m.name = label
    m.position = at
    var mesh: BoxMesh = BoxMesh.new()
    mesh.size = dimensions
    m.mesh = mesh
    var mat: StandardMaterial3D = StandardMaterial3D.new()
    mat.albedo_color = tint
    mat.roughness = 0.93 if label.begins_with("Grass") else 0.67
    m.material_override = mat
    add_child(m)
    return m

func _tube(label: String, a: Vector3, b: Vector3, radius: float, tint: Color) -> void:
    var direction: Vector3 = b - a
    var tube: MeshInstance3D = MeshInstance3D.new()
    tube.name = label
    var mesh: CylinderMesh = CylinderMesh.new()
    mesh.top_radius = radius
    mesh.bottom_radius = radius
    mesh.height = direction.length()
    mesh.radial_segments = 12
    tube.mesh = mesh
    tube.position = (a + b) * 0.5
    tube.quaternion = Quaternion(Vector3.UP, direction.normalized())
    var mat: StandardMaterial3D = StandardMaterial3D.new()
    mat.albedo_color = tint
    mat.roughness = 0.42
    mat.metallic = 0.14
    tube.material_override = mat
    add_child(tube)

func _pitch_line(a: Vector3, b: Vector3, tint: Color, width: float = 0.1) -> void:
    var diff: Vector3 = b - a
    if diff.length() < 0.01:
        return
    var segment: MeshInstance3D = _box("PitchMarking", (a + b) / 2.0 + Vector3.UP * 0.057,
        Vector3(width, width if absf(diff.y) > 0.1 else 0.018, diff.length()), tint)
    if absf(diff.y) > 0.1:
        segment.rotation.x = atan2(-diff.y, diff.z)
    else:
        segment.rotation.y = atan2(diff.x, diff.z)

func _field_circle(center: Vector3, radius: float, tint: Color) -> void:
    var points: int = 40
    for i in range(points):
        var a: float = TAU * float(i) / float(points)
        var b: float = TAU * float(i + 1) / float(points)
        _pitch_line(center + Vector3(cos(a) * radius, 0, sin(a) * radius),
            center + Vector3(cos(b) * radius, 0, sin(b) * radius), tint, 0.09)
