import io,sys
from PIL import Image, ImageDraw
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
old = Image.open(".work/probe/squashed.jpg").convert("RGB")          # 1280x720 压扁
new = Image.open("assets/img/poster/tour-live.jpg").convert("RGB")   # 720x1280 正确
# 同一高度并排
H = 760
ow = int(old.width * H/old.height); nw = int(new.width * H/new.height)
old = old.resize((ow,H), Image.LANCZOS); new = new.resize((nw,H), Image.LANCZOS)
pad, top = 24, 54
W = ow + nw + pad*3
out = Image.new("RGB",(W, H+top+pad),(10,12,14))
out.paste(old,(pad,top)); out.paste(new,(pad*2+ow,top))
d=ImageDraw.Draw(out)
d.text((pad,20),"修复前：竖拍画面被压进 1280x720（横向拉宽、纵向压扁）",fill=(230,110,110))
d.text((pad*2+ow,20),"修复后：按 9:16 原始方向重编 720x1280",fill=(110,200,230))
out.save(".work/final/5-before-after.jpg",quality=90)
print(out.size)
