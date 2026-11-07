import os,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
os.chdir(r"D:\code\unitree-site")
import re
raw_h=open("index-v4.html",encoding="utf-8").read()
raw_c=open("assets/css/site-v4.css",encoding="utf-8").read()
MAP=[("assets/img/v3/still/hero-poster.jpg","assets/img/og.jpg"),("assets/img/v3/ui/","assets/img/ui/"),
     ("assets/img/v3/poster/","assets/img/poster/"),("assets/video/v3/","assets/video/"),("assets/fonts/v3/","assets/fonts/")]
def newpath(p):
    for a,b in MAP:
        if p.startswith(a): return b+p[len(a):]
    return p
old=set()
for m in re.finditer(r'(?:src|poster|href|content)="(assets/[^"]+)"',raw_h): old.add(m.group(1))
for m in re.finditer(r'srcset="([^"]+)"',raw_h):
    for part in m.group(1).split(","):
        u=part.strip().split(" ")[0]
        if u.startswith("assets/"): old.add(u)
for m in re.finditer(r'url\("\.\./([^"]+)"\)',raw_c): old.add("assets/"+m.group(1))
old.add("assets/css/site-v4.css"); old.add("assets/js/site-v4.js")
for op in sorted(old):
    np = "assets/css/site.css" if op=="assets/css/site-v4.css" else ("assets/js/site.js" if op=="assets/js/site-v4.js" else newpath(op))
    if not os.path.isfile(op): print("缺源",op); continue
    if os.path.abspath(np)==os.path.abspath(op): continue
    try:
        os.makedirs(os.path.dirname(np),exist_ok=True)
        with open(op,"rb") as f: data=f.read()
        with open(np,"wb") as f: f.write(data)
    except PermissionError as e:
        print("锁住:",op,"->",np,e)
