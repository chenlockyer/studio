import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="index.html"; h=open(P,encoding="utf-8").read()

# ---------- 1) 联系区：加「保存二维码」入口 ----------
old = '''          <p class="qr-d">备注「G1 + 场地类型」。通过后把场地照片、尺寸和点位数量发过来就行。</p>
        </figcaption>'''
new = '''          <p class="qr-d">备注「G1 + 场地类型」。通过后把场地照片、尺寸和点位数量发过来就行。</p>
          <a class="qr-save" href="assets/img/wechat-qr.png"
             download="宇树机器人实验室-微信二维码.png">手机上扫不了自己的屏？保存图片，微信「扫一扫 → 相册」识别</a>
        </figcaption>'''
assert old in h, "figcaption 未命中"
h = h.replace(old, new, 1)

# ---------- 2) 弹层：删掉「填一份需求表单」（表单已不存在），换成保存入口 ----------
old2 = '''    <a class="wx-alt" href="#contact" data-wx-close>不方便加微信？填一份需求表单 →</a>'''
new2 = '''    <a class="qr-save wx-save" href="assets/img/wechat-qr.png"
       download="宇树机器人实验室-微信二维码.png">手机上扫不了自己的屏？保存图片，微信「扫一扫 → 相册」识别</a>
    <a class="wx-alt" href="#figs" data-wx-close>先看看我们交付过什么 →</a>'''
assert old2 in h, "wx-alt 未命中"
h = h.replace(old2, new2, 1)

open(P,"w",encoding="utf-8").write(h)
print("HTML 已更新")
print("  「填一份需求表单」剩余:", h.count("填一份需求表单"))
print("  .qr-save 出现:", h.count("qr-save"))
