// 用 CDP 精确截取页面某个锚点/滚动位置的截图。
// 用法: node shot.mjs <url> <outdir> <w> <h> <target1> [target2 ...]
//   target = "#selector"（滚到该元素顶部）或 "@12345"（绝对 y）
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import { setTimeout as sleep } from "node:timers/promises";

const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9411;

const [url, outdir, wArg, hArg, ...targets] = process.argv.slice(2);
const W = Number(wArg || 1440), H = Number(hArg || 1000);
mkdirSync(outdir, { recursive: true });

const proc = spawn(CHROME, [
  "--headless", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
  "--no-first-run", "--no-default-browser-check",
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${process.cwd()}\\.work\\cdpprof`,
  "--window-size=800,600", "about:blank",
], { stdio: "ignore" });

async function getJSON(path) {
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}${path}`);
      if (r.ok) return await r.json();
    } catch { /* 还没起来 */ }
    await sleep(150);
  }
  throw new Error("CDP 未就绪");
}

const ver = await getJSON("/json/version");
const ws = new WebSocket(ver.webSocketDebuggerUrl);
let id = 0;
const pending = new Map();
ws.addEventListener("message", (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
});
await new Promise((res) => ws.addEventListener("open", res, { once: true }));

function send(method, params = {}, sessionId) {
  const msg = { id: ++id, method, params };
  if (sessionId) msg.sessionId = sessionId;
  return new Promise((res) => { pending.set(msg.id, res); ws.send(JSON.stringify(msg)); });
}

const { result: { targetId } } = await send("Target.createTarget", { url: "about:blank" });
const { result: { sessionId } } = await send("Target.attachToTarget", { targetId, flatten: true });
const S = (m, p) => send(m, p, sessionId);

await S("Page.enable");
await S("Runtime.enable");
await S("Emulation.setDeviceMetricsOverride", {
  width: W, height: H, deviceScaleFactor: 1, mobile: W < 600,
});
await S("Page.navigate", { url });
await sleep(1200);

// 触发懒加载与视频海报
await S("Runtime.evaluate", {
  expression: `(async () => {
    document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager');
    for (const v of document.querySelectorAll('video')) { try { v.preload='metadata'; v.load(); } catch(e){} }
  })()`, awaitPromise: true,
});
await sleep(1500);

const evalJS = async (expression) => {
  const r = await S("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
  return r.result?.result?.value;
};

const pageH = await evalJS("document.documentElement.scrollHeight");
console.log("页面高度", pageH);

for (const t of targets) {
  let y;
  let name;
  if (t.startsWith("#")) {
    name = t.slice(1);
    y = await evalJS(`(() => { const e = document.querySelector(${JSON.stringify(t)});
      return e ? Math.round(e.getBoundingClientRect().top + window.scrollY) : 0; })()`);
  } else {
    name = "y" + t.slice(1);
    y = Number(t.slice(1));
  }
  // 预留吸顶导航高度
  y = Math.max(0, y - 0);
  await evalJS(`window.scrollTo(0, ${y}); new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))`);
  await sleep(700);
  // 强制落定入场动画，避免截图卡在渐变中间（布局验证用）
  await evalJS(`document.querySelectorAll('.rv').forEach(e => e.classList.add('is-in'))`);
  await sleep(450);
  const shot = await S("Page.captureScreenshot", { format: "png", captureBeyondViewport: false });
  const file = `${outdir}\\${name}.png`;
  writeFileSync(file, Buffer.from(shot.result.data, "base64"));
  console.log(`  ${name}  y=${y}  -> ${file}`);
}

ws.close();
proc.kill();
process.exit(0);
