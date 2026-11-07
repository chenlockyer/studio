import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="assets/js/site.js"; j=open(P,encoding="utf-8").read()

# 1) 站名
j=j.replace("   落地组 · site.js","   宇树机器人实验室 · site.js",1)

# 2) 入场清单里把 .ask 换成 .contact-qr
j=j.replace("    '.contact-say > *', '.ask',","    '.contact-say > *', '.contact-qr',",1)

# 3) 整段删掉表单逻辑（第 4 节）
start = j.find("  /* ---------------- 4 · 表单：复制成一段话，不做假提交 ---------------- */")
end   = j.find("  /* ---------------- 6 · 微信二维码弹层 ---------------- */")
assert start > 0 and end > start, (start, end)
j = j[:start] + j[end:]

# 4) 重新编号注释
j=j.replace("/* ---------------- 6 · 微信二维码弹层 ---------------- */",
            "/* ---------------- 4 · 微信二维码弹层 ---------------- */",1)
j=j.replace("/* ---------------- 5 · 控件按下反馈 ---------------- */",
            "/* ---------------- 5 · 控件按下反馈 ---------------- */",1)

# 5) 顶部说明同步（不再有「可复制」这条能力）
j=j.replace("全部是增强：关掉脚本，页面仍然完整可读、可导航、可复制。",
            "全部是增强：关掉脚本，页面仍然完整可读、可导航。",1)

open(P,"w",encoding="utf-8").write(j)
print("site.js 改造完成")
print("  剩余 ask-form:", j.count("ask-form"), " ask-hint:", j.count("ask-hint"))
print("  行数:", len(j.split(chr(10))))
