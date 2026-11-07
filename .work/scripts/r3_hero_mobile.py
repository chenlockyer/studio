import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="assets/css/site.css"; c=open(P,encoding="utf-8").read()

old = """  .hero {
    min-height: 94svh;
    padding-top: calc(var(--pad) + 4.5rem);
    padding-bottom: 2.75rem;
  }
  .hero-video { object-position: center 26%; }
  .hero-media { background-position: center 26%; }"""
new = """  /* 手机上不再把 16:9 画面裁进竖框（横向会被裁掉 72% 且糊）；改成整块 16:9 视频带 + 下方文字 */
  .hero {
    min-height: auto;
    display: block;
    padding-top: 3.6rem;
    padding-bottom: 2.75rem;
  }
  .hero-media {
    position: relative;
    inset: auto;
    z-index: auto;
    aspect-ratio: 16 / 9;
    margin-inline: calc(-1 * var(--pad));
    background-position: center 42%;
  }
  .hero-video { object-position: center 42%; }
  .hero-scrim { display: none; }
  .hero-inner { padding-top: 1.35rem; }"""
assert old in c, "still not found"
c = c.replace(old, new, 1)
open(P,"w",encoding="utf-8").write(c)
print("已改：≤760 首屏改为 16:9 视频带 + 下方文字")
