# -*- coding: utf-8 -*-
"""Full verification of all deliverables."""
import os, json, sys, subprocess
from PIL import Image
from fontTools.ttLib import TTFont

ROOT = r"D:\code\unitree-site"
W = os.path.join(ROOT, ".work")
FONTS = os.path.join(ROOT, "assets", "fonts")
fail = []
log = []


def say(s):
    log.append(s)
    print(s)
    sys.stdout.flush()


man = json.load(open(os.path.join(W, "media-manifest.json"), encoding="utf-8"))

# ---------- (a) every manifest file exists and non-zero ----------
say("=== (a) manifest files exist / non-zero ===")
paths = []
for r in man["raster"]:
    paths.append(("raster", r["path"], r["bytes"]))
for r in man["posters"]:
    paths.append(("poster", r["path"], r["bytes"]))
for r in man["videos"]:
    paths.append(("video", r["path"], r["bytes"]))
for r in man["fonts"]["files"]:
    paths.append(("font", r["path"], r["bytes"]))

missing, zero, mismatch = [], [], []
for kind, rel, claimed in paths:
    p = os.path.join(ROOT, rel.replace("/", os.sep))
    if not os.path.isfile(p):
        missing.append(rel); continue
    actual = os.path.getsize(p)
    if actual == 0:
        zero.append(rel)
    if actual != claimed:
        mismatch.append((rel, claimed, actual))
say("  entries=%d  missing=%d  zero=%d  size_mismatch=%d" % (len(paths), len(missing), len(zero), len(mismatch)))
for x in missing: say("   MISSING %s" % x)
for x in zero: say("   ZERO %s" % x)
for x in mismatch: say("   SIZE-MISMATCH %s claimed=%d actual=%d" % x)
if missing or zero or mismatch:
    fail.append("(a) manifest/files")

# ---------- (b) every emitted AVIF opens in Pillow ----------
say("=== (b) AVIF decode check ===")
avifs = sorted([p for p in os.listdir(os.path.join(ROOT, "assets", "img", "opt"))
                if p.endswith(".avif")])
bad_avif = []
for f in avifs:
    p = os.path.join(ROOT, "assets", "img", "opt", f)
    try:
        with Image.open(p) as im:
            im.load()
            if im.width == 0 or im.height == 0:
                bad_avif.append((f, "zero dims"))
    except Exception as e:
        bad_avif.append((f, repr(e)))
say("  avif_files=%d  failures=%d" % (len(avifs), len(bad_avif)))
for b in bad_avif: say("   BAD %s %s" % b)
if bad_avif:
    fail.append("(b) avif decode")

# also verify dimensions recorded in manifest match the decoded pixel size
say("  -- manifest width/height vs decoded --")
dims_bad = []
for r in man["raster"] + man["posters"]:
    p = os.path.join(ROOT, r["path"].replace("/", os.sep))
    try:
        with Image.open(p) as im:
            if (im.width, im.height) != (r["width"], r["height"]):
                dims_bad.append((r["path"], (r["width"], r["height"]), (im.width, im.height)))
    except Exception as e:
        dims_bad.append((r["path"], "open-fail", repr(e)))
say("  dimension_mismatches=%d" % len(dims_bad))
for d in dims_bad[:10]: say("   DIM %s" % (d,))
if dims_bad:
    fail.append("(b) dims")

# ---------- (c) videos ----------
say("=== (c) video ffprobe ===")
for v in man["videos"]:
    p = os.path.join(ROOT, v["path"].replace("/", os.sep))
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=codec_name,width,height,r_frame_rate,nb_frames",
         "-show_entries", "format=duration,size", "-of", "json", p],
        capture_output=True, text=True)
    d = json.loads(out.stdout)
    st = d["streams"][0]; fmt = d["format"]
    dur = float(fmt["duration"]); size = int(fmt["size"])
    say("  %-22s codec=%s %dx%d fps=%s frames=%s dur=%.3fs bytes=%d" % (
        os.path.basename(p), st["codec_name"], st["width"], st["height"],
        st["r_frame_rate"], st.get("nb_frames"), dur, size))
    if st["codec_name"] != "h264":
        fail.append("(c) codec %s" % v["path"])
    if abs(dur - v["duration"]) > 0.35:
        fail.append("(c) duration %s" % v["path"])


# ---------- (d) font cmap ASCII check ----------
say("=== (d) font subset cmap ===")
for fn in ("noto-sans-sc-400.subset.woff2", "noto-sans-sc-500.subset.woff2",
           "noto-sans-sc-700.subset.woff2", "epilogue-latin.woff2"):
    p = os.path.join(FONTS, fn)
    t = TTFont(p, lazy=True)
    cm = t.getBestCmap()
    cps = sorted(cm)
    asci = [c for c in cps if c < 0x80]
    fam = t["name"].getDebugName(1)
    t.close()
    say("  %-32s bytes=%-7d glyphs=%-4d min=U+%04X max=U+%04X ascii=%d family=%r" % (
        fn, os.path.getsize(p), len(cps), cps[0], cps[-1], len(asci), fam))
    if fn.startswith("noto"):
        if asci:
            fail.append("(d) noto has ascii: %s" % fn)
        # upstream family names are preserved verbatim (never renamed by us):
        # 400/700 -> "Noto Sans SC", 500 -> "Noto Sans SC Medium" (Google's own name).
        # @font-face matches on the CSS font-family descriptor, so both resolve as "Noto Sans SC".
        if fam not in ("Noto Sans SC", "Noto Sans SC Medium"):
            fail.append("(d) noto family renamed: %r" % fam)
    else:
        if fam != "Epilogue":
            fail.append("(d) epilogue family renamed: %r" % fam)
        if not asci:
            fail.append("(d) epilogue missing ascii")

# ---------- (e) totals ----------
say("=== (e) totals ===")
tot = json.load(open(os.path.join(W, "totals.json"), encoding="utf-8"))
raster_b = sum(r["bytes"] for r in man["raster"])
post_b = sum(r["bytes"] for r in man["posters"])
vid_b = sum(r["bytes"] for r in man["videos"])
font_b = sum(r["bytes"] for r in man["fonts"]["files"])
say("  raster=%d  posters=%d  videos=%d  fonts=%d" % (raster_b, post_b, vid_b, font_b))
say("  ADDED TOTAL = %d bytes (%.2f MB)" % (raster_b + post_b + vid_b + font_b,
                                            (raster_b + post_b + vid_b + font_b) / 1048576))
say("  img  before=%d after=%d  (%.2f MB -> %.2f MB)" % (
    tot["img_before"], tot["img_after"], tot["img_before"] / 1048576, tot["img_after"] / 1048576))
say("  video before=%d after=%d (%.2f MB -> %.2f MB)" % (
    tot["vid_before"], tot["vid_after"], tot["vid_before"] / 1048576, tot["vid_after"] / 1048576))
say("  fonts after=%d (%.2f KB)" % (font_b, font_b / 1024))

say("")
if fail:
    say(">>> FAILURES: " + "; ".join(fail))
else:
    say(">>> ALL CHECKS PASSED")

open(os.path.join(W, "verify.log"), "w", encoding="utf-8").write("\n".join(log))
