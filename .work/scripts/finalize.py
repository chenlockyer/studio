import re,os,shutil,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
os.chdir(r"D:\code\unitree-site")

raw_h = open("index-v4.html", encoding="utf-8").read()
raw_c = open("assets/css/site-v4.css", encoding="utf-8").read()

MAP = [
  ("assets/img/v3/still/hero-poster.jpg", "assets/img/og.jpg"),
  ("assets/img/v3/ui/",                    "assets/img/ui/"),
  ("assets/img/v3/poster/",                "assets/img/poster/"),
  ("assets/video/v3/",                     "assets/video/"),
  ("assets/fonts/v3/",                     "assets/fonts/"),
]
def newpath(p):
    for a,b in MAP:
        if p.startswith(a): return b + p[len(a):]
    return p

# 原始引用（含 OG 图与字体）
old = set()
for m in re.finditer(r'(?:src|poster|href|content)="(assets/[^"]+)"', raw_h): old.add(m.group(1))
for m in re.finditer(r'srcset="([^"]+)"', raw_h):
    for part in m.group(1).split(","):
        u=part.strip().split(" ")[0]
        if u.startswith("assets/"): old.add(u)
for m in re.finditer(r'url\("\.\./([^"]+)"\)', raw_c): old.add("assets/"+m.group(1))
old.add("assets/css/site-v4.css"); old.add("assets/js/site-v4.js")

moved=[]; missing=[]
for op in sorted(old):
    np = "assets/css/site.css" if op=="assets/css/site-v4.css" else ("assets/js/site.js" if op=="assets/js/site-v4.js" else newpath(op))
    if not os.path.isfile(op): missing.append(op); continue
    os.makedirs(os.path.dirname(np), exist_ok=True)
    shutil.copy2(op,np); moved.append((op,np))
print(f"搬运 {len(moved)} / 缺失 {len(missing)}")
for m in missing: print("  缺:",m)

# 改写并写出
h = raw_h
for a,b in MAP: h = h.replace(a,b)
h = h.replace("assets/css/site-v4.css","assets/css/site.css").replace("assets/js/site-v4.js","assets/js/site.js")
c = raw_c.replace("../fonts/v3/","../fonts/")
open("index.html","w",encoding="utf-8").write(h)
open("assets/css/site.css","w",encoding="utf-8").write(c)

# 二次校验
r2=set()
for m in re.finditer(r'(?:src|poster|href|content)="(assets/[^"]+)"',h): r2.add(m.group(1))
for m in re.finditer(r'srcset="([^"]+)"',h):
    for part in m.group(1).split(","):
        u=part.strip().split(" ")[0]
        if u.startswith("assets/"): r2.add(u)
for m in re.finditer(r'url\("\.\./([^"]+)"\)',c): r2.add("assets/"+m.group(1))
r2.add("assets/css/site.css"); r2.add("assets/js/site.js")
bad=[r for r in sorted(r2) if not os.path.isfile(r)]
print(f"\nindex.html: {len(r2)} 引用，缺失 {len(bad)}")
for b in bad: print("  缺:",b)
print("GO2:", h.count("GO2"))
