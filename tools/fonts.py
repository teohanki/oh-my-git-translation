import glob
import os
import shutil
import sys

from fontTools import subset


def gb2312_level1():
    chars = set()
    for hi in range(0xB0, 0xD8):
        for lo in range(0xA1, 0xFF):
            try:
                chars.add(bytes([hi, lo]).decode("gb2312"))
            except UnicodeDecodeError:
                pass
    return chars


def jis_level1():
    chars = set()
    for row in range(16, 48):
        for cell in range(1, 95):
            try:
                chars.add(bytes([row + 0xA0, cell + 0xA0]).decode("euc_jp"))
            except UnicodeDecodeError:
                pass
    return chars


def block(start, end):
    return {chr(c) for c in range(start, end + 1)}


def po_chars(path):
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        return set(f.read())


def make_subset(source, target, chars):
    options = subset.Options()
    options.layout_features = ["*"]
    options.name_IDs = ["*"]
    options.notdef_outline = True
    font = subset.load_font(source, options)
    subsetter = subset.Subsetter(options)
    subsetter.populate(unicodes=sorted(ord(c) for c in chars))
    subsetter.subset(font)
    subset.save_font(font, target, options)


def main():
    source_dir, project_dir = sys.argv[1], sys.argv[2]
    fonts_dir = os.path.join(project_dir, "fonts")
    locale_dir = os.path.join(project_dir, "locale")

    shutil.copy(os.path.join(source_dir, "PT_Sans-Web-Regular.ttf"), os.path.join(fonts_dir, "pt-sans-regular.ttf"))
    shutil.copy(os.path.join(source_dir, "PT_Sans-Web-Bold.ttf"), os.path.join(fonts_dir, "pt-sans-bold.ttf"))

    used = set()
    for path in glob.glob(os.path.join(locale_dir, "*.po")):
        used |= po_chars(path)
    common = block(0x3000, 0x303F) | block(0x3040, 0x30FF) | block(0xFF00, 0xFFEF) | set("→←↑↓♥★☆○●…‥・「」『』【】")

    make_subset(
        os.path.join(source_dir, "NotoSansSC-Regular.otf"),
        os.path.join(fonts_dir, "noto-sans-sc.otf"),
        gb2312_level1() | used | common,
    )
    make_subset(
        os.path.join(source_dir, "NotoSansJP-Regular.otf"),
        os.path.join(fonts_dir, "noto-sans-jp.otf"),
        jis_level1() | used | common,
    )


if __name__ == "__main__":
    main()
