import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
msg = """修：视频长宽比 + 手机首屏不再裁切

- <video width height> 属性是表现性提示，会把高度钉死，导致 aspect-ratio 失效；
  .media-wide video 与 .chain-video > video 补 height:auto，三处视频恢复真实比例
  （navi/group 16:9，chain 9:16）。桌面端此前「看着正常」只是容器宽度恰好等于 720 的巧合。
- 手机首屏改为整块 16:9 视频带 + 下方文字，不再把 16:9 裁进竖框（原横向裁掉 72%）。
"""
open(".work/commit-msg.txt","w",encoding="utf-8",newline="\n").write(msg)
print("msg bytes head:", open(".work/commit-msg.txt","rb").read(3))
