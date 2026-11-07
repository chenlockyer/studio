import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
p = "index-v4.html"
h = open(p, encoding="utf-8").read()

R = [
# FAQ 包进两栏网格，右侧放转化入口，填掉空着的 712px
('<div class="faq-list">',
 '''<div class="faq-grid">
      <div class="faq-list">'''),
]
missed = []
for a,b in R:
    if a in h: h = h.replace(a,b,1)
    else: missed.append(a[:60])

# 在 faq-list 结束处插入 aside。找到 faq 区块里第一个 </div> 之后紧跟 </div>\n  </section> 的结构
import re
# 定位 faq-list 的结尾：从 faq-grid 开始，匹配到最后一个 </details> 之后的 </div>
i = h.find('<div class="faq-list">')
assert i > 0
j = h.find('</details>', i)
# 找到最后一个属于 faq 的 </details>
last = h.rfind('</details>', i, h.find('</section>', i))
k = h.find('</div>', last)
aside = '''
      </div>

      <aside class="faq-aside">
        <p class="faq-aside-k">没找到你的问题？</p>
        <p class="faq-aside-d">把场地情况说清楚——多大、几个点位、什么时候要。我们按你的实际条件给排法，不先报价。</p>
        <a class="btn btn-led" href="#contact">说清你的场地</a>
        <p class="faq-aside-meta">深圳坪山 · 工作时间内 30 分钟回一条</p>
      </aside>
    </div>'''
h = h[:k] + aside + h[k+len('</div>'):]

open(p,"w",encoding="utf-8").write(h)
print("FAQ 两栏插入完成" if 'faq-aside' in h else "失败")
for m in missed: print("  未命中:", m)
