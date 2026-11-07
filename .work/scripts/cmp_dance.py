import io,sys
from PIL import Image
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
for p in [".work/probe/dance-first.jpg",".work/probe/jiangnan-6s.jpg"]:
    im=Image.open(p); print(f"{p:36s} {im.size[0]}x{im.size[1]}  AR={im.size[0]/im.size[1]:.4f}")
# 并排放，等高
a=Image.open(".work/probe/dance-first.jpg").convert("RGB").resize((360,640))
b=Image.open(".work/probe/jiangnan-6s.jpg").convert("RGB").resize((360,640))
out=Image.new("RGB",(740,640),(20,22,24))
out.paste(b,(0,0)); out.paste(a,(380,0))
out.save(".work/probe/dance-compare.jpg", quality=88)
print("对比图: 左=江南.mp4 6.0s  右=dance-live.mp4 首帧")
