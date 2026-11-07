import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
P = "assets/css/site.css"
c = open(P, encoding="utf-8").read()
orig_len = len(c)

# ---------- A. 删除表单与旧微信入口的全部规则 ----------
drop_patterns = [
    r"\.ask \{[^}]*\}\n",
    r"\.field \{ [^}]*\}\n",
    r"\.field-label \{[^}]*\}\n",
    r"\.field input, \.field select \{[^}]*\}\n",
    r"\.field input:hover, \.field select:hover \{[^}]*\}\n",
    r"\.field input::placeholder \{[^}]*\}\n",
    r"\.btn-dark \{[^}]*\}\n",
    r"\.btn-dark:hover \{[^}]*\}\n",
    r"\.ask-hint \{[^}]*\}\n",
    r"\.ask-fallback \{[^}]*\}\n",
    r"\.ask-fallback\[hidden\] \{[^}]*\}\n",
    r"\.ask-fallback \.field-label \{[^}]*\}\n",
    r"\.ask-fallback textarea \{[^}]*\}\n",
    r"\.contact-wx \{[^}]*\}\n",
    r"\.contact-wx:hover \{[^}]*\}\n",
    r"\.contact-wx-k \{[^}]*\}\n",
    r"\.contact-wx-d \{[^}]*\}\n",
]
removed = 0
for p in drop_patterns:
    new_c, k = re.subn(p, "", c, flags=re.S)
    if k:
        c = new_c
        removed += k
print(f"  删掉 {removed} 条规则")

# @media 内的单行覆盖
c, k1 = re.subn(r"\n  \.ask \{ max-width: 34rem; \}", "", c)
print(f"  删掉 @media 内 .ask 覆盖 {k1} 条")

# ---------- B. 联系区两列比例：QR 列收窄到二维码宽度 ----------
c = c.replace(
    "  grid-template-columns: minmax(0, 1fr) minmax(0, 30rem);\n  gap: clamp(1.5rem, 4vw, 4rem);",
    "  grid-template-columns: minmax(0, 1fr) minmax(0, 18rem);\n  gap: clamp(2rem, 5vw, 5rem);", 1)

# ---------- C. 新增二维码面板样式 ----------
anchor = ".contact-promise {"
qr_css = '''.contact-qr {
  margin: 0;
  display: grid;
  gap: clamp(0.9rem, 1.8vw, 1.2rem);
  justify-items: start;
}
.contact-qr img {
  display: block;
  width: min(100%, 16rem);
  height: auto;
  padding: 0.55rem;
  background: #fff;
}
.qr-k { font-size: var(--t-md); font-weight: 700; line-height: 1.3; }
.qr-d { margin-top: 0.3rem; font-size: var(--t-sm); line-height: 1.6; color: var(--soft); max-width: 26ch; }

'''
assert anchor in c
c = c.replace(anchor, qr_css + anchor, 1)

open(P, "w", encoding="utf-8").write(c)
print(f"\nsite.css {orig_len} → {len(c)} 字节")
for probe in [".ask", ".field", ".btn-dark", ".contact-wx", ".contact-qr", ".qr-k"]:
    print(f"  {probe:14s} 出现 {c.count(probe)} 次")
