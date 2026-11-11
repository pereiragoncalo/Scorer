extends Node2D
## PenaltyMind: prototipo de penaltis para Godot 4, sem dependencias externas.

const KeeperBrain = preload("res://scripts/keeper_brain.gd")
const W: float = 720.0
const H: float = 1280.0
const GOAL := Rect2(98.0, 326.0, 524.0, 246.0)
const BALL_START := Vector2(360.0, 995.0)
const SHOT_DURATION: float = 0.62
const RESULT_DURATION: float = 1.6
const SHOTS_PER_MATCH: int = 10
const C_BG := Color("#101f32")
const C_WHITE := Color("#f4f7fc")
const C_DIM := Color("#adc2d5")
const C_LIME := Color("#ccff70")
const C_CYAN := Color("#67e7ee")
const C_GOLD := Color("#ffd37b")
const C_RED := Color("#ff808b")
const BTN_NEW := Rect2(78.0, 1136.0, 264.0, 76.0)
const BTN_RESET := Rect2(378.0, 1136.0, 264.0, 76.0)

var brain
var font: Font
var phase: int = 0 # 0 pronto, 1 remate, 2 resultado, 3 fim
var elapsed: float = 0.0
var shots: int = 0
var goals: int = 0
var saves: int = 0
var aiming: bool = false
var start_in_goal: bool = false
var aim: Vector2 = Vector2(360.0, 440.0)
var target: Vector2 = Vector2(360.0, 440.0)
var predicted_zone: int = 4
var shot_zone: int = 4
var keeper_will_save: bool = false
var feedback: String = "TOCA NA BALIZA PARA REMATAR"
var feedback_color: Color = C_CYAN
var last_result: String = ""

func _ready() -> void:
    brain = KeeperBrain.new()
    font = ThemeDB.fallback_font
    queue_redraw()

func _process(delta: float) -> void:
    if phase == 1:
        elapsed += delta
        if elapsed >= SHOT_DURATION:
            _finish_shot()
    elif phase == 2:
        elapsed += delta
        if elapsed >= RESULT_DURATION:
            if shots >= SHOTS_PER_MATCH:
                phase = 3
                feedback = "FIM DE SERIE - NOVO JOGO?"
                feedback_color = C_GOLD
            else:
                phase = 0
                feedback = "TOCA NA BALIZA PARA REMATAR"
                feedback_color = C_CYAN
    queue_redraw()

func _input(event: InputEvent) -> void:
    if event is InputEventScreenTouch:
        if event.pressed:
            _pointer_down(event.position)
        else:
            _pointer_up(event.position)
    elif event is InputEventScreenDrag:
        _pointer_move(event.position)
    elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
        if event.pressed:
            _pointer_down(event.position)
        else:
            _pointer_up(event.position)
    elif event is InputEventMouseMotion:
        _pointer_move(event.position)
    elif event is InputEventKey and event.pressed and not event.echo:
        if event.keycode == KEY_SPACE or event.keycode == KEY_ENTER:
            if phase == 3:
                _new_match()
            elif phase == 0:
                _launch_shot(aim)
        elif event.keycode == KEY_R:
            _new_match()

func _pointer_down(p: Vector2) -> void:
    if BTN_NEW.has_point(p):
        _new_match()
        return
    if BTN_RESET.has_point(p):
        brain.reset_memory()
        _new_match()
        feedback = "MEMORIA DA IA APAGADA"
        feedback_color = C_GOLD
        return
    if phase != 0:
        return
    start_in_goal = GOAL.grow(24.0).has_point(p)
    if start_in_goal:
        aim = _clamp_to_goal(p)
        aiming = true
    elif p.distance_to(BALL_START) < 95.0:
        aiming = true

func _pointer_move(p: Vector2) -> void:
    if aiming and phase == 0:
        if start_in_goal or p.y < 860.0:
            aim = _clamp_to_goal(p)

