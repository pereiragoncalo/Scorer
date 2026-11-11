extends "res://scripts/match.gd"
## Scorer 2 v0.3 — mesma estrutura de oportunidades do Scorer 1.
## Sem controlo livre do jogador: o tempo avanca e para nos lances.
## A cena base fornece apenas estadio, modelos 3D, balizas e publico.

enum Stage { MATCH, OPPORTUNITY, AIM, FLIGHT, REVIEW, HALF_TIME, FINAL }
const OPPORTUNITY_TIMES: Array[float] = [14.0, 41.0, 76.0]
const GOAL_X: float = 52.0
const FLIGHT_SECONDS: float = 0.82

var stage: Stage = Stage.MATCH
var clock_min: float = 0.0
var current_opportunity: int = 0
var home_goals: int = 0
var away_goals: int = 0
var personal_goals: int = 0
var shot_count: int = 0
var half_finished: bool = false
var timer: float = 0.0
var remaining: float = 5.0
var shot_time: float = 0.0
var aim_x: float = 0.0
var aim_h: float = 1.2
var kick_power: float = 0.75
var shot_start: Vector3 = Vector3.ZERO
var shot_end: Vector3 = Vector3.ZERO
var keeper_start: Vector3 = Vector3.ZERO
var keeper_end: Vector3 = Vector3.ZERO
var shot_verdict: String = ""
var opportunity_type: String = "REMATE"
var opportunity_hard: bool = false
var rng2: RandomNumberGenerator = RandomNumberGenerator.new()
var aim_indicator: MeshInstance3D
var shot_button: Button
var top_notice: Label
var clock_label: Label
var chance_label: Label
var power_readout: Label
var instruction: Label
var current_keeper: Node3D
var all_players: Array[Node3D] = []

func _ready() -> void:
    rng2.randomize()
    Engine.max_fps = 60
    _build_environment()
    _build_field()
    _build_stadium()
    _build_teams()
    _build_camera()
    _build_ui()
    for bot in bots:
        all_players.append(bot["node"])
        if bool(bot["keeper"]):
            current_keeper = bot["node"]
    var marker_mesh: SphereMesh = SphereMesh.new()
    marker_mesh.radius = 0.17
    marker_mesh.height = 0.34
    aim_indicator = MeshInstance3D.new()
    aim_indicator.name = "AutomaticAimingMarker"
    aim_indicator.mesh = marker_mesh
    var material: StandardMaterial3D = StandardMaterial3D.new()
    material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
    material.albedo_color = Color("#caff66")
    aim_indicator.material_override = material
    add_child(aim_indicator)
    _new_match()

func _physics_process(delta: float) -> void:
    match stage:
        Stage.MATCH:
            _advance_match(delta)
        Stage.AIM:
            _aim_tick(delta)
        Stage.FLIGHT:
            _flight_tick(delta)
        Stage.REVIEW:
            timer -= delta
            if timer <= 0:
                _end_chance()
        _:
            pass
    _refresh_ui()

func _new_match() -> void:
    stage = Stage.MATCH
    clock_min = 0.0
    current_opportunity = 0
    home_goals = 0
    away_goals = 0
    personal_goals = 0
    shot_count = 0
    half_finished = false
    status_message = "O RELOGIO AVANCA ATE A PROXIMA OPORTUNIDADE"
    _hide_actors()

func _advance_match(delta: float) -> void:
    var previous: float = clock_min
    var boundary: float = 90.0 if half_finished else 45.0
    if current_opportunity < OPPORTUNITY_TIMES.size():
        boundary = minf(boundary, OPPORTUNITY_TIMES[current_opportunity])
    clock_min = minf(boundary, clock_min + delta * 3.25)
    for minute in [23.0, 53.0, 85.0]:
        if previous < minute and clock_min >= minute:
            if rng2.randf() < 0.48:
                away_goals += 1
            elif rng2.randf() < 0.25:
                home_goals += 1
    if current_opportunity < OPPORTUNITY_TIMES.size() and clock_min >= OPPORTUNITY_TIMES[current_opportunity]:
        stage = Stage.OPPORTUNITY
        status_message = "OPORTUNIDADE DE GOLO!"
    elif not half_finished and clock_min >= 45.0:
        stage = Stage.HALF_TIME
        half_finished = true
        status_message = "INTERVALO"
    elif clock_min >= 90.0:
        stage = Stage.FINAL
        status_message = "FIM DO JOGO — %d GOLOS EM %d OPORTUNIDADES" % [personal_goals, shot_count]

