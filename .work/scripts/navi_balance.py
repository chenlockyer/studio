import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="assets/css/site.css"; c=open(P,encoding="utf-8").read()
c=c.replace("""  grid-template-columns: minmax(0, 1fr) minmax(0, 20rem);
  gap: clamp(1.5rem, 4vw, 3.5rem);
  align-items: start;
}
.navi-left {
  display: grid;
  gap: clamp(1.5rem, 3vw, 2.25rem);
  align-content: start;
}""","""  grid-template-columns: minmax(0, 1fr) minmax(0, 20rem);
  gap: clamp(1.5rem, 4vw, 3.5rem);
  align-items: stretch;
}
/* 左栏撑到与视频同高：四步在上，「现场数据」压到底边，空出来的那截就不会显成缺口 */
.navi-left {
  display: grid;
  gap: clamp(1.5rem, 3vw, 2.25rem);
  align-content: space-between;
}""",1)
open(P,"w",encoding="utf-8").write(c)
print("已让左栏与视频等高，现场数据贴底")
