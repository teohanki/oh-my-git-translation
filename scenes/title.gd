extends Control

func _ready():
	if !OS.has_feature("standalone") and !game.skipped_title:
		game.skipped_title = true
		get_tree().change_scene("res://scenes/level_select.tscn")
		return
	_add_menu_items()

func _add_menu_items():
	var menu = $VBoxContainer

	var support = Button.new()
	support.text = tr("Support the translator")
	support.set("custom_colors/font_color", Color(1.0, 0.55, 0.62))
	support.connect("pressed", self, "support")
	menu.add_child(support)
	menu.move_child(support, menu.get_child_count() - 2)

	var picker = OptionButton.new()
	picker.align = Button.ALIGN_CENTER
	picker.hint_tooltip = tr("Language")
	for i in range(i18n.LANGUAGES.size()):
		picker.add_item(i18n.LANGUAGES[i][1], i)
		if i18n.LANGUAGES[i][0] == i18n.current:
			picker.select(i)
	picker.connect("item_selected", self, "language_selected")
	menu.add_child(picker)
	menu.move_child(picker, menu.get_child_count() - 2)

	if i18n.first_run:
		i18n.first_run = false
		i18n.remember()
		_open_picker(picker)

func _open_picker(picker):
	yield(get_tree(), "idle_frame")
	yield(get_tree(), "idle_frame")
	var popup = picker.get_popup()
	popup.set_global_position(picker.rect_global_position + Vector2(0, picker.rect_size.y))
	popup.set_size(Vector2(picker.rect_size.x, 0))
	popup.popup()

func language_selected(index):
	i18n.set_language(i18n.LANGUAGES[index][0])
	get_tree().reload_current_scene()

func support():
	get_tree().change_scene("res://scenes/support.tscn")

func quit():
	get_tree().quit()

func levels():
	get_tree().change_scene("res://scenes/level_select.tscn")


func on_survey_pressed():
	game.open_survey()


func sandbox():
	game.current_chapter = levels.chapters.size() - 1
	game.current_level = levels.chapters[game.current_chapter].levels.size() -1
	get_tree().change_scene("res://scenes/main.tscn")
