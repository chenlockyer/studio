import io,sys,glob
from PIL import Image
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
for p in sorted(glob.glob("assets/img/poster/*.jpg")):
    im=Image.open(p); print(f"  {p:28s} {im.size[0]}x{im.size[1]}  AR={im.size[0]/im.size[1]:.4f}")
