import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="index.html"; h=open(p,encoding="utf-8").read()

# 1) 导览段：宽幅 16:9 figure -> 竖版 figure；四步跟着收进两列栅格
old_fig = """      <figure class="media-wide">
        <video class="loop" muted loop playsinline preload="none"
               poster="assets/img/poster/tour-live.jpg" width="1280" height="720"
               aria-label="G1 在展厅里自主带路，正面 LED 面罩亮起，走向访客">
          <source src="assets/video/tour-live.mp4" type="video/mp4">
        </video>
        <figcaption>展厅里自主带路。定位与建图跑在本体上，断网也能继续走。</figcaption>
      </figure>

      <ol class="steps4">"""
new_fig = """      <div class="navi-grid">
        <ol class="steps4 steps-col">"""
assert old_fig in h, "找不到导览的 figure+ol 块"
h = h.replace(old_fig, new_fig, 1)

# 2) 四步结束 </ol> 之后补竖版视频 + 关掉栅格
old_tail = """        <li class="step">
          <p class="step-k">导览方案</p>
          <p>配置站点顺序、每站讲解词和临时变更规则，保存即生效。</p>
        </li>
      </ol>"""
new_tail = """        <li class="step">
          <p class="step-k">导览方案</p>
          <p>配置站点顺序、每站讲解词和临时变更规则，保存即生效。</p>
        </li>
        </ol>

        <figure class="navi-video">
          <video class="loop" muted loop playsinline preload="none"
                 poster="assets/img/poster/tour-live.jpg" width="720" height="1280"
                 aria-label="G1 在展厅里自主带路，正面 LED 面罩亮起，走向访客">
            <source src="assets/video/tour-live.mp4" type="video/mp4">
          </video>
          <figcaption>展厅里自主带路。定位与建图跑在本体上，断网也能继续走。</figcaption>
        </figure>
      </div>"""
assert old_tail in h, "找不到四步结尾"
h = h.replace(old_tail, new_tail, 1)
open(p,"w",encoding="utf-8").write(h)
print("HTML 已改")

# 3) CSS
P="assets/css/site.css"; c=open(P,encoding="utf-8").read()
css = """
/* ---------- 导览区块：竖版真机视频在右，四步在左（与动作区块左右镜像）---------- */
.navi-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 22rem);
  gap: clamp(1.5rem, 4vw, 3.5rem);
  align-items: start;
}
.navi-video > video {
  display: block;
  width: 100%;
  height: auto;          /* 必须写：<video width height> 属性会把高度钉死，aspect-ratio 就失效了 */
  aspect-ratio: 9 / 16;
  object-fit: cover;
  background: var(--panel);
}
.navi-video figcaption {
  margin-top: 0.7rem;
  font-size: var(--t-sm);
  line-height: 1.55;
  color: var(--soft);
}
@media (max-width: 900px) {
  .navi-grid { grid-template-columns: 1fr; }
  .navi-video { max-width: 19rem; order: -1; }
}
@media (max-width: 620px) {
  .navi-video { max-width: 15rem; }
}
"""
anchor = "/* ---------- 动作区块：竖版真机视频 + 右侧四步（与导览的宽幅视频区分构图）---------- */"
assert anchor in c
c = c.replace(anchor, css.strip() + "\n\n" + anchor, 1)
# 动作区块注释里的「与导览的宽幅视频区分构图」已不成立，改掉
c = c.replace("/* ---------- 动作区块：竖版真机视频 + 右侧四步（与导览的宽幅视频区分构图）---------- */",
              "/* ---------- 动作区块：竖版真机视频在左，四步在右（与导览左右镜像）---------- */",1)
open(P,"w",encoding="utf-8").write(c)
print("CSS 已改")
