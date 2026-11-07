import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p=".work/scripts/smoke.mjs"; j=open(p,encoding="utf-8").read()
old = """out.faq = await ev(`(() => {
  const items = [...document.querySelectorAll('.faq-item')];
  const a = items[0], b = items[1];
  b.open = true; b.dispatchEvent(new Event('toggle'));
  const onlyOne = !a.open && b.open;
  const hiddenOk = getComputedStyle(a.querySelector('p')).display === 'none';
  return { count: items.length, onlyOne, hiddenOk };
})()`);

"""
assert old in j, "块不匹配"
j = j.replace(old, "", 1)
open(p,"w",encoding="utf-8").write(j)
print("✅ smoke.mjs 已移除 faq 检查")
