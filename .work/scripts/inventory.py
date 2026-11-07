import os, json, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
base = r"D:\code\unitree-site\assets\img"
rows = []
for name in sorted(os.listdir(base)):
    p = os.path.join(base, name)
    if not os.path.isfile(p): continue
    ext = os.path.splitext(name)[1].lower()
    if ext not in ('.jpg','.jpeg','.png','.webp'): continue
    with Image.open(p) as im:
        rows.append({
            "name": name, "ext": ext, "bytes": os.path.getsize(p),
            "w": im.width, "h": im.height, "mode": im.mode,
            "has_alpha": (im.mode in ('RGBA','LA','PA') or (im.mode=='P' and 'transparency' in im.info)),
        })
print(json.dumps(rows, ensure_ascii=False, indent=1))
json.dump(rows, open(r"D:\code\unitree-site\.work\inventory.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
