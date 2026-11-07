import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="assets/css/site.css"; c=open(p,encoding="utf-8").read()

# 1) 平板 768：指令表改单列 + 导览四步改 2×2，避免挤成竖条
old="""  .nav { display: none; }
  .btn-bar { margin-left: auto; }"""
new="""  .nav { display: none; }
  .btn-bar { margin-left: auto; }
  .cmd { grid-template-columns: 1fr; }
  .steps4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }"""
assert old in c; c=c.replace(old,new,1)

# 2) 清掉已删除结构残留的规则（course-grid / course-facts / course-photo / cf* / dstep-n）
drop_lines = [
 "  .course-grid { grid-template-columns: 1fr; }",
 "  .course-facts { grid-template-columns: repeat(3, minmax(0, 1fr)); }",
 "  .cf-n { font-size: var(--t-md); }",
 "  .cf-wide { grid-column: auto; }",
 "  .course-facts { grid-template-columns: 1fr 1fr; }",
 "  .cf-wide { grid-column: 1 / -1; }",
]
removed=0
for d in drop_lines:
    if d in c:
        c=c.replace(d+"\n","",1); removed+=1

# 多行规则块：以选择器开头的整段
blocks = [
 ".course-grid {", ".course-facts {", ".cf-wide {", ".course-photo {",
 ".cf {", ".cf-n {", ".cf-t {", ".dstep-n {",
]
lines=c.split("\n"); out=[]; i=0; n=len(lines)
while i<n:
    ln=lines[i]
    s=ln.strip()
    if any(s.startswith(b) for b in blocks):
        depth=0; started=False
        while i<n:
            depth += lines[i].count("{") - lines[i].count("}")
            if "{" in lines[i]: started=True
            i+=1
            if started and depth<=0: break
        removed+=1
        continue
    out.append(ln); i+=1
c="\n".join(out)
open(p,"w",encoding="utf-8").write(c)
print(f"清理规则 {removed} 处；剩余 .course-* 出现 {c.count('.course-')} 次，.cf 出现 {len(re.findall(r'\.cf[ .{-]', c))} 次")
