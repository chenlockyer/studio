import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="index.html"; h=open(P,encoding="utf-8").read()

BASE="https://chenlockyer.github.io/studio/"

# 1) og:image 与 canonical：Pages 上的地址已知了，写成绝对 URL，微信/社交分享才有图
h=h.replace('<meta property="og:image" content="assets/img/og.jpg">',
  f'<meta property="og:image" content="{BASE}assets/img/og.jpg">\n'
  f'<meta property="og:image:width" content="1200">\n'
  f'<meta property="og:image:height" content="675">\n'
  f'<meta property="og:url" content="{BASE}">\n'
  f'<meta name="twitter:card" content="summary_large_image">\n'
  f'<link rel="canonical" href="{BASE}">', 1)
open(P,"w",encoding="utf-8").write(h)

# 2) 检查页面里有没有根绝对路径（会破坏 /studio/ 子路径部署）
bad=[m for m in re.findall(r'(?:href|src|action)="(/[^/"][^"]*)"', h)]
print("根绝对路径:", bad if bad else "无")
print("og:image:", re.search(r'og:image" content="([^"]+)"', h).group(1))
print("canonical:", re.search(r'canonical" href="([^"]+)"', h).group(1))
