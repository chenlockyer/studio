import io, sys, re
from fontTools.ttLib import TTFont

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

html = open("index.html", encoding="utf-8").read()
js = open("assets/js/site.js", encoding="utf-8").read()


def text_of(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<(script|style)\b.*?</\1>", "", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return s


used = set(text_of(html)) | set(re.findall(r'"([^"]*)"', js))
used = {ch for ch in used if ch.strip()}
cjk = {ch for ch in used if "\u3400" <= ch <= "\u9fff"}
print("页面用字 {} 个（汉字 {}）".format(len(used), len(cjk)))

fonts = ["smiley-display", "noto-400", "noto-700"]
cmaps = {f: TTFont("assets/fonts/{}.woff2".format(f)).getBestCmap() for f in fonts}

for f in fonts:
    cmap = cmaps[f]
    missing = sorted(ch for ch in used if ord(ch) not in cmap)
    print("  {:<16s} 缺 {:2d} 个  {}".format(f, len(missing), " ".join(missing[:24])))

print()
for ch in "宇树机器人实验室绩验":
    ok = all(ord(ch) in cmaps[f] for f in fonts)
    print("    {} U+{:04X}: {}".format(ch, ord(ch), "有" if ok else "缺"))
