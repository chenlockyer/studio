import io,sys
from PIL import Image, ImageChops
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
def crop(src, box, scale=7):
    im=Image.open(src); c=im.crop(box)
    return c.resize((c.width*scale,c.height*scale), Image.LANCZOS)
box=(105,185,250,232)   # “实绩”两字
b=crop(".taste-skill/v4k/desktop-page-03.jpg", box)
a=crop(".taste-skill/r2b/desktop-page-03.jpg", box)
W,H=b.size
out=Image.new("RGB",(W, H*2+14), (236,238,240))
out.paste(b,(0,0)); out.paste(a,(0,H+14))
out.save(".work/shots/beforeafter/ji.png")
print(out.size)
