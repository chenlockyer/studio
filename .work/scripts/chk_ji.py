import io,sys
from fontTools.ttLib import TTFont
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
for f in ["smiley-display","noto-400","noto-700"]:
    t=TTFont(f"assets/fonts/{f}.woff2")
    cmap=t.getBestCmap()
    print(f"{f:16s} 字形 {len(t.getGlyphOrder())}  绩={'有' if 0x7EE9 in cmap else '无'}")
