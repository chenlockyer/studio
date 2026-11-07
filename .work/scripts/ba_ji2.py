import io,sys
from PIL import Image, ImageDraw
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
box=(120,178,235,242); S=7
def crop(src):
    im=Image.open(src); c=im.crop(box)
    return c.resize((c.width*S,c.height*S), Image.LANCZOS)
b=crop(".taste-skill/v4k/desktop-page-03.jpg")
a=crop(".taste-skill/r2b/desktop-page-03.jpg")
W,H=b.size
pad=16
out=Image.new("RGB",(W, H*2+pad), (250,250,251))
out.paste(b,(0,0)); out.paste(a,(0,H+pad))
d=ImageDraw.Draw(out)
d.text((10,8),"before",fill=(190,60,60))
d.text((10,H+pad+8),"after",fill=(30,120,190))
out.save(".work/shots/beforeafter/ji2.png")
print(out.size)
