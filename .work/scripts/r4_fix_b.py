import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="assets/css/site.css"; c=open(P,encoding="utf-8").read()
old = """.goals-list b {
  color: var(--paper-ink);
  font-weight: 700;
}"""
new = """.goals-list b {
  color: var(--ink);          /* 课程安排里的日期标签 —— 深色底上必须用 ink，不是 paper-ink */
  font-weight: 700;
}"""
assert old in c
open(P,"w",encoding="utf-8").write(c.replace(old,new,1))
print("✅ .goals-list b 改用 --ink")
