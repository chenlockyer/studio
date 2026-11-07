import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="assets/css/site.css"; c=open(P,encoding="utf-8").read()
for line in ["  .faq-item summary { font-size: var(--t-base); padding: 0.95rem 1rem; }\n",
             "  .faq-item p { padding: 0 1rem 1.2rem; }\n"]:
    if line in c: c=c.replace(line,"",1); print("删:", line.strip())
open(P,"w",encoding="utf-8").write(c)
print("faq 残留：", c.count("faq"))

# ---------- JS ----------
P2="assets/js/site.js"; j=open(P2,encoding="utf-8").read()
old = """    '.course-spec', '.goals-k', '.goals-list li', '.caution',
    '.faq-item', '.faq-aside',
    '.contact-say > *', '.contact-qr',"""
new = """    '.course-spec', '.goals', '.goals-k', '.goals-list li', '.caution',
    '.contact-say > *', '.contact-qr',"""
assert old in j, "PARTS 不匹配"
j = j.replace(old, new, 1)

# 删掉问答单开互斥整段
import re
m = re.search(r"  /\* -+ 3 · 问答：同组只开一个 -+ \*/\n.*?\n\n", j, re.S)
assert m, "找不到问答逻辑"
j = j[:m.start()] + j[m.end():]
j = j.replace("/* ---------------- 4 · 微信二维码弹层 ---------------- */",
              "/* ---------------- 3 · 微信二维码弹层 ---------------- */",1)
j = j.replace("/* ---------------- 5 · 控件按下反馈 ---------------- */",
              "/* ---------------- 4 · 控件按下反馈 ---------------- */",1)
j = j.replace("$$('.btn, .faq-item summary')", "$$('.btn')",1)
open(P2,"w",encoding="utf-8").write(j)
print("\nJS 中 faq 残留：", j.count("faq"))
