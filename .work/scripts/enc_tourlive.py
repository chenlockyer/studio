import os, subprocess, io, sys
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\code\unitree-site"
SRC  = r"D:\my_media\video\unitree_g1\导览\导览投入使用.mp4"
OUT  = os.path.join(ROOT,"assets","video","v3","tour-live.mp4")
POS  = os.path.join(ROOT,"assets","img","v3","poster","tour-live.jpg")

# 源里 28.0s 起是正面全身、LED 面罩亮着的干净镜头（无烧录字幕、无遮挡）
for crf in (27,30,33,36):
    r = subprocess.run(["ffmpeg","-y","-v","error","-ss","28.000","-t","6.000","-i",SRC,
        "-vf","scale=1280:720:flags=lanczos","-r","30","-c:v","libx264","-profile:v","high",
        "-pix_fmt","yuv420p","-crf",str(crf),"-preset","slow","-an","-movflags","+faststart",OUT],
        capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL", r.stderr[-400:]); sys.exit(1)
    if os.path.getsize(OUT) <= 640*1024: break
print(f"tour-live.mp4  {os.path.getsize(OUT)/1024:.1f} KB")

tmp = os.path.join(ROOT,".work","probe","_t.png")
subprocess.run(["ffmpeg","-y","-v","error","-i",OUT,"-frames:v","1","-vf","scale=1440:-2:flags=lanczos",tmp],capture_output=True)
im = Image.open(tmp).convert("RGB"); im.save(POS,"JPEG",quality=82,optimize=True,progressive=True)
os.remove(tmp)
print(f"poster  {im.width}x{im.height}  {os.path.getsize(POS)/1024:.1f} KB")
