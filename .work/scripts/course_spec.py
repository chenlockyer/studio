import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="index-v4.html"; h=open(p,encoding="utf-8").read()

start = h.index('      <div class="course-grid">')
end   = h.index('      <div class="goals">')
old   = h[start:end]
assert 'course-facts' in old and 'lab-bench' in old, "course block shape unexpected"

new = '''      <p class="course-spec">
        <span><b>2</b> 天</span>
        <span><b>12</b> 学时</span>
        <span><b>20–24</b> 人分 4 组轮换</span>
        <span><b>2</b> 台 G1 EDU · 23 与 29 自由度各一台</span>
      </p>

'''
h = h[:start] + new + h[end:]
open(p,"w",encoding="utf-8").write(h)
print("培训区块：照片与卡片格改为规格条")

p2="assets/css/site-v4.css"; s=open(p2,encoding="utf-8").read()
s += '''
/* ---------- 培训：一行规格，不用卡片格 ---------- */
.course-spec {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: clamp(1.25rem, 3.5vw, 3.25rem);
  margin-top: clamp(1.5rem, 3vw, 2.25rem);
  padding: clamp(0.6rem, 1.2vw, 0.9rem) 0 clamp(0.6rem, 1.2vw, 0.9rem) clamp(1rem, 2vw, 1.5rem);
  border-left: 3px solid var(--led);
  font-size: var(--t-base);
  color: var(--soft);
}
.course-spec b {
  font-family: var(--font-display);
  font-size: var(--t-lg);
  font-weight: 400;
  line-height: 1;
  color: var(--led);
  margin-right: 0.35rem;
}
/* 平板：四步与三条事实不再挤成一行 */
@media (max-width: 900px) {
  .steps-d { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
'''
open(p2,"w",encoding="utf-8").write(s)
print("CSS 已加 .course-spec 与 ≤900 steps-d 两列")
