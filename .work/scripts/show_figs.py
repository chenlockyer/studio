import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
h=open("index.html",encoding="utf-8").read()
i=h.find('id="figs"'); j=h.find('</section>', i)
print(h[i-60:j])
print("\n=== 独立出现的 24 / 3 站点 ===")
import re
for m in re.finditer(r'.{18}(?<![0-9])24(?!0).{18}', h):
    print("  24 →", m.group(0).replace("\n"," "))
