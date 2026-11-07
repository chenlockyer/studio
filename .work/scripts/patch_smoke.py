import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p=".work/scripts/smoke.mjs"; j=open(p,encoding="utf-8").read()
# 删掉 faq 检查块（FAQ 栏目已在第四轮删除）
m = re.search(r"\n\s*(?://\s*)?faq:\s*\(\)\s*=>\s*\{.*?\n\s*\},", j, re.S)
print("找到 faq 块：", bool(m))
if m:
    j = j[:m.start()] + "\n" + j[m.end():]
    open(p,"w",encoding="utf-8").write(j)
    print("✅ 已删")
else:
    # 打印附近内容便于定位
    i=j.find("faq")
    print(j[max(0,i-300):i+600])
