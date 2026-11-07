# -*- coding: utf-8 -*-
"""TASK 5: build .work/media-manifest.json + .work/media-report.md"""
import os, json, glob, subprocess

ROOT = r"D:\code\unitree-site"
W = os.path.join(ROOT, ".work")
IMG = os.path.join(ROOT, "assets", "img")
OPT = os.path.join(ROOT, "assets", "img", "opt")
VID = os.path.join(ROOT, "assets", "video")
VOPT = os.path.join(ROOT, "assets", "video", "opt")
FONTS = os.path.join(ROOT, "assets", "fonts")

SLUG_MAP = {
    "contact": "bg-contact.jpg", "course": "bg-course.jpg", "multi": "bg-multi.jpg",
    "stage": "bg-stage.jpg", "tour": "bg-tour.jpg",
    "reel1": "reel-1-front.jpg", "reel2": "reel-2-walk.jpg", "reel3": "reel-3-dance.jpg",
    "reel4": "reel-4-conduct.jpg",
    "thumb-stage": "thumb-stage.jpg", "thumb-tour": "thumb-tour-card.jpg",
    "ui-map": "ui-1-map.jpg", "ui-plan": "ui-2-plan.jpg", "ui-edit": "ui-3-edit.jpg",
    "navi-home": "\u5bfc\u89c8\u4e3b\u9875\u9762.png",
    "navi-prep": "\u5bfc\u89c8-\u51c6\u5907\u9875\u9762.png",
    "gc-board": "\u7fa4\u63a7-\u4e3b\u9875\u9762.png",
    "gc-dance": "\u7fa4\u63a7-\u5b98\u65b9\u821e\u8e48\u9875\u9762.png",
    "gc-keys": "\u7fa4\u63a7-\u81ea\u5b9a\u4e49\u6309\u952e.png",
    "gc-phone": "\u7fa4\u63a7\u624b\u673a\u7aef.jpg",
    "gc-queue": "\u652f\u6301\u81ea\u5b9a\u4e49\u821e\u8e48\u961f\u5217\u4e00\u952e\u4e0b\u53d1.png",
}

raster = json.load(open(os.path.join(W, "raster-results.json"), encoding="utf-8"))
posters = json.load(open(os.path.join(W, "poster-results.json"), encoding="utf-8"))
corpus = json.load(open(os.path.join(W, "corpus-meta.json"), encoding="utf-8"))

videos = []
for name, src_name, spec in (
    ("tour-walk-720.mp4", "tour-walk.mp4", "scale=720:-2 fps=30 crf30 preset=slow profile=high yuv420p +faststart -an"),
    ("dance-540.mp4", "dance.mp4", "scale=540:-2 fps=30 crf32 preset=slow profile=high yuv420p +faststart -an"),
):
    p = os.path.join(VOPT, name)
    sp = os.path.join(VID, src_name)
    pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                         "-show_entries", "stream=codec_name,width,height,r_frame_rate,nb_frames",
                         "-show_entries", "format=duration,size", "-of", "json", p],
                        capture_output=True, text=True)
    meta = json.loads(pr.stdout)
    st = meta["streams"][0]
    videos.append({
        "path": "assets/video/opt/%s" % name, "source": "assets/video/%s" % src_name,
        "bytes": os.path.getsize(p), "sourceBytes": os.path.getsize(sp), "settings": spec,
        "codec": st["codec_name"], "width": st["width"], "height": st["height"],
        "fps": st["r_frame_rate"], "frames": int(st.get("nb_frames", 0)),
        "duration": float(meta["format"]["duration"]),
    })

font_files = []
for fn in sorted(os.listdir(FONTS)):
    if fn.endswith(".woff2"):
        p = os.path.join(FONTS, fn)
        font_files.append({"path": "assets/fonts/%s" % fn, "bytes": os.path.getsize(p)})

# codepoint coverage of all subset fonts (union)
from fontTools.ttLib import TTFont
cov = set()
for fn in ("noto-sans-sc-400.subset.woff2", "noto-sans-sc-500.subset.woff2",
           "noto-sans-sc-700.subset.woff2", "epilogue-latin.woff2"):
    p = os.path.join(FONTS, fn)
    if os.path.isfile(p):
        t = TTFont(p, lazy=True); cov |= set(t.getBestCmap()); t.close()

manifest = {
    "raster": raster,
    "videos": videos,
    "posters": posters,
    "fonts": {"files": font_files, "coversCodepoints": len(cov)},
}
json.dump(manifest, open(os.path.join(W, "media-manifest.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ---------- totals ----------
img_before = sum(os.path.getsize(os.path.join(IMG, f)) for f in os.listdir(IMG)
                 if os.path.isfile(os.path.join(IMG, f)))
img_after = sum(r["bytes"] for r in raster) + sum(r["bytes"] for r in posters)
vid_before = sum(os.path.getsize(os.path.join(VID, f)) for f in os.listdir(VID)
                 if os.path.isfile(os.path.join(VID, f)))
vid_after = sum(v["bytes"] for v in videos)
fonts_after = sum(f["bytes"] for f in font_files)

print(json.dumps({"img_before": img_before, "img_after": img_after,
                  "vid_before": vid_before, "vid_after": vid_after,
                  "fonts_after": fonts_after}, indent=1))
json.dump({"img_before": img_before, "img_after": img_after, "vid_before": vid_before,
           "vid_after": vid_after, "fonts_after": fonts_after},
          open(os.path.join(W, "totals.json"), "w", encoding="utf-8"), indent=1)