func _pointer_up(p: Vector2) -> void:
    if not aiming or phase != 0:
        return
    aiming = false
    if start_in_goal:
        _launch_shot(_clamp_to_goal(p))
    elif p.y < 860.0:
        _launch_shot(_clamp_to_goal(p))
    else:
        feedback = "ARRASTA A BOLA ATE A BALIZA"
        feedback_color = C_GOLD

func _clamp_to_goal(p: Vector2) -> Vector2:
    return Vector2(clampf(p.x, GOAL.position.x + 16.0, GOAL.end.x - 16.0),
            clampf(p.y, GOAL.position.y + 16.0, GOAL.end.y - 16.0))

func _zone_for(p: Vector2) -> int:
    var col: int = clampi(int(floor((p.x - GOAL.position.x) / (GOAL.size.x / 3.0))), 0, 2)
    var row: int = 0 if p.y < GOAL.position.y + GOAL.size.y / 2.0 else 1
    return row * 3 + col

func _zone_center(zone: int) -> Vector2:
    var col: int = zone % 3
    var row: int = int(zone / 3)
    return Vector2(GOAL.position.x + (float(col) + 0.5) * GOAL.size.x / 3.0,
            GOAL.position.y + (float(row) + 0.5) * GOAL.size.y / 2.0)

func _launch_shot(shot_target: Vector2) -> void:
    if phase != 0:
        return
    target = shot_target
    shot_zone = _zone_for(target)
    predicted_zone = brain.choose_zone()
    keeper_will_save = brain.did_save(predicted_zone, shot_zone)
    brain.observe_shot(shot_zone)
    shots += 1
    elapsed = 0.0
    phase = 1
    feedback = "REMATE!"
    feedback_color = C_WHITE

func _finish_shot() -> void:
    if keeper_will_save:
        saves += 1
        last_result = "DEFESA!"
        feedback_color = C_RED
    else:
        goals += 1
        last_result = "GOOOOLO!"
        feedback_color = C_LIME
    feedback = last_result
    phase = 2
    elapsed = 0.0

func _new_match() -> void:
    shots = 0
    goals = 0
    saves = 0
    phase = 0
    elapsed = 0.0
    aiming = false
    aim = Vector2(360.0, 440.0)
    feedback = "TOCA NA BALIZA PARA REMATAR"
    feedback_color = C_CYAN

func _draw() -> void:
    draw_rect(Rect2(Vector2.ZERO, Vector2(W, H)), C_BG)
    _draw_stadium()
    _draw_pitch()
    _draw_goal()
    _draw_keeper()
    _draw_ball()
    _draw_header()
    _draw_hud()

func _draw_stadium() -> void:
    draw_rect(Rect2(0, 162, W, 175), Color("#1d334f"))
    draw_rect(Rect2(0, 241, W, 75), Color("#14283f"))
    for i in range(60):
        var x: float = 9.0 + float((i * 61 + 17) % 702)
        var y: float = 192.0 + float((i * 37 + 13) % 117)
        var c: Color = C_GOLD if i % 7 == 0 else (C_CYAN if i % 4 == 0 else Color("#6486a4"))
        draw_circle(Vector2(x, y), 2.5, c)
    draw_line(Vector2(0, 311), Vector2(W, 311), Color("#627b99"), 6)

func _draw_pitch() -> void:
    draw_rect(Rect2(0, 574, W, 523), Color("#155b47"))
    for i in range(7):
        if i % 2 == 0:
            draw_rect(Rect2(0, 576 + i * 75, W, 75), Color("#17674d"))
    draw_line(Vector2(54, 573), Vector2(54, 1091), Color("#c8e8d6"), 3)
    draw_line(Vector2(666, 573), Vector2(666, 1091), Color("#c8e8d6"), 3)
    draw_arc(Vector2(360, 874), 175, 0.12, PI - 0.12, 36, Color("#a8d4bb"), 3)
    draw_circle(Vector2(360, 966), 5, C_WHITE)
    draw_rect(Rect2(0, 1097, W, 183), C_BG)

