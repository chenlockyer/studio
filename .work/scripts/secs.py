import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
d=json.load(open(".work/probe/rep.json",encoding="utf-8-sig"))
for vp in d["viewports"]:
    print(f"=== w={vp['width']} ===")
    for s in vp["layout"]["sections"]:
        print(f"  {s['top']:6d}..{s['top']+s['height']:6d}  {s['sel']}")
