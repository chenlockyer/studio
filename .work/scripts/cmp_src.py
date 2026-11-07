import io,sys
from PIL import Image
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
for p in [".work/probe/src-28.jpg","assets/img/poster/tour-live.jpg"]:
    im=Image.open(p); print(f"  {p:34s} {im.size[0]}x{im.size[1]}  AR={im.size[0]/im.size[1]:.4f}")
