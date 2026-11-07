# -*- coding: utf-8 -*-
"""
v3 字体子集流水线：以最终文案（copy-v3.txt）+ 页面 HTML 为语料，
产出 assets/fonts/v3/*.woff2。

设计要点：
- 拉丁走 Inter（变量字重），中文走 Smiley Sans。
- Smiley Sans 只有 Regular（400）+ 斜体倾斜。中文标题的"重"靠字号与紧排，
  不靠字重——所以中文只出一档，CSS 里 700 会回落到同一文件（font-synthesis 控制）。
  为解决"标题需要更粗"的问题，另出一档用描边加粗（stroke）实现的伪粗体？不做——
  那是造假。改用：中文标题用 Smiley Sans，正文用 Noto Sans SC 400/700 已有文件。
  即：中文两族并存，各有职责：
    * Smiley Sans  → 只用于 display / head（标题层），个性来源
    * Noto Sans SC → 正文与小字（可读性）
- Inter 只有一个文件（变量），覆盖拉丁与数字。
"""
import os, sys, json, re, subprocess, hashlib

ROOT = r"D:\code\unitree-site"
W = os.path.join(ROOT, ".work")
FONTS_SRC = os.path.join(W, "fonts")
OUT = os.path.join(ROOT, "assets", "fonts", "v3")
os.makedirs(OUT, exist_ok=True)

PY = sys.executable

# ---- 1. 收集语料：文案 deck + HTML 里所有文字 ----
def gather_text():
    chunks = []
    p = os.path.join(W, "copy-v3.txt")
    if os.path.isfile(p):
        chunks.append(open(p, encoding="utf-8").read())
    for f in ("index.html",):
        fp = os.path.join(ROOT, f)
        if os.path.isfile(fp):
            html = open(fp, encoding="utf-8").read()
            # 去掉标签与注释，保留可见文本
            html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
            html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
            html = re.sub(r"<[^>]+>", " ", html)
            chunks.append(html)
    # JS 里可能有动态文案
    js = os.path.join(ROOT, "assets", "js", "site.js")
    if os.path.isfile(js):
        chunks.append(open(js, encoding="utf-8").read())
    return "\n".join(chunks)

def chars_of(text):
    s = set(text)
    # 补齐常用标点、数字、字母，避免动态内容缺字
    s |= set("0123456789")
    s |= set("abcdefghijklmnopqrstuvwxyz")
    s |= set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    s |= set(" .,:;!?()[]{}<>/\\-_+*=@#%&'\"`~^|$")
    s |= set("，。、；：？！（）【】《》“”‘’—…·～　")
    s |= set("←↑→↓←↑→↓·×÷°±≤≥≠≈√∞")
    s |= set("①②③④⑤⑥⑦⑧⑨⑩")
    s |= set("一二三四五六七八九十百千万亿零两")
    # 去掉控制字符
    return {c for c in s if ord(c) >= 0x20 or c in "\n\t"}

def write_textfile(path, chars):
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(sorted(chars)))

def subset(src, textfile, outname, extra):
    outp = os.path.join(OUT, outname)
    cmd = [PY, "-m", "fontTools.subset", src,
           "--text-file=%s" % textfile,
           "--output-file=%s" % outp] + extra
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED", outname)
        print(r.stdout[-2500:]); print(r.stderr[-2500:])
        return None
    return outp

def coverage(fontpath, chars):
    from fontTools.ttLib import TTFont
    t = TTFont(fontpath, lazy=True)
    cm = set(t.getBestCmap())
    t.close()
    missing = sorted(c for c in chars if ord(c) not in cm)
    return missing

def main():
    text = gather_text()
    chars = chars_of(text)
    n_cjk = sum(1 for c in chars if 0x4E00 <= ord(c) <= 0x9FFF)
    print("语料：%d 字符，其中汉字 %d" % (len(chars), n_cjk))

    cjk_txt = os.path.join(W, "v3-cjk-glyphs.txt")
    all_txt = os.path.join(W, "v3-all-glyphs.txt")
    write_textfile(cjk_txt, chars)
    write_textfile(all_txt, chars)

    jobs = []
    # --- 中文标题：Smiley Sans（压缩斜体，唯一的中文 display 字体）---
    smiley = os.path.join(FONTS_SRC, "smiley", "SmileySans-Oblique.ttf")
    if os.path.isfile(smiley):
        jobs.append(("中文标题 SmileySans", smiley, cjk_txt, "smiley-display.woff2",
                     ["--flavor=woff2", "--layout-features=*", "--no-hinting", "--desubroutinize"]))
    else:
        print("!! 缺 SmileySans:", smiley)

    # --- 中文正文：Noto Sans SC 400 / 700（已有源）---
    for wt in ("400", "700"):
        srcp = os.path.join(FONTS_SRC, "NotoSansSC-%s.ttf" % wt)
        if os.path.isfile(srcp):
            jobs.append(("中文正文 Noto %s" % wt, srcp, cjk_txt, "noto-%s.woff2" % wt,
                         ["--flavor=woff2", "--layout-features=*", "--no-hinting", "--desubroutinize"]))

    # --- 拉丁/数字：Inter 变量 ---
    inter = None
    for cand in ("Inter-VF.ttf", "Inter.ttf", "inter-var.ttf"):
        p = os.path.join(FONTS_SRC, cand)
        if os.path.isfile(p):
            inter = p; break
    if inter:
        jobs.append(("拉丁 Inter VF", inter, all_txt, "inter.woff2",
                     ["--flavor=woff2", "--layout-features=*", "--no-hinting"]))
    else:
        print("!! 未找到 Inter 源，稍后下载")

    results = []
    for label, src, txt, outname, extra in jobs:
        print("\n-- subset %s" % label)
        outp = subset(src, txt, outname, extra)
        if not outp:
            continue
        b = os.path.getsize(outp)
        miss = coverage(outp, chars)
        cjk_miss = [c for c in miss if 0x4E00 <= ord(c) <= 0x9FFF]
        results.append({"label": label, "file": outname, "bytes": b,
                        "missing": len(miss), "missing_cjk": len(cjk_miss),
                        "missing_sample": "".join(miss[:40])})
        print("   %-26s %8d B (%6.1f KB)  missing=%d (CJK %d) %s"
              % (outname, b, b / 1024, len(miss), len(cjk_miss), "".join(miss[:30])))

    json.dump(results, open(os.path.join(W, "v3-font-results.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    tot = sum(r["bytes"] for r in results)
    print("\n字体总计 %d B (%.1f KB)" % (tot, tot / 1024))
    bad = [r for r in results if r["missing_cjk"] > 0]
    if bad:
        print("\n!! 有缺字（页面会回落系统字体）：")
        for r in bad:
            print("   %s -> %s" % (r["file"], r["missing_sample"]))
    else:
        print("✓ 所有字体覆盖完整，无缺字")

if __name__ == "__main__":
    main()
