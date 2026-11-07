# 三项修改：
#   1) 「交付实绩」的「绩」缺字形 —— 字体已在 fonts_v4.py 里重建，本脚本只改文案结构不动字体
#   2) 联系方式点击弹微信二维码
#   3) 隐去「深圳坪山」，改成全球交付
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P_HTML = "index.html"
P_CSS = "assets/css/site.css"
P_JS = "assets/js/site.js"

h = open(P_HTML, encoding="utf-8").read()


def sub(old, new, why, count=1):
    global h
    if old not in h:
        print(f"  ✗ 未命中：{why}")
        return False
    h = h.replace(old, new, count)
    print(f"  ✓ {why}")
    return True


print("[1] 隐去深圳坪山，改全球交付")
sub(
    '已交付导览 7 台 / 3 个客户，群控 3 套。深圳坪山，珠三角当天可达。',
    '已交付导览 7 台 / 3 个客户，群控 3 套。全球范围可交付，勘察与交接可到场。',
    'meta description')
sub('action,深圳机器人,师资培训', 'action,机器人落地交付,师资培训', 'meta keywords')
sub('<span class="wm-sub">深圳坪山</span>', '<span class="wm-sub">全球交付</span>', '页头小字')
sub('<p>深圳坪山。珠三角地区当天可达；外省按项目排期，勘察与交接各到场一次。</p>',
    '<p>项目按全球范围安排：场地勘察、建图标注、联调与交接可以到场，其余环节远程完成。差旅与到场次数按项目写进合同。</p>',
    'FAQ 地点回答')
sub('<summary>你们在哪里，能来现场吗？</summary>', '<summary>我们不在同一个城市，能交付吗？</summary>', 'FAQ 地点提问')
sub('<p class="faq-aside-meta">深圳坪山 · 工作时间内 30 分钟回一条</p>',
    '<p class="faq-aside-meta">全球交付 · 工作时间内 30 分钟回一条</p>', 'FAQ 侧栏')
sub('<p class="contact-promise">深圳坪山 · 工作时间 30 分钟内回复</p>',
    '<p class="contact-promise">全球交付 · 工作时间 30 分钟内回复</p>', '联系区承诺')
sub('        <p>深圳坪山</p>', '        <p>全球范围可交付</p>', '页脚现场列')

print("[2] 主 CTA 改为打开微信二维码")
# 页头
sub('<a class="btn btn-led btn-bar" href="#contact">获取方案</a>',
    '<a class="btn btn-led btn-bar" href="assets/img/wechat-qr.png" data-wx>获取方案</a>', '页头获取方案')
# 首屏
sub('<a class="btn btn-led btn-lg" href="#contact">说清你的场地</a>',
    '<a class="btn btn-led btn-lg" href="assets/img/wechat-qr.png" data-wx>说清你的场地</a>', '首屏主按钮')
# 培训
sub('<a class="btn btn-led" href="#contact">预约开班</a>',
    '<a class="btn btn-led" href="assets/img/wechat-qr.png" data-wx>预约开班</a>', '培训预约')
# FAQ 侧栏
sub('<a class="btn btn-led" href="#contact">说清你的场地</a>',
    '<a class="btn btn-led" href="assets/img/wechat-qr.png" data-wx>说清你的场地</a>', 'FAQ 侧栏按钮')

# 联系区：加一个扫码入口（表单旁边两条路都留着）
sub('        <p class="contact-promise">全球交付 · 工作时间 30 分钟内回复</p>',
    '''        <p class="contact-promise">全球交付 · 工作时间 30 分钟内回复</p>
        <a class="contact-wx" href="assets/img/wechat-qr.png" data-wx>
          <span class="contact-wx-k">微信</span>
          <span class="contact-wx-d">扫码加微信，直接发场地照片和尺寸</span>
        </a>''',
    '联系区扫码入口')

print("[3] 插入二维码弹层")
dialog = '''
<dialog class="wx" id="wx-dialog" aria-labelledby="wx-title">
  <div class="wx-card">
    <button class="wx-close" type="button" aria-label="关闭二维码">
      <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false">
        <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      </svg>
    </button>
    <p class="wx-k">微信 · 落地组</p>
    <p class="wx-title" id="wx-title">扫码加微信，直接聊你的场地</p>
    <div class="wx-qr">
      <img src="assets/img/wechat-qr.png" width="720" height="720" alt="落地组微信二维码" decoding="async">
    </div>
    <p class="wx-hint">加好友时备注「G1 + 场地类型」，工作时间 30 分钟内回。</p>
    <a class="wx-alt" href="#contact" data-wx-close>不方便加微信？填一份需求表单 →</a>
  </div>
</dialog>
'''
assert "</body>" in h
h = h.replace("</body>", dialog.lstrip("\n") + "\n</body>", 1)
print("  ✓ 弹层已插入")

