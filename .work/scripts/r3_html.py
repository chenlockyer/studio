import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
P = "index.html"
h = open(P, encoding="utf-8").read()
n = 0

def sub(old, new, count=1, label=""):
    global h, n
    if old not in h:
        print(f"  ✗ 未命中: {label or old[:50]!r}")
        return False
    h = h.replace(old, new, count)
    n += 1
    return True

# ---------- 1) 站名：落地组 → 宇树机器人实验室 ----------
sub("<title>落地组 · 宇树 G1 机器人落地交付｜场馆导览 · 多机群控 · 动作定制</title>",
    "<title>宇树机器人实验室 · 宇树 G1 机器人落地交付｜场馆导览 · 多机群控 · 动作定制</title>",
    label="title")
sub('<meta property="og:title" content="落地组 · 宇树 G1 机器人落地交付">',
    '<meta property="og:title" content="宇树机器人实验室 · 宇树 G1 机器人落地交付">',
    label="og:title")
sub('<span class="wm">落地组</span>', '<span class="wm">宇树机器人实验室</span>', label="wordmark")
sub('<p class="foot-name">落地组</p>', '<p class="foot-name">宇树机器人实验室</p>', label="foot-name")
sub('<p class="wx-k">微信 · 落地组</p>', '<p class="wx-k">微信 · 宇树机器人实验室</p>', label="wx-k")
sub('alt="落地组微信二维码"', 'alt="宇树机器人实验室微信二维码，扫码加微信"', label="qr alt")

# ---------- 2) 联系区：删表单，改二维码为主 ----------
old_form_start = '      <form class="ask" id="ask-form" novalidate>'
i = h.find(old_form_start)
assert i > 0, "找不到表单起始"
j = h.find('</form>\n', i)
assert j > 0, "找不到表单结束"
old_block = h[i:j+len('</form>\n')]
new_block = '''      <figure class="contact-qr">
        <img src="assets/img/wechat-qr.png" width="720" height="720"
             alt="宇树机器人实验室微信二维码，扫码即可加微信" decoding="async">
        <figcaption>
          <p class="qr-k">扫一扫，加微信</p>
          <p class="qr-d">备注「G1 + 场地类型」。通过后把场地照片、尺寸和点位数量发过来就行。</p>
        </figcaption>
      </figure>
'''
h = h[:i] + new_block + h[j+len('</form>\n'):]
n += 1
print("  ✓ 表单已替换为二维码面板")

# 左侧文案：明确「不用填表」，并移除已删除的 .contact-wx 入口
sub('''        <p class="contact-sub">
          先不报价。告诉我们场地情况，我们给出设备数量、站点规划、上线周期和交付清单。
        </p>''',
    '''        <p class="contact-sub">
          不用填表。加微信，把场地照片和尺寸发过来，我们给出设备数量、站点规划、上线周期和交付清单。
        </p>''', label="contact-sub")
sub('''        <a class="contact-wx" href="assets/img/wechat-qr.png" data-wx>
          <span class="contact-wx-k">微信</span>
          <span class="contact-wx-d">扫码加微信，直接发场地照片和尺寸</span>
        </a>
''', '', label="contact-wx 删除")

open(P, "w", encoding="utf-8").write(h)
print(f"\nindex.html 共替换 {n} 处")
print("剩余「落地组」:", h.count("落地组"))
print("剩余 <form:", h.count("<form"), " ask-form:", h.count("ask-form"))
