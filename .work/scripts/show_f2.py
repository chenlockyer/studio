import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
d=json.load(open(".work/probe/rep.json",encoding="utf-8-sig"))
print(json.dumps(d["findings"],ensure_ascii=False,indent=1)[:3000])
print("\n--- surfaces vp1 ---")
print(json.dumps(d["viewports"][1]["metrics"].get("surfaces"),ensure_ascii=False,indent=1)[:2000])
