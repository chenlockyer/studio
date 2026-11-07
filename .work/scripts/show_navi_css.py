import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
c=open("assets/css/site.css",encoding="utf-8").read()
i=c.find(".navi-grid")
print(c[i-120:i+900])
