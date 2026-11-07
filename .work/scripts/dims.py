import io,sys,glob
from PIL import Image
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
for p in sorted(glob.glob("assets/img/poster/*.jpg"))+["assets/img/og.jpg"]:
    im=Image.open(p)
    w,h=im.size
    print(f"  {p.split('/')[-1]:24s} {w}x{h}  {w/h:.2f}")