open(P_HTML, "w", encoding="utf-8").write(h)

# ---------------- CSS ----------------
c = open(P_CSS, encoding="utf-8").read()
css = '''
/* ================================================================
   微信二维码弹层
   ================================================================ */
.wx {
  width: min(92vw, 25rem);
  max-width: none;
  padding: 0;
  border: 0;
  background: transparent;
  color: var(--paper-ink);
}
.wx::backdrop {
  background: rgba(4, 6, 8, 0.84);
  backdrop-filter: blur(6px);
}
.wx-card {
  position: relative;
  padding: clamp(1.5rem, 4vw, 2rem) clamp(1.25rem, 3.5vw, 1.75rem) clamp(1.25rem, 3.5vw, 1.6rem);
  background: var(--paper);
  text-align: center;
}
.wx-close {
  position: absolute;
  top: 0.25rem;
  right: 0.25rem;
  display: grid;
  place-items: center;
  width: 2.75rem;
  height: 2.75rem;
  border: 0;
  background: transparent;
  color: var(--paper-soft);
  cursor: pointer;
}
.wx-close:hover { color: var(--paper-ink); }
.wx-k {
  font-size: var(--t-sm);
  letter-spacing: 0.1em;
  color: var(--paper-soft);
}
.wx-title {
  margin-top: 0.5rem;
  font-family: var(--font-display);
  font-size: var(--t-lg);
  font-weight: 400;
  line-height: 1.2;
  letter-spacing: -0.01em;
}
.wx-qr {
  width: min(56vw, 13.5rem);
  margin: 1.25rem auto 0;
  aspect-ratio: 1;
  background: #fff;
}
.wx-qr img { display: block; width: 100%; height: 100%; }
.wx-hint {
  margin-top: 1rem;
  font-size: var(--t-sm);
  line-height: 1.6;
  color: var(--paper-soft);
}
.wx-alt {
  display: inline-block;
  margin-top: 0.9rem;
  font-size: var(--t-sm);
  color: #0a5f8a;
  text-decoration: underline;
  text-underline-offset: 0.25em;
}

/* 联系区里的扫码入口 */
.contact-wx {
  display: inline-flex;
  align-items: baseline;
  gap: 0.6rem;
  margin-top: clamp(1.25rem, 3vw, 1.75rem);
  padding: 0.7rem 1rem;
  border-left: 3px solid var(--led);
  background: var(--panel);
  color: var(--ink);
  text-decoration: none;
  transition: background var(--d-hover) var(--ease);
}
.contact-wx:hover { background: var(--panel-2); }
.contact-wx-k { font-size: var(--t-sm); color: var(--led); letter-spacing: 0.08em; }
.contact-wx-d { font-size: var(--t-base); }
'''
if ".wx-card" not in c:
    c = c.rstrip() + "\n" + css
    open(P_CSS, "w", encoding="utf-8").write(c)
    print("  ✓ CSS 已追加")

# ---------------- JS ----------------
j = open(P_JS, encoding="utf-8").read()
js = '''
  /* ---------------- 6 · 微信二维码弹层 ---------------- */
  const wxDialog = document.getElementById('wx-dialog');
  if (wxDialog && typeof wxDialog.showModal === 'function') {
    // 没有弹层能力的环境下，这些 <a> 会退化成直接打开二维码图片 —— 不拦截
    $$('[data-wx]').forEach((a) => {
      a.addEventListener('click', (e) => {
        e.preventDefault();
        wxDialog.showModal();
      });
    });
    wxDialog.addEventListener('click', (e) => {
      if (e.target === wxDialog) wxDialog.close();   // 点遮罩关闭
    });
    $$('[data-wx-close]').forEach((a) => {
      a.addEventListener('click', () => wxDialog.close());
    });
  }
'''
if "wx-dialog" not in j:
    j = j.replace("  /* ---------------- 5 · 控件按下反馈 ---------------- */",
                  js.strip("\n") + "\n\n  /* ---------------- 5 · 控件按下反馈 ---------------- */", 1)
    open(P_JS, "w", encoding="utf-8").write(j)
    print("  ✓ JS 已插入")
print("\n改完。")
