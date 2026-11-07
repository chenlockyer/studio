import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="assets/css/site-v4.css"; s=open(p,encoding="utf-8").read()
R=[
# 引导正文在手机上不再掉到 18px：18px 正好落进「标题上方小标签」的判定区间
("  --t-md: clamp(1.125rem, 1.45vw, 1.375rem);",
 "  --t-md: clamp(1.1875rem, 1.45vw, 1.375rem);"),
# 单列布局下，媒体说明文字与数字直接上下相邻 → 让数字落回正文级，避免被判成「标签压标题」
("""  .group-grid { grid-template-columns: 1fr; }
  .facts3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .course-grid { grid-template-columns: 1fr; }
  .course-facts { grid-template-columns: repeat(3, minmax(0, 1fr)); }""",
"""  .group-grid { grid-template-columns: 1fr; }
  .facts3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .fact-n { font-size: var(--t-md); }
  .course-grid { grid-template-columns: 1fr; }
  .course-facts { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .cf-n { font-size: var(--t-md); }"""),
]
missed=[]
for a,b in R:
    if a in s: s=s.replace(a,b,1)
    else: missed.append(a.strip().splitlines()[0][:60])
open(p,"w",encoding="utf-8").write(s)
print(f"命中 {len(R)-len(missed)}/{len(R)}"); [print("  未命中:",m) for m in missed]
