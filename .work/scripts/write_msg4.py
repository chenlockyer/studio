import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
msg = """修：导览视频被压扁——竖拍素材编码时丢了方向

导览投入使用.mp4 是竖拍片：容器写 1920x1080，带 -90 度旋转矩阵，
解码后实际是 1080x1920。原来的编码把竖画面直接压进 1280x720，
整幅画面横向拉宽、纵向压扁，人形机器人变矮胖、LED 面罩变扁椭圆。

- tour-live.mp4 按原始 9:16 重编（720x1280，28.0-33.0s，setsar=1）
- 导览区块改成「四步 + 现场数据」在左、竖版视频在右，与动作区块左右镜像
- 编码后强制校验 width/height 与解码尺寸一致、SAR=1:1

四个视频渲染框现在与源比例完全一致：
  hero 1.778  navi 0.563  group 1.778  chain 0.563
"""
open(".work/commit-msg.txt","w",encoding="utf-8",newline="\n").write(msg)
