import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="assets/css/site.css"; c=open(p,encoding="utf-8").read()
c=c.replace("落地组 · site-v4.css","落地组 · site.css")
c=c.replace(".media-wide figcaption,\n.shot figcaption,\n.course-photo figcaption {",".media-wide figcaption,\n.media-wide .chain-video + figcaption {")
old=""".course-photo > picture { display: block; background: var(--panel); }
.course-photo img { width: 100%; aspect-ratio: 16 / 11; object-fit: cover; }
"""
c=c.replace(old,"")
open(p,"w",encoding="utf-8").write(c)
print("清理完成；.course-photo 剩余:", c.count(".course-photo"), " .shot 剩余:", c.count(".shot "))
