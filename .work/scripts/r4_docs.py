import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")

# ---------- README ----------
P="README.md"; r=open(P,encoding="utf-8").read()
reps = [
 ("| `#course` | 师资培训 | 2 天 12 学时规格条 + 七项结业验收 |\n"
  "| `#faq` | 常见问题 | 10 条真实问答（`<details>`，单开互斥） |\n"
  "| `#contact` | 联系 | 微信扫码入口 + 四项表单，一键合成一段话复制到剪贴板 |",
  "| `#course` | 线下教培 | 具身智能实战课程：2 天 12 学时规格条 + 课程安排 + 七项结业验收 |\n"
  "| `#contact` | 联系 | 微信二维码 + 「加微信，把场地照片和尺寸发过来」 |"),
 ("| 常见问题 | `<details>` 单开互斥 |\n", ""),
 ("把 `.wm-sub` / FAQ 最后一条 / 页脚「现场」列改回去",
  "把 `.wm-sub` / 页脚「现场」列改回去"),
]
for a,b in reps:
    if a in r:
        r=r.replace(a,b,1); print("README 改：", a.split("\n")[0][:40])
open(P,"w",encoding="utf-8").write(r)

# ---------- REPORT ----------
P2="REPORT.md"; t=open(P2,encoding="utf-8").read()
t = t.replace("| `lopsided` | 常见问题区右侧留 712px 空白 | 改成两列：左问答列表 + 右 sticky 的「没找到你的问题？」卡片 |",
              "| `lopsided` | 常见问题区右侧留 712px 空白 | 当时改成两列：左问答列表 + 右 sticky 卡片（该栏目第四轮已按要求整块删除） |")
t = t.replace("- **问答**：`<details>` 原生折叠，JS 只加\"同组只开一个\"",
              "- ~~**问答**~~：第四轮按要求删除整个栏目（导航项、`<details>` 互斥逻辑、CSS 一并清掉）")
t = t.replace("问答 10 条 / 单开互斥 OK / 折叠项 display:none OK",
              "问答栏目已删除（第四轮）")
t = t.replace("页头「获取方案」、首屏「说清你的场地」、培训「预约开班」、问答侧栏四处按钮，点开同一个原生 `<dialog>` 弹层展示二维码",
              "页头「获取方案」、首屏「说清你的场地」、培训「预约开班」三处按钮，点开同一个原生 `<dialog>` 弹层展示二维码（问答侧栏那个随栏目一起删了）")
open(P2,"w",encoding="utf-8").write(t)
print("✅ REPORT 已同步")
