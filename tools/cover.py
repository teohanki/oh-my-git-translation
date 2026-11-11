import sys
from PIL import Image, ImageDraw, ImageFont

logo_path, cabin, ptsans, sc, jp, out = sys.argv[1:7]

S = 2
MENU_W, MENU_H = 370, 535

def font(path, size):
    return ImageFont.truetype(path, size * S)

def center_text(draw, cx, cy, text, fnt, fill):
    draw.text((cx * S, cy * S), text, font=fnt, fill=fill, anchor="mm")

menu = Image.new("RGB", (MENU_W * S, MENU_H * S), (0, 0, 0))
d = ImageDraw.Draw(menu)

def box(x0, y0, x1, y1, fill, outline, radius=3):
    d.rounded_rectangle((x0 * S, y0 * S, x1 * S, y1 * S), radius=radius * S, fill=fill, outline=outline, width=S)

main = font(cabin, 24)
white = (240, 240, 240)
rows = [("Levels", white), ("Sandbox", white), ("Support the translator", (255, 140, 158)), ("English", white)]
for i, (label, color) in enumerate(rows):
    top = 7 + i * 44
    box(10, top, 361, top + 40, (57, 57, 57), (26, 26, 26))
    center_text(d, 185 if i < 3 else 180, top + 21, label, main, color)

d.polygon([(349 * S, 157 * S), (353 * S, 157 * S), (351 * S, 154 * S)], fill=white)
d.polygon([(349 * S, 161 * S), (353 * S, 161 * S), (351 * S, 164 * S)], fill=white)

box(10, 179, 361, 525, (43, 43, 43), (19, 19, 19))
d.rectangle((11 * S, 180 * S, 360 * S, 200 * S), fill=(43, 43, 43))

languages = [
    ("English", cabin), ("简体中文", sc), ("Español", cabin), ("Français", cabin),
    ("Português (Brasil)", cabin), ("Русский", ptsans), ("Bahasa Indonesia", cabin),
    ("Deutsch", cabin), ("日本語", jp), ("Türkçe", cabin),
]
for i, (label, path) in enumerate(languages):
    y = 204 + i * 33
    if i == 0:
        d.ellipse((21 * S, (y - 5) * S, 31 * S, (y + 5) * S), outline=(225, 225, 225), width=2 * S)
    else:
        d.ellipse((22 * S, (y - 5) * S, 32 * S, (y + 5) * S), fill=(225, 225, 225))
    d.text((40 * S, y * S), label, font=font(path, 23), fill=white, anchor="lm")

menu = menu.resize((int(MENU_W * 1.12), int(MENU_H * 1.12)), Image.LANCZOS)

width, height = 1600, 720
canvas = Image.new("RGB", (width, height), (0, 0, 0))
logo = Image.open(logo_path).convert("RGBA")
logo = logo.resize((int(logo.width * 540 / logo.height), 540), Image.LANCZOS)
canvas.paste(logo, (170, (height - logo.height) // 2), logo)
canvas.paste(menu, (930, (height - menu.height) // 2))
canvas.save(out, optimize=True)
