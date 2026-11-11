extends Node

signal language_changed

const LANGUAGES = [
	["en", "English"],
	["zh_CN", "简体中文"],
	["es", "Español"],
	["fr", "Français"],
	["pt_BR", "Português (Brasil)"],
	["ru", "Русский"],
	["id", "Bahasa Indonesia"],
	["de", "Deutsch"],
	["ja", "日本語"],
	["tr", "Türkçe"],
]

const CHAPTERS = {
	"intro": "Introduction",
	"files": "Files",
	"branches": "Branches",
	"merge": "Merging",
	"index": "The index",
	"remotes": "Remotes",
	"changing-the-past": "Changing the past",
	"shit-happens": "Fixing mistakes",
	"workflows": "Workflows",
	"bisect": "Bisect",
	"stash": "Stashing",
	"tags": "Tags",
	"sandbox": "Sandbox",
}

const SETTINGS_PATH = "user://settings.cfg"

var current = "en"
var first_run = false
var _translation = null

var _cabin_regular = preload("res://fonts/cabin-regular.ttf")
var _cabin_bold = preload("res://fonts/cabin-bold.ttf")
var _pt_regular = preload("res://fonts/pt-sans-regular.ttf")
var _pt_bold = preload("res://fonts/pt-sans-bold.ttf")
var _iosevka = preload("res://fonts/iosevka-regular.ttf")
var _cjk_sc = preload("res://fonts/noto-sans-sc.otf")
var _cjk_jp = preload("res://fonts/noto-sans-jp.otf")
var _fonts = {}

func _init():
	var lang = _load_setting()
	if lang == null:
		first_run = true
		lang = detect_system_language()
	_apply(lang)

func detect_system_language():
	var locale = OS.get_locale()
	for entry in LANGUAGES:
		if entry[0] == locale:
			return entry[0]
	var prefix = locale.split("_")[0]
	for entry in LANGUAGES:
		if entry[0].split("_")[0] == prefix:
			return entry[0]
	return "en"

func remember():
	_save_setting(current)

func set_language(lang):
	if lang == current:
		_save_setting(lang)
		return
	_apply(lang)
	_save_setting(lang)
	if has_node("/root/levels"):
		get_node("/root/levels").reload()
	emit_signal("language_changed")

func language_name(lang):
	for entry in LANGUAGES:
		if entry[0] == lang:
			return entry[1]
	return lang

func chapter_name(slug):
	if not CHAPTERS.has(slug):
		return slug
	if current == "en":
		return slug
	return tr(CHAPTERS[slug])

func block(text):
	var inner = text.strip_edges()
	if inner == "":
		return text
	var translated = tr(inner)
	if translated == inner:
		return text
	var start = text.find(inner)
	return text.substr(0, start) + translated + text.substr(start + inner.length())

func _apply(lang):
	if _translation != null:
		TranslationServer.remove_translation(_translation)
		_translation = null
	var known = false
	for entry in LANGUAGES:
		if entry[0] == lang:
			known = true
	if not known:
		lang = "en"
	if lang != "en":
		var path = "res://locale/%s.po" % lang
		if ResourceLoader.exists(path):
			_translation = load(path)
			TranslationServer.add_translation(_translation)
		else:
			lang = "en"
	current = lang
	TranslationServer.set_locale(lang)
	_apply_fonts()

func _apply_fonts():
	var regular = _cabin_regular
	var bold = _cabin_bold
	var latin_regular = _pt_regular
	var latin_bold = _pt_bold
	if current == "ru":
		regular = _pt_regular
		bold = _pt_bold
		latin_regular = _cabin_regular
		latin_bold = _cabin_bold
	var cjk = [_cjk_sc, _cjk_jp]
	if current == "ja":
		cjk = [_cjk_jp, _cjk_sc]
	_set_font("res://fonts/default.tres", regular, [latin_regular] + cjk)
	_set_font("res://fonts/small.tres", regular, [latin_regular] + cjk)
	_set_font("res://fonts/big.tres", bold, [latin_bold] + cjk)
	_set_font("res://fonts/monospace.tres", _iosevka, cjk)

func _set_font(path, main, fallbacks):
	if not _fonts.has(path):
		_fonts[path] = load(path)
	var font = _fonts[path]
	font.font_data = main
	while font.get_fallback_count() > 0:
		font.remove_fallback(0)
	for data in fallbacks:
		font.add_fallback(data)

func _load_setting():
	var config = ConfigFile.new()
	if config.load(SETTINGS_PATH) != OK:
		return null
	return config.get_value("game", "language", null)

func _save_setting(lang):
	var config = ConfigFile.new()
	config.load(SETTINGS_PATH)
	config.set_value("game", "language", lang)
	config.save(SETTINGS_PATH)
