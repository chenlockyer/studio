# 按程序打分选出的时间点重编码 hero 槽位：1:1，机器人居中，够大。
import os, subprocess, io, sys, json
from PIL import Image, ImageOps
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = r"D:\code\unitree-site"
MEDIA = r"D:\my_media\video\unitree_g1"
VOUT = os.path.join(ROOT,"assets","video","v3boot")
POUT = os.path.join(ROOT,"assets","img","v3boot","poster")
os.makedirs(VOUT, exist_ok=True); os.makedirs(POUT, exist_ok=True)

def enc(src, t0, dur, out, size=640, crf=31, budget=300):
    outp = os.path.join(VOUT, out)
    # 1:1 居中裁切
    vf = f"scale={size}:{size}:force_original_aspect_ratio=increase,crop={size}:{size}"
    for c in (crf, crf+4, crf+8, crf+12):
        r = subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{t0:.3f}","-t",f"{dur:.3f}",
            "-i",src,"-vf",vf,"-r","30","-c:v","libx264","-profile:v","high",
            "-pix_fmt","yuv420p","-crf",str(c),"-preset","slow","-an",
            "-movflags","+faststart",outp], capture_output=True, text=True)
        if r.returncode!=0:
            print("  FAIL", out, r.stderr[-300:]); return None
        if os.path.getsize(outp) <= budget*1024: break
    return outp

# (key, 源, 起始秒, 时长)  —— 时间点来自 slotpick.py 的前景占比+居中打分
JOBS = [
 ("slot-1", os.path.join(ROOT,"assets","video","tour-walk.mp4"), 0.05, 2.8),
 ("slot-2", os.path.join(MEDIA,"导览","导览投入使用.mp4"),       7.6,  3.0),
 ("slot-3", os.path.join(MEDIA,"群控","群控.mp4"),             20.4,  3.0),
 ("slot-4", os.path.join(MEDIA,"江南.mp4"),                   25.6,  3.0),
]
for key, src, t0, dur in JOBS:
    if not os.path.isfile(src):
        print("MISSING", src); continue
    p = enc(src, t0, dur, key+".mp4")
    if not p: continue
    # poster = 视频第 0 帧，尺寸自动 = 视频尺寸
    tmp = os.path.join(POUT,"_t.png")
    subprocess.run(["ffmpeg","-y","-v","error","-i",p,"-frames:v","1","-vf","scale=iw*2:-2:flags=lanczos",tmp],
                   capture_output=True)
    im = Image.open(tmp).convert("RGB")
    jp = os.path.join(POUT, key+".jpg")
    im.save(jp,"JPEG",quality=84,optimize=True,progressive=True)
    os.remove(tmp)
    print(f"  {key}.mp4  {os.path.getsize(p)/1024:6.1f} KB   poster {im.width}x{im.height} {os.path.getsize(jp)/1024:5.1f} KB")
print("\nslot 重编码完成")
