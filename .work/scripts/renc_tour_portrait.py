import io,sys,subprocess,os
from PIL import Image
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
SRC = r"D:\my_media\video\unitree_g1\导览\导览投入使用.mp4"
OUT = r"assets\video\tour-live.mp4"
POST = r"assets\img\poster\tour-live.jpg"
T0, DUR = 28.0, 5.0

def enc(crf, budget_kb=700):
    # 源带 -90 旋转，ffmpeg 解码时自动转正为 1080x1920；按 9:16 等比缩放，绝不改变比例
    vf = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1"
    for c in (crf, crf+4, crf+8):
        r = subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{T0}","-t",f"{DUR}","-i",SRC,
            "-vf",vf,"-r","30","-c:v","libx264","-profile:v","high","-pix_fmt","yuv420p",
            "-crf",str(c),"-preset","slow","-an","-movflags","+faststart",OUT],
            capture_output=True, text=True)
        if r.returncode != 0:
            print("FAIL", r.stderr[-400:]); return None
        if os.path.getsize(OUT) <= budget_kb*1024: break
    return OUT

p = enc(27)
print(f"编码完成 {os.path.getsize(p)/1024:.1f} KB")

# 校验：容器元数据与解码尺寸必须一致，且 SAR 必须是 1:1
probe = subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
    "-show_entries","stream=width,height,sample_aspect_ratio,display_aspect_ratio",
    "-of","default=nw=1",OUT], capture_output=True, text=True).stdout
print("  " + probe.replace("\n","\n  ").strip())

# 海报 = 视频第 0 帧，尺寸自动与视频一致
tmp = ".work/probe/_t.png"
subprocess.run(["ffmpeg","-y","-v","error","-i",OUT,"-frames:v","1",tmp], capture_output=True)
im = Image.open(tmp).convert("RGB")
im.save(POST,"JPEG",quality=86,optimize=True,progressive=True)
os.remove(tmp)
print(f"  poster {im.size[0]}x{im.size[1]} AR={im.size[0]/im.size[1]:.4f}  {os.path.getsize(POST)/1024:.1f} KB")

