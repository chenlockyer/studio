import os, subprocess, json
from PIL import Image, ImageOps
MEDIA = r"D:\my_media\video\unitree_g1"
ROOT = r"D:\code\unitree-site"
OUT = os.path.join(ROOT,"assets","img","v3boot","poster")

# poster 必须与视频实际尺寸一致，否则浏览器会拉伸。
# 直接从已编码好的 v3boot 视频里取第 0 帧 —— 这是最可靠的做法。
VID = os.path.join(ROOT,"assets","video","v3boot")
JOBS = [
    ("group-sync.mp4","group-sync.jpg"),
    ("choreo-chain.mp4","choreo-chain.jpg"),
    ("navi-run.mp4","navi-run.jpg"),
    ("slam-build.mp4","slam-build.jpg"),
    ("dance-loop.mp4","dance-loop.jpg"),
    ("slot-1.mp4","slot-1.jpg"),
    ("slot-2.mp4","slot-2.jpg"),
    ("slot-3.mp4","slot-3.jpg"),
    ("slot-4.mp4","slot-4.jpg"),
]
for vid, jpg in JOBS:
    src = os.path.join(VID, vid)
    if not os.path.isfile(src):
        print("MISSING", vid); continue
    tmp = os.path.join(OUT, "_t.png")
    r = subprocess.run(["ffmpeg","-y","-v","error","-i",src,"-frames:v","1","-vf","scale=iw*2:-2:flags=lanczos",tmp],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL", vid, r.stderr[-200:]); continue
    im = Image.open(tmp).convert("RGB")
    outp = os.path.join(OUT, jpg)
    im.save(outp, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"  {jpg:20s} {im.width}x{im.height}  {os.path.getsize(outp)/1024:7.1f} KB")
    os.remove(tmp)

# 同步更新 boot-manifest 里的 poster 尺寸
mp = os.path.join(ROOT,".work","boot-manifest.json")
m = json.load(open(mp, encoding="utf-8"))
for p in m["posters"]:
    fp = os.path.join(ROOT, p["path"].replace("/", os.sep))
    if os.path.isfile(fp):
        im = Image.open(fp)
        p["w"], p["h"] = im.width, im.height
        p["bytes"] = os.path.getsize(fp)
json.dump(m, open(mp,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nposter 尺寸已修正并写回 manifest")
