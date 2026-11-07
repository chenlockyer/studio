import re, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def build_boot():
    h = open("index-v3.html", encoding="utf-8").read()
    h = h.replace("assets/img/v3/", "assets/img/v3boot/")
    h = h.replace("assets/video/v3/", "assets/video/v3boot/")
    for ext in ("avif", "webp"):
        h = re.sub(r',?\s*assets/img/v3boot/still/lab-bench-1440\.%s 1440w' % ext, '', h)
    open("index-boot.html", "w", encoding="utf-8").write(h)

    refs = set()
    for m in re.finditer(r'(?:src|poster|href|srcset)="([^"]+)"', h):
        for part in m.group(1).split(","):
            u = part.strip().split(" ")[0]
            if u.startswith("assets/"):
                refs.add(u)
    missing = sorted(r for r in refs if not os.path.isfile(r.replace("/", os.sep)))
    print(f"引用 {len(refs)}，缺失 {len(missing)}")
    for r in missing: print("  MISSING", r)

build_boot()
