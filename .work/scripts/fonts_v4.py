# 重建字体子集：语料直接从当前 index.html 抽，确保「页面上出现的每一个字」都有字形。
# 之前 v3b 用的是早期 copy deck 生成的字符表，后来文案改过（新增「绩」等字），
# 页面就回退到系统字体，出现「交付实绩」里「绩」字形不一致的问题。
import os, sys, re, io, subprocess, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = r"D:\code\unitree-site"
W = os.path.join(ROOT, ".work")
OUT = os.path.join(ROOT, "assets", "fonts")
PY = sys.executable

h = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

# 1) 正文文本节点
body = re.sub(r"<script[\s\S]*?</script>", " ", h)
body = re.sub(r"<style[\s\S]*?</style>", " ", body)
body = re.sub(r"<!--[\s\S]*?-->", " ", body)
text = html.unescape(re.sub(r"<[^>]+>", " ", body))
chars = set(text)

# 2) 属性里会被看到的文字（alt / aria-label / title / placeholder / content / value）
for attr in ("alt", "aria-label", "title", "placeholder", "content", "value"):
    for m in re.findall(attr + r'="([^"]*)"', h):
        chars |= set(html.unescape(m))

# 3) JS 里生成的文案（复制到剪贴板的那段）
js = open(os.path.join(ROOT, "assets", "js", "site.js"), encoding="utf-8").read()
for m in re.findall(r"[`'\"]([^`'\"]*[\u4e00-\u9fff][^`'\"]*)[`'\"]", js):
    chars |= set(m)

# 4) 保底：ASCII 可打印 + 页面会用到的符号
chars |= set(chr(c) for c in range(0x20, 0x7F))
chars |= set("·—–…→←↑↓「」『』（）【】《》〈〉×÷±≈°′″‰℃€£¥§¶†‡•※→⇒≥≤≠∞√∑∏∫")

# 丢掉空白控制符
for c in "\n\r\t":
    chars.discard(c)

alltxt = os.path.join(W, "v4-glyphs.txt")
open(alltxt, "w", encoding="utf-8").write("".join(sorted(chars)))
cjk = [c for c in chars if 0x4E00 <= ord(c) <= 0x9FFF]
print(f"语料字符 {len(chars)} 个（其中汉字 {len(cjk)} 个）")

jobs = [
    ("Smiley 标题", os.path.join(W, "fonts", "smiley", "SmileySans-Oblique.ttf"), "smiley-display.woff2"),
    ("Noto 400",  os.path.join(W, "fonts", "NotoSansSC-400.ttf"), "noto-400.woff2"),
    ("Noto 700",  os.path.join(W, "fonts", "NotoSansSC-700.ttf"), "noto-700.woff2"),
]

from fontTools.ttLib import TTFont
total = 0
bad = 0
for label, src, out in jobs:
    op = os.path.join(OUT, out)
    cmd = [PY, "-m", "fontTools.subset", src, "--text-file=" + alltxt,
           "--output-file=" + op, "--flavor=woff2", "--layout-features=*",
           "--no-hinting", "--desubroutinize"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("  失败", out, r.stderr[-600:]); bad += 1; continue
    t = TTFont(op, lazy=True); cm = set(t.getBestCmap()); t.close()
    miss = sorted(c for c in chars if ord(c) not in cm)
    size = os.path.getsize(op); total += size
    flag = "OK" if not miss else f"缺 {len(miss)}"
    if miss: bad += 1
    print(f"  {out:22s} {size/1024:6.1f} KB  {len(cm):4d} 字形  {flag}")
    if miss:
        print("      缺字:", "".join(miss[:40]))
print(f"\n字体合计 {total/1024:.1f} KB")
sys.exit(0 if bad == 0 else 1)
