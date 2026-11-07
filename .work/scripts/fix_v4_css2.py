import io, sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="assets/css/site-v4.css"; s=open(p,encoding="utf-8").read()
R=[
# 群控三条要点：去掉盒子，改成短竖条 + 文字，和培训的实心色块形成两种构成
(""".fact {
  padding: clamp(0.9rem, 1.6vw, 1.25rem);
  background: var(--panel);
}""",
""".fact {
  padding: 0;
}
.fact::before {
  content: "";
  display: block;
  width: 1.75rem;
  height: 3px;
  background: var(--led);
  margin-bottom: 0.7rem;
}"""),
# h1 统一一种字面：小行也用 display 字面，避免标题中途换字体
("""  font-family: var(--font-cn);
  font-size: var(--t-md);
  font-weight: 700;
  line-height: 1.5;
  letter-spacing: 0;
  color: #cfd7dc;
  margin-bottom: 0.9em;""",
"""  font-family: var(--font-display);
  font-size: var(--t-md);
  font-weight: 400;
  line-height: 1.45;
  letter-spacing: 0.01em;
  color: #cfd7dc;
  margin-bottom: 0.85em;"""),
# 首屏按钮字级抬到 t-md：既是视觉重量，也让「按钮文字」不再被误判成标题上方的小标签
(".btn-lg { min-height: 54px; padding: 0 2rem; font-size: var(--t-base); }",
 ".btn-lg { min-height: 56px; padding: 0 2rem; font-size: var(--t-md); }"),
]
missed=[]
for a,b in R:
    if a in s: s=s.replace(a,b,1)
    else: missed.append(a.strip().splitlines()[0][:60])
open(p,"w",encoding="utf-8").write(s)
print(f"命中 {len(R)-len(missed)}/{len(R)}"); [print("  未命中:",m) for m in missed]
