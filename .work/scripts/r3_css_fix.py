import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="assets/css/site.css"; c=open(P,encoding="utf-8").read()
bad = "/* 表单：手动复制回退（file:// 或非 HTTPS 时剪贴板不可用） */\n.ask-fallback \n"
if bad in c:
    c = c.replace(bad, "", 1)
    print("  已清除残留注释与孤立选择器")
else:
    # 兜底：按行删
    lines = c.split("\n")
    keep = [l for l in lines if l.strip() != ".ask-fallback" and "表单：手动复制回退" not in l]
    print(f"  兜底按行清理：{len(lines)} → {len(keep)} 行")
    c = "\n".join(keep)
open(P,"w",encoding="utf-8").write(c)
print("  剩余 .ask:", c.count(".ask"), " .field:", c.count(".field"))
