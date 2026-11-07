import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
# 404 页：GitHub Pages 项目站跑在 /studio/ 子路径下，必须用绝对地址指回站点
P="404.html"; h=open(P,encoding="utf-8").read()
h=h.replace('<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">',
            '<link rel="icon" href="https://chenlockyer.github.io/studio/assets/favicon.svg" type="image/svg+xml">')
h=h.replace('<a href="/">回首页</a>',
            '<a href="https://chenlockyer.github.io/studio/">回首页</a>')
open(P,"w",encoding="utf-8").write(h)
print("404.html 已改为绝对地址")
print("  剩余根绝对路径:", h.count('href="/'))
