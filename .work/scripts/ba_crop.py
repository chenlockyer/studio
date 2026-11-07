import io,sys
from PIL import Image
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
# 找「交付实绩」所在行：在两张截图里扫描浅色区域，定位标题块
def crop(src, out, box):
    im=Image.open(src); c=im.crop(box); c=c.resize((c.width*3,c.height*3), Image.LANCZOS); c.save(out); return c.size
print(crop(".taste-skill/v4k/desktop-page-03.jpg", ".work/shots/beforeafter/before.png", (30,180,340,235)))
print(crop(".taste-skill/r2b/desktop-page-03.jpg", ".work/shots/beforeafter/after.png",  (30,180,340,235)))
