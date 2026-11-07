import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")

# ---------- HTML ----------
p="index-v4.html"; h=open(p,encoding="utf-8").read()
old_facts = '''        <div class="facts3">
          <div class="fact">
            <p class="fact-n">2.0<span class="u">秒</span></p>
            <p class="fact-t">同步模式</p>
            <p class="fact-d">同步模式默认间隔。间隔调准，多台动作才不会散队。</p>
          </div>
          <div class="fact">
            <p class="fact-n">一键<span class="u">急停</span></p>
            <p class="fact-t">安全保护</p>
            <p class="fact-d">红色按钮是紧急保护模式。不论队列执行到哪一步，一键全部停止。现场演练第一课。</p>
          </div>
          <div class="fact">
            <p class="fact-n">手机<span class="u">下发</span></p>
            <p class="fact-t">移动端</p>
            <p class="fact-d">移动端跑同一张指令表：勾选设备、选队列、一键执行。现场没有电脑也能改。</p>
          </div>
        </div>'''
new_facts = '''        <div class="facts3">
          <div class="fact">
            <p class="fact-t">同步间隔默认 2.0 秒</p>
            <p class="fact-d">间隔调准，多台动作才不会散队。间隔在后台可改。</p>
          </div>
          <div class="fact">
            <p class="fact-t">一键急停</p>
            <p class="fact-d">不论队列执行到哪一步，红色按钮一键全部停止。现场演练第一课。</p>
          </div>
          <div class="fact">
            <p class="fact-t">手机端下发</p>
            <p class="fact-d">移动端跑同一张指令表：勾选设备、选队列、一键执行。现场没有电脑也能改。</p>
          </div>
        </div>'''
assert old_facts in h, "facts3 not found"
h = h.replace(old_facts, new_facts, 1)

# 首屏三个数字：标签收紧，读数更快
h = h.replace('<span class="hf"><b>7</b> 台导览设备已交付</span>', '<span class="hf"><b>7</b> 台导览设备</span>')
h = h.replace('<span class="hf"><b>3</b> 个客户正在使用</span>', '<span class="hf"><b>3</b> 个客户</span>')
h = h.replace('<span class="hf"><b>24</b> 米学院楼直线路线</span>', '<span class="hf"><b>24</b> 米直线路线</span>')
open(p,"w",encoding="utf-8").write(h)
print("HTML 完成")

# ---------- CSS ----------
p2="assets/css/site-v4.css"; s=open(p2,encoding="utf-8").read()
R=[
("""".fact-n {
  font-family: var(--font-display);
  font-size: var(--t-lg);
  line-height: 1;
  color: var(--led);
}
.fact-n .u { font-size: var(--t-sm); margin-left: 0.14em; color: var(--soft); }
.fact-t { margin-top: 0.3rem; font-size: var(--t-base); font-weight: 700; line-height: 1.3; }""".strip('"'),
""".fact-t { font-size: var(--t-md); font-weight: 700; line-height: 1.4; }"""),
("  .fact-n { font-size: var(--t-md); }\n", ""),
# 手机：首屏数字回到 --t-lg（仍未进入「标题」判定，因为按钮已是 19px）
("  .hf b { font-size: var(--t-md); }", "  .hf b { font-size: var(--t-lg); }"),
]
missed=[]
for a,b in R:
    if a in s: s=s.replace(a,b,1)
    else: missed.append(a.strip().splitlines()[0][:60])
open(p2,"w",encoding="utf-8").write(s)
print(f"CSS 命中 {len(R)-len(missed)}/{len(R)}"); [print("  未命中:",m) for m in missed]
