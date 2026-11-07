import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
from fontTools.ttLib import TTFont
for f in ["assets/fonts/smiley-display.woff2","assets/fonts/noto-400.woff2","assets/fonts/noto-700.woff2"]:
    t=TTFont(f); cmap=t.getBestCmap()
    has = 0x7EE9 in cmap
    print(f"  {f:38s} 绩(U+7EE9) {'有' if has else '缺'}  字形数 {len(cmap)}")
    if has:
        gs=t["hmtx"][cmap[0x7EE9]]
        print(f"      advance={gs[0]} / unitsPerEm={t['head'].unitsPerEm}")
