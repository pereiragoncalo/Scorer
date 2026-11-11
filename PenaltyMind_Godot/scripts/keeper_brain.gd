extends RefCounted
## Guarda-redes adaptativo, offline, com memoria local e seis zonas.

const DEFAULT_SAVE_PATH: String = "user://penaltymind_memory.json"
const ZONE_COUNT: int = 6
const MAX_RECENT: int = 15

var counts: Array[int] = [0, 0, 0, 0, 0, 0]
var recent: Array[int] = []
var rng: RandomNumberGenerator = RandomNumberGenerator.new()
var save_path: String = DEFAULT_SAVE_PATH

func _init(custom_save_path: String = DEFAULT_SAVE_PATH) -> void:
    save_path = custom_save_path
    rng.randomize()
    load_memory()

func total_shots() -> int:
    var total: int = 0
    for n in counts:
        total += n
    return total

func choose_zone() -> int:
    if total_shots() < 3 or rng.randf() < 0.28:
        return rng.randi_range(0, ZONE_COUNT - 1)
    var weights: Array[float] = []
    for zone in range(ZONE_COUNT):
        var weight: float = 1.0 + float(counts[zone]) * 0.25
        for old_zone in recent:
            if old_zone == zone:
                weight += 1.35
        weights.append(weight)
    if rng.randf() < 0.62:
        var best_zone: int = 0
        var best_weight: float = weights[0]
        for zone in range(1, ZONE_COUNT):
            if weights[zone] > best_weight:
                best_weight = weights[zone]
                best_zone = zone
        return best_zone
    var total_weight: float = 0.0
    for weight in weights:
        total_weight += weight
    var pick: float = rng.randf() * total_weight
    for zone in range(ZONE_COUNT):
        pick -= weights[zone]
        if pick <= 0.0:
            return zone
    return ZONE_COUNT - 1

func did_save(predicted_zone: int, shot_zone: int) -> bool:
    var pred_col: int = predicted_zone % 3
    var shot_col: int = shot_zone % 3
    var pred_row: int = int(predicted_zone / 3)
    var shot_row: int = int(shot_zone / 3)
    var col_distance: int = abs(pred_col - shot_col)
    var row_distance: int = abs(pred_row - shot_row)
    var chance: float = 0.05
    if col_distance == 0 and row_distance == 0:
        chance = 0.78
    elif col_distance == 0:
        chance = 0.37
    elif col_distance == 1 and row_distance == 0:
        chance = 0.22
    elif col_distance == 1 and row_distance == 1:
        chance = 0.10
    return rng.randf() < chance

func observe_shot(zone: int) -> void:
    if zone < 0 or zone >= ZONE_COUNT:
        return
    counts[zone] += 1
    recent.append(zone)
    if recent.size() > MAX_RECENT:
        recent.pop_front()
    save_memory()

func frequency(zone: int) -> float:
    if zone < 0 or zone >= ZONE_COUNT or total_shots() == 0:
        return 0.0
    return float(counts[zone]) / float(total_shots())

func reset_memory() -> void:
    counts = [0, 0, 0, 0, 0, 0]
    recent.clear()
    save_memory()

func save_memory() -> void:
    var f: FileAccess = FileAccess.open(save_path, FileAccess.WRITE)
    if f == null:
        push_warning("Nao foi possivel gravar a memoria do guarda-redes.")
        return
    var data: Dictionary = {"version": 1, "counts": counts, "recent": recent}
    f.store_string(JSON.stringify(data))
    f.close()

func load_memory() -> void:
    if not FileAccess.file_exists(save_path):
        return
    var f: FileAccess = FileAccess.open(save_path, FileAccess.READ)
    if f == null:
        return
    var parsed: Variant = JSON.parse_string(f.get_as_text())
    f.close()
    if not (parsed is Dictionary):
        return
    var data: Dictionary = parsed
    if not data.has("counts") or not (data["counts"] is Array):
        return
    var saved_counts: Array = data["counts"]
    if saved_counts.size() != ZONE_COUNT:
        return
    var restored: Array[int] = []
    for n in saved_counts:
        restored.append(clampi(int(n), 0, 1000000))
    counts = restored
    recent.clear()
    if data.has("recent") and data["recent"] is Array:
        for n in data["recent"]:
            var zone: int = int(n)
            if zone >= 0 and zone < ZONE_COUNT:
                recent.append(zone)
    while recent.size() > MAX_RECENT:
        recent.pop_front()
