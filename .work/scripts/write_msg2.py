import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
msg = """文档：更新 README 与 REPORT（改名 / 去表单 / 上线）

- README 补线上地址、上线流程（master→origin/main 的 commit-tree 快进法）、
  新目录项（404.html / robots.txt / DEPLOY.md / .nojekyll）
- REPORT 新增第 9 章：改名会动字符集所以必须重建字体、删表单只留微信的取舍、
  视频长宽比 bug 的完整根因链（width/height 属性压过 aspect-ratio）、
  手机首屏改 16:9 视频带、GitHub Pages 子路径部署要点
"""
open(".work/commit-msg.txt","w",encoding="utf-8",newline="\n").write(msg)
