import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
# 让弹层本身接住初始焦点，关闭按钮的焦点环只在键盘 Tab 时出现
p="index.html"; h=open(p,encoding="utf-8").read()
h=h.replace('<dialog class="wx" id="wx-dialog" aria-labelledby="wx-title">',
            '<dialog class="wx" id="wx-dialog" tabindex="-1" aria-labelledby="wx-title">',1)
open(p,"w",encoding="utf-8").write(h)

p2="assets/css/site.css"; c=open(p2,encoding="utf-8").read()
c=c.replace(""".wx::backdrop {""",
""".wx:focus { outline: none; }
.wx::backdrop {""",1)
open(p2,"w",encoding="utf-8").write(c)

p3="assets/js/site.js"; j=open(p3,encoding="utf-8").read()
j=j.replace("""        e.preventDefault();
        wxDialog.showModal();""",
"""        e.preventDefault();
        wxDialog.showModal();
        wxDialog.focus();          // 焦点落在弹层本身，关闭按钮的焦点环只在键盘 Tab 时出现""",1)
open(p3,"w",encoding="utf-8").write(j)
print("已调整初始焦点")
