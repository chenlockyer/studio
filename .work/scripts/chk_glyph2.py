import io,sys,re,html
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
from fontTools.ttLib import TTFont
h=open("index.html",encoding="utf-8").read()
body=re.sub(r"<script[\s\S]*?</script>"," ",h)
body=re.sub(r"<!--[\s\S]*?-->"," ",body)
page=set(html.unescape(re.sub(r"<[^>]+>"," ",body)))
for attr in ("alt","aria-label","title","placeholder","content"):
    for m in re.findall(attr+r'="([^"]*)"',h): page|=set(html.unescape(m))
page.discard("\n"); page.discard("\r")
print(f"页面实际用字 {len(page)} 个")
for f in ["assets/fonts/smiley-display.woff2","assets/fonts/noto-400.woff2","assets/fonts/noto-700.woff2"]:
    t=TTFont(f,lazy=True); cm=set(t.getBestCmap()); t.close()
    miss=sorted(c for c in page if ord(c) not in cm)
    print(f"  {f:40s} 缺 {len(miss):2d}  {''.join(miss[:20])}")
    print(f"      绩(U+7EE9): {'有' if 0x7EE9 in cm else '缺'}")
