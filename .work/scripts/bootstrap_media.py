# -*- coding: utf-8 -*-
"""
Bootstrap 媒体：在 media-pipeline 队友产出之前，先用现有素材把 v3 页面立起来，
以便尽早验证设计。产物写到 assets/img/v3boot/ 与 assets/video/v3boot/，
不进 assets/*/v3/（那是队友的范围），避免写冲突。
"""
import os, sys, json, subprocess, shutil

ROOT = r"D:\code\unitree-site"
PY = sys.executable
IMG_OUT = os.path.join(ROOT, "assets", "img", "v3boot")
VID_OUT = os.path.join(ROOT, "assets", "video", "v3boot")
os.makedirs(IMG_OUT, exist_ok=True)
os.makedirs(os.path.join(IMG_OUT, "still"), exist_ok=True)
os.makedirs(os.path.join(IMG_OUT, "poster"), exist_ok=True)
os.makedirs(os.path.join(IMG_OUT, "ui"), exist_ok=True)
os.makedirs(VID_OUT, exist_ok=True)

MEDIA = r"D:\my_media\video\unitree_g1"
from PIL import Image, ImageOps

AVIF_Q, AVIF_SPEED = 52, 4
WEBP_Q, WEBP_METHOD = 78, 6
JPEG_Q = 82
FLATTEN = (10, 12, 14)


def ff(*args):
    r = subprocess.run(["ffmpeg", "-y", "-v", "error"] + list(args),
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("  ffmpeg FAIL:", " ".join(args)[:180])
        print("  ", (r.stderr or "")[-500:])
        return False
    return True


def grab_frame(src, t, out_png, scale_filter=None):
    vf = []
    if scale_filter:
        vf.append(scale_filter)
    cmd = ["-ss", f"{t:.3f}", "-i", src, "-frames:v", "1"]
    if vf:
        cmd += ["-vf", ",".join(vf)]
    cmd += [out_png]
    return ff(*cmd)


def load_rgb(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "PA") or "transparency" in im.info:
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
    h = max(1, round(im.height * w / im.width))
    return im.resize((w, h), Image.LANCZOS)


def emit_ladder(im, slug, subdir="still", widths=(480, 960, 1440), budget_kb=200):
    """出 AVIF + WebP 阶梯 + jpg 兜底"""
    d = os.path.join(IMG_OUT, subdir)
    ladder = [w for w in widths if w <= im.width]
    if not ladder:
        ladder = [im.width]
    rows = []
    for w in ladder:
        r = resize(im, w)
        ap = os.path.join(d, f"{slug}-{w}.avif")
        wp = os.path.join(d, f"{slug}-{w}.webp")
        q = AVIF_Q
        r.save(ap, "AVIF", quality=q, speed=AVIF_SPEED)
        # 超预算就降 q
        while os.path.getsize(ap) > budget_kb * 1024 and q > 28:
            q -= 8
            r.save(ap, "AVIF", quality=q, speed=AVIF_SPEED)
        r.save(wp, "WEBP", quality=WEBP_Q, method=WEBP_METHOD)
        rows.append({"fmt": "avif", "w": r.width, "h": r.height,
                     "path": f"assets/img/v3boot/{subdir}/{slug}-{w}.avif",
                     "bytes": os.path.getsize(ap)})
        rows.append({"fmt": "webp", "w": r.width, "h": r.height,
                     "path": f"assets/img/v3boot/{subdir}/{slug}-{w}.webp",
                     "bytes": os.path.getsize(wp)})
    # jpg 兜底：取 960 或原生
    jw = min(960, im.width)
    jr = resize(im, jw)
    jp = os.path.join(d, f"{slug}-960.jpg")
    jr.save(jp, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
    rows.append({"fmt": "jpg", "w": jr.width, "h": jr.height,
                 "path": f"assets/img/v3boot/{subdir}/{slug}-960.jpg",
                 "bytes": os.path.getsize(jp)})
    return rows


def encode_video(src, out_name, t0, dur, w, h=None, crf=30, budget_kb=None):
    outp = os.path.join(VID_OUT, out_name)
    vf = f"scale={w}:-2"
    if h:
        # 裁成固定比例：先缩放覆盖，再居中裁切
        vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    ok = ff("-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", src,
            "-vf", vf, "-r", "30",
            "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-crf", str(crf), "-preset", "slow", "-an", "-movflags", "+faststart",
            outp)
    if not ok:
        return None
    if budget_kb and os.path.getsize(outp) > budget_kb * 1024:
        for c in (34, 38, 42):
            ff("-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", src,
               "-vf", vf, "-r", "30",
               "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
               "-crf", str(c), "-preset", "slow", "-an", "-movflags", "+faststart",
               outp)
            if os.path.getsize(outp) <= budget_kb * 1024:
                break
    return outp


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height,r_frame_rate",
                        "-show_entries", "format=duration,size", "-of", "json", p],
                       capture_output=True, text=True)
    return json.loads(r.stdout)


