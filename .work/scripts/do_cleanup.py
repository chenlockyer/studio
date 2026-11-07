import os,shutil,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
os.chdir(r"D:\code\unitree-site")
os.makedirs(".work/source-img",exist_ok=True)
pngs=["导览-准备页面.png","导览主页面.png","支持自定义舞蹈队列一键下发.png","群控-主页面.png","群控-官方舞蹈页面.png","群控-自定义按键.png"]
for p in pngs:
    src=os.path.join("assets/img",p)
    if os.path.isfile(src):
        shutil.move(src, os.path.join(".work/source-img",p)); print("存档原图:",p)
drop=[l for l in open(".work/drop-list.txt",encoding="utf-8").read().splitlines() if l.strip()]
n=0; freed=0
for f in drop:
    if not os.path.isfile(f): continue
    freed+=os.path.getsize(f); os.remove(f); n+=1
print(f"\n删除 {n} 个文件，释放 {freed/1024/1024:.2f} MB")
# 删掉空的旧目录
for d in ("assets/img/opt","assets/img/v3","assets/img/v3boot","assets/img/still","assets/video/v3","assets/video/v3boot","assets/video/opt","assets/fonts/v3"):
    if os.path.isdir(d) and not os.listdir(d): os.rmdir(d); print("删空目录:",d)