func _begin_chance() -> void:
    if stage != Stage.OPPORTUNITY:
        return
    stage = Stage.AIM
    timer = rng2.randf_range(0.0, 4.0)
    remaining = 6.5 if current_opportunity == 0 else 3.7
    opportunity_hard = current_opportunity > 0
    opportunity_type = ["REMATE", "CABECEAMENTO", "LIVRE DIRETO"][current_opportunity]
    var distance: float = 9.5
    var lane: float = rng2.randf_range(-5.0, 5.0)
    if opportunity_type == "CABECEAMENTO":
        distance = rng2.randf_range(4.5, 5.0)
    elif opportunity_type == "LIVRE DIRETO":
        distance = 20.0
        lane = rng2.randf_range(-9.5, 9.5)
    else:
        distance = rng2.randf_range(8.0, 15.0)
    controlled.position = Vector3(GOAL_X - distance - 0.75, 0, lane)
    controlled.rotation.y = -PI / 2.0
    ball.position = Vector3(GOAL_X - distance, 1.35 if opportunity_type == "CABECEAMENTO" else 0.24, lane)
    current_keeper.position = Vector3(GOAL_X - 1.3, 0, 0)
    current_keeper.rotation.y = PI / 2.0
    for bot in bots:
        var actor: Node3D = bot["node"]
        actor.visible = false
    var n: int = 0
    for bot in bots:
        if int(bot["team"]) != 1 or bool(bot["keeper"]):
            continue
        var d: Node3D = bot["node"]
        if opportunity_type == "LIVRE DIRETO":
            d.position = Vector3(ball.position.x + 9.15, 0, lane + (float(n) - 1.5) * 0.8)
            d.visible = true
        else:
            d.position = Vector3(lerpf(ball.position.x, GOAL_X, 0.5 + float(n) * 0.08), 0,
                                 lerpf(lane, 0.0, 0.5) + (float(n) - 1.5) * 1.8)
            d.visible = n < (4 if opportunity_hard else 2)
        d.rotation.y = PI / 2.0
        n += 1
    controlled.visible = true
    current_keeper.visible = true
    ball.visible = true
    aim_indicator.visible = true
    status_message = opportunity_type + " — ESCOLHE O MOMENTO CERTO"

func _aim_tick(delta: float) -> void:
    timer += delta * (3.75 if opportunity_hard else 2.2)
    aim_x = sin(timer) * 4.22 + cos(timer * 0.51) * 0.3
    aim_h = 1.02 + sin(timer * 1.27 + 0.4) * 1.5
    kick_power = 0.58 + 0.42 * (0.5 + 0.5 * sin(timer * 0.78))
    remaining = maxf(0.0, remaining - delta)
    aim_indicator.position = Vector3(GOAL_X - 0.13, aim_h, aim_x)
    var valid: bool = absf(aim_x) < 3.58 and aim_h > 0.17 and aim_h < 2.35
    var mat: StandardMaterial3D = aim_indicator.material_override
    mat.albedo_color = Color("#caff66") if valid else Color("#ff7773")
    controlled.animate_motion(0.0, delta)
    if remaining <= 0:
        shot_count += 1
        shot_verdict = "TEMPO ESGOTADO"
        status_message = shot_verdict
        stage = Stage.REVIEW
        timer = 1.7

func _shoot() -> void:
    if stage != Stage.AIM:
        return
    shot_count += 1
    stage = Stage.FLIGHT
    shot_time = 0.0
    shot_start = ball.position
    var dispersion: float = (0.24 if opportunity_hard else 0.12) + 0.25 * (1.0 - kick_power)
    shot_end = Vector3(GOAL_X + 0.5, aim_h + rng2.randf_range(-dispersion, dispersion),
                       aim_x + rng2.randf_range(-dispersion, dispersion))
    keeper_start = current_keeper.position
    keeper_end = Vector3(GOAL_X - 1.1, maxf(0.0, shot_end.y - 1.1) * 0.6,
                         clampf(shot_end.z * (0.88 if opportunity_hard else 0.6)
                             + rng2.randf_range(-0.65, 0.65), -3.1, 3.1))
    shot_verdict = _evaluate_shot()
    aim_indicator.visible = false
    status_message = "REMATE!"

