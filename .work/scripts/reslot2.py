import os, subprocess, io, sys
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT=r"D:\code\unitree-site"; MEDIA=r"D:\my_media\video\unitree_g1"
VOUT=os.path.join(ROOT,"assets","video","v3boot"); POUT=os.path.join(ROOT,"assets","img","v3boot","poster")

def enc(src,t0,dur,out,size=640,crf=31,budget=300,crop_zoom=None):
    outp=os.path.join(VOUT,out)
    if crop_zoom:
        # 先按比例缩放，再按 zoom 系数居中放大裁切（让主体更大）
        z=crop_zoom
        vf=(f"scale=-2:{int(size*z)}:force_original_aspect_ratio=increase,"
            f"crop={size}:{size}")
    else:
        vf=f"scale={size}:{size}:force_original_aspect_ratio=increase,crop={size}:{size}"
    for c in (crf,crf+4,crf+8,crf+12,crf+16):
        r=subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{t0:.3f}","-t",f"{dur:.3f}",
            "-i",src,"-vf",vf,"-r","30","-c:v","libx264","-profile:v","high",
            "-pix_fmt","yuv420p","-crf",str(c),"-preset","slow","-an",
            "-movflags","+faststart",outp],capture_output=True,text=True)
        if r.returncode!=0: print("  FAIL",out,r.stderr[-300:]); return None
        if os.path.getsize(outp)<=budget*1024: break
    return outp

# slot-1 换成"G1 正面 LED 特写"（原 slot-2 那段最清楚），其余顺延调整构图
JOBS=[
 ("slot-1", os.path.join(MEDIA,"导览","导览投入使用.mp4"), 7.8, 3.0, None),   # 正面 LED，走廊
 ("slot-2", os.path.join(ROOT,"assets","video","tour-walk.mp4"), 0.3, 2.8, None), # 行走
 ("slot-3", os.path.join(MEDIA,"群控","群控.mp4"), 20.4, 3.0, 1.35),          # 多机，放大 1.35x
 ("slot-4", os.path.join(MEDIA,"江南.mp4"), 25.6, 3.0, 1.3),                  # 舞蹈，放大 1.3x
]
for key,src,t0,dur,zoom in JOBS:
    if not os.path.isfile(src): print("MISSING",src); continue
    p=enc(src,t0,dur,key+".mp4",crop_zoom=zoom)
    if not p: continue
    tmp=os.path.join(POUT,"_t.png")
    subprocess.run(["ffmpeg","-y","-v","error","-i",p,"-frames:v","1","-vf","scale=iw*2:-2:flags=lanczos",tmp],capture_output=True)
    im=Image.open(tmp).convert("RGB"); jp=os.path.join(POUT,key+".jpg")
    im.save(jp,"JPEG",quality=84,optimize=True,progressive=True); os.remove(tmp)
    print(f"  {key}.mp4 {os.path.getsize(p)/1024:6.1f} KB  poster {im.width}x{im.height}")
