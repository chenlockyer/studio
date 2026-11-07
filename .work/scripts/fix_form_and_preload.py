import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")

# ---- 1. 去掉 preload 的 crossorigin（file:// 下会刷 CORS 报错，而 @font-face 本身能正常加载）----
p="index.html"; h=open(p,encoding="utf-8").read()
before=h
h=h.replace('<link rel="preload" href="assets/fonts/smiley-display.woff2" as="font" type="font/woff2" crossorigin>\n','')
h=h.replace('<link rel="preload" href="assets/fonts/noto-400.woff2" as="font" type="font/woff2" crossorigin>\n','')
open(p,"w",encoding="utf-8").write(h)
print("移除 preload 行:", "是" if h!=before else "否")

# ---- 2. 表单加一个可手动复制的回退框 ----
h=open(p,encoding="utf-8").read()
old='''        <button class="btn btn-dark" type="submit">复制需求</button>
        <p class="ask-hint" id="ask-hint" role="status">
          填写后点击按钮，四项内容会合成一段话复制到剪贴板，直接粘贴到微信发送给我们。
        </p>'''
new='''        <button class="btn btn-dark" type="submit">复制需求</button>
        <p class="ask-hint" id="ask-hint" role="status">
          填写后点击按钮，四项内容会合成一段话复制到剪贴板，直接粘贴到微信发送给我们。
        </p>
        <label class="ask-fallback" id="ask-fallback" hidden>
          <span class="field-label">浏览器不让自动复制，全选这段后按 Ctrl+C</span>
          <textarea id="ask-brief" rows="4" readonly></textarea>
        </label>'''
assert old in h, "表单尾部未找到"
h=h.replace(old,new,1)
open(p,"w",encoding="utf-8").write(h)
print("加入回退文本框: 是")
