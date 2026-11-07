import re,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
h=open("index.html",encoding="utf-8").read()
for cls in ["media-wide","chain-video","steps4","facts3","cmd","tagrow","steps-d","dstep","handover","paper","fig","course-spec","goals-k","goals-list","caution","faq-item","faq-aside","contact-say","ask"]:
    n=len(re.findall(r'class="[^"]*\b'+re.escape(cls)+r'\b', h))
    print(f"  .{cls:14s} {n}")
