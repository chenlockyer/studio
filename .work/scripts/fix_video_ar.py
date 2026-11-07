import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="assets/css/site.css"; c=open(P,encoding="utf-8").read()

# 根因：<video width height> 是表现性提示，会把高度钉死，aspect-ratio 失效
old1 = """.media-wide video {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;"""
new1 = """.media-wide video {
  width: 100%;
  height: auto;          /* 必须写：<video width height> 属性会把高度钉死，aspect-ratio 就失效了 */
  aspect-ratio: 16 / 9;
  object-fit: cover;"""
assert old1 in c
c = c.replace(old1, new1, 1)

old2 = """.chain-video > video {
  display: block;
  width: 100%;
  aspect-ratio: 9 / 16;
  object-fit: cover;"""
new2 = """.chain-video > video {
  display: block;
  width: 100%;
  height: auto;          /* 同上 */
  aspect-ratio: 9 / 16;
  object-fit: cover;"""
assert old2 in c
c = c.replace(old2, new2, 1)

open(P,"w",encoding="utf-8").write(c)
print("已给两处 video 加 height:auto")
