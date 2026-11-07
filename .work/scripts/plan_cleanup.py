import os,re,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
os.chdir(r"D:\code\unitree-site")
h=open("index.html",encoding="utf-8").read()
c=open("assets/css/site.css",encoding="utf-8").read()
keep=set()
for m in re.finditer(r'(?:src|poster|href|content)="(assets/[^"]+)"',h): keep.add(m.group(1))
for m in re.finditer(r'srcset="([^"]+)"',h):
    for part in m.group(1).split(","):
        u=part.strip().split(" ")[0]
        if u.startswith("assets/"): keep.add(u)
for m in re.finditer(r'url\("\.\./([^"]+)"\)',c): keep.add("assets/"+m.group(1))
keep={k.replace("\\","/") for k in keep}
keep.add("assets/css/site.css"); keep.add("assets/js/site.js")

allf=set()
for root,dirs,fs in os.walk("assets"):
    for f in fs: allf.add(os.path.join(root,f).replace("\\","/"))
drop=sorted(allf-keep)
total=sum(os.path.getsize(f) for f in drop)
print(f"保留 {len(keep)} 个；将删除 {len(drop)} 个，合计 {total/1024/1024:.2f} MB")
for f in drop[:15]: print("  -",f)
print("  ...")
with open(".work/drop-list.txt","w",encoding="utf-8") as fh:
    fh.write("\n".join(drop))
