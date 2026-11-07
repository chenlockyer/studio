import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
msg = """修：导览区块布局——左栏内容量配不上竖版视频，中间空一大块

竖版视频 19rem 撑出 540px 高，而左栏只有四步 + 一行现场数据（约 250px），
中间留了 290px 的空洞。

- 把两张软件界面截图从「栅格外的整行」并进左栏，放在四步与现场数据之间
- 左栏改成 align-content: start，与视频列同高（左 ~640 / 右 ~580）
- 视频宽度 22rem 收到 19rem
"""
open(".work/commit-msg.txt","w",encoding="utf-8",newline="\n").write(msg)
