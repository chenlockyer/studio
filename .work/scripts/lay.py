import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
d=json.load(open(".work/probe/rep.json",encoding="utf-8-sig"))
vp=d["viewports"][1]
lay=vp.get("layout")
print("layout type:",type(lay), list(lay.keys()) if isinstance(lay,dict) else len(lay))
print(json.dumps(lay,ensure_ascii=False)[:1500])
