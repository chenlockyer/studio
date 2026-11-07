# 重新子集化：去掉 Inter，让 Noto 承担拉丁+数字（它的拉丁是 Source Sans 派生，干净）。
# 同时给 Smiley 也补上拉丁/数字——标题里的 "G1" 应该跟中文同一族。
import os, sys, json, io, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = r"D:\code\unitree-site"
W = os.path.join(ROOT, ".work")
OUT = os.path.join(ROOT, "assets", "fonts", "v3")
PY = sys.executable

chars = set(open(os.path.join(W, "v3-all-glyphs.txt"), encoding="utf-8").read())
chars.discard("\n")
chars.discard("\r")
alltxt = os.path.join(W, "v3-glyphs-clean.txt")
open(alltxt, "w", encoding="utf-8").write("".join(sorted(chars)))
print("语料字符:", len(chars))

jobs = [
    ("Smiley 标题", os.path.join(W, "fonts", "smiley", "SmileySans-Oblique.ttf"), "smiley-display.woff2"),
    ("Noto 400",  os.path.join(W, "fonts", "NotoSansSC-400.ttf"), "noto-400.woff2"),
    ("Noto 700",  os.path.join(W, "fonts", "NotoSansSC-700.ttf"), "noto-700.woff2"),
]
rows=[]
for label, src, out in jobs:
    op = os.path.join(OUT, out)
    cmd = [PY, "-m", "fontTools.subset", src, "--text-file=" + alltxt,
           "--output-file=" + op, "--flavor=woff2", "--layout-features=*",
           "--no-hinting", "--desubroutinize"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL", out, r.stderr[-800:]); continue
    from fontTools.ttLib import TTFont
    t = TTFont(op, lazy=True); cm=set(t.getBestCmap()); t.close()
    miss = [c for c in chars if ord(c) not in cm]
    mcjk = [c for c in miss if 0x4E00 <= ord(c) <= 0x9FFF]
    rows.append((out, os.path.getsize(op), len(miss), len(mcjk), "".join(miss[:20])))
    print(f"  {out:22s} {os.path.getsize(op)/1024:6.1f} KB  missing={len(miss)} CJK={len(mcjk)} {''.join(miss[:15])}")

# 删掉 inter.woff2（不再使用）
ip = os.path.join(OUT, "inter.woff2")
if os.path.isfile(ip):
    os.remove(ip); print("已删除 inter.woff2（收敛到 2 族）")
tot = sum(r[1] for r in rows)
print(f"\n字体总计 {tot/1024:.1f} KB")
