import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="REPORT.md"; t=open(P,encoding="utf-8").read()
reps=[
 ("| `group-sync.mp4`（首屏） | `群控/群控.mp4` | 29.5s 起 9.0s | 1280×720 / 30fps / 718 KB |",
  "| `group-sync.mp4`（首屏） | `群控/群控.mp4` | **4.0s 起 9.0s** | 1280×720 / 30fps / 544 KB |"),
 ("| `group-ops.mp4`（群控区块） | `群控/群控.mp4` | 44.0s 起 8.0s | 1280×720 / 30fps / 607 KB |",
  "| `group-ops.mp4`（群控区块） | `群控/群控.mp4` | **16.5s 起 8.0s** | 1280×720 / 30fps / 540 KB |"),
 ("后来单独从 `群控.mp4` 44s 处另编了一段（画面里是 5 台机器人拉开站位 + 前景笔记本），重复感消除。",
  "后来单独从 `群控.mp4` 另编了一段（5 台机器人拉开站位 + 前景笔记本），重复感消除。\n第五轮按用户要求把两段都挪到母带**前半段**（首屏 4.0s、群控 16.5s）——后半段画面偏暗、构图被大机器人和手柄特写打断，做全屏背景不好看。"),
]
for a,b in reps:
    if a in t: t=t.replace(a,b,1); print("✅", a[:34])
open(P,"w",encoding="utf-8").write(t)
