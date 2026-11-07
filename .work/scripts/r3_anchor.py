import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="index.html"; h=open(P,encoding="utf-8").read()
h = h.replace('<section class="paper" aria-labelledby="figs-title">',
              '<section class="paper" id="figs" aria-labelledby="figs-title">', 1)
open(P,"w",encoding="utf-8").write(h)

# 全量核对页面内锚点是否都有对应 id
ids = set(re.findall(r'\sid="([^"]+)"', h))
hrefs = set(re.findall(r'href="#([^"]+)"', h))
missing = sorted(x for x in hrefs if x not in ids)
print("页面内锚点:", sorted(hrefs))
print("缺失目标:", missing if missing else "无")
