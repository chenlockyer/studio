import io,sys,os,subprocess
from PIL import Image
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")

SRC = r"D:\my_media\video\unitree_g1\群控\群控.mp4"
V = "assets/video"; P = "assets/img/poster"

def enc(out, t0, dur, crf=30, budget_kb=None):
    for c in (crf, crf+3, crf+6, crf+9):
        r = subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{t0}","-t",f"{dur}","-i",SRC,
            "-vf","scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1",
            "-r","30","-c:v","libx264","-profile:v","high","-pix_fmt","yuv420p",
            "-crf",str(c),"-preset","slow","-an","-movflags","+faststart",out],
            capture_output=True, text=True)
        if r.returncode != 0:
            print("  FAIL", r.stderr[-300:]); return None
        kb = os.path.getsize(out)/1024
        if budget_kb is None or kb <= budget_kb:
            break
    return kb

def poster(vid, out):
    tmp = ".work/probe/_p.png"
    subprocess.run(["ffmpeg","-y","-v","error","-i",vid,"-frames:v","1",
                    "-vf","scale=iw*2:-2:flags=lanczos",tmp], capture_output=True)
    im = Image.open(tmp).convert("RGB")
    im.save(out,"JPEG",quality=84,optimize=True,progressive=True)
    os.remove(tmp)
    return im.size, os.path.getsize(out)/1024

# 首屏：4.0–13.0 秒（明亮的展厅全景，前景笔记本）
kb = enc(f"{V}/group-sync.mp4", 4.0, 9.0, crf=30, budget_kb=760)
sz, pkb = poster(f"{V}/group-sync.mp4", f"{P}/group-sync.jpg")
print(f"首屏 group-sync   4.0–13.0s  {kb:.1f} KB   poster {sz[0]}x{sz[1]} {pkb:.1f} KB")

# 群控区块：16.5–24.5 秒（多机排开，与首屏机位不同）
kb = enc(f"{V}/group-ops.mp4", 16.5, 8.0, crf=30, budget_kb=660)
sz, pkb = poster(f"{V}/group-ops.mp4", f"{P}/group-ops.jpg")
print(f"群控 group-ops   16.5–24.5s  {kb:.1f} KB   poster {sz[0]}x{sz[1]} {pkb:.1f} KB")