func _draw_goal() -> void:
    draw_rect(GOAL.grow(7), Color("#071624"))
    draw_rect(GOAL, Color("#173b4f"))
    for x in range(0, 13):
        var vx: float = GOAL.position.x + GOAL.size.x * float(x) / 12.0
        draw_line(Vector2(vx, GOAL.position.y), Vector2(vx, GOAL.end.y), Color("#49687c", 0.4), 1)
    for y in range(0, 7):
        var vy: float = GOAL.position.y + GOAL.size.y * float(y) / 6.0
        draw_line(Vector2(GOAL.position.x, vy), Vector2(GOAL.end.x, vy), Color("#49687c", 0.4), 1)
    draw_line(GOAL.position, Vector2(GOAL.end.x, GOAL.position.y), C_WHITE, 10, true)
    draw_line(GOAL.position, Vector2(GOAL.position.x, GOAL.end.y), C_WHITE, 10, true)
    draw_line(Vector2(GOAL.end.x, GOAL.position.y), GOAL.end, C_WHITE, 10, true)
    draw_line(Vector2(GOAL.position.x, GOAL.end.y), GOAL.end, Color("#c4dbe3"), 6, true)
    if phase == 0 or aiming:
        draw_circle(aim, 31, Color(C_CYAN, 0.08))
        draw_arc(aim, 24, 0, TAU, 32, C_CYAN, 3)
        draw_line(aim - Vector2(34, 0), aim - Vector2(14, 0), C_CYAN, 2)
        draw_line(aim + Vector2(14, 0), aim + Vector2(34, 0), C_CYAN, 2)
        draw_line(aim - Vector2(0, 34), aim - Vector2(0, 14), C_CYAN, 2)
        draw_line(aim + Vector2(0, 14), aim + Vector2(0, 34), C_CYAN, 2)

func _draw_keeper() -> void:
    var pos: Vector2 = Vector2(360, 521)
    var lean: float = 0.0
    if phase == 1:
        var t: float = clampf(elapsed / SHOT_DURATION, 0.0, 1.0)
        pos = pos.lerp(_zone_center(predicted_zone), _smooth(t))
        lean = clampf((pos.x - 360.0) / 210.0, -1.0, 1.0)
    elif phase == 2 or phase == 3:
        pos = _zone_center(predicted_zone)
        lean = clampf((pos.x - 360.0) / 210.0, -1.0, 1.0)
    var torso: Vector2 = pos - Vector2(0, 19)
    draw_line(torso + Vector2(-13, 6), torso + Vector2(-28 - lean * 10, 37), Color("#e8ecf1"), 10, true)
    draw_line(torso + Vector2(13, 6), torso + Vector2(28 - lean * 10, 37), Color("#e8ecf1"), 10, true)
    draw_line(torso + Vector2(-16, -13), torso + Vector2(-47 - lean * 13, -30), Color("#f7c59b"), 11, true)
    draw_line(torso + Vector2(16, -13), torso + Vector2(47 - lean * 13, -30), Color("#f7c59b"), 11, true)
    draw_circle(torso + Vector2(-48 - lean * 13, -30), 10, C_GOLD)
    draw_circle(torso + Vector2(48 - lean * 13, -30), 10, C_GOLD)
    draw_rect(Rect2(torso - Vector2(22, 29), Vector2(44, 42)), Color("#f68d47"))
    draw_rect(Rect2(torso - Vector2(22, 29), Vector2(44, 6)), Color("#ffd07a"))
    draw_circle(torso - Vector2(0, 46), 17, Color("#f6c8a4"))
    draw_arc(torso - Vector2(0, 50), 16, PI + 0.4, TAU - 0.4, 9, Color("#172431"), 8)

