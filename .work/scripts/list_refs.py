import re,os,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
h=open("index-v4.html",encoding="utf-8").read()
c=open("assets/css/site-v4.css",encoding="utf-8").read()
refs=set()
for m in re.finditer(r'(?:src|poster|href|content)="(assets/[^"]+)"',h): refs.add(m.group(1))
for m in re.finditer(r'srcset="([^"]+)"',h):
    for part in m.group(1).split(","):
        u=part.strip().split(" ")[0]
        if u.startswith("assets/"): refs.add(u)
for m in re.finditer(r'url\("\.\./([^"]+)"\)',c): refs.add(m.group(1))
print(f"引用 {len(refs)} 个文件")
for r in sorted(refs): print("  ",r, os.path.getsize(r)//1024, "KB")