func _evaluate_shot() -> String:
    if absf(shot_end.z) > 3.55 or shot_end.y < 0.14 or shot_end.y > 2.37:
        return "REMATE FORA!"
    if Vector2(shot_end.z - keeper_end.z, shot_end.y - (keeper_end.y + 1.05)).length() < (0.88 if opportunity_hard else 0.64):
        return "DEFESA DO GUARDA-REDES!"
    for bot in bots:
        if int(bot["team"]) != 1 or bool(bot["keeper"]):
            continue
        var d: Node3D = bot["node"]
        if not d.visible:
            continue
        var t: float = (d.position.x - shot_start.x) / maxf(0.1, shot_end.x - shot_start.x)
        if t < 0.10 or t > 0.9:
            continue
        var shot_z: float = lerpf(shot_start.z, shot_end.z, t)
        var shot_y: float = lerpf(shot_start.y, shot_end.y, t) + 1.3 * 4.0 * t * (1.0 - t)
        if absf(shot_z - d.position.z) < 0.35 and shot_y < 1.85:
            return "REMATE BLOQUEADO!"
    return "GOOOOLO!"

func _flight_tick(delta: float) -> void:
    shot_time += delta
    var t: float = clampf(shot_time / FLIGHT_SECONDS, 0.0, 1.0)
    ball.position = shot_start.lerp(shot_end, t) + Vector3.UP * (1.3 * 4.0 * t * (1.0 - t))
    ball.rotation.z += delta * 10.0
    current_keeper.position = keeper_start.lerp(keeper_end, smoothstep(0.10, 0.88, t))
    current_keeper.animate_motion(0.67, delta)
    controlled.animate_motion(0.7 if t < 0.48 else 0.0, delta)
    if t >= 1.0:
        stage = Stage.REVIEW
        timer = 2.1
        status_message = shot_verdict
        if shot_verdict == "GOOOOLO!":
            home_goals += 1
            personal_goals += 1
            controlled.celebrate()
            if nets.has(1):
                nets[1].impact(ball.global_position)

func _end_chance() -> void:
    current_opportunity += 1
    stage = Stage.MATCH
    _hide_actors()
    status_message = "O JOGO CONTINUA"

func _hide_actors() -> void:
    controlled.visible = false
    ball.visible = false
    if is_instance_valid(aim_indicator):
        aim_indicator.visible = false
    for a in all_players:
        a.visible = false

func _build_camera() -> void:
    camera = Camera3D.new()
    camera.current = true
    camera.name = "FixedStadiumOpportunityView"
    camera.projection = Camera3D.PROJECTION_PERSPECTIVE
    camera.fov = 46.0
    camera.position = Vector3(10.0, 9.5, -46.0)
    camera.near = 0.1
    camera.far = 180.0
    add_child(camera)
    camera.look_at(Vector3(43.0, 1.1, 0.0), Vector3.UP)

