import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
g=open(".gitignore",encoding="utf-8").read()
add = """
# 部署产物与工具（由脚本生成，不入库）
dist/
.work/tools/
.work/deliver/
.wrangler/
node_modules/
"""
if "dist/" not in g:
    g = g.rstrip("\n") + "\n" + add
    open(".gitignore","w",encoding="utf-8").write(g)
    print("已补充 .gitignore")
else:
    print("已存在")
