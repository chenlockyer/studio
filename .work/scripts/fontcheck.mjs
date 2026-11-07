import { spawn } from "node:child_process";
import { setTimeout as sleep } from "node:timers/promises";
const CHROME="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", PORT=9413;
const proc=spawn(CHROME,["--headless","--disable-gpu","--mute-audio","--no-first-run","--no-default-browser-check",`--remote-debugging-port=${PORT}`,`--user-data-dir=${process.cwd()}\\.work\\cdpprof3`,"--window-size=1440,900","about:blank"],{stdio:"ignore"});
async function gj(p){for(let i=0;i<80;i++){try{const r=await fetch(`http://127.0.0.1:${PORT}${p}`);if(r.ok)return await r.json();}catch{}await sleep(150);}throw new Error("no cdp");}
const v=await gj("/json/version");const ws=new WebSocket(v.webSocketDebuggerUrl);let id=0;const pend=new Map();
ws.addEventListener("message",e=>{const m=JSON.parse(e.data);if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id);}});
await new Promise(r=>ws.addEventListener("open",r,{once:true}));
const send=(me,pa={},s)=>{const msg={id:++id,method:me,params:pa};if(s)msg.sessionId=s;return new Promise(res=>{pend.set(msg.id,res);ws.send(JSON.stringify(msg));});};
const {result:{targetId}}=await send("Target.createTarget",{url:"about:blank"});
const {result:{sessionId}}=await send("Target.attachToTarget",{targetId,flatten:true});
const S=(m,p)=>send(m,p,sessionId);
await S("Page.enable");await S("Runtime.enable");
await S("Page.navigate",{url:"file:///D:/code/unitree-site/index.html"});
await sleep(2500);
const r=await S("Runtime.evaluate",{returnByValue:true,awaitPromise:true,expression:`(async()=>{
  await document.fonts.ready;
  const h1=document.querySelector('h1');
  const cs=getComputedStyle(h1.querySelector('span')||h1);
  return {
    smileyLoaded: document.fonts.check('16px Smiley'),
    noto400Loaded: document.fonts.check('16px "Noto Sans SC"'),
    h1Font: cs.fontFamily,
    loadedList: [...document.fonts].map(f=>f.family+':'+f.status),
  };
})()`});
console.log(JSON.stringify(r.result.result.value,null,1));
ws.close();proc.kill();process.exit(0);
