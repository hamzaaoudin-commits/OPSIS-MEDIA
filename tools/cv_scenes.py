#!/usr/bin/env python3
"""Couvertures scènes (remplacent les couvertures gabarit) : lit tools/cvs_*.txt -> data/covers.json"""
import json,glob,os,math
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
CV=os.path.join(R,'data','covers.json')
def S(i,top,bot,lt,ac,shapes):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300"><defs><linearGradient id="g%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs><rect width="200" height="300" fill="url(#g%s)"/>%s</svg>'%(i,top,bot,i,shapes))
def c(x,y,r,f,o=1):return '<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>'%(x,y,r,f,o)
def r(x,y,w,h,f,rx=0,t=''):return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"%s/>'%(x,y,w,h,rx,f,(' transform="%s"'%t if t else ''))
def e(x,y,rx,ry,f,o=1):return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" opacity="%s"/>'%(x,y,rx,ry,f,o)
def p(dd,s,w,f='none',t=''):return '<path d="%s" stroke="%s" stroke-width="%s" fill="%s" stroke-linecap="round"%s/>'%(dd,s,w,f,(' transform="%s"'%t if t else ''))
def pg(pts,f,t=''):return '<polygon points="%s" fill="%s"%s/>'%(pts,f,(' transform="%s"'%t if t else ''))

def gl(x,y,rr,col,o=.25): return c(x,y,rr,col,o)
ST=[(20,30),(62,18),(150,26),(182,60),(40,84),(122,44),(172,104),(14,130),(92,12)]
def stars(pts=ST,col='#FFFFFF'): return ''.join(c(a,b,1.2,col,.75) for a,b in pts)
def ln(a,b,col,w=2,o=1): return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" opacity="%s" stroke-linecap="round"/>'%(a[0],a[1],b[0],b[1],col,w,o)
SC={}
for f in sorted(glob.glob(os.path.join(R,'tools','cvs_*.txt'))): exec(open(f).read())
if __name__=='__main__':
    cv=json.load(open(CV))
    for i,(t,b,sh) in SC.items(): cv[i]=S(i,t,b,'#fff','#fff',sh)
    json.dump(cv,open(CV,'w'),ensure_ascii=False)
    print(len(SC),'couvertures scènes')
