import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")

# ---- HTML：标题缩短、提示收紧 ----
p="index.html"; h=open(p,encoding="utf-8").read()
rep=[
 ('<p class="wx-title" id="wx-title">扫码加微信，直接聊你的场地</p>',
  '<p class="wx-title" id="wx-title">加微信，直接聊场地</p>'),
 ('<p class="wx-hint">加好友时备注「G1 + 场地类型」，工作时间 30 分钟内回。</p>',
  '<p class="wx-hint">备注「G1 + 场地类型，30 分钟内回。</p>'),
]
for a,b in rep:
    assert a in h, a[:40]
    h=h.replace(a,b,1)
# 提示文案补全对称括号
h=h.replace('备注「G1 + 场地类型，30 分钟内回。','备注「G1 + 场地类型」，30 分钟内回。')
open(p,"w",encoding="utf-8").write(h)
print("HTML 已改")

# ---- CSS：卡片加宽、标题平衡换行、焦点环改成 LED 细环 ----
p2="assets/css/site.css"; c=open(p2,encoding="utf-8").read()
c=c.replace("  width: min(92vw, 25rem);\n  max-width: none;","  width: min(92vw, 27rem);\n  max-width: none;",1)
c=c.replace("""  line-height: 1.2;
  letter-spacing: -0.01em;
}""","""  line-height: 1.2;
  letter-spacing: -0.01em;
  text-wrap: balance;
}""",1)
c=c.replace(""".wx-close:hover { color: var(--paper-ink); }""",
""".wx-close:hover { color: var(--paper-ink); }
.wx-close:focus-visible {
  outline: 2px solid var(--led);
  outline-offset: -6px;
  border-radius: 2px;
  color: var(--paper-ink);
}""",1)
open(p2,"w",encoding="utf-8").write(c)
print("CSS 已改")
