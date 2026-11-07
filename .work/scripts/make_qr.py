import io,sys,os
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
import numpy as np
from PIL import Image
src=r"C:\Users\11051\Pictures\个人信息\微信二维码.png"
im=Image.open(src).convert("L")
a=np.asarray(im)
dark = a < 100
# 只看中部区域，避开顶部头像与底部文字
h,w=a.shape
band = dark[int(h*0.28):int(h*0.80), :]
ys,xs = np.nonzero(band)
y0,y1 = ys.min()+int(h*0.28), ys.max()+int(h*0.28)
x0,x1 = xs.min(), xs.max()
print(f"二维码区域 x {x0}-{x1}  y {y0}-{y1}  ({x1-x0+1}x{y1-y0+1})")

pad = int((x1-x0)*0.08)          # 留出静区，保证可扫
box = (max(0,x0-pad), max(0,y0-pad), min(w,x1+pad), min(h,y1+pad))
print("裁切框", box)
im2 = Image.open(src).convert("RGB").crop(box)
# 统一成正方形并放大到 720（二维码需要像素级锐利）
side = max(im2.size)
canvas = Image.new("RGB",(side,side),(255,255,255))
canvas.paste(im2, ((side-im2.width)//2, (side-im2.height)//2))
out = canvas.resize((720,720), Image.NEAREST)
os.makedirs("assets/img", exist_ok=True)
p="assets/img/wechat-qr.png"
out.save(p,"PNG",optimize=True)
print(f"输出 {p}  720x720  {os.path.getsize(p)/1024:.1f} KB")
