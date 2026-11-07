import subprocess, os, io, sys, tempfile
import numpy as np
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
MEDIA = r"D:\my_media\video\unitree_g1"
SRC = os.path.join(MEDIA,"群控","群控.mp4")

def grab(src,t,w=128):
    tmp=tempfile.mktemp(suffix=".png")
    subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{t:.2f}","-i",src,"-frames:v","1","-vf",f"scale={w}:{w//16*9}",tmp],capture_output=True)
    if not os.path.isfile(tmp): return None
    a=np.asarray(Image.open(tmp).convert("L"),dtype=np.float32); os.remove(tmp); return a

def norm(a):
    a=a-a.mean(); s=a.std(); return a/(s if s>1e-6 else 1)

p=norm(grab("assets/video/group-sync.mp4",0))
rows=[]
t=15.0
while t<=45.0:
    f=grab(SRC,t)
    if f is not None and f.shape==p.shape:
        rows.append((float((norm(f)*p).mean()), t))
    t+=0.5
rows.sort(reverse=True)
print("最相似的 6 个时间点（相关系数, 秒）:")
for c,t in rows[:6]: print(f"  {c:.4f}  {t:6.2f}s")
