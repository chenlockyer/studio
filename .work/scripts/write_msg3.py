import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
msg = """仓库瘦身：.work 中间产物不再入库也不再公开

GitHub Pages 会把仓库里所有文件按原样对外提供，之前 .work/ 被跟踪，
导致 .work/fonts/NotoSansSC-400.ttf（10.6 MB）这类内部文件能被公开访问，
仓库树 39.4 MB。

- .gitignore 改为只放行 .work/scripts/（可复现的管线脚本）与 .work/source-img/（不可再生的原始界面截图）
- 从索引移除 50 个中间产物：3 个 Noto 母版 TTF（31.7 MB）、抽帧 PNG、trial woff2、日志与临时 JSON
- 本地文件全部保留在工作区，脚本仍可直接运行

仓库树 39.4 MB → 5.5 MB，文件数 207 → 166。
"""
open(".work/commit-msg.txt","w",encoding="utf-8",newline="\n").write(msg)
print("head:", open(".work/commit-msg.txt","rb").read(3))
