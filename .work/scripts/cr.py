import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
d=json.load(open(".work/probe/rep.json",encoding="utf-8-sig"))
for i,vp in enumerate(d["viewports"]):
    cr=(vp["metrics"].get("surfaces") or {}).get("cardRows")
    if cr: print(f"vp{i} w={vp['width']}: ", json.dumps(cr,ensure_ascii=False))
