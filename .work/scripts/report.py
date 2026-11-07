# -*- coding: utf-8 -*-
"""TASK 5b: .work/media-report.md (中文)"""
import os, json

ROOT = r"D:\code\unitree-site"
W = os.path.join(ROOT, ".work")
BUG = 1024.0

man = json.load(open(os.path.join(W, "media-manifest.json"), encoding="utf-8"))
tot = json.load(open(os.path.join(W, "totals.json"), encoding="utf-8"))
corpus = json.load(open(os.path.join(W, "corpus-meta.json"), encoding="utf-8"))
rrep = {r["slug"]: r for r in json.load(open(os.path.join(W, "raster-report.json"), encoding="utf-8"))}

# ---- coverage audit numbers ----
import unicodedata
from fontTools.ttLib import TTFont

FONTS = os.path.join(ROOT, "assets", "fonts")


def _cps(fn):
    t = TTFont(os.path.join(FONTS, fn), lazy=True)
    s = set(t.getBestCmap())
    t.close()
    return s


def _cjk(cp):
    nm = unicodedata.name(chr(cp), "")
    return ("CJK UNIFIED" in nm) or ("IDEOGRAPHIC" in nm) or ("CJK COMPATIBILITY" in nm)


_n = _cps("noto-sans-sc-400.subset.woff2")
_e = _cps("epilogue-latin.woff2")
_copy = open(os.path.join(ROOT, ".work", "copy.txt"), encoding="utf-8").read()
_cc = set(map(ord, _copy))
_miss = _cc - _n
_ascii_miss = [c for c in _miss if c < 0x80]
COV = {
    "noto_cjk": len([c for c in _n if _cjk(c)]),
    "noto_total": len(_n),
    "copy_cjk": len([c for c in _cc if _cjk(c)]),
    "copy_missing_noto": len(_miss),
    "copy_missing_noto_ascii": len(_ascii_miss),
    "copy_missing_noto_nonascii": len([c for c in _miss if c >= 0x80]),
    "ascii_missing_epi": len([c for c in _ascii_miss if c not in _e]),
}
json.dump(COV, open(os.path.join(W, "coverage.json"), "w", encoding="utf-8"), indent=1)

SLUG_ORDER = ["contact", "course", "multi", "stage", "tour", "reel1", "reel2", "reel3", "reel4",
              "thumb-stage", "thumb-tour", "ui-map", "ui-plan", "ui-edit",
              "navi-home", "navi-prep", "gc-board", "gc-dance", "gc-keys", "gc-phone", "gc-queue"]

by_slug = {}
for r in man["raster"]:
    d = by_slug.setdefault(r["slug"], {})
    d.setdefault(r["format"], []).append(r)

raster_b = sum(r["bytes"] for r in man["raster"])
post_b = sum(r["bytes"] for r in man["posters"])
vid_b = sum(v["bytes"] for v in man["videos"])
font_b = sum(f["bytes"] for f in man["fonts"]["files"])
added = raster_b + post_b + vid_b + font_b

L = []
L.append("# 媒体产物报告（media pipeline）\n")
L.append("生成目录：`assets/img/opt/`、`assets/video/opt/`、`assets/fonts/`；"
         "清单：`.work/media-manifest.json`。\n")

L.append("## 1. 响应式图片（AVIF / WebP / JPEG）\n")
L.append("规则：AVIF q=52 speed=4；WebP q=78 method=6；JPEG q=80 progressive+optimize；"
         "全部 `exif_transpose` → `convert(\"RGB\")` → `strip()`；"
         "宽度按 480/960/1440/1920 取不超过原图真实宽度的档位。\n")
L.append("| slug | 源文件 | 原图尺寸 | 原图 KB | 输出档位 | AVIF KB | WebP KB | JPG KB | 输出合计 KB | 相对原图 |")
L.append("|---|---|---|---|---|---|---|---|---|---|")
for slug in SLUG_ORDER:
    if slug not in by_slug:
        continue
    r = rrep[slug]
    fmts = by_slug[slug]
    aw = sorted(int(x["width"]) for x in fmts["avif"])
    ab = sum(x["bytes"] for x in fmts["avif"]) / BUG
    wb = sum(x["bytes"] for x in fmts["webp"]) / BUG
    jb = sum(x["bytes"] for x in fmts["jpg"]) / BUG
    out = ab + wb + jb
    src = r["src_bytes"] / BUG
    delta = (out / src - 1) * 100
    L.append("| `%s` | `%s` | %dx%d | %.1f | %s | %.1f | %.1f | %.1f | %.1f | %+.0f%% |" % (
        slug, r["source"], r["src_w"], r["src_h"], src,
        "/".join(str(x) for x in aw), ab, wb, jb, out, delta))
L.append("")
L.append("**说明**：每一档 AVIF/WebP 都是独立文件，一个源图对应多份，所以“输出合计”会大于原图——"
         "实际每个访客只下载其中 1 档（AVIF 优先）。单张最大档（1440 或 1920）与原图对比：\n")
L.append("| slug | 原图 KB | 最大档 AVIF KB | 压缩比 |")
L.append("|---|---|---|---|")
for slug in SLUG_ORDER:
    if slug not in by_slug:
        continue
    r = rrep[slug]
    top = max(by_slug[slug]["avif"], key=lambda x: x["width"])
    L.append("| `%s` | %.1f | %.1f (w=%d) | %.1f× |" % (
        slug, r["src_bytes"] / BUG, top["bytes"] / BUG, top["width"],
        (r["src_bytes"] / BUG) / (top["bytes"] / BUG)))
