import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="index.html"; h=open(p,encoding="utf-8").read()

# 把两张界面截图从「栅格外的整行」挪进左栏，让左栏内容量配得上竖版视频的高度
m = re.search(r'(      <div class="shots2">.*?</div>\n)', h, re.S)
assert m, "找不到 shots2 块"
shots = m.group(1)
assert "navi-home" in shots
h = h.replace(shots, "", 1)                      # 先从原位移除

anchor = """        <p class="factline">
          <b>现场数据</b>　学院楼线：209 实验室、210 实验室、电梯口。3 个站点，直线 24 米。
        </p>
        </div>"""
assert anchor in h, "找不到左栏结尾"
# 缩进两格塞进左栏，放在现场数据之前
shots_indented = "\n".join("  " + ln if ln.strip() else ln for ln in shots.rstrip("\n").split("\n")) + "\n"
new_anchor = shots_indented + anchor
h = h.replace(anchor, new_anchor, 1)
open(p,"w",encoding="utf-8").write(h)
print("✅ HTML：两张界面截图已并入左栏")

P="assets/css/site.css"; c=open(P,encoding="utf-8").read()
old = """.navi-left {
  display: grid;
  gap: clamp(1.5rem, 3vw, 2.25rem);
  align-content: space-between;   /* 四步在上，「现场数据」压到底 */
}"""
new = """.navi-left {
  display: grid;
  gap: clamp(1.5rem, 3vw, 2.25rem);
  align-content: start;
}
.navi-left .shots2 { margin-top: 0; }"""
assert old in c
c = c.replace(old, new, 1)
open(P,"w",encoding="utf-8").write(c)
print("✅ CSS 已同步")
