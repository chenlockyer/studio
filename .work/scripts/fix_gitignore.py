import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p=".gitignore"
s=open(p,encoding="utf-8").read()
s=s.replace(".work/source-img/*.png\n","")
s=s.replace(".work/**/*.png\n", "!.work/source-img/\n.work/**/*.png\n")
open(p,"w",encoding="utf-8").write(s.rstrip()+"\n")
print(open(p,encoding="utf-8").read())
