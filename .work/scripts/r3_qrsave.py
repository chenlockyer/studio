import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")

# ---------- HTML：加「保存二维码」入口（仅窄屏显示）----------
P="index.html"; h=open(P,encoding="utf-8").read()
old = '''        <figcaption>
          <p class="qr-k">扫一扫，加微信</p>
          <p class="qr-d">备注「G1 + 场地类型」。通过后把场地照片、尺寸和点位数量发过来就行。</p>
        </figcaption>'''
new = '''        <figcaption>
          <p class="qr-k">扫一扫，加微信</p>
          <p class="qr-d">备注「G1 + 场地类型」。通过后把场地照片、尺寸和点位数量发过来就行。</p>
          <a class="qr-save" href="assets/img/wechat-qr.png"
             download="宇树机器人实验室-微信二维码.png">手机上打不开扫码？保存图片，用微信「扫一扫 → 相册」识别</a>
        </figcaption>'''
assert old in h
h = h.replace(old, new, 1)

# 弹层里也加一份（手机点 CTA 弹出来时同样能存图）
old2 = '''        <p class="wx-hint">备注「G1 + 场地类型」，30 分钟内回。</p>'''
new2 = '''        <p class="wx-hint">备注「G1 + 场地类型」，30 分钟内回。</p>
        <a class="qr-save wx-save" href="assets/img/wechat-qr.png"
           download="宇树机器人实验室-微信二维码.png">手机上打不开扫码？保存图片，用微信「扫一扫 → 相册」识别</a>'''
assert old2 in h
h = h.replace(old2, new2, 1)
open(P,"w",encoding="utf-8").write(h)
print("HTML：已加两处保存二维码入口")

# ---------- CSS ----------
P2="assets/css/site.css"; c=open(P2,encoding="utf-8").read()
c = c.replace(""".qr-d { margin-top: 0.3rem;""",
""".qr-save {
  display: none;
  margin-top: 0.55rem;
  font-size: var(--t-sm);
  line-height: 1.55;
  color: var(--led);
  text-decoration: underline;
  text-underline-offset: 3px;
  max-width: 24ch;
}
@media (max-width: 760px) {
  .qr-save { display: block; }
}
.qr-d { margin-top: 0.3rem;""", 1)
open(P2,"w",encoding="utf-8").write(c)
print("CSS：.qr-save 已加（≤760px 才显示）")
