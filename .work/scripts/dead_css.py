import re,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
h=open("index.html",encoding="utf-8").read()
c=open("assets/css/site.css",encoding="utf-8").read()
cls=set(re.findall(r'\.([a-zA-Z][\w-]*)', c))
used=set()
for m in re.findall(r'class="([^"]*)"', h):
    used.update(m.split())
dead=sorted(x for x in cls if x not in used and not x.startswith(("woff","avif","webp")))
print("CSS 中未被 HTML 使用的类:", len(dead))
print("  ", " ".join(dead[:60]))