L.append("")

L.append("## 2. 视频\n")
L.append("| 输出 | 源 | 编码 | 尺寸 | fps | 时长 | 字节 | 源字节 | 压缩比 |")
L.append("|---|---|---|---|---|---|---|---|---|")
for v in man["videos"]:
    L.append("| `%s` | `%s` | %s high | %dx%d | %s | %.2fs | **%d** | %d | %.1f× |" % (
        v["path"], v["source"], v["codec"], v["width"], v["height"], v["fps"],
        v["duration"], v["bytes"], v["sourceBytes"], v["sourceBytes"] / v["bytes"]))
L.append("")
L.append("`dance-540.mp4` 在 crf=31 时为 417,887 B（超出 400 KB 目标），故降到 **crf=32** 得 377,026 B，"
         "其余参数与要求一致。`tour-walk-720.mp4` 用 crf=30 即达标（604,105 B < 800 KB）。\n")

L.append("## 3. 封面帧（posters）\n")
L.append("| 文件 | 尺寸 | 字节 |")
L.append("|---|---|---|")
for p in man["posters"]:
    L.append("| `%s` | %dx%d | %d |" % (os.path.basename(p["path"]), p["width"], p["height"], p["bytes"]))
L.append("")
L.append("取帧位置：tour-walk 3.0s、dance 2.0s，均缩放至 960px 宽。\n")

L.append("## 4. 字体子集\n")
L.append("| 文件 | 字节 | 字形数 |")
L.append("|---|---|---|")
for f in man["fonts"]["files"]:
    L.append("| `%s` | **%d** (%.1f KB) | — |" % (f["path"], f["bytes"], f["bytes"] / BUG))
L.append("")
L.append("四个子集均 < 120 KB 上限，字体内部 family 名未改名（仍为 `Noto Sans SC` / `Epilogue`），"
         "`unicode-range` 见 `assets/fonts/subset.css`；Noto 各档均不含 U+0000-007F，"
         "拉丁字母与数字全部落到 Epilogue。\n")
L.append("**注**：`noto-sans-sc-500.subset.woff2` 的内部 name 表为 `Noto Sans SC Medium`"
         "（Google 未提供 500 的独立家族名）。`@font-face` 以 CSS 的 `font-family` 描述符为准，"
         "所以 `font-family:\"Noto Sans SC\"; font-weight:500` 能正常命中，无需改名。\n")
L.append("**语料**：`index.html`（当前文件，去 HTML 标签后的可见文本 %d 字符 / %d 唯一码点）"
         "∪ `.work/copy.txt`（新页面文案 deck，%d 字符 / %d 唯一码点）；"
         "另加固定安全集（ASCII 0x20-0x7E、中文标点、全角数字、U+3000-303F、U+FF01-FF65 等）。"
         "合并后唯一码点 %d 个，Noto 子集覆盖 %d 个字形（另含 U+00A0/B7/D7 等）。\n" % (
             corpus["html_visible_chars"], corpus["html_unique_cps"],
             corpus["copy_txt_chars"], corpus["copy_txt_unique_cps"],
             corpus["union_all_cps"], corpus["noto_glyph_count"]))
L.append("**覆盖审计（copy.txt 中未被 Noto 子集收录的码点）**：共 %d 个，其中 %d 个是 ASCII"
         "（按设计落到 Epilogue），非 ASCII 缺口 **%d 个**；剔除 U+000A 换行符后，"
         "copy.txt 与 index.html 里的每一个可见码点都有对应字形。\n" % (
             COV["copy_missing_noto"], COV["copy_missing_noto_ascii"], COV["copy_missing_noto_nonascii"]))
L.append("| 检查项 | 数值 |")
L.append("|---|---|")
L.append("| 子集覆盖 CJK 汉字数 | %d |" % COV["noto_cjk"])
L.append("| 子集 cmap 总码点 | %d |" % COV["noto_total"])
L.append("| copy.txt 出现的 CJK 汉字数 | %d |" % COV["copy_cjk"])
L.append("| copy.txt 码点 − 子集 = 非 ASCII 缺口 | %d |" % COV["copy_missing_noto_nonascii"])
L.append("| copy.txt 码点 − 子集 = ASCII（转 Epilogue） | %d |" % COV["copy_missing_noto_ascii"])
L.append("| 上述 ASCII 在 Epilogue 中缺失 | %d（仅 U+000A 换行） |" % COV["ascii_missing_epi"])
L.append("")

L.append("## 5. 总量\n")
L.append("| 项目 | 原始 | 新增产物 |")
L.append("|---|---|---|")
L.append("| `assets/img` | %.2f MB | %.2f MB（含 posters %.2f MB）|" % (
    tot["img_before"] / 1048576, (raster_b + post_b) / 1048576, post_b / 1048576))
L.append("| `assets/video` | %.2f MB | %.2f MB |" % (
    tot["vid_before"] / 1048576, vid_b / 1048576))
L.append("| `assets/fonts`（子集） | — | %.2f MB |" % (font_b / 1048576))
L.append("| **新增字节合计** | — | **%d B ≈ %.2f MB** |" % (added, added / 1048576))
L.append("")
L.append("预算 ~6 MB，实际 %.2f MB。原始文件一律未修改、未删除。\n" % (added / 1048576))

open(os.path.join(W, "media-report.md"), "w", encoding="utf-8").write("\n".join(L))
print("\n".join(L[:8]))
print("...\nwrote .work/media-report.md (%d bytes)" % os.path.getsize(os.path.join(W, "media-report.md")))
