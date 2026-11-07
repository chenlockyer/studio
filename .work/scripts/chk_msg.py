import subprocess, io, sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
raw = subprocess.run(["git","log","-1","--format=%B","deploy-gh"], capture_output=True).stdout
print("首 3 字节:", raw[:3])
body = raw.decode("utf-8")
print("首字符:", repr(body[0]))
print("--- 正文 ---")
print(body.strip()[:400])
