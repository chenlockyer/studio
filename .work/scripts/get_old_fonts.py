import io,sys,subprocess
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
for f in ["smiley-display","noto-400","noto-700"]:
    b = subprocess.run(["git","show",f"4822f09:assets/fonts/{f}.woff2"],capture_output=True).stdout
    open(f".work/shots/beforeafter/old-{f}.woff2","wb").write(b)
    print(f"old-{f}.woff2 {len(b)} bytes")
