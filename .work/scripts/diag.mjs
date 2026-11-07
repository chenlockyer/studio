// 诊断：抓取页面在指定视口下的 hero 媒体状态
import { spawn } from "node:child_process";
import { setTimeout as sleep } from "node:timers/promises";

const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9415;
const url = process.argv[2];
const W = Number(process.argv[3] || 390);
const H = Number(process.argv[4] || 844);

const proc = spawn(CHROME, [
  "--headless", "--disable-gpu", "--mute-audio", "--no-first-run",
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${process.cwd()}\\.work\\cdpprof5`,
  "--window-size=800,600", "about:blank",
], { stdio: "ignore" });

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

const events = [];
await S("Page.enable"); await S("Runtime.enable");
await S("Network.enable");
ws.addEventListener("message", (e) => {
  const m = JSON.parse(e.data);
  if (m.method === "Network.loadingFailed") events.push(`FAILED ${m.params.errorText} type=${m.params.type}`);
  if (m.method === "Network.responseReceived" && m.params.response.url.match(/\.(mp4|jpg|png|woff2)$/))
    events.push(`${m.params.response.status} ${m.params.response.url.split("/").pop()}`);
});
await S("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: 1, mobile: W < 600 });
await S("Page.navigate", { url });
await sleep(6000);

const r = await S("Runtime.evaluate", {
  returnByValue: true, awaitPromise: true,
  expression: `(() => {
    const v = document.querySelector('.hero-video, video');
    const out = { url: location.href, title: document.title };
    if (v) out.video = { src: v.currentSrc, poster: v.poster, readyState: v.readyState,
      networkState: v.networkState, paused: v.paused, error: v.error && v.error.code,
      w: v.videoWidth, h: v.videoHeight,
      rect: (() => { const b = v.getBoundingClientRect(); return [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)]; })() };
    const box = document.querySelector('.hero-media');
    if (box) out.heroBox = getComputedStyle(box).backgroundColor + " / " + box.getBoundingClientRect().width + "x" + box.getBoundingClientRect().height;
    out.imgs = [...document.images].map(i => ({ f: i.currentSrc.split('/').pop(), nw: i.naturalWidth, ok: i.complete }));
    return out;
  })()`,
});
console.log(JSON.stringify(r.result?.result?.value, null, 1));
console.log("网络事件:\n " + events.join("\n "));
ws.close(); proc.kill(); process.exit(0);
