import io,sys,re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
p="index-v4.html"; h=open(p,encoding="utf-8").read(); orig=h

R=[
# --- FAIL: eyebrow（kicker 压在标题上）→ 把 kicker 的信息并进 H1 的第二行 ---
('<p class="hero-kicker">宇树 G1 机器人落地交付</p>\n\n      <h1 class="hero-title">\n        场馆导览<span class="sep">·</span>多机群控<span class="sep">·</span>动作定制\n      </h1>',
 '<h1 class="hero-title">\n        <span class="hero-title-l1">宇树 G1 机器人落地交付</span>\n        场馆导览<span class="sep">·</span>多机群控<span class="sep">·</span>动作定制\n      </h1>'),

# --- FAIL: 三个数字的 label 压在数字上 → 改成「数字在前，说明在后」的行内式 ---
('''      <dl class="hero-figs">
        <div class="hf">
          <dd class="hf-n">7</dd>
          <dt class="hf-l">台导览设备已交付</dt>
        </div>
        <div class="hf">
          <dd class="hf-n">3</dd>
          <dt class="hf-l">个客户正在使用</dt>
        </div>
        <div class="hf">
          <dd class="hf-n">24<span class="hf-u">米</span></dd>
          <dt class="hf-l">学院楼直线路线</dt>
        </div>
      </dl>''',
 '''      <p class="hero-figs">
        <span class="hf"><b>7</b> 台导览设备已交付</span>
        <span class="hf"><b>3</b> 个客户正在使用</span>
        <span class="hf"><b>24</b> 米学院楼直线路线</span>
      </p>'''),

# --- FAIL: 01/02/03/04 装饰编号 → 导览四步改成真 <ol>，用文字表达顺序 ---
('''      <div class="steps4">
        <div class="step">
          <p class="step-n">01</p>
          <p class="step-k">建图管理</p>
          <p>G1 用本体雷达走一遍现场，边走边出图，不依赖外网。</p>
        </div>
        <div class="step">
          <p class="step-n">02</p>
          <p class="step-k">站点标注</p>
          <p>在地图上标定每个站点的位置与朝向，朝向决定讲解时面向哪里。</p>
        </div>
        <div class="step">
          <p class="step-n">03</p>
          <p class="step-k">人设配置</p>
          <p>设定讲解员身份、语言风格和禁答范围，超范围问题自动转人工。</p>
        </div>
        <div class="step">
          <p class="step-n">04</p>
          <p class="step-k">导览方案</p>
          <p>配置站点顺序、每站讲解词和临时变更规则，保存即生效。</p>
        </div>
      </div>''',
 '''      <ol class="steps4">
        <li class="step">
          <p class="step-k">建图管理</p>
          <p>G1 用本体雷达走一遍现场，边走边出图，不依赖外网。</p>
        </li>
        <li class="step">
          <p class="step-k">站点标注</p>
          <p>在地图上标定每个站点的位置与朝向，朝向决定讲解时面向哪里。</p>
        </li>
        <li class="step">
          <p class="step-k">人设配置</p>
          <p>设定讲解员身份、语言风格和禁答范围，超范围问题自动转人工。</p>
        </li>
        <li class="step">
          <p class="step-k">导览方案</p>
          <p>配置站点顺序、每站讲解词和临时变更规则，保存即生效。</p>
        </li>
      </ol>'''),

# --- 动作链四步同样处理 ---
('''      <div class="steps4">
        <div class="step">
          <p class="step-n">01</p>
          <p class="step-k">人体动作提取</p>
          <p>单目视频估算人体参数。手机拍一段舞，就能转成可用的动作数据。</p>
        </div>
        <div class="step">
          <p class="step-n">02</p>
          <p class="step-k">仿真环境训练</p>
          <p>在 IsaacSim 中训练校验。碰撞、跌倒、失控全部发生在仿真里，试错成本为零。</p>
        </div>
        <div class="step">
          <p class="step-n">03</p>
          <p class="step-k">跨引擎复验</p>
          <p>在 MuJoCo 中做二次验证。两个物理引擎结果一致，才进入真机部署。</p>
        </div>
        <div class="step">
          <p class="step-n">04</p>
          <p class="step-k">真机部署调优</p>
          <p>上机后还需收敛稳定性：地面材质、现场灯光、观众距离都会影响效果。</p>
        </div>
      </div>''',
 '''      <ol class="steps4">
        <li class="step">
          <p class="step-k">人体动作提取</p>
          <p>单目视频估算人体参数。手机拍一段舞，就能转成可用的动作数据。</p>
        </li>
        <li class="step">
          <p class="step-k">仿真环境训练</p>
          <p>在 IsaacSim 中训练校验。碰撞、跌倒、失控全部发生在仿真里，试错成本为零。</p>
        </li>
        <li class="step">
          <p class="step-k">跨引擎复验</p>
          <p>在 MuJoCo 中做二次验证。两个物理引擎结果一致，才进入真机部署。</p>
        </li>
        <li class="step">
          <p class="step-k">真机部署调优</p>
          <p>上机后还需收敛稳定性：地面材质、现场灯光、观众距离都会影响效果。</p>
        </li>
      </ol>'''),

# --- 交付四步：一/二/三/四 也是装饰编号 → 改真 <ol> ---
('''      <div class="steps-d">
        <div class="dstep">
          <p class="dstep-n">一</p>''',
 '''      <ol class="steps-d">
        <li class="dstep">'''),
('<p class="dstep-k">现场勘察</p>\n          <p>地面、光线、网络、人流、充电位，任何一项都会影响可行性。勘察完成后出方案。</p>\n        </div>',
 '<p class="dstep-k">现场勘察</p>\n          <p>地面、光线、网络、人流、充电位，任何一项都会影响可行性。勘察完成后出方案。</p>\n        </li>'),
('''        <div class="dstep">
          <p class="dstep-n">二</p>''', '        <li class="dstep">'),
('<p class="dstep-k">激光建图</p>\n          <p>建图使用本体雷达，不依赖外网。走偏现场可见，墙线偏差事后可修。</p>\n        </div>',
 '<p class="dstep-k">激光建图</p>\n          <p>建图使用本体雷达，不依赖外网。走偏现场可见，墙线偏差事后可修。</p>\n        </li>'),
('''        <div class="dstep">
          <p class="dstep-n">三</p>''', '        <li class="dstep">'),
('<p class="dstep-k">路线编排</p>\n          <p>站点顺序、每站朝向、讲解内容，全部在场馆自有后台配置。</p>\n        </div>',
 '<p class="dstep-k">路线编排</p>\n          <p>站点顺序、每站朝向、讲解内容，全部在场馆自有后台配置。</p>\n        </li>'),
('''        <div class="dstep">
          <p class="dstep-n">四</p>''', '        <li class="dstep">'),
('<p class="dstep-k">联调交接</p>\n          <p>到站、讲解、被打断、返回路线全流程验证。培训两名人员：开机、改方案、急停。</p>\n        </div>\n      </div>',
 '<p class="dstep-k">联调交接</p>\n          <p>到站、讲解、被打断、返回路线全流程验证。培训两名人员：开机、改方案、急停。</p>\n        </li>\n      </ol>'),

# --- FAIL: 页面里出现的 3 条细线 → 换成色块分隔 ---
('<div class="foot-cols">', '<div class="foot-cols foot-cols-plain">'),
]
missed=[]
for a,b in R:
    if a in h: h=h.replace(a,b,1)
    else: missed.append(a[:64].replace("\n","⏎"))
open(p,"w",encoding="utf-8").write(h)
print(f"命中 {len(R)-len(missed)}/{len(R)}")
for m in missed: print("  未命中:", m)
