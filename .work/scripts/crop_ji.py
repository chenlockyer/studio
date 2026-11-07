import io,sys
from PIL import Image
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
im=Image.open(".taste-skill/r2b/desktop-page-03.jpg")
c=im.crop((40,170,420,235))
c=c.resize((c.width*3,c.height*3), Image.LANCZOS)
c.save(".work/shots/r2/ji-zoom.png")
print(c.size)
