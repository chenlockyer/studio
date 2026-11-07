import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
msg = """第四轮：删常见问题栏目 / 课程改成「具身智能实战课程」/ 师资培训→线下教培

- 删掉整个常见问题栏目（导航项、section、.faq-* CSS 约 2KB、JS 单开互斥 20 行）
- 课程区块改成课程的样子：h2「具身智能实战课程」，加「课程安排」四段
  （第一天上午/下午、第二天上午/下午），日期标签用 ink 色加粗
- 师资培训 → 线下教培（meta、导航、页脚、区块注释共 4 处）
- 联系区删掉「不用填表。」；课程区删掉「也可安排上门授课，设备由我们携带。」
- 文案变了，重建字体子集：231.4 KB（原 252.9），页面 506 字零缺字
- 顺带修 shot.mjs：截图前强制落定入场动画，避免截到渐变中间

inspect 0 FAIL / 0 WARN；lint 0/0；smoke 4 段视频 ready=4、锚点 9/0 缺失、
横向溢出 0、破图 0、控制台 0 条。页面 12.1 → 9 屏。
"""
open(".work/commit-msg.txt","w",encoding="utf-8",newline="\n").write(msg)