manifest = {"videos": [], "stills": [], "ui": [], "posters": []}

# ============ 1. 视频 ============
print("=" * 60)
print("A. 视频")
# 群控同步（展厅多机）
group = os.path.join(MEDIA, "群控", "群控.mp4")
specs = [
    # (out, src, t0, dur, w, h, crf, budget_kb)
    ("group-sync.mp4", group, 18.0, 8.0, 1280, 720, 30, 900),
    ("choreo-chain.mp4", os.path.join(MEDIA, "宇树人形机器人全身运动控制.mp4"), 12.0, 10.0, 1280, 720, 30, 900),
    ("navi-run.mp4", os.path.join(MEDIA, "导览", "导览投入使用.mp4"), 8.0, 9.0, 1280, 720, 30, 900),
    ("slam-build.mp4", os.path.join(MEDIA, "导览", "建图巡逻.mp4"), 6.0, 8.0, 1280, 720, 30, 900),
    ("dance-loop.mp4", os.path.join(MEDIA, "江南.mp4"), 5.0, 7.0, 720, 960, 31, 900),
]
for out, src, t0, dur, w, h, crf, budget in specs:
    if not os.path.isfile(src):
        print("  MISSING src:", src); continue
    p = encode_video(src, out, t0, dur, w, h, crf, budget)
    if not p:
        continue
    meta = probe(p)
    st = meta["streams"][0]
    manifest["videos"].append({
        "slug": out, "src": os.path.basename(src), "t0": t0, "dur": dur,
        "w": st["width"], "h": st["height"], "bytes": os.path.getsize(p),
        "duration": round(float(meta["format"]["duration"]), 2),
    })
    print(f"  {out:22s} {st['width']}x{st['height']} {os.path.getsize(p)/1024:7.1f} KB")

# hero 循环槽位（1:1，短，轻）
slot_specs = [
    ("slot-1.mp4", os.path.join(ROOT, "assets", "video", "tour-walk.mp4"), 0.5, 3.0, "走廊行走"),
    ("slot-2.mp4", os.path.join(MEDIA, "导览", "导览投入使用.mp4"), 3.0, 3.0, "正面 LED"),
    ("slot-3.mp4", os.path.join(MEDIA, "群控", "群控.mp4"), 20.0, 3.0, "多机同框"),
    ("slot-4.mp4", os.path.join(MEDIA, "江南.mp4"), 6.0, 3.0, "舞蹈"),
]
for out, src, t0, dur, label in slot_specs:
    if not os.path.isfile(src):
        print("  MISSING slot src:", src); continue
    p = encode_video(src, out, t0, dur, 640, 640, 31, 300)
    if not p:
        continue
    meta = probe(p)
    st = meta["streams"][0]
    manifest["videos"].append({
        "slug": out, "src": os.path.basename(src), "t0": t0, "dur": dur,
        "label": label,
        "w": st["width"], "h": st["height"], "bytes": os.path.getsize(p),
        "duration": round(float(meta["format"]["duration"]), 2),
    })
    print(f"  {out:22s} {st['width']}x{st['height']} {os.path.getsize(p)/1024:7.1f} KB  ({label})")

