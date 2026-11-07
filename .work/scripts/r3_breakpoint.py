import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="assets/css/site.css"; c=open(P,encoding="utf-8").read()

# 768 下联系区仍保持两列（文字 + 二维码并排），只有真正窄屏才堆叠
old = "  .contact-grid { grid-template-columns: 1fr; }"
assert old in c
c = c.replace(old, "  .contact-grid { grid-template-columns: minmax(0, 1fr) minmax(0, 14rem); }", 1)

# 760px 以下才堆叠
c = c.replace("""@media (max-width: 760px) {""",
"""@media (max-width: 760px) {
  .contact-grid { grid-template-columns: 1fr; }
  .contact-qr img { width: min(100%, 14rem); }""", 1)

open(P,"w",encoding="utf-8").write(c)
print("联系区断点已调整：1080–761 两列，760 以下堆叠")
