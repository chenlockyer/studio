import html.parser, sys, collections
class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.err=[]
        self.void={'area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr'}
    def handle_starttag(self,t,a):
        if t not in self.void: self.stack.append((t,self.getpos()))
    def handle_endtag(self,t):
        if t in self.void: return
        if not self.stack: self.err.append(('extra-close',t,self.getpos())); return
        if self.stack[-1][0]==t: self.stack.pop()
        else: self.err.append(('mismatch',t,self.getpos(),'open='+self.stack[-1][0]))
p=P(); p.feed(open('index.html',encoding='utf-8').read())
print('unclosed:',[ (t,pos) for t,pos in p.stack])
print('errors:',p.err[:10])
