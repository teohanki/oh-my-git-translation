extends Control

const LAVA_URL = "https://app.lava.top/teohanki"
const BOOSTY_URL = "https://boosty.to/teohanki/donate"
const REPO_URL = "https://github.com/teohanki/oh-my-git-translation"

const ACCENT = Color(1.0, 0.353, 0.431)
const TEXT = Color(0.85, 0.85, 0.85)
const DIM = Color(0.6, 0.6, 0.6)

var _small = preload("res://fonts/small.tres")

func _ready():
	var ru = i18n.current == "ru"
	var column = $Column

	var hello = Label.new()
	hello.text = tr("Hi, I'm Teo Hanki!")
	hello.set("custom_fonts/font", preload("res://fonts/big.tres"))
	hello.set("custom_colors/font_color", Color(1, 1, 1))
	column.add_child(hello)

	var lines = Array(tr("I translate Oh My Git! on my own, in my free time.\nThe translation is free and will always stay free.\nEvery donation helps me keep it up to date and add new languages.\nThank you!").split("\n"))
	var last = lines.pop_back()
	if lines.size() > 0:
		var pitch = Label.new()
		pitch.text = PoolStringArray(lines).join("\n")
		pitch.set("custom_colors/font_color", TEXT)
		column.add_child(pitch)
	var thanks = HBoxContainer.new()
	var thanks_label = Label.new()
	thanks_label.text = last
	thanks_label.set("custom_colors/font_color", TEXT)
	thanks.add_child(thanks_label)
	var heart = Label.new()
	heart.text = "♥"
	heart.set("custom_colors/font_color", ACCENT)
	thanks.add_child(heart)
	column.add_child(thanks)

	_spacer(column, 30)

	var lava_methods = "Visa, Mastercard, Apple Pay, PayPal, SEPA,\nPIX, iDEAL, Bancontact, MB WAY, Mir, SBP"
	var boosty_methods = "Visa, Mastercard, Mir, SBP"
	if ru:
		lava_methods = lava_methods.replace("Mir, SBP", "МИР, СБП")
		boosty_methods = boosty_methods.replace("Mir, SBP", "МИР, СБП")

	_link(column, "lava.top", LAVA_URL)
	_note(column, lava_methods, DIM)
	_link(column, "Boosty", BOOSTY_URL)
	_note(column, boosty_methods, DIM)
	_link(column, "GitHub", REPO_URL)
	_note(column, tr("new versions, bug reports, ideas"), DIM)

	_spacer(column, 10)
	_note(column, tr("opens in your browser"), DIM)
	_spacer(column, 30)

	var back = Button.new()
	back.text = tr("Back")
	back.size_flags_horizontal = 0
	back.rect_min_size = Vector2(200, 0)
	back.connect("pressed", self, "back")
	column.add_child(back)

func _link(parent, title, url):
	var button = LinkButton.new()
	button.text = title
	button.underline = LinkButton.UNDERLINE_MODE_ON_HOVER
	button.size_flags_horizontal = 0
	button.set("custom_colors/font_color", ACCENT)
	button.set("custom_colors/font_color_hover", Color(1, 0.6, 0.65))
	button.set("custom_colors/font_color_pressed", Color(1, 0.6, 0.65))
	button.connect("pressed", self, "open", [url])
	parent.add_child(button)

func _note(parent, text, color):
	var label = Label.new()
	label.text = text
	label.set("custom_fonts/font", _small)
	label.set("custom_colors/font_color", color)
	parent.add_child(label)

func _spacer(parent, height):
	var space = Control.new()
	space.rect_min_size = Vector2(0, height)
	parent.add_child(space)

func open(url):
	OS.shell_open(url)

func back():
	get_tree().change_scene("res://scenes/title.tscn")

func _input(event):
	if event.is_action_pressed("ui_cancel"):
		back()
