import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
d=json.load(open(".work/probe/rep.json",encoding="utf-8-sig"))
for i,vp in enumerate(d.get("viewports",[])):
    m=vp.get("metrics",{})
    cr=m.get("cardRows") or m.get("card_rows")
    print(f"--- viewport {i} w={vp.get('width')} ---")
    if cr: print(json.dumps(cr,ensure_ascii=False,indent=1)[:1200])
    for k in ("warnings","fails"):
        for w in (m.get(k) or []):
            print(" ",k[:4],":",w)