func _draw_ball() -> void:
    var pos: Vector2 = BALL_START
    var radius: float = 24.0
    if phase == 1:
        var t: float = clampf(elapsed / SHOT_DURATION, 0.0, 1.0)
        pos = BALL_START.lerp(target, _smooth(t))
        radius = lerpf(24.0, 12.0, t)
    elif phase == 2 or phase == 3:
        pos = target
        radius = 12.0
        if keeper_will_save:
            pos = _zone_center(predicted_zone) + Vector2(14, 2)
    if phase == 0 or aiming:
        draw_circle(BALL_START + Vector2(4, 19), 22, Color("#091c20", 0.55))
    draw_circle(pos, radius + 2, Color("#0e2e36"))
    draw_circle(pos, radius, C_WHITE)
    var pentagon: PackedVector2Array = PackedVector2Array()
    for i in range(5):
        var a: float = -PI / 2.0 + float(i) * TAU / 5.0
        pentagon.append(pos + Vector2(cos(a), sin(a)) * radius * 0.45)
    draw_colored_polygon(pentagon, Color("#132436"))
    for i in range(5):
        var a: float = -PI / 2.0 + float(i) * TAU / 5.0
        draw_line(pos + Vector2(cos(a), sin(a)) * radius * 0.54,
            pos + Vector2(cos(a), sin(a)) * radius * 0.94, Color("#294356"), 2)

func _draw_header() -> void:
    _center("PENALTY", 67, 51, C_WHITE)
    _center("MIND", 123, 48, C_LIME)
    _center("O GUARDA-REDES APRENDE OS TEUS REMATES", 151, 15, C_DIM)
    _center("10 PENALTIS  -  IA OFFLINE", 220, 22, C_WHITE)

func _draw_hud() -> void:
    draw_rect(Rect2(38, 1098, 644, 8), Color("#344958"))
    var progress: float = float(shots) / float(SHOTS_PER_MATCH)
    draw_rect(Rect2(38, 1098, 644.0 * progress, 8), C_LIME)
    _center(feedback, 660, 27, feedback_color)
    if phase == 0:
        _center("TOCA NA BALIZA OU ARRASTA A BOLA", 703, 18, C_WHITE)
    elif phase == 3:
        _center("A IA LEMBRA-SE DOS TEUS REMATES", 703, 18, C_DIM)
    else:
        _center("O GUARDA-REDES TENTOU ADIVINHAR O LADO", 703, 18, C_DIM)
    _draw_score_panel()
    _draw_button(BTN_NEW, "NOVO JOGO", C_CYAN)
    _draw_button(BTN_RESET, "APAGAR MEMORIA", C_GOLD)
    _center("V0.1  -  SEM INTERNET  -  SEM ANUNCIOS", 1251, 15, C_DIM)

func _draw_score_panel() -> void:
    var values: Array[String] = [str(shots) + "/10", str(goals), str(saves), str(brain.total_shots())]
    var names: Array[String] = ["REMATES", "GOLOS", "DEFESAS", "MEMORIA IA"]
    for i in range(4):
        var px: float = 42.0 + float(i) * 166.0
        draw_rect(Rect2(px, 760, 150, 135), Color("#20394b"))
        _center_at(values[i], px + 75, 817, 40, C_WHITE if i != 1 else C_LIME)
        _center_at(names[i], px + 75, 865, 17, C_DIM)
    _center("AREAS FAVORITAS DO JOGADOR", 927, 18, C_DIM)
    for i in range(6):
        var x: float = 140.0 + float(i) * 74.0
        var frequency: float = brain.frequency(i)
        draw_rect(Rect2(x, 947, 52, 77), Color("#294556"))
        if frequency > 0.0:
            draw_rect(Rect2(x, 1024.0 - frequency * 77.0, 52, frequency * 77.0), C_LIME)
        _center_at(str(i + 1), x + 26, 1055, 17, C_DIM)

func _draw_button(rect: Rect2, label: String, accent: Color) -> void:
    draw_rect(rect, Color("#243f50"))
    draw_rect(rect, accent, false, 3)
    _center_at(label, rect.position.x + rect.size.x / 2.0, rect.position.y + 47.0, 22, C_WHITE)

func _center(text: String, y: float, size: int, color: Color) -> void:
    _center_at(text, W * 0.5, y, size, color)

func _center_at(text: String, x: float, y: float, size: int, color: Color) -> void:
    var width: float = font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, size).x
    draw_string(font, Vector2(x - width * 0.5, y), text, HORIZONTAL_ALIGNMENT_LEFT, -1, size, color)

func _smooth(t: float) -> float:
    return t * t * (3.0 - 2.0 * t)
