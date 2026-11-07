import { spawn } from "node:child_process";
import { setTimeout as sleep } from "node:timers/promises";
import { writeFileSync, mkdirSync } from "node:fs";
const CHROME="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", PORT=9414;
const proc=spawn(CHROME,["--headless","--disable-gpu","--hide-scrollbars","--mute-audio","--no-first-run","--no-default-browser-check",`--remote-debugging-port=${PORT}`,`--user-data-dir=${process.cwd()}\\.work\\cdpprof4`,"about:blank"],{stdio:"ignore"});
async function gj(p){for(let i=0;i<80;i++){try{const r=await fetch(`http://127.0.0.1:${PORT}${p}`);if(r.ok)return await r.json();}catch{}await sleep(150);}throw new Error("no cdp");}
const v=await gj("/json/version");const ws=new WebSocket(v.webSocketDebuggerUrl);let id=0;const pend=new Map();
ws.addEventListener("message",e=>{const m=JSON.parse(e.data);if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id);}});
await new Promise(r=>ws.addEventListener("open",r,{once:true}));
const send=(me,pa={},s)=>{const msg={id:++id,method:me,params:pa};if(s)msg.sessionId=s;return new Promise(res=>{pend.set(msg.id,res);ws.send(JSON.stringify(msg));});};
const {result:{targetId}}=await send("Target.createTarget",{url:"about:blank"});
const {result:{sessionId}}=await send("Target.attachToTarget",{targetId,flatten:true});
const S=(m,p)=>send(m,p,sessionId);
await S("Page.enable");await S("Runtime.enable");
const ev=async(ex)=>{const r=await S("Runtime.evaluate",{expression:ex,returnByValue:true,awaitPromise:true});return r.result?.result?.value;};
mkdirSync(".work/shots/wx",{recursive:true});

for (const [w,h,label,cta] of [[1440,900,"desktop",'document.querySelector(".btn-bar")'],[390,844,"mobile",'document.querySelector(".hero-act .btn")']]) {
  await S("Emulation.setDeviceMetricsOverride",{width:w,height:h,deviceScaleFactor:1,mobile:w<600});
  await S("Page.navigate",{url:"file:///D:/code/unitree-site/index.html"});
  await sleep(1800);
  await ev(`document.querySelectorAll('video').forEach(v=>v.pause())`);
  await ev(`(()=>{const a=${cta}; a.click(); return true;})()`);
  await sleep(600);
  const open = await ev(`document.getElementById('wx-dialog').open`);
  const shot = await S("Page.captureScreenshot",{format:"png"});
  writeFileSync(`.work/shots/wx/${label}.png`, Buffer.from(shot.result.data,"base64"));
  // 测试 ESC 关闭
  await S("Input.dispatchKeyEvent",{type:"keyDown",key:"Escape",code:"Escape",windowsVirtualKeyCode:27});
  await S("Input.dispatchKeyEvent",{type:"keyUp",key:"Escape",code:"Escape",windowsVirtualKeyCode:27});
  await sleep(400);
  const closed = await ev(`!document.getElementById('wx-dialog').open`);
  console.log(`${label}: 打开=${open}  ESC关闭=${closed}`);
}
ws.close();proc.kill();process.exit(0);
