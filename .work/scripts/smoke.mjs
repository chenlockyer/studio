// 冒烟测试：控制台错误、视频可播、问答可展开、表单可复制、导航锚点齐全。
import { spawn } from "node:child_process";
import { setTimeout as sleep } from "node:timers/promises";

const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9412;
const URL = "file:///D:/code/unitree-site/index.html";

const proc = spawn(CHROME, [
  "--headless", "--disable-gpu", "--mute-audio", "--autoplay-policy=no-user-gesture-required",
  "--no-first-run", "--no-default-browser-check",
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${process.cwd()}\\.work\\cdpprof2`,
  "--window-size=1440,900", "about:blank",
], { stdio: "ignore" });

async function getJSON(path) {
  for (let i = 0; i < 80; i++) {
    try { const r = await fetch(`http://127.0.0.1:${PORT}${path}`); if (r.ok) return await r.json(); } catch {}
    await sleep(150);
  }
  throw new Error("CDP 未就绪");
}
const ver = await getJSON("/json/version");
const ws = new WebSocket(ver.webSocketDebuggerUrl);
let id = 0; const pending = new Map(); const logs = [];
ws.addEventListener("message", (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); return; }
  if (m.method === "Runtime.consoleAPICalled" && ["error", "warning"].includes(m.params.type))
    logs.push(`[console.${m.params.type}] ` + m.params.args.map(a => a.value ?? a.description ?? "").join(" "));
  if (m.method === "Runtime.exceptionThrown") logs.push("[exception] " + (m.params.exceptionDetails?.text || ""));
  if (m.method === "Log.entryAdded" && m.params.entry.level === "error") logs.push("[log] " + m.params.entry.text);
});
await new Promise(r => ws.addEventListener("open", r, { once: true }));
function send(method, params = {}, sessionId) {
  const msg = { id: ++id, method, params }; if (sessionId) msg.sessionId = sessionId;
  return new Promise(res => { pending.set(msg.id, res); ws.send(JSON.stringify(msg)); });
}
const { result: { targetId } } = await send("Target.createTarget", { url: "about:blank" });
const { result: { sessionId } } = await send("Target.attachToTarget", { targetId, flatten: true });
const S = (m, p) => send(m, p, sessionId);

await S("Page.enable"); await S("Runtime.enable"); await S("Log.enable");
await S("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
await S("Page.navigate", { url: URL });
await sleep(2500);

const ev = async (expression) => {
  const r = await S("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
  if (r.result?.exceptionDetails) return { __err: r.result.exceptionDetails.text };
  return r.result?.result?.value;
};

const out = {};
out.anchors = await ev(`(() => {
  const ids = [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href').slice(1)).filter(Boolean);
  const missing = [...new Set(ids)].filter(id => !document.getElementById(id));
  return { total: ids.length, missing };
})()`);

out.videos = await ev(`(async () => {
  const vs = [...document.querySelectorAll('video')];
  for (const v of vs) { try { v.preload='auto'; v.muted=true; await v.play().catch(()=>{}); } catch(e){} }
  await new Promise(r => setTimeout(r, 1200));
  return vs.map(v => ({ src: v.currentSrc.split('/').pop(), ready: v.readyState, w: v.videoWidth, paused: v.paused }));
})()`);

// 没有表单了：验证联系区二维码 + 弹层 + 「加微信」CTA 的渐进增强
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
})()`);

out.layout = await ev(`(() => ({
  overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  pageH: document.documentElement.scrollHeight,
  h1: document.querySelector('h1')?.innerText.replace(/\\n/g,' / '),
  go2: document.body.innerText.includes('GO2'),
  imgsBroken: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.currentSrc.split('/').pop()),
}))()`);

console.log(JSON.stringify({ ...out, logs }, null, 1));
ws.close(); proc.kill(); process.exit(0);
