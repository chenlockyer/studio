import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
p = "assets/css/site-v4.css"
s = open(p, encoding="utf-8").read()
orig = s

R = [
# ---------- 1. 统一左右边距：.wrap 内容宽 = --mw，与 .hero-inner 对齐 ----------
(""".wrap {
  width: 100%;
  max-width: var(--mw);
  margin-inline: auto;
  padding-inline: var(--pad);
}""",
""".wrap {
  width: 100%;
  /* 内容真正占满 --mw：把内边距算进 max-width，和 .hero-inner 的边缘对齐 */
  max-width: calc(var(--mw) + var(--pad) * 2);
  margin-inline: auto;
  padding-inline: var(--pad);
}"""),

# ---------- 2. 顶栏：去掉 1px 底线，靠毛玻璃与色调差分隔 ----------
("""  background: rgba(10, 12, 14, 0.82);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}""",
"""  background: rgba(10, 12, 14, 0.9);
  backdrop-filter: blur(14px) saturate(120%);
}"""),

# ---------- 3. hero 标题：放开 measure，两行装下 ----------
("""  line-height: 1.06;
  letter-spacing: -0.01em;
  max-width: 20ch;
}
/* 第一行先说清是什么生意，第二行才是业务名词 */
.hero-title-l1 {
  display: block;
  font-size: 0.46em;
  line-height: 1.35;
  letter-spacing: 0.01em;
  color: #c3ccd2;
  margin-bottom: 0.28em;
}""",
"""  line-height: 1.06;
  letter-spacing: -0.01em;
  max-width: 100%;
}
/* 第一行先说清是什么生意，第二行才是业务名词。
   它是 h1 的子行，不是压在上面的小标签。 */
.hero-title-l1 {
  display: block;
  font-family: var(--font-cn);
  font-size: var(--t-md);
  font-weight: 700;
  line-height: 1.5;
  letter-spacing: 0;
  color: #cfd7dc;
  margin-bottom: 0.9em;
}"""),

# ---------- 4. 首屏数字：去细线、拉开距离、字号回落到字阶内 ----------
("""/* 首屏三个数字：数字在前、说明在后，一行读完，不叠标签 */
.hero-figs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem clamp(1.25rem, 3.5vw, 3rem);
  margin-top: clamp(0.5rem, 2.5vh, 1.75rem);
  padding-top: clamp(1rem, 2.5vh, 1.75rem);
  border-top: 1px solid rgba(255, 255, 255, 0.16);
  width: 100%;
  font-size: var(--t-base);
  color: var(--soft);
}
.hf { display: inline-flex; align-items: baseline; gap: 0.4rem; }
.hf b {
  font-family: var(--font-display);
  font-size: clamp(1.6rem, 2.6vw, 2.25rem);
  font-weight: 400;
  line-height: 1;
  color: var(--ink);
}""",
"""/* 首屏三个数字：数字在前、说明在后，一行读完。
   分隔靠留白和色调，不靠细线。 */
.hero-figs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem clamp(1.75rem, 4vw, 3.5rem);
  margin-top: clamp(1.75rem, 4vh, 2.75rem);
  width: 100%;
  font-size: var(--t-base);
  color: #aab5bd;
}
.hf { display: inline-flex; align-items: baseline; gap: 0.45rem; }
.hf b {
  font-family: var(--font-display);
  font-size: var(--t-lg);
  font-weight: 400;
  line-height: 1;
  color: var(--ink);
}"""),

# ---------- 5. 四步：去掉卡片盒子，用留白与短竖条分隔 ----------
(""".step {
  display: grid;
  gap: 0.4rem;
  align-content: start;
  padding: clamp(1rem, 1.8vw, 1.5rem);
  background: var(--panel);
  counter-increment: s4;
}""",
""".step {
  display: grid;
  gap: 0.45rem;
  align-content: start;
  counter-increment: s4;
}"""),

# ---------- 6. fact-n 落到字阶 ----------
(""".fact-n {
  font-family: var(--font-display);
  font-size: clamp(1.5rem, 2.4vw, 2.125rem);""",
""".fact-n {
  font-family: var(--font-display);
  font-size: var(--t-lg);"""),
(".fact-n .u { font-size: 0.5em; margin-left: 0.12em; color: var(--soft); }",
 ".fact-n .u { font-size: var(--t-sm); margin-left: 0.14em; color: var(--soft); }"),

# ---------- 7. 交付实绩：数字在上、说明在下（原来 column-reverse 把标签顶到了上面） ----------
(""".fig { display: flex; flex-direction: column-reverse; gap: 0.3rem; }""",
 """.fig { display: flex; flex-direction: column; gap: 0.35rem; }"""),
(""".fig-n {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 5.6vw, 4.75rem);""",
""".fig-n {
  font-family: var(--font-display);
  font-size: var(--t-xl);"""),
(".fig-u { font-size: 0.34em; margin-left: 0.1em; color: var(--paper-soft); }",
 ".fig-u { font-size: var(--t-md); margin-left: 0.12em; color: var(--paper-soft); }"),

# ---------- 8. 培训数字与验收标题回落到字阶 ----------
(""".cf-n {
  font-family: var(--font-display);
  font-size: clamp(1.9rem, 3.2vw, 2.75rem);""",
""".cf-n {
  font-family: var(--font-display);
  font-size: var(--t-lg);"""),
(""".goals-k {
  font-family: var(--font-display);
  font-size: var(--t-lg);""",
""".goals-k {
  font-size: var(--t-md);
  font-weight: 700;"""),

# ---------- 9. FAQ 两栏：右边放转化入口，避免整屏空一半 ----------
(""".faq-list { display: grid; gap: 2px; max-width: 62rem; }""",
""".faq-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 21rem;
  gap: clamp(1.75rem, 4vw, 4rem);
  align-items: start;
}
.faq-aside {
  display: grid;
  gap: 0.9rem;
  justify-items: start;
  padding: clamp(1.25rem, 2.4vw, 2rem);
  background: var(--panel);
  position: sticky;
  top: 6rem;
}
.faq-aside-k { font-size: var(--t-md); font-weight: 700; line-height: 1.4; }
.faq-aside-d { font-size: var(--t-base); line-height: 1.65; color: var(--soft); }
.faq-aside-meta { font-size: var(--t-sm); color: var(--soft); }
.faq-list { display: grid; gap: 2px; }"""),

# ---------- 10. 页脚：去细线，用色调块分隔 ----------
(""".foot-cols {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr));
  gap: clamp(1rem, 2.4vw, 2rem);
  margin-top: clamp(1.75rem, 3.5vw, 2.75rem);
  padding-top: clamp(1.25rem, 2.5vw, 2rem);
  border-top: 1px solid var(--panel-2);
  font-size: var(--t-sm);""",
""".foot-cols {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr));
  gap: clamp(1rem, 2.4vw, 2rem);
  margin-top: clamp(1.75rem, 3.5vw, 2.75rem);
  padding-top: clamp(1.25rem, 2.5vw, 2rem);
  font-size: var(--t-sm);"""),

# ---------- 11. 按钮与字标回落到字阶 ----------
(".btn-lg { min-height: 54px; padding: 0 2rem; font-size: 1.125rem; }",
 ".btn-lg { min-height: 54px; padding: 0 2rem; font-size: var(--t-base); }"),
(""".wm {
  font-family: var(--font-display);
  font-size: 1.3rem;""",
""".wm {
  font-family: var(--font-display);
  font-size: var(--t-md);"""),

# ---------- 12. 小屏：FAQ 单栏、数字字号同步 ----------
(""".faq-item summary { font-size: var(--t-base); padding: 0.95rem 1rem; }""",
""".faq-grid { grid-template-columns: 1fr; }
  .faq-aside { position: static; }
  .faq-item summary { font-size: var(--t-base); padding: 0.95rem 1rem; }"""),
("""  .hero-figs { gap: 1rem 1.5rem; }
  .hf-n { font-size: 1.75rem; }
  .hf-l { font-size: 0.8125rem; }""",
"""  .hero-figs { gap: 0.7rem 1.35rem; }
  .hf b { font-size: var(--t-md); }"""),
("""  .fig-n { font-size: clamp(2.25rem, 11vw, 3rem); }""",
"""  .fig-n { font-size: var(--t-lg); }"""),
]

missed = []
for a, b in R:
    if a in s:
        s = s.replace(a, b, 1)
    else:
        missed.append(a.strip().splitlines()[0][:70])

# 清掉不再存在的 hero-kicker 样式块
import re
s = re.sub(r"\n\.hero-kicker \{.*?\n\}\n", "\n", s, flags=re.S)
s = s.replace(".hero-kicker, .hero-title, .hero-sub, .hero-act, .hero-figs {", ".hero-title, .hero-sub, .hero-act, .hero-figs {")

open(p, "w", encoding="utf-8").write(s)
print(f"CSS 命中 {len(R)-len(missed)}/{len(R)}")
for m in missed: print("  未命中:", m)
print("hero-kicker 残留:", s.count("hero-kicker"))
