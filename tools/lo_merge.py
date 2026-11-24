#!/usr/bin/env python3
"""Intègre les récits Lore et mythologie (data/lo_src/lc*.json) : D.LCD, TH, YR, BLURB, FMT, FIN, couvertures."""
import json,glob,os,subprocess,sys
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
C=os.path.join(R,'data','content.json');CV=os.path.join(R,'data','covers.json')
d=json.load(open(C));cv=json.load(open(CV))
for k in('TH','YR','FMT','FIN','BLURB'):d.setdefault(k,{})
# (haut, bas, clair, accent, formes)
def S(i,top,bot,lt,ac,shapes):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300"><defs><linearGradient id="g%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs><rect width="200" height="300" fill="url(#g%s)"/>%s</svg>'%(i,top,bot,i,shapes))
def c(x,y,r,f,o=1):return '<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>'%(x,y,r,f,o)
def r(x,y,w,h,f,rx=0,t=''):return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"%s/>'%(x,y,w,h,rx,f,(' transform="%s"'%t if t else ''))
def e(x,y,rx,ry,f,o=1):return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" opacity="%s"/>'%(x,y,rx,ry,f,o)
def p(dd,s,w,f='none',t=''):return '<path d="%s" stroke="%s" stroke-width="%s" fill="%s" stroke-linecap="round"%s/>'%(dd,s,w,f,(' transform="%s"'%t if t else ''))
def pg(pts,f,t=''):return '<polygon points="%s" fill="%s"%s/>'%(pts,f,(' transform="%s"'%t if t else ''))
COV={}
exec(open(os.path.join(R,'tools','lo_cov.txt')).read())
for f in sorted(glob.glob(os.path.join(R,'data','lo_src','lc*.json'))):
    i=os.path.basename(f)[:-5]
    x=json.load(open(f))
    rec={'id':i,'name':x['name'],'sub':x['sub'],'dates':x['dates'],'country':x['country'],'job':x['job'],'src':' || '.join(x['src']),'body':x['body']}
    PE=d['D']['LCD']
    k=next((n for n,y in enumerate(PE) if y['id']==i),None)
    if k is None: PE.append(rec)
    else: PE[k]=rec
    d['TH'][i]='licences';d['YR'][i]=x['yr'];d['BLURB'][i]=x['blurb'];d['FMT'][i]=x['fmt'];d['FIN'][i]={'n':x['note']}
    t,b,lt,ac,sh=COV[i];cv[i]=S(i,t,b,lt,ac,sh)
json.dump(d,open(C,'w'),ensure_ascii=False,separators=(',',':'))
json.dump(cv,open(CV,'w'),ensure_ascii=False,separators=(',',':'))
print(len(d['D']['LCD']),'récits Licences au total')
import re
SH=os.path.join(R,'src','shell.html');s=open(SH).read()
ids=sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(R,'data','lo_src','lc*.json')))
s2=re.sub(r'\{n:"Lore et mythologie",ids:\[[^\]]*\]\}','{n:"Lore et mythologie",ids:['+','.join("'%s'"%i for i in ids)+']}',s)
if s2!=s: open(SH,'w').write(s2)
