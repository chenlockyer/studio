import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
d=json.load(open(".work/probe/rep.json",encoding="utf-8-sig"))
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="eyebrows" and isinstance(v,list) and v:
                print("EYEBROWS at",path)
                for e in v: print("  ",e)
            walk(v,path+"/"+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,path+f"[{i}]")
walk(d)
