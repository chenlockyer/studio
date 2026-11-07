import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P=".work/scripts/smoke.mjs"; s=open(P,encoding="utf-8").read()

old = """out.form = await ev(`(async () => {
  const f = document.getElementById('ask-form');
  f.querySelector('[name=who]').value = '张老师';
  f.querySelector('[name=contact]').value = '138xxxx0000';
  f.requestSubmit();
  await new Promise(r => setTimeout(r, 500));
  return { hint: document.getElementById('ask-hint').textContent.trim().slice(0, 80) };
})()`);"""

new = """// 没有表单了：验证联系区二维码 + 弹层 + 「加微信」CTA 的渐进增强
out.contact = await ev(`(async () => {
  const fig = document.querySelector('.contact-qr img');
  const cta = document.querySelector('[data-wx]');
  const dlg = document.getElementById('wx-dialog');
  const before = dlg.open;
  cta.click();
  await new Promise(r => setTimeout(r, 250));
  const opened = dlg.open;
  dlg.close();
  return {
    qrInPage: !!fig && fig.complete && fig.naturalWidth === 720,
    ctaHref: cta.getAttribute('href'),
    ctaCount: document.querySelectorAll('[data-wx]').length,
    dialogBeforeOpen: before,
    dialogOpens: opened,
    hasForm: !!document.querySelector('form'),
    brand: document.title.split(' · ')[0],
  };
})()`);"""

assert old in s
s = s.replace(old, new, 1)
open(P,"w",encoding="utf-8").write(s)
print("smoke.mjs 已改为验证二维码与弹层")
