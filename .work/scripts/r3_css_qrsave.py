import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
P="assets/css/site.css"; c=open(P,encoding="utf-8").read()
if ".qr-save" not in c:
    c = c.replace(""".qr-d { margin-top: 0.3rem;""",
""".qr-save {
  display: none;
  margin-top: 0.6rem;
  max-width: 26ch;
  font-size: var(--t-sm);
  line-height: 1.55;
  color: var(--led);
  text-decoration: underline;
  text-underline-offset: 3px;
}
@media (max-width: 760px) {
  .qr-save { display: block; }
}
.wx-save { max-width: 30ch; }
.qr-d { margin-top: 0.3rem;""", 1)
    open(P,"w",encoding="utf-8").write(c)
    print("CSS 已加 .qr-save")
else:
    print("CSS 已有 .qr-save")
