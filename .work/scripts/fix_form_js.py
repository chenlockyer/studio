import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")

# ---- JS：复制失败时显示可手动复制的文本框并自动全选 ----
p="assets/js/site.js"; s=open(p,encoding="utf-8").read()
old = """  const form = document.getElementById('ask-form');
  const hint = document.getElementById('ask-hint');
  if (form && hint) {
    const DEFAULT_HINT = hint.textContent.trim();
"""
new = """  const form = document.getElementById('ask-form');
  const hint = document.getElementById('ask-hint');
  const fallback = document.getElementById('ask-fallback');
  const briefBox = document.getElementById('ask-brief');
  if (form && hint) {
    const DEFAULT_HINT = hint.textContent.trim();
"""
assert old in s
s = s.replace(old, new, 1)

old2 = """      try {
        await navigator.clipboard.writeText(brief);
        hint.textContent = `已复制：${brief.replace(/\\n/g, ' · ')}`;
      } catch {
        hint.textContent = `复制没成功，请手动复制这段：${brief.replace(/\\n/g, ' · ')}`;
      }"""
new2 = """      const showFallback = () => {
        if (!fallback || !briefBox) return;
        briefBox.value = brief;
        fallback.hidden = false;
        briefBox.focus();
        briefBox.select();
      };

      try {
        await navigator.clipboard.writeText(brief);
        hint.textContent = '已复制。直接粘贴到微信发给我们即可。';
        if (fallback) fallback.hidden = true;
      } catch {
        // file:// 打开或非 HTTPS 时剪贴板接口不可用：给一段可全选的手动复制文本
        hint.textContent = '这段需求已经生成，全选下面内容复制即可。';
        showFallback();
      }"""
assert old2 in s
s = s.replace(old2, new2, 1)

old3 = """    form.addEventListener('reset', () => { hint.textContent = DEFAULT_HINT; });"""
new3 = """    form.addEventListener('reset', () => {
      hint.textContent = DEFAULT_HINT;
      if (fallback) fallback.hidden = true;
    });"""
assert old3 in s
s = s.replace(old3, new3, 1)

open(p,"w",encoding="utf-8").write(s)
print("site.js 复制回退逻辑已更新")

# ---- CSS：回退文本框样式 ----
p2="assets/css/site.css"; c=open(p2,encoding="utf-8").read()
add = """
/* 表单：手动复制回退（file:// 或非 HTTPS 时剪贴板不可用） */
.ask-fallback { display: block; margin-top: 0.75rem; }
.ask-fallback[hidden] { display: none; }
.ask-fallback .field-label { display: block; margin-bottom: 0.375rem; }
.ask-fallback textarea {
  width: 100%;
  padding: 0.75rem 0.875rem;
  border: 1px solid rgba(10, 12, 14, 0.22);
  border-radius: 2px;
  background: #fff;
  color: var(--ink-on-paper);
  font: inherit;
  font-size: var(--t-sm);
  line-height: 1.6;
  resize: vertical;
}
"""
if ".ask-fallback" not in c:
    c = c.rstrip() + "\n" + add
    open(p2,"w",encoding="utf-8").write(c)
    print("CSS 已加 .ask-fallback 样式")
else:
    print("CSS 已存在 .ask-fallback，跳过")
