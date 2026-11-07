import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
d=json.load(open(".work/probe/rep.json",encoding="utf-8-sig"))
print("top keys:", list(d.keys()))
vp=d.get("viewports",[])
print("viewports:",len(vp))
if vp:
    print("vp0 keys:", list(vp[0].keys()))
    m=vp[0].get("metrics",{})
    print("metrics keys:", list(m.keys()))
    print()
    print(json.dumps(vp[1],ensure_ascii=False)[:2500])
