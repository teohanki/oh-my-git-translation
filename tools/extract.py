import json
import os
import re
import sys

UI_TYPES = {"Label", "Button", "LinkButton", "CheckBox", "CheckButton"}
PLACEHOLDERS = {
    "label", "Description", "0", "3", "title", "root", "dir", "x", "filename",
    "object_id", "Repo name", "Level name here!", "Level description here!", "Text here",
    "Oh My Git!",
    "This is a hint! This is a hint! This is a hint! This is a hint! This is a hint! This is a hint! This is a hint! This is a hint! This is a hint!",
}
EXTRA = [
    "Good job, you solved the level!\n\nFeel free to try a few more things or click 'Next level'.",
]


class Catalog:
    def __init__(self):
        self.entries = []
        self.index = {}

    def add(self, msgid, ref):
        msgid = msgid.strip()
        if not msgid or msgid in PLACEHOLDERS or msgid.startswith("git "):
            return
        if msgid in self.index:
            refs = self.index[msgid]
            if ref not in refs:
                refs.append(ref)
            return
        self.index[msgid] = [ref]
        self.entries.append(msgid)


def parse_level(text):
    sections = {}
    current = None
    for line in text.split("\n"):
        if line.startswith(";"):
            continue
        m = re.match(r"^\[(.*)\]$", line)
        if m:
            current = m.group(1)
            sections[current] = ""
            continue
        m = re.match(r"^([a-z ]+)=(.*)$", line)
        if m:
            sections[m.group(1).strip()] = m.group(2).strip()
            continue
        if current:
            sections[current] += line + "\n"
    return {k: v.strip() for k, v in sections.items()}


def read_sequence(path):
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def extract_levels(root, cat):
    levels_dir = os.path.join(root, "levels")
    for chapter in read_sequence(os.path.join(levels_dir, "sequence")):
        for level in read_sequence(os.path.join(levels_dir, chapter, "sequence")):
            rel = "levels/%s/%s" % (chapter, level)
            with open(os.path.join(root, rel), encoding="utf-8") as f:
                config = parse_level(f.read())
            if "title" in config:
                cat.add(config["title"], rel)
            for part in config.get("description", "").split("---"):
                cat.add(part, rel)
            cat.add(config.get("cli", ""), rel)
            cat.add(config.get("congrats", ""), rel)
            for key, value in config.items():
                if key.startswith("win") or key.startswith("actions"):
                    for line in value.split("\n"):
                        if key.startswith("win") and line.startswith("#"):
                            cat.add(line[1:], rel)
                        for hint in re.findall(r'hint "([^"]*)"', line):
                            cat.add(hint, rel)


def extract_cards(root, cat):
    with open(os.path.join(root, "resources", "cards.json"), encoding="utf-8") as f:
        for card in json.load(f):
            cat.add(card.get("description", ""), "resources/cards.json")


def unescape(s):
    return s.replace('\\"', '"').replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", "\\")


def extract_scenes(root, cat):
    scenes = os.path.join(root, "scenes")
    for name in sorted(os.listdir(scenes)):
        path = os.path.join(scenes, name)
        rel = "scenes/" + name
        if name.endswith(".tscn"):
            with open(path, encoding="utf-8") as f:
                text = f.read()
            node_type = None
            for block in re.split(r"(?m)^(?=\[)", text):
                m = re.match(r'\[node name="[^"]*" type="([^"]+)"', block)
                if m:
                    node_type = m.group(1)
                elif block.startswith("["):
                    node_type = None
                if node_type not in UI_TYPES:
                    continue
                for value in re.findall(r'(?m)^(?:text|hint_tooltip) = "((?:[^"\\]|\\.)*)"', block, re.S):
                    cat.add(unescape(value), rel)
        elif name.endswith(".gd"):
            with open(path, encoding="utf-8") as f:
                text = "\n".join(line for line in f.read().split("\n") if not line.strip().startswith("#"))
            for value in re.findall(r'\btr\("((?:[^"\\]|\\.)*)"\)', text):
                cat.add(unescape(value), rel)
            for value in re.findall(r'\bnotify\("((?:[^"\\]|\\.)*)"', text):
                cat.add(unescape(value), rel)
            m = re.search(r"var button_texts = \[(.*?)\]", text)
            if m:
                for value in re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1)):
                    cat.add(unescape(value), rel)
            m = re.search(r"const CHAPTERS = \{(.*?)\}", text, re.S)
            if m:
                for value in re.findall(r':\s*"((?:[^"\\]|\\.)*)"', m.group(1)):
                    cat.add(unescape(value), rel)
    for value in EXTRA:
        cat.add(value, "scenes/level.gd")


def po_string(s):
    s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\t", "\\t")
    if "\n" not in s:
        return '"%s"' % s
    lines = s.split("\n")
    out = ['""']
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            out.append('"%s\\n"' % line)
        elif line:
            out.append('"%s"' % line)
    return "\n".join(out)


def write_pot(cat, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write('msgid ""\nmsgstr ""\n"Project-Id-Version: Oh My Git!\\n"\n"MIME-Version: 1.0\\n"\n"Content-Type: text/plain; charset=UTF-8\\n"\n"Content-Transfer-Encoding: 8bit\\n"\n\n')
        for msgid in cat.entries:
            for ref in cat.index[msgid]:
                f.write("#: %s\n" % ref)
            f.write("msgid %s\nmsgstr \"\"\n\n" % po_string(msgid))


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    cat = Catalog()
    extract_levels(root, cat)
    extract_cards(root, cat)
    extract_scenes(root, cat)
    os.makedirs(os.path.join(root, "locale"), exist_ok=True)
    write_pot(cat, os.path.join(root, "locale", "messages.pot"))
    print(len(cat.entries), "strings")


if __name__ == "__main__":
    main()
