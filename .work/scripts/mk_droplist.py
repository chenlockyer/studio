import io,sys,subprocess
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
out = subprocess.run(["git","ls-tree","-r","--name-only","master","--",".work"],
                     capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
drop = [p for p in out if not (p.startswith(".work/scripts/") or p.startswith(".work/source-img/"))]
open(".work/drop-tracked.txt","w",encoding="utf-8",newline="\n").write("\n".join(drop)+"\n")
print("drop:", len(drop))
for p in drop[:4]: print("  ", p)
