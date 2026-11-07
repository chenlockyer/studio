import os, subprocess, io, sys
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT=r"D:\code\unitree-site"; MEDIA=r"D:\my_media\video\unitree_g1"
VOUT=os.path.join(ROOT,"assets","video","v3boot"); POUT=os.path.join(ROOT,"assets","img","v3boot","poster")

def enc(src,t0,dur,out,size=640,crf=31,budget=300,zoom=1.0):
    """zoom>1 时先放大再居中裁切，让主体更大。所有中间尺寸强制偶数。"""
    outp=os.path.join(VOUT,out)
    zw=int(round(size*zoom/2))*2          # 偶数
    vf=(f"scale={zw}:{zw}:force_original_aspect_ratio=increase,"
        f"crop={size}:{size}")
    for c in (crf,crf+4,crf+8,crf+12,crf+16):
        r=subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{t0:.3f}","-t",f"{dur:.3f}",
            "-i",src,"-vf",vf,"-r","30","-c:v","libx264","-profile:v","high",
            "-pix_fmt","yuv420p","-crf",str(c),"-preset","slow","-an",
            "-movflags","+faststart",outp],capture_output=True,text=True)
        if r.returncode!=0: print("  FAIL",out,"crf",c,r.stderr[-260:]); return None
        if os.path.getsize(outp)<=budget*1024: break
    return outp

for key,src,t0,dur,zoom in [
 ("slot-4", os.path.join(MEDIA,"江南.mp4"), 25.6, 3.0, 1.3),
]:
    p=enc(src,t0,dur,key+".mp4",zoom=zoom)
    if not p: continue
    tmp=os.path.join(POUT,"_t.png")
    subprocess.run(["ffmpeg","-y","-v","error","-i",p,"-frames:v","1","-vf","scale=iw*2:-2:flags=lanczos",tmp],capture_output=True)
    im=Image.open(tmp).convert("RGB"); jp=os.path.join(POUT,key+".jpg")
    im.save(jp,"JPEG",quality=84,optimize=True,progressive=True); os.remove(tmp)
    print(f"  {key}.mp4 {os.path.getsize(p)/1024:6.1f} KB  poster {im.width}x{im.height}")
print("\n=== 全部 slot 校验 ===")
for k in ("slot-1","slot-2","slot-3","slot-4"):
    v=os.path.join(VOUT,k+".mp4")
    if os.path.isfile(v):
        r=subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
            "-show_entries","stream=width,height,nb_frames","-show_entries","format=duration",
            "-of","csv=p=0",v],capture_output=True,text=True)
        print(f"  {k}: {r.stdout.strip()}  {os.path.getsize(v)/1024:.1f} KB")