# ============ 2. 视频 poster ============
print()
print("B. Poster")
poster_src = {
    "group-sync.jpg": (group, 20.0),
    "choreo-chain.jpg": (os.path.join(MEDIA, "宇树人形机器人全身运动控制.mp4"), 15.0),
    "navi-run.jpg": (os.path.join(MEDIA, "导览", "导览投入使用.mp4"), 10.0),
    "slam-build.jpg": (os.path.join(MEDIA, "导览", "建图巡逻.mp4"), 8.0),
    "dance-loop.jpg": (os.path.join(MEDIA, "江南.mp4"), 7.0),
    "slot-1.jpg": (os.path.join(ROOT, "assets", "video", "tour-walk.mp4"), 1.5),
    "slot-2.jpg": (os.path.join(MEDIA, "导览", "导览投入使用.mp4"), 4.0),
    "slot-3.jpg": (group, 21.0),
    "slot-4.jpg": (os.path.join(MEDIA, "江南.mp4"), 7.5),
}
for name, (src, t) in poster_src.items():
    if not os.path.isfile(src):
        continue
    tmp = os.path.join(IMG_OUT, "poster", "_tmp.png")
    ok = grab_frame(src, t, tmp, "scale=1280:-2")
    if not ok:
        continue
    im = load_rgb(tmp)
    # poster 按实际比例输出，不裁
    outp = os.path.join(IMG_OUT, "poster", name)
    im.save(outp, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
    manifest["posters"].append({"name": name, "path": f"assets/img/v3boot/poster/{name}",
                                "w": im.width, "h": im.height, "bytes": os.path.getsize(outp)})
    print(f"  {name:22s} {im.width}x{im.height} {os.path.getsize(outp)/1024:7.1f} KB")
os.path.exists(os.path.join(IMG_OUT, "poster", "_tmp.png")) and os.remove(os.path.join(IMG_OUT, "poster", "_tmp.png"))

# ============ 3. 关键静帧 ============
print()
print("C. 关键静帧（响应式阶梯）")
stills = [
    ("group-wide", group, 24.0, 16),      # 群控多机同框，横
    ("g1-walk", os.path.join(ROOT, "assets", "video", "tour-walk.mp4"), 1.2, 9),
    ("g1-face", os.path.join(MEDIA, "导览", "导览投入使用.mp4"), 4.2, 9),
    ("navi-hall", os.path.join(MEDIA, "导览", "导览投入使用.mp4"), 11.0, 16),
    ("lab-bench", os.path.join(ROOT, "assets", "img", "bg-course.jpg"), None, None),
    ("choreo-sim", os.path.join(MEDIA, "mojoco仿真动作.mp4"), 10.0, 16),
    ("stage-dark", os.path.join(MEDIA, "群控", "群控.mp4"), 34.0, 16),
    ("conductor", os.path.join(MEDIA, "人形机器人指挥家.mp4"), 20.0, 16),
]
for slug, src, t, ratio in stills:
    if not os.path.isfile(src):
        print("  MISSING still src:", src); continue
    if t is None:
        im = load_rgb(src)
    else:
        tmp = os.path.join(IMG_OUT, "still", "_tmp_%s.png" % slug)
        ok = grab_frame(src, t, tmp, "scale=1920:-2")
        if not ok:
            continue
        im = load_rgb(tmp)
        os.remove(tmp)
    rows = emit_ladder(im, slug)
    manifest["stills"].append({"slug": slug, "src": os.path.basename(src), "t": t, "variants": rows})
    tot = sum(r["bytes"] for r in rows)
    print(f"  {slug:14s} {im.width}x{im.height}  {len(rows)} variants  {tot/1024:7.1f} KB")

# ============ 4. 界面截图 ============
print()
print("D. 界面截图")
ui_src = {
    "navi-home": "导览主页面.png",
    "navi-prep": "导览-准备页面.png",
    "gc-dance": "群控-官方舞蹈页面.png",
    "gc-board": "群控-主页面.png",
    "gc-phone": "群控手机端.jpg",
    "gc-keys": "群控-自定义按键.png",
    "gc-queue": "支持自定义舞蹈队列一键下发.png",
}
SRCIMG = os.path.join(ROOT, "assets", "img")
for slug, fname in ui_src.items():
    p = os.path.join(SRCIMG, fname)
    if not os.path.isfile(p):
        print("  MISSING:", fname); continue
    im = load_rgb(p)
    rows = emit_ladder(im, slug, "ui", widths=(480, 960, im.width), budget_kb=260)
    manifest["ui"].append({"slug": slug, "src": fname, "w": im.width, "h": im.height, "variants": rows})
    tot = sum(r["bytes"] for r in rows)
    print(f"  {slug:14s} {im.width}x{im.height}  {len(rows)} variants  {tot/1024:7.1f} KB")

json.dump(manifest, open(os.path.join(ROOT, ".work", "boot-manifest.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print()
print("=" * 60)
for k in ("videos", "posters", "stills", "ui"):
    n = len(manifest[k])
    if k == "videos":
        b = sum(x["bytes"] for x in manifest[k])
    elif k == "posters":
        b = sum(x["bytes"] for x in manifest[k])
    else:
        b = sum(v["bytes"] for x in manifest[k] for v in x["variants"])
    print(f"{k:10s} {n:3d} 项   {b/1048576:6.2f} MB")
print("done")
