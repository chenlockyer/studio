import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p=open("REPORT.md",encoding="utf-8").read()
p=p.replace("## 10 · 第三轮修改（改名 / 只留微信 / 上线）","## 9 · 第三轮修改（改名 / 只留微信 / 上线）",1)
p=p.replace("## 9 · 还差你补的","## 10 · 还差你补的",1)
# 子标题编号同步
p=p.replace("### 10.1 名字","### 9.1 名字",1)
p=p.replace("### 10.2 删掉表单","### 9.2 删掉表单",1)
p=p.replace("### 10.3 视频长宽比","### 9.3 视频长宽比",1)
p=p.replace("### 10.4 手机首屏","### 9.4 手机首屏",1)
p=p.replace("### 10.5 上线","### 9.5 上线",1)
p=p.replace("见 8.1 的教训","见 8.1 的教训",1)
open("REPORT.md","w",encoding="utf-8").write(p)
print("章号已顺序化为 9 / 10")
