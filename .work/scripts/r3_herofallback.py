import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="assets/css/site.css"; c=open(P,encoding="utf-8").read()

# 首帧兜底：把海报铺成 .hero-media 的背景。视频还没解码出来时首屏就不是黑的。
old = ".hero-media { position: absolute; inset: 0; z-index: -1; }"
new = """/* 首帧兜底：视频解码前先用海报顶上，慢网下首屏不会是一块黑 */
.hero-media {
  position: absolute;
  inset: 0;
  z-index: -1;
  background: var(--ground) url("../img/og.jpg") center 32% / cover no-repeat;
}"""
assert old in c
c = c.replace(old, new, 1)

old2 = "  .hero-video { object-position: center 26%; }"
assert old2 in c
c = c.replace(old2, "  .hero-video { object-position: center 26%; }\n  .hero-media { background-position: center 26%; }", 1)

open(P,"w",encoding="utf-8").write(c)
print("已给 .hero-media 加海报底图")
