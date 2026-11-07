import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="index-v4.html"; h=open(p,encoding="utf-8").read()
old = '''          </picture>
          <figcaption>课程在真实设备和真实场地里进行，不是投影演示。</figcaption>
        </figure>'''
new = '''          </picture>
        </figure>'''
assert old in h
h=h.replace(old,new,1)
open(p,"w",encoding="utf-8").write(h)
print("移除培训照片说明（与导语重复）")
