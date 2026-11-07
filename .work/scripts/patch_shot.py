import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p=".work/scripts/shot.mjs"; j=open(p,encoding="utf-8").read()
old = """  await evalJS(`window.scrollTo(0, ${y}); new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))`);
  await sleep(700);"""
new = """  await evalJS(`window.scrollTo(0, ${y}); new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))`);
  await sleep(700);
  // 强制落定入场动画，避免截图卡在渐变中间（布局验证用）
  await evalJS(`document.querySelectorAll('.rv').forEach(e => e.classList.add('is-in'))`);
  await sleep(450);"""
assert old in j
open(p,"w",encoding="utf-8").write(j.replace(old,new,1))
print("✅ shot.mjs 现在会强制落定 .rv")
