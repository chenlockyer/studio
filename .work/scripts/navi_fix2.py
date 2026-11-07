import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="assets/css/site.css"; c=open(P,encoding="utf-8").read()

old = """.navi-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 22rem);
  gap: clamp(1.5rem, 4vw, 3.5rem);
  align-items: start;
}
.navi-left {
  display: grid;
  gap: clamp(1.5rem, 3vw, 2.25rem);
  align-content: start;
}"""
new = """.navi-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 19rem);
  gap: clamp(1.5rem, 4vw, 3.5rem);
  align-items: stretch;      /* 左栏撑到与视频同高，底边才对得齐 */
}
.navi-left {
  display: grid;
  gap: clamp(1.5rem, 3vw, 2.25rem);
  align-content: space-between;   /* 四步在上，「现场数据」压到底 */
}"""
assert old in c, "navi-grid 块与预期不符"
c = c.replace(old, new, 1)
open(P,"w",encoding="utf-8").write(c)
print("✅ 已改：19rem 视频 + 左栏拉伸、现场数据贴底")
