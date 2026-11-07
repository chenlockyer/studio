import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="index-v4.html"; h=open(p,encoding="utf-8").read()

old = '''      <figure class="media-wide">
        <video class="loop" muted loop playsinline preload="none"
               poster="assets/img/v3/poster/choreo-chain.jpg" width="1280" height="720"
               aria-label="同一段动作在仿真与真机环境中依次执行">
          <source src="assets/video/v3/choreo-chain.mp4" type="video/mp4">
        </video>
        <figcaption>同一段动作，在仿真与真机环境中依次执行。</figcaption>
      </figure>

      <ol class="steps4">'''
new = '''      <div class="chain-grid">
      <figure class="chain-video">
        <video class="loop" muted loop playsinline preload="none"
               poster="assets/img/v3/poster/dance-live.jpg" width="720" height="1280"
               aria-label="G1 在实验室里完整跳完一支编好的舞，面罩 LED 亮着">
          <source src="assets/video/v3/dance-live.mp4" type="video/mp4">
        </video>
        <figcaption>编好的舞，在真机上完整跳完。</figcaption>
      </figure>

      <ol class="steps4 steps-col">'''
assert old in h, "chain figure not found"
h = h.replace(old, new, 1)

# 关掉 chain-grid（steps4 结束后、tagrow 之前）
old2 = '''      </ol>

      <div class="tagrow">'''
new2 = '''      </ol>
      </div>

      <div class="tagrow">'''
assert old2 in h, "tagrow anchor not found"
h = h.replace(old2, new2, 1)
open(p,"w",encoding="utf-8").write(h)
print("chain 区块改为竖版视频 + 右侧四步")

# ---------- CSS ----------
p2="assets/css/site-v4.css"; s=open(p2,encoding="utf-8").read()

s += '''
/* ---------- 动作区块：竖版真机视频 + 右侧四步（与导览的宽幅视频区分构图）---------- */
.chain-grid {
  display: grid;
  grid-template-columns: minmax(0, 21rem) minmax(0, 1fr);
  gap: clamp(1.5rem, 4vw, 3.5rem);
  align-items: start;
}
.chain-video > video {
  display: block;
  width: 100%;
  aspect-ratio: 9 / 16;
  object-fit: cover;
  background: var(--panel);
}
.chain-video figcaption {
  margin-top: 0.7rem;
  font-size: var(--t-sm);
  line-height: 1.55;
  color: var(--soft);
}
.steps-col {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: clamp(1.35rem, 3vw, 2.25rem);
}
@media (max-width: 900px) {
  .chain-grid { grid-template-columns: 1fr; }
  .chain-video { max-width: 19rem; }
}
@media (max-width: 620px) {
  .steps-col { grid-template-columns: 1fr; }
  .chain-video { max-width: 15rem; }
}

/* ---------- 培训事实：不再用整块 LED 底色，改成细竖条 + 数字作为标记 ---------- */
.cf {
  padding: 0 0 0 clamp(0.85rem, 1.4vw, 1.15rem);
  border-left: 3px solid var(--led);
  background: transparent;
  color: inherit;
}
.cf-n {
  font-family: var(--font-display);
  font-size: var(--t-lg);
  line-height: 1;
  color: var(--led);
}
.cf-t {
  margin-top: 0.45rem;
  font-size: var(--t-sm);
  font-weight: 400;
  line-height: 1.5;
  color: var(--soft);
}
'''
open(p2,"w",encoding="utf-8").write(s)
print("CSS 已追加 chain-grid / steps-col，并覆盖 .cf")
