import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="assets/css/site-v4.css"; s=open(p,encoding="utf-8").read()
R=[
# 交付四步：把 2px 顶边换成与 .step 一致的短竖条，避免"四张一样的卡片"
(""".dstep {
  display: grid;
  gap: 0.35rem;
  align-content: start;
  padding-top: clamp(0.9rem, 1.6vw, 1.25rem);
  border-top: 2px solid var(--led);
}""",
""".dstep {
  display: grid;
  gap: 0.35rem;
  align-content: start;
}
.dstep::before {
  content: "";
  width: 1.5rem;
  height: 3px;
  background: var(--led);
  margin-bottom: 0.7rem;
}"""),
# 问答：常态行不铺底色，只有展开的那一条有面板色
(".faq-item { background: var(--ground); }",
 ".faq-item[open] { background: var(--ground); }"),
]
missed=[]
for a,b in R:
    if a in s: s=s.replace(a,b,1)
    else: missed.append(a.strip().splitlines()[0][:60])
open(p,"w",encoding="utf-8").write(s)
print(f"命中 {len(R)-len(missed)}/{len(R)}")
[print("  未命中:",m) for m in missed]
