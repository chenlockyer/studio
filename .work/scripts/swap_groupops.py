import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="index.html"; h=open(p,encoding="utf-8").read()

# 群控区块（第二个 group-sync 出现处）换成 group-ops，避免与首屏同一段素材重复
idx = h.find('id="group"')
assert idx>0, "找不到 group 区块"
head, tail = h[:idx], h[idx:]
n_before = tail.count("group-sync")
tail = tail.replace('poster="assets/img/poster/group-sync.jpg"', 'poster="assets/img/poster/group-ops.jpg"', 1)
tail = tail.replace('assets/video/group-sync.mp4', 'assets/video/group-ops.mp4', 1)
h = head + tail
open(p,"w",encoding="utf-8").write(h)
print(f"group 区块内 group-sync 出现 {n_before} 处 → 换 1 处为 group-ops")
print("全页 group-ops 出现:", h.count("group-ops"), " group-sync 出现:", h.count("group-sync"))
