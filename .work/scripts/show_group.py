import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
h=open("index.html",encoding="utf-8").read()
i=h.find('id="group"'); j=h.find('id="chain"')
print(h[i-260:j-260])
