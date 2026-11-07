// 量每个 video 的渲染框、固有尺寸、object-fit，找出被拉伸/放大的是哪个
import { spawn } from "node:child_process";
import { setTimeout as sleep } from "node:timers/promises";
import { writeFileSync } from "node:fs";

const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9416;
const url = process.argv[2];
const W = Number(process.argv[3] || 390);
const H = Number(process.argv[4] || 844);
const outPng = process.argv[5];

const proc = spawn(CHROME, ["--headless", "--disable-gpu", "--mute-audio", "--no-first-run",
  `--remote-debugging-port=${PORT}`, `--user-data-dir=${process.cwd()}\\.work\\cdpprof6`,
  "--window-size=800,600", "about:blank"], { stdio: "ignore" });

async function getJSON(p) {
  for (let i = 0; i < 60; i++) {
    try { const r = await fetch(`http://127.0.0.1:${PORT}${p}`); if (r.ok) return r.json(); } catch {}
    await sleep(150);
  }
  throw new Error("CDP 未就绪");
}
const ver = await getJSON("/json/version");
const ws = new WebSocket(ver.webSocketDebuggerUrl);
let id = 0; const pending = new Map();
ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
const send = (method, params = {}, sid) => { const msg = { id: ++id, method, params }; if (sid) msg.sessionId = sid; return new Promise((res) => { pending.set(msg.id, res); ws.send(JSON.stringify(msg)); }); };

const { result: { targetId } } = await send("Target.createTarget", { url: "about:blank" });
const { result: { sessionId } } = await send("Target.attachToTarget", { targetId, flatten: true });
const S = (m, p) => send(m, p, sessionId);
await S("Page.enable"); await S("Runtime.enable");
await S("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: 1, mobile: W < 600 });
await S("Page.navigate", { url });
await sleep(3500);
await S("Runtime.evaluate", { expression: `document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')` });
await sleep(1200);

const r = await S("Runtime.evaluate", {
  returnByValue: true, awaitPromise: true,
  expression: `(() => [...document.querySelectorAll('video')].map((v, i) => {
    const b = v.getBoundingClientRect();
    const cs = getComputedStyle(v);
    const sec = v.closest('section');
    return {
      i,
      section: sec ? (sec.id || sec.className) : '?',
      cls: v.className,
      src: (v.currentSrc || v.querySelector('source')?.src || '').split('/').pop(),
      intrinsic: v.videoWidth + 'x' + v.videoHeight,
      intrinsicAR: v.videoWidth ? +(v.videoWidth / v.videoHeight).toFixed(3) : null,
      box: Math.round(b.width) + 'x' + Math.round(b.height),
      boxAR: +(b.width / b.height).toFixed(3),
      objectFit: cs.objectFit,
      objectPosition: cs.objectPosition,
      aspectRatioCSS: cs.aspectRatio,
      cssW: cs.width, cssH: cs.height,
    };
  }))()`,
});
console.table(r.result?.result?.value || []);
console.log(JSON.stringify(r.result?.result?.value, null, 1));

if (outPng) {
  const shot = await S("Page.captureScreenshot", { format: "png" });
  writeFileSync(outPng, Buffer.from(shot.result.data, "base64"));
}
ws.close(); proc.kill(); process.exit(0);
