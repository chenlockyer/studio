# -*- coding: utf-8 -*-
"""Build the font subset corpus from index.html (+ optional .work/copy.txt)."""
import os, re, json, html, sys, unicodedata

ROOT = r"D:\code\unitree-site"
HTML = os.path.join(ROOT, "index.html")
COPY = os.path.join(ROOT, ".work", "copy.txt")

INLINE_SKIP = re.compile(r"<(script|style|noscript|template)\b[^>]*>.*?</\1\s*>", re.I | re.S)
COMMENT = re.compile(r"<!--.*?-->", re.S)
TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"[ \t\r\n\f\v]+")


def visible_text(h):
    h = COMMENT.sub(" ", h)
    h = INLINE_SKIP.sub(" ", h)          # script/style content is not visible text
    h = TAG.sub(" ", h)
    h = html.unescape(h)
    return WS.sub(" ", h)


def read(p):
    with open(p, "rb") as f:
        raw = f.read()
    for enc in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace"), "utf-8(replace)"


def cjk_only(cps):
    """Codepoints belonging to the CJK / CJK-punct families (non-ASCII side)."""
    out = set()
    for cp in cps:
        if cp < 0x80:
            continue
        blk = unicodedata.name(chr(cp), "")
        if any(k in blk for k in ("CJK", "IDEOGRAPHIC", "FULLWIDTH", "HALFWIDTH",
                                  "HIRAGANA", "KATAKANA", "BOPOMOFO", "KANGXI",
                                  "HANGUL", "VERTICAL", "DUNNO")):
            out.add(cp)
    return out


# ---- safety set (always included) ----
SAFETY = set()
SAFETY |= set(range(0x20, 0x7F))                                    # ASCII printable
for ch in "。，、；：？！（）【】《》「」『』…—～·－＋×→←↑↓／":
    SAFETY.add(ord(ch))
SAFETY |= set(range(0xFF10, 0xFF1A))                                # fullwidth digits ０-９
SAFETY |= set(range(0x3000, 0x3040))                                # CJK symbols & punctuation
SAFETY |= set(range(0xFF01, 0xFF66))                                # fullwidth forms

html_src, html_enc = read(HTML)
html_text = visible_text(html_src)

copy_text = None
copy_enc = None
if os.path.isfile(COPY):
    copy_text, copy_enc = read(COPY)

corpus_text = html_text if copy_text is None else (html_text + "\n" + copy_text)
html_cps = set(map(ord, html_text))
copy_cps = set(map(ord, copy_text)) if copy_text is not None else set()
corpus_cps = set(map(ord, corpus_text))

ALL = corpus_cps | SAFETY

# ---- Noto subset target: non-ASCII corpus + non-ASCII safety, ASCII excluded ----
noto_cps = {cp for cp in ALL if cp >= 0x80}
noto_cps |= {ord(c) for c in "。，、；：？！（）【】《》「」『』…—～·－＋×→←↑↓／"}
noto_cps |= set(range(0xFF10, 0xFF1A)) | set(range(0x3000, 0x3040)) | set(range(0xFF01, 0xFF66))
noto_cps = {cp for cp in noto_cps if cp >= 0x80}

# ---- Epilogue target ----
EPI = set()
EPI |= set(range(0x0020, 0x007F))
EPI |= set(range(0x00A0, 0x0100))
EPI |= set(range(0x2000, 0x2070))
EPI |= set(range(0x2190, 0x2200))
EPI.add(0x00D7)
EPI.add(0x2212)


def to_file(cps, path):
    """pyftsubset --text-file: one codepoint per line as UTF-8 chars."""
    s = "".join(chr(cp) for cp in sorted(cps))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    return len(s)


n1 = to_file(noto_cps, os.path.join(ROOT, ".work", "noto-glyphs.txt"))
n2 = to_file(EPI, os.path.join(ROOT, ".work", "epilogue-glyphs.txt"))

meta = {
    "html_encoding": html_enc,
    "html_visible_chars": len(html_text),
    "html_unique_cps": len(html_cps),
    "copy_txt_present": copy_text is not None,
    "copy_txt_encoding": copy_enc,
    "copy_txt_chars": len(copy_text) if copy_text is not None else 0,
    "copy_txt_unique_cps": len(copy_cps),
    "corpus_unique_cps": len(corpus_cps),
    "safety_unique_cps": len(SAFETY),
    "union_all_cps": len(ALL),
    "noto_glyph_count": n1,
    "noto_ascii_included": sum(1 for cp in noto_cps if cp < 0x80),
    "epilogue_glyph_count": n2,
    "noto_min_cp": min(noto_cps), "noto_max_cp": max(noto_cps),
}
json.dump(meta, open(os.path.join(ROOT, ".work", "corpus-meta.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(json.dumps(meta, ensure_ascii=False, indent=1))
print("\nnoto sample:", "".join(chr(c) for c in sorted(noto_cps)[:40]))
