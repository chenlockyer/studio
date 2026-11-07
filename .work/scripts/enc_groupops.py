import subprocess, os, io, sys
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
os.chdir(r"D:\code\unitree-site")
SRC = r"D:\my_media\video\unitree_g1\群控\群控.mp4"
OUT = r"assets\video\group-ops.mp4"
vf = "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30"
for crf in (27,30,33,36):
    r=subprocess.run(["ffmpeg","-y","-v","error","-ss","44.0","-t","8.0","-i",SRC,
        "-vf",vf,"-c:v","libx264","-profile:v","high","-pix_fmt","yuv420p",
        "-crf",str(crf),"-preset","slow","-an","-movflags","+faststart",OUT],
        capture_output=True,text=True)
    if r.returncode!=0: print("FAIL", r.stderr[-400:]); break
    kb=os.path.getsize(OUT)/1024
    print(f"crf {crf} -> {kb:.0f} KB")
    if kb<=760: break

tmp=".work/probe/_poster.png"
subprocess.run(["ffmpeg","-y","-v","error","-i",OUT,"-frames:v","1","-vf","scale=iw*2:-2:flags=lanczos",tmp],capture_output=True)
im=Image.open(tmp).convert("RGB"); os.remove(tmp)
p=r"assets\img\poster\group-ops.jpg"
im.save(p,"JPEG",quality=84,optimize=True,progressive=True)
print(f"poster {im.width}x{im.height}  {os.path.getsize(p)/1024:.0f} KB")
