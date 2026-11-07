import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="index.html"; h=open(p,encoding="utf-8").read()

# 左栏把四步与「现场数据」合成一列，右栏竖版视频，避免左栏下方大片空白
old = """      <div class="navi-grid">
        <ol class="steps4 steps-col">"""
new = """      <div class="navi-grid">
        <div class="navi-left">
        <ol class="steps4 steps-col">"""
assert old in h
h = h.replace(old, new, 1)

old2 = """        </ol>

        <figure class="navi-video">"""
new2 = """        </ol>

        <p class="factline">
          <b>现场数据</b>　学院楼线：209 实验室、210 实验室、电梯口。3 个站点，直线 24 米。
        </p>
        </div>

        <figure class="navi-video">"""
assert old2 in h
h = h.replace(old2, new2, 1)

# 删掉原来位于栅格之后的 factline
old3 = """      <p class="factline">
        <b>现场数据</b>　学院楼线：209 实验室、210 实验室、电梯口。3 个站点，直线 24 米。
      </p>

      <div class="shots2">"""
new3 = """      <div class="shots2">"""
assert old3 in h
h = h.replace(old3, new3, 1)
open(p,"w",encoding="utf-8").write(h)
print("HTML：四步 + 现场数据合成左栏")

P="assets/css/site.css"; c=open(P,encoding="utf-8").read()
c = c.replace(""".navi-video > video {""",
""".navi-left {
  display: grid;
  gap: clamp(1.5rem, 3vw, 2.25rem);
  align-content: start;
}
.navi-left .steps4 { margin-bottom: 0; }
.navi-video > video {""",1)
c = c.replace("  grid-template-columns: minmax(0, 1fr) minmax(0, 22rem);",
              "  grid-template-columns: minmax(0, 1fr) minmax(0, 20rem);",1)
open(P,"w",encoding="utf-8").write(c)
print("CSS：左栏容器 + 视频收到 20rem")
