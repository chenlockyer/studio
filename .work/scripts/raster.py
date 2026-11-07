# -*- coding: utf-8 -*-
"""TASK 1: responsive raster derivatives -> assets/img/opt/"""
import os, sys, json, io, time
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None

ROOT = r"D:\code\unitree-site"
SRC = os.path.join(ROOT, "assets", "img")
OUT = os.path.join(ROOT, "assets", "img", "opt")
os.makedirs(OUT, exist_ok=True)

WIDTHS = [480, 960, 1440, 1920]
FLATTEN = (0x0B, 0x0D, 0x0F)  # #0b0d0f

# slug -> source filename (CJK read from dir listing, never hand-typed)
SLUG_MAP = {
    "contact": "bg-contact.jpg",
    "course": "bg-course.jpg",
    "multi": "bg-multi.jpg",
    "stage": "bg-stage.jpg",
    "tour": "bg-tour.jpg",
    "reel1": "reel-1-front.jpg",
    "reel2": "reel-2-walk.jpg",
    "reel3": "reel-3-dance.jpg",
    "reel4": "reel-4-conduct.jpg",
    "thumb-stage": "thumb-stage.jpg",
    "thumb-tour": "thumb-tour-card.jpg",
    "ui-map": "ui-1-map.jpg",
    "ui-plan": "ui-2-plan.jpg",
    "ui-edit": "ui-3-edit.jpg",
    "navi-home": "\u5bfc\u89c8\u4e3b\u9875\u9762.png",
    "navi-prep": "\u5bfc\u89c8-\u51c6\u5907\u9875\u9762.png",
    "gc-board": "\u7fa4\u63a7-\u4e3b\u9875\u9762.png",
    "gc-dance": "\u7fa4\u63a7-\u5b98\u65b9\u821e\u8e48\u9875\u9762.png",
    "gc-keys": "\u7fa4\u63a7-\u81ea\u5b9a\u4e49\u6309\u952e.png",
    "gc-phone": "\u7fa4\u63a7\u624b\u673a\u7aef.jpg",
    "gc-queue": "\u652f\u6301\u81ea\u5b9a\u4e49\u821e\u8e48\u961f\u5217\u4e00\u952e\u4e0b\u53d1.png",
}

AVIF_Q, AVIF_SPEED = 52, 4
WEBP_Q, WEBP_METHOD = 78, 6
JPEG_Q = 80


def load_rgb(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    has_alpha = (im.mode in ("RGBA", "LA", "PA")) or ("transparency" in im.info)
    if has_alpha:
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, FLATTEN)
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    im.info = {}  # strip metadata before any save
    return im


def resize(im, w):
    if w >= im.width:
        return im.copy()
    h = max(1, round(im.height * w / im.width))
    return im.resize((w, h), Image.LANCZOS)


def save_avif(im, path, q=AVIF_Q):
    im.save(path, "AVIF", quality=q, speed=AVIF_SPEED)


def save_webp(im, path):
    im.save(path, "WEBP", quality=WEBP_Q, method=WEBP_METHOD)


def save_jpeg(im, path):
    im.save(path, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)


def main():
    results = []
    report = []
    manifest_rows = []
    inv = {r["name"]: r for r in json.load(open(os.path.join(ROOT, ".work", "inventory.json"), encoding="utf-8"))}

    for slug, fname in SLUG_MAP.items():
        path = os.path.join(SRC, fname)
        if not os.path.isfile(path):
            report.append({"slug": slug, "error": "missing source: %r" % fname})
            print("MISSING %s -> %r" % (slug, fname)); sys.stdout.flush()
            continue
        t0 = time.time()
        im = load_rgb(path)
        src_w, src_h = im.width, im.height
        src_bytes = os.path.getsize(path)

        # ladder: skip widths larger than the source's real width
        ladder = [w for w in WIDTHS if w <= src_w]
        # source narrower than the smallest tier -> emit native 1x so the slug is not naked
        if not ladder:
            ladder = [src_w]

        slug_files = []
        avif_paths = []
        for w in ladder:
            r = resize(im, w)
            ap = os.path.join(OUT, "%s-%d.avif" % (slug, w))
            wp = os.path.join(OUT, "%s-%d.webp" % (slug, w))
            save_avif(r, ap)
            save_webp(r, wp)
            avif_paths.append((ap, w, r.size))
            slug_files.append(("avif", w, r.size, ap))
            slug_files.append(("webp", w, r.size, wp))

        # AVIF per-slug budget guard: >400KB set -> lower quality (never skip a width)
        avif_total = sum(os.path.getsize(p) for p, _, _ in avif_paths)
        q_used = AVIF_Q
        if avif_total > 400 * 1024:
            for q_try in (46, 40, 34):
                for ap, w, size in avif_paths:
                    save_avif(resize(im, w), ap, q=q_try)
                avif_total = sum(os.path.getsize(p) for p, _, _ in avif_paths)
                q_used = q_try
                if avif_total <= 400 * 1024:
                    break

        # JPEG fallback: canonical -960 slot; pixel width is min(960, src_w) so we never upscale
        jw = min(960, src_w)
        jr = resize(im, jw)
        jp = os.path.join(OUT, "%s-960.jpg" % slug)
        save_jpeg(jr, jp)
        slug_files.append(("jpg", jw, jr.size, jp))

        for fmt, w, size, p in slug_files:
            manifest_rows.append({
                "path": "assets/img/opt/%s" % os.path.basename(p),
                "slug": slug, "format": fmt, "width": size[0], "height": size[1],
                "bytes": os.path.getsize(p),
            })
        report.append({
            "slug": slug, "source": fname, "src_w": src_w, "src_h": src_h, "src_bytes": src_bytes,
            "ladder": ladder, "avif_q": q_used,
            "out_bytes": sum(os.path.getsize(p) for _, _, _, p in slug_files),
            "secs": round(time.time() - t0, 1),
        })
        print("OK %-11s %-28s %4dx%-4d ladder=%-18s avifQ=%d %.1fs" % (
            slug, (fname[:26]), src_w, src_h, str(ladder), q_used, time.time() - t0))
        sys.stdout.flush()

    json.dump(manifest_rows, open(os.path.join(ROOT, ".work", "raster-results.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    json.dump(report, open(os.path.join(ROOT, ".work", "raster-report.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    total = sum(r["bytes"] for r in manifest_rows)
    print("\nfiles=%d total_bytes=%d (%.2f MB)" % (len(manifest_rows), total, total / 1048576))


if __name__ == "__main__":
    main()
