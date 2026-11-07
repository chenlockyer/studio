import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
c=open("assets/css/site.css",encoding="utf-8").read()
for key in [".goals {", ".goals-k", ".goals-list", ".course-spec {", ".caution {"]:
    i=c.find(key)
    if i<0: print(key,"NOT FOUND"); continue
    print("-----", key)
    print(c[i:i+420])
