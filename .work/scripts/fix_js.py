import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="assets/js/site.js"; s=open(p,encoding="utf-8").read()
old = """  const PARTS = [
    '.sec-head .h', '.sec-head .lead',
    '.media-wide', '.step', '.factline', '.shot',
    '.facts3 .fact', '.cmd-block', '.tagrow',
    '.dstep', '.handover', '.fig',
    '.course-photo', '.course-facts .cf', '.goals-k', '.goals-list li', '.caution',
    '.faq-item',
    '.contact-say > *', '.ask',
  ];"""
new = """  const PARTS = [
    '.sec-head .h', '.sec-head .lead',
    '.media-wide', '.chain-video', '.steps4 .step', '.facts3 .fact',
    '.cmd', '.tagrow',
    '.steps-d .dstep', '.handover', '.paper .fig',
    '.course-spec', '.goals-k', '.goals-list li', '.caution',
    '.faq-item', '.faq-aside',
    '.contact-say > *', '.ask',
  ];"""
assert old in s, "PARTS block not found"
s = s.replace(old, new, 1)
s = s.replace("落地组 · site-v4.js", "落地组 · site.js")
open(p,"w",encoding="utf-8").write(s)
print("site.js 的入场选择器已对齐当前 DOM")
