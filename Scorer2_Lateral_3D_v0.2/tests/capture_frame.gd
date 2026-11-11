extends SceneTree
## Disposable graphical smoke test: captures the match and an active opportunity.

func _initialize() -> void:
    call_deferred("_capture")

func _capture() -> void:
    var packed: PackedScene = load("res://scenes/main.tscn")
    var game: Node = packed.instantiate()
    root.add_child(game)
    current_scene = game
    await create_timer(1.0).timeout
    _save("res://build/frame_match.png")
    game.set("stage", 1) # Stage.OPPORTUNITY
    game.call("_begin_chance")
    await create_timer(0.6).timeout
    _save("res://build/frame_opportunity.png")
    quit()

func _save(path: String) -> void:
    var image: Image = root.get_viewport().get_texture().get_image()
    if image == null or image.is_empty():
        push_error("Screenshot is empty: " + path)
        return
    var result: Error = image.save_png(ProjectSettings.globalize_path(path))
    if result != OK:
        push_error("Screenshot save failed: " + path)
    else:
        print("Captured frame ", path, " at ", image.get_size())
