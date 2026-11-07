# 补齐 v4 需要的静帧与界面图（队友还没产出这部分）
import os, io, sys, subprocess
from PIL import Image, ImageOps
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT=r"D:\code\unitree-site"; MEDIA=r"D:\my_media\video\unitree_g1"
STILL=os.path.join(ROOT,"assets","img","v3","still")
POST=os.path.join(ROOT,"assets","img","v3","poster")
UI=os.path.join(ROOT,"assets","img","v3","ui")
for d in (STILL,POST,UI): os.makedirs(d, exist_ok=True)

AVIF_Q,AVIF_SPEED=52,4; WEBP_Q,WEBP_METHOD=78,6; JPEG_Q=82
FLAT=(10,12,14)

def load(p):
    im=Image.open(p); im=ImageOps.exif_transpose(im)
    if im.mode in ("RGBA","LA","PA") or "transparency" in im.info:
        im=im.convert("RGBA"); bg=Image.new("RGB",im.size,FLAT)
        bg.paste(im,mask=im.split()[-1]); im=bg
    else: im=im.convert("RGB")
    im.info={}; return im

def rz(im,w):
    if w>=im.width: return im.copy()
    return im.resize((w,max(1,round(im.height*w/im.width))),Image.LANCZOS)

def ladder(im,slug,outdir,widths=(480,960,1440),budget=220):
    lad=[w for w in widths if w<=im.width] or [im.width]
    for w in lad:
        r=rz(im,w)
        ap=os.path.join(outdir,f"{slug}-{w}.avif"); q=AVIF_Q
        r.save(ap,"AVIF",quality=q,speed=AVIF_SPEED)
        while os.path.getsize(ap)>budget*1024 and q>26:
            q-=8; r.save(ap,"AVIF",quality=q,speed=AVIF_SPEED)
        r.save(os.path.join(outdir,f"{slug}-{w}.webp"),"WEBP",quality=WEBP_Q,method=WEBP_METHOD)
    jw=min(960,im.width); jr=rz(im,jw)
    jr.save(os.path.join(outdir,f"{slug}-960.jpg"),"JPEG",quality=JPEG_Q,optimize=True,progressive=True)
    return lad

def grab(src,t,scale="scale=1920:-2"):
    tmp=os.path.join(STILL,"_t.png")
    r=subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{t:.2f}","-i",src,
        "-frames:v","1","-vf",scale,tmp],capture_output=True,text=True)
    if r.returncode!=0: print("  grab FAIL",os.path.basename(src),r.stderr[-200:]); return None
    im=load(tmp); os.remove(tmp); return im

print("=== 静帧 ===")
ST=[
 ("hero-poster", os.path.join(MEDIA,"群控","群控.mp4"), 22.5),
 ("lab-bench",   os.path.join(ROOT,"assets","img","bg-course.jpg"), None),
]
for slug,src,t in ST:
    if t is None:
        im=load(src)
    else:
        im=grab(src,t)
    if im is None: continue
    lad=ladder(im,slug,STILL)
    print(f"  {slug:14s} {im.width}x{im.height} 档位{lad}")

# hero poster 同时出一张直接给 <video poster> 用的
hp=os.path.join(STILL,"hero-poster-1440.jpg")
if os.path.isfile(hp):
    pass
im=grab(os.path.join(MEDIA,"群控","群控.mp4"),22.5)
if im:
    im.resize((1920,round(1920*im.height/im.width)),Image.LANCZOS).save(
        os.path.join(STILL,"hero-poster.jpg"),"JPEG",quality=84,optimize=True,progressive=True)
    print(f"  hero-poster.jpg  {im.width}x{im.height}")

print("\n=== 视频 poster（取自 v3 视频第 0 帧，尺寸与视频一致）===")
V3=os.path.join(ROOT,"assets","video","v3")
for name in ("group-sync","slam-build","choreo-chain","slot-1","slot-2","slot-3","slot-4"):
    v=os.path.join(V3,name+".mp4")
    if not os.path.isfile(v): print("  缺视频",name); continue
    tmp=os.path.join(POST,"_t.png")
    subprocess.run(["ffmpeg","-y","-v","error","-i",v,"-frames:v","1",
        "-vf","scale=iw*2:-2:flags=lanczos",tmp],capture_output=True)
    if not os.path.isfile(tmp): print("  FAIL",name); continue
    im=Image.open(tmp).convert("RGB")
    jp=os.path.join(POST,name+".jpg")
    im.save(jp,"JPEG",quality=84,optimize=True,progressive=True)
    os.remove(tmp)
    print(f"  {name+'.jpg':20s} {im.width}x{im.height}  {os.path.getsize(jp)/1024:6.1f} KB")

print("\n=== 界面图 ===")
UISRC={"navi-home":"导览主页面.png","navi-prep":"导览-准备页面.png",
       "gc-dance":"群控-官方舞蹈页面.png","gc-board":"群控-主页面.png",
       "gc-phone":"群控手机端.jpg","gc-keys":"群控-自定义按键.png",
       "gc-queue":"支持自定义舞蹈队列一键下发.png"}
SRCIMG=os.path.join(ROOT,"assets","img")
for slug,fn in UISRC.items():
    p=os.path.join(SRCIMG,fn)
    if not os.path.isfile(p): print("  缺源",fn); continue
    im=load(p)
    lad=ladder(im,slug,UI,widths=(480,960,im.width),budget=280)
    print(f"  {slug:12s} {im.width}x{im.height} 档位{lad}")
print("\ndone")
