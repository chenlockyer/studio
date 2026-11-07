import os, subprocess, io, sys
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\code\unitree-site"
SRC  = r"D:\my_media\video\unitree_g1\江南.mp4"
OUT  = os.path.join(ROOT,"assets","video","v3","dance-live.mp4")
POS  = os.path.join(ROOT,"assets","img","v3","poster","dance-live.jpg")

# 6.0s 起是整段里动作幅度最大的 5 秒（踢腿、挥臂），竖拍 720x1280，无烧录字幕
for crf in (28,31,34,37):
    r = subprocess.run(["ffmpeg","-y","-v","error","-ss","6.000","-t","5.000","-i",SRC,
        "-vf","scale=720:1280:flags=lanczos","-r","30","-c:v","libx264","-profile:v","high",
        "-pix_fmt","yuv420p","-crf",str(crf),"-preset","slow","-an","-movflags","+faststart",OUT],
        capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL", r.stderr[-400:]); sys.exit(1)
    if os.path.getsize(OUT) <= 560*1024: break
print(f"dance-live.mp4  {os.path.getsize(OUT)/1024:.1f} KB")

tmp = os.path.join(ROOT,".work","probe","_t.png")
subprocess.run(["ffmpeg","-y","-v","error","-i",OUT,"-frames:v","1","-vf","scale=810:-2:flags=lanczos",tmp],capture_output=True)
im = Image.open(tmp).convert("RGB"); im.save(POS,"JPEG",quality=82,optimize=True,progressive=True)
os.remove(tmp)
print(f"poster  {im.width}x{im.height}  {os.path.getsize(POS)/1024:.1f} KB")
