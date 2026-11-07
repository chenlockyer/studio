import io,sys,os
from PIL import Image, ImageDraw, ImageFont
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")

def zh(size):
    for p in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\simhei.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

old = Image.open(".work/probe/squashed.jpg").convert("RGB")
new = Image.open("assets/img/poster/tour-live.jpg").convert("RGB")
H = 760
ow = int(old.width*H/old.height); nw = int(new.width*H/new.height)
old = old.resize((ow,H), Image.LANCZOS); new = new.resize((nw,H), Image.LANCZOS)
pad, top = 26, 66
W = ow+nw+pad*3
out = Image.new("RGB",(W, H+top+pad),(10,12,14))
out.paste(old,(pad,top)); out.paste(new,(pad*2+ow,top))
d = ImageDraw.Draw(out)
f = zh(26)
d.text((pad,22), "修复前：竖拍画面被压进 1280×720 —— 横向拉宽、纵向压扁", font=f, fill=(240,120,120))
d.text((pad*2+ow,22), "修复后：按 9:16 原始方向重编", font=f, fill=(120,205,235))
out.save(".work/final/5-before-after.jpg", quality=92)
print(out.size)
