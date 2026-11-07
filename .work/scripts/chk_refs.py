import io,sys,re,os
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
h=open("index.html",encoding="utf-8").read()
refs=set()
for m in re.findall(r'(?:src|href|poster)="([^"]+)"', h): refs.add(m)
for m in re.findall(r'(?:srcset)="([^"]+)"', h):
    for part in m.split(","): refs.add(part.strip().split(" ")[0])
missing=[r for r in refs if not r.startswith(("#","http","mailto")) and not os.path.isfile(r)]
print(f"引用 {len(refs)} 个，缺失 {len(missing)}: {missing}")
print("GO2 出现:", h.count("GO2"))
