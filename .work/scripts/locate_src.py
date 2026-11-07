# 用首帧指纹在源视频里找起始时间点，以便在报告里写准确的素材区间。
import subprocess, os, io, sys, tempfile
import numpy as np
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
MEDIA = r"D:\my_media\video\unitree_g1"

def grab(src, t, w=160):
    tmp = tempfile.mktemp(suffix=".png")
    subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{t:.2f}","-i",src,"-frames:v","1",
                    "-vf",f"scale={w}:-2",tmp], capture_output=True)
    if not os.path.isfile(tmp): return None
    a = np.asarray(Image.open(tmp).convert("L").resize((w, w//2)), dtype=np.float32)
    os.remove(tmp); return a

def find(src, probe, tmax=70, step=0.25):
    p = grab(probe, 0.0)
    if p is None: return None
    best=(1e9,-1)
    t=0.0
    while t < tmax:
        f = grab(src, t)
        if f is not None and f.shape == p.shape:
            d = float(np.abs(f-p).mean())
            if d < best[0]: best=(d,t)
        t += step
    return best

for name, probe, src in [
    ("group-sync.mp4", "assets/video/group-sync.mp4", os.path.join(MEDIA,"群控","群控.mp4")),
    ("dance-live.mp4", "assets/video/dance-live.mp4", os.path.join(MEDIA,"江南.mp4")),
]:
    d,t = find(src, probe)
    print(f"{name}  ← {os.path.basename(src)}  起始约 {t:.2f}s  (首帧差 {d:.2f})")
