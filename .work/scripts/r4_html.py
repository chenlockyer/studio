import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="index.html"; h=open(p,encoding="utf-8").read()
n0=len(h)

# 1) 导航项
old_nav = '    <a href="#faq">常见问题</a>\n'
assert old_nav in h, "找不到 faq 导航项"
h = h.replace(old_nav, "", 1)
print("✅ 导航项已删")

# 2) FAQ 整块
m = re.search(r'  <!-- =+\n       七 · 常见问题\n       =+ -->\n  <section class="sec sec-alt" id="faq".*?</section>\n\n', h, re.S)
assert m, "找不到 FAQ 区块"
h = h[:m.start()] + h[m.end():]
print(f"✅ FAQ 区块已删（{m.end()-m.start()} 字节）")

# 3) 联系区
old_c = "不用填表。加微信"
assert old_c in h
h = h.replace(old_c, "加微信", 1)
print("✅ 「不用填表。」已删")

# 4) 课程区块
old_head = """       六 · 师资培训
       ============================================================ -->
  <section class="sec" id="course" aria-labelledby="course-title">
    <div class="wrap">
      <div class="sec-head">
        <h2 class="h" id="course-title">两天 12 学时，教到你们的人能独立操作</h2>
        <p class="lead">
          不是听讲式科普。两天 12 学时，约 75% 时间在真机上操作，20 到 24 人分 4 组轮换。
        </p>
      </div>

      <p class="course-spec">
        <span><b>2</b> 天</span>
        <span><b>12</b> 学时</span>
        <span><b>20–24</b> 人分 4 组轮换</span>
        <span><b>2</b> 台 G1 EDU · 23 与 29 自由度各一台</span>
      </p>

      <div class="goals">"""
new_head = """       六 · 线下教培
       ============================================================ -->
  <section class="sec" id="course" aria-labelledby="course-title">
    <div class="wrap">
      <div class="sec-head">
        <h2 class="h" id="course-title">具身智能实战课程</h2>
        <p class="lead">
          面向高校与场馆团队的线下教培。不是听讲式科普——两天 12 学时，约 75% 时间在真机上操作，
          20 到 24 人分 4 组轮换，每组都有自己的上手时间。
        </p>
      </div>

      <p class="course-spec">
        <span><b>2</b> 天</span>
        <span><b>12</b> 学时</span>
        <span><b>20–24</b> 人分 4 组轮换</span>
        <span><b>2</b> 台 G1 EDU · 23 与 29 自由度各一台</span>
      </p>

      <div class="goals">
        <p class="goals-k">课程<br>安排</p>
        <ol class="goals-list">
          <li><b>第一天 · 上午</b>　安全规程与 SDK 环境：先把底线立住，再碰硬件。</li>
          <li><b>第一天 · 下午</b>　G1 人形上手，两人一组：起身、站立、行走。</li>
          <li><b>第二天 · 上午</b>　从关节数到高层接口：状态读得出来，动作才控得住。</li>
          <li><b>第二天 · 下午</b>　综合演练与结业验收：同一套代码先仿真、后真机。</li>
        </ol>
      </div>

      <div class="goals">"""
assert old_head in h, "找不到课程区块头部"
h = h.replace(old_head, new_head, 1)
print("✅ 课程区块已改写")

# 5) 上门授课那句
old_note = """        <a class="btn btn-led" href="assets/img/wechat-qr.png" data-wx>预约开班</a>
        <span class="caution-note">也可安排上门授课，设备由我们携带。</span>
      </div>"""
assert old_note in h, "找不到上门授课那句"
h = h.replace(old_note, """        <a class="btn btn-led" href="assets/img/wechat-qr.png" data-wx>预约开班</a>
      </div>""", 1)
print("✅ 「也可安排上门授课…」已删")

# 6) 师资培训 → 线下教培
cnt = h.count("师资培训"); h = h.replace("师资培训","线下教培")
print(f"✅ 师资培训 → 线下教培：{cnt} 处")

open(p,"w",encoding="utf-8").write(h)
print(f"\nindex.html {n0} → {len(h)} 字节")
for k in ["常见问题","不用填表","上门授课","师资培训","faq","线下教培","具身智能实战课程"]:
    print(f"  含「{k}」：{h.count(k)}")
