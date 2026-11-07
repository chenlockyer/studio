import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p=open("REPORT.md",encoding="utf-8").read()

anchor = "**教训**：`width`/`height` 属性与 `aspect-ratio` 同时存在时，属性会赢。要么把属性删掉，要么必须补 `height: auto`。"
assert anchor in p

add = anchor + """

### 9.3b 同一块视频的第二层原因：竖拍素材被压扁了

修完 CSS 之后你说「仍然是被压扁了一样」，再查发现是**编码阶段**的错，与 CSS 无关。

`导览\\导览投入使用.mp4` 与 `导览\\建图巡逻.mp4` 是**竖拍片**：容器元数据写的是 `1920×1080`，但流里带 −90° 旋转矩阵，解码后真实画面是 **1080×1920**（9:16）。ffmpeg 解码时会自动转正，`ffprobe` 只读容器，所以从参数上看不出来。

我的编码命令把解码后的 1080×1920 直接压进 1280×720，于是整幅画面横向拉宽、纵向压扁——人形机器人变成「矮胖」，LED 面罩压成扁椭圆。而容器又没写 SAR（`sample_aspect_ratio=N/A`），播放器按 1:1 解释，压扁就固化了。

逐条核对所有源的方向后确认：只有这两条是竖拍，其余（群控、江南、mimic、指挥家、全身运动控制…）方向都正常。

修法：

- `tour-live.mp4` 按它本来的 9:16 重编（720×1280，`scale=...:force_original_aspect_ratio=increase,crop=...` 加 `setsar=1`，取 28.0–33.0 s）
- 导览区块因此从「通栏 16:9 视频」改成「四步在左 + 竖版视频在右」，与动作区块左右镜像
- 编码后强制校验：`width/height` 与解码尺寸一致、SAR 必须 `1:1`

**教训**：`ffprobe` 报的 `width×height` 是**容器里存的编码尺寸**，不是**人眼看到的画面尺寸**。带旋转矩阵的手机视频两者正好相反。编码前必须先抽一帧确认实际方向，或者直接看 `stream_side_data.rotation`。"""
p = p.replace(anchor, add, 1)
open("REPORT.md","w",encoding="utf-8").write(p)
print("REPORT 9.3b 已补")
