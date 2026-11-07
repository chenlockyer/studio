import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="index.html"; s=open(p,encoding="utf-8").read()
s=s.replace("动作定制,深圳机器人,师资培训","动作定制,机器人全球交付,师资培训")
open(p,"w",encoding="utf-8").write(s)
print("keywords 已改")
