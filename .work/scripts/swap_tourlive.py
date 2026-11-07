import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="index-v4.html"; h=open(p,encoding="utf-8").read()
old = '''      <figure class="media-wide">
        <video class="loop" muted loop playsinline preload="none"
               poster="assets/img/v3/poster/slam-build.jpg" width="1280" height="720"
               aria-label="G1 在学院楼内建图并带路，本体雷达实时生成点云">
          <source src="assets/video/v3/slam-build.mp4" type="video/mp4">
        </video>
        <figcaption>真机建图与运行时的本体雷达点云，实时生成，不依赖外网。</figcaption>
      </figure>'''
new = '''      <figure class="media-wide">
        <video class="loop" muted loop playsinline preload="none"
               poster="assets/img/v3/poster/tour-live.jpg" width="1280" height="720"
               aria-label="G1 在展厅里自主带路，正面 LED 面罩亮起，走向访客">
          <source src="assets/video/v3/tour-live.mp4" type="video/mp4">
        </video>
        <figcaption>展厅里自主带路。定位与建图跑在本体上，断网也能继续走。</figcaption>
      </figure>'''
assert old in h, "slam-build figure not found"
h=h.replace(old,new,1)
open(p,"w",encoding="utf-8").write(h)
print("HTML 换入 tour-live")
