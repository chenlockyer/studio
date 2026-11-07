# 把站点装配成一个干净的 dist/，只放要上线的东西。
# 用法：python .work/scripts/build_dist.py
import io, os, shutil, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIST = os.path.join(ROOT, "dist")

if os.path.isdir(DIST):
    shutil.rmtree(DIST)
os.makedirs(DIST)

# 根目录的单个文件
for f in ("index.html", "404.html", "robots.txt", "_headers", "_redirects", "favicon.svg"):
    src = os.path.join(ROOT, f)
    if os.path.isfile(src):
        shutil.copyfile(src, os.path.join(DIST, f))
        print(f"  {f}")

# assets 整棵树
src_assets = os.path.join(ROOT, "assets")
n = 0
total = 0
for dirpath, dirnames, filenames in os.walk(src_assets):
    rel = os.path.relpath(dirpath, ROOT)
    os.makedirs(os.path.join(DIST, rel), exist_ok=True)
    for fn in filenames:
        s = os.path.join(dirpath, fn)
        d = os.path.join(DIST, rel, fn)
        with open(s, "rb") as fh:
            data = fh.read()
        with open(d, "wb") as fh:
            fh.write(data)
        n += 1
        total += len(data)
print(f"  assets/ {n} 个文件 {total / 1024 / 1024:.2f} MB")

grand = 0
count = 0
for dirpath, _, filenames in os.walk(DIST):
    for fn in filenames:
        grand += os.path.getsize(os.path.join(dirpath, fn))
        count += 1
print(f"\ndist/ 共 {count} 个文件 {grand / 1024 / 1024:.2f} MB")
