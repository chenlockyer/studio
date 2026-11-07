# -*- coding: utf-8 -*-
"""TASK 2b: poster frames -> assets/img/opt/poster-{tour,dance}.{jpg,webp,avif} @960w"""
import os
from PIL import Image

ROOT = r"D:\code\unitree-site"
FRAMES = os.path.join(ROOT, ".work", "frames")
OUT = os.path.join(ROOT, "assets", "img", "opt")
FLATTEN = (0x0B, 0x0D, 0x0F)
TARGET_W = 960


def load_rgb(path):
    im = Image.open(path)
    has_alpha = (im.mode in ("RGBA", "LA", "PA")) or ("transparency" in im.info)
    if has_alpha:
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, FLATTEN)
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    im.info = {}
    return im


def resize(im, w):
    if w >= im.width:
        return im.copy()
    return im.resize((w, max(1, round(im.height * w / im.width))), Image.LANCZOS)


rows = []
for slug in ("tour", "dance"):
    src = os.path.join(FRAMES, "%s.png" % slug)
    im = load_rgb(src)
    r = resize(im, TARGET_W)
    for fmt, ext, kw in (
        ("jpg", "jpg", dict(quality=80, optimize=True, progressive=True)),
        ("webp", "webp", dict(quality=78, method=6)),
        ("avif", "avif", dict(quality=52, speed=4)),
    ):
        p = os.path.join(OUT, "poster-%s.%s" % (slug, ext))
        r.save(p, {"jpg": "JPEG", "webp": "WEBP", "avif": "AVIF"}[fmt], **kw)
        rows.append({"path": "assets/img/opt/%s" % os.path.basename(p), "slug": "poster-%s" % slug,
                     "format": fmt, "width": r.width, "height": r.height,
                     "bytes": os.path.getsize(p), "role": "poster"})
        print("%-28s %-5s %dx%d %d B" % (os.path.basename(p), fmt, r.width, r.height, os.path.getsize(p)))

import json
json.dump(rows, open(os.path.join(ROOT, ".work", "poster-results.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nposter files=%d total=%d B" % (len(rows), sum(r["bytes"] for r in rows)))
