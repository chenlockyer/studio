import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="assets/css/site-v4.css"; s=open(p,encoding="utf-8").read()
R=[
# 手机：区块间距与首屏下边距都要大于 72px，否则上一段短句会被判成下个标题的「小标签」
("""  .hero {
    min-height: 94svh;
    padding-top: calc(var(--pad) + 4.5rem);
    padding-bottom: 1.75rem;
  }""",
"""  .hero {
    min-height: 94svh;
    padding-top: calc(var(--pad) + 4.5rem);
    padding-bottom: 2.75rem;
  }"""),
("  .sec { padding: clamp(2.25rem, 8vw, 3.5rem) 0; }",
 "  .sec { padding: clamp(2.75rem, 9vw, 3.75rem) 0; }"),
# 折叠的问答正文不参与布局：Chrome 现在用 content-visibility 隐藏它，几何框还在
(".faq-item p {",
 ".faq-item:not([open]) > p { display: none; }\n.faq-item p {"),
]
missed=[]
for a,b in R:
    if a in s: s=s.replace(a,b,1)
    else: missed.append(a.strip().splitlines()[0][:60])
open(p,"w",encoding="utf-8").write(s)
print(f"命中 {len(R)-len(missed)}/{len(R)}"); [print("  未命中:",m) for m in missed]
