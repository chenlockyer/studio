import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="assets/css/site.css"; c=open(P,encoding="utf-8").read(); n0=len(c)

# 1) 删掉整个「问答」CSS 段（含注释头）直到下一个注释头
m = re.search(r'/\* =+\n   问答\n   =+ \*/\n.*?(?=/\* =+\n   [^\n]*\n   =+ \*/)', c, re.S)
assert m, "找不到问答 CSS 段"
print("  删问答段：", m.end()-m.start(), "字节")
c = c[:m.start()] + c[m.end():]

# 2) 删掉媒体查询里的 faq 覆盖行
for line in ['  .faq { grid-template-columns: 1fr; }\n',
             '  .faq-grid { grid-template-columns: 1fr; }\n',
             '  .faq-list { grid-template-columns: 1fr; }\n',
             '  .faq-aside { position: static; }\n',
             '  .faq-aside { display: none; }\n']:
    if line in c:
        c = c.replace(line, "", 1); print("  删覆盖：", line.strip())

# 3) 课程安排里的日期标签要有对比度
c = c.replace(""".goals-list li::before {""",
""".goals-list b {
  color: var(--paper-ink);
  font-weight: 700;
}
.goals-list li::before {""", 1)
print("  ✅ .goals-list b 已补")

# 4) 删掉已无用的 .caution-note
c = c.replace(".caution-note { font-size: var(--t-base); color: var(--soft); }\n", "", 1)

open(P,"w",encoding="utf-8").write(c)
print(f"\nsite.css {n0} → {len(c)} 字节")
for k in ["faq","FAQ","问答"]:
    print(f"  残留「{k}」：{c.count(k)}")