func _build_ui() -> void:
    var l: CanvasLayer = CanvasLayer.new()
    add_child(l)
    var ui: Control = Control.new()
    ui.set_anchors_preset(Control.PRESET_FULL_RECT)
    ui.mouse_filter = Control.MOUSE_FILTER_PASS
    l.add_child(ui)
    _ui_rect(ui, Vector2(18, 15), Vector2(450, 105), Color(0.02, 0.09, 0.16, 0.88))
    score_label = _ui_label(ui, "SCORER 2", Vector2(35, 25), Vector2(420, 38), 30, Color.WHITE)
    clock_label = _ui_label(ui, "00:00", Vector2(40, 72), Vector2(370, 38), 23, Color("#ceeafa"))
    top_notice = _ui_label(ui, "", Vector2(270, 125), Vector2(730, 55), 28, Color("#d4ff76"))
    top_notice.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    instruction = _ui_label(ui, "", Vector2(220, 190), Vector2(830, 35), 18, Color.WHITE)
    instruction.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    chance_label = _ui_label(ui, "", Vector2(24, 609), Vector2(550, 40), 25, Color.WHITE)
    power_readout = _ui_label(ui, "", Vector2(25, 653), Vector2(545, 35), 22, Color("#d0f1b9"))
    shot_button = Button.new()
    shot_button.text = "JOGAR OPORTUNIDADE"
    shot_button.position = Vector2(935, 576)
    shot_button.size = Vector2(320, 105)
    shot_button.add_theme_font_size_override("font_size", 26)
    var shot_style: StyleBoxFlat = StyleBoxFlat.new()
    shot_style.bg_color = Color("#dd8e42")
    shot_style.set_corner_radius_all(14)
    shot_button.add_theme_stylebox_override("normal", shot_style)
    shot_button.pressed.connect(_main_button)
    ui.add_child(shot_button)
    _hud_button(ui, "NOVO JOGO", Vector2(1050, 20), Vector2(205, 65), Color("#24556a"), _new_match)

func _refresh_ui() -> void:
    score_label.text = "CASA %d   —   %d FORA" % [home_goals, away_goals]
    clock_label.text = "%02d:%02d    |   %s" % [int(clock_min), int((clock_min - floorf(clock_min)) * 60.0),
        "1.ª PARTE" if clock_min < 45.0 else "2.ª PARTE"]
    top_notice.text = status_message
    chance_label.text = "OPORTUNIDADES: %d/3   GOLOS: %d" % [shot_count, personal_goals]
    shot_button.visible = stage in [Stage.OPPORTUNITY, Stage.AIM, Stage.HALF_TIME, Stage.FINAL]
    match stage:
        Stage.OPPORTUNITY:
            shot_button.text = "JOGAR OPORTUNIDADE"
            instruction.text = "O JOGO PAROU PARA O TEU LANCE"
            power_readout.text = ""
        Stage.AIM:
            shot_button.text = "REMATAR"
            instruction.text = "TOCA NA BALIZA OU NO BOTAO NO MOMENTO CERTO"
            power_readout.text = "TEMPO: %.1f s    POTENCIA: %d%%" % [remaining, int(kick_power * 100.0)]
        Stage.HALF_TIME:
            shot_button.text = "SEGUNDA PARTE"
            instruction.text = "INTERVALO"
            power_readout.text = ""
        Stage.FINAL:
            shot_button.text = "NOVO JOGO"
            instruction.text = "90 MINUTOS CONCLUIDOS"
            power_readout.text = ""
        Stage.MATCH:
            instruction.text = "RELOGIO A AVANCAR — SEM MOVIMENTACAO LIVRE"
            power_readout.text = ""
        _:
            instruction.text = "RESULTADO DA OPORTUNIDADE"
            power_readout.text = ""

func _main_button() -> void:
    match stage:
        Stage.OPPORTUNITY: _begin_chance()
        Stage.AIM: _shoot()
        Stage.HALF_TIME:
            stage = Stage.MATCH
            status_message = "SEGUNDA PARTE"
        Stage.FINAL: _new_match()

func _input(event: InputEvent) -> void:
    if stage != Stage.AIM:
        return
    if event is InputEventScreenTouch and event.pressed:
        _tap_goal(event.position)
    elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
        _tap_goal(event.position)
    elif event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_SPACE:
        _shoot()

func _tap_goal(pos: Vector2) -> void:
    # Toque na baliza = apontar diretamente e rematar, como no Scorer 1.
    var ray_origin: Vector3 = camera.project_ray_origin(pos)
    var ray_dir: Vector3 = camera.project_ray_normal(pos)
    if absf(ray_dir.x) < 0.001:
        return
    var dist: float = (GOAL_X - ray_origin.x) / ray_dir.x
    if dist <= 0.0:
        return
    var hit: Vector3 = ray_origin + ray_dir * dist
    if absf(hit.z) < 4.2 and hit.y > -0.3 and hit.y < 2.9:
        aim_x = hit.z
        aim_h = hit.y
        _shoot()
