import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="index.html"; h=open(p,encoding="utf-8").read(); n0=len(h)
def sub(a,b,cnt=1,tag=""):
    global h
    assert a in h, "找不到："+a[:50]
    n=h.count(a); h=h.replace(a,b) if cnt==0 else h.replace(a,b,cnt)
    print(f"  ✅ {tag}（{n if cnt==0 else 1} 处）")

# ---- 24 米 → 240 米；3 站点 → 13 站点 ----
sub('<span class="hf"><b>24</b> 米直线路线</span>',
    '<span class="hf"><b>240</b> 米直线路线</span>', 1, "首屏数字 24→240")
sub('<b>现场数据</b>　学院楼线：209 实验室、210 实验室、电梯口。3 个站点，直线 24 米。',
    '<b>现场数据</b>　学院楼线：209 实验室、210 实验室、电梯口等 13 个站点，直线 240 米。',
    1, "导览现场数据")
sub('<dt class="fig-l">直线路线，3 个站点</dt>',
    '<dt class="fig-l">直线路线，13 个站点</dt>', 1, "交付实绩说明")
sub('<p>3 站 24 米</p>', '<p>13 站 240 米</p>', 1, "页脚")

# ---- 群控 lead：同步间隔 → 毫秒级时间同步 ----
sub("""          群控不是同时按下播放。每条指令由真实手柄按键序列构成，包含触发延迟、持续时长和动线范围，
          通过队列控制顺序，同步间隔保证多台动作对齐。""",
"""          群控不是同时按下播放。每条指令由真实手柄按键序列构成，包含触发延迟、持续时长和动线范围，
          通过队列控制顺序；多机之间用硬件时间同步对齐，动作误差在毫秒级。""",
    1, "群控导语")

# ---- 群控三条要点 → 四条（去掉同步间隔，改成毫秒级同步 + 动作兼容） ----
sub("""          <div class="fact">
            <p class="fact-t">同步间隔默认 2.0 秒</p>
            <p class="fact-d">间隔调准，多台动作才不会散队。间隔在后台可改。</p>
          </div>""",
"""          <div class="fact">
            <p class="fact-t">毫秒级同步</p>
            <p class="fact-d">多机之间走硬件时间同步，不用人工对表。队列跑起来动作误差在毫秒级，不会散队。</p>
          </div>
          <div class="fact">
            <p class="fact-t">官方动作 + 第三方动作</p>
            <p class="fact-d">宇树官方动作库直接可用；客户自己或我们编的第三方动作，同样能进队列下发。</p>
          </div>""",
    1, "群控要点")
open(p,"w",encoding="utf-8").write(h)
print(f"\nindex.html {n0} → {len(h)} 字节")
for k in ["24 米","3 个站点","3 站","同步间隔默认","毫秒级同步","第三方动作","240 米","13 个站点"]:
    print(f"  含「{k}」：{h.count(k)}")
