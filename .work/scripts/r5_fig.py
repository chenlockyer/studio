import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="index.html"; h=open(p,encoding="utf-8").read()
a='<dd class="fig-n">24<span class="fig-u">米</span></dd>'
b='<dd class="fig-n">240<span class="fig-u">米</span></dd>'
assert a in h
open(p,"w",encoding="utf-8").write(h.replace(a,b,1))
print("✅ 交付实绩大数字 24 → 240")
