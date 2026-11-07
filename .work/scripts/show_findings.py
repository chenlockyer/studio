import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
d=json.load(open(".work/probe/rep.json",encoding="utf-8-sig"))
for f in d["findings"]:
    print(f.get("level"), f.get("rule"), "@", f.get("at"), "->", (f.get("detail") or f.get("message") or "")[:400])
