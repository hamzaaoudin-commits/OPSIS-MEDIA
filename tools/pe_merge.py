#!/usr/bin/env python3
"""Intègre les récits Personnes ajoutés (data/pe_src/pe*.json) : D.PED, TH, YR, BLURB, FMT, FIN, couvertures."""
import json,glob,os,subprocess,sys
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
C=os.path.join(R,'data','content.json');CV=os.path.join(R,'data','covers.json')
d=json.load(open(C));cv=json.load(open(CV))
for k in('TH','YR','FMT','FIN','BLURB'):d.setdefault(k,{})
# (haut, bas, clair, accent, formes)
def S(i,top,bot,lt,ac,shapes):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300"><defs><linearGradient id="g%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs><rect width="200" height="300" fill="url(#g%s)"/><circle cx="100" cy="112" r="70" fill="%s" opacity=".9"/>%s</svg>'%(i,top,bot,i,lt,shapes))
def c(x,y,r,f,o=1):return '<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>'%(x,y,r,f,o)
def r(x,y,w,h,f,rx=0,t=''):return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"%s/>'%(x,y,w,h,rx,f,(' transform="%s"'%t if t else ''))
def e(x,y,rx,ry,f,o=1):return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" opacity="%s"/>'%(x,y,rx,ry,f,o)
def p(dd,s,w,f='none',t=''):return '<path d="%s" stroke="%s" stroke-width="%s" fill="%s" stroke-linecap="round"%s/>'%(dd,s,w,f,(' transform="%s"'%t if t else ''))
def pg(pts,f,t=''):return '<polygon points="%s" fill="%s"%s/>'%(pts,f,(' transform="%s"'%t if t else ''))
COV={
'pe01':('#1F5A3A','#05140B','#E3F3E4','#F2C14E', r(54,70,96,60,'#F4EBD0',3,'rotate(-8 102 100)')+r(60,86,96,60,'#FFF8E1',3,'rotate(5 108 116)')+pg('60,86 108,116 156,86','#E3D7B0','rotate(5 108 116)')+p('M40 250 L80 216 L108 232 L168 176','#F2C14E',5)+pg('168,176 150,180 164,194','#F2C14E')+r(36,262,128,5,'#E3F3E4',2)+c(60,236,3,'#F2C14E')+c(100,244,3,'#F2C14E')),
'pe02':('#2B3A55','#060912','#E6ECF7','#E8B04A', ''.join(r(48+i*22,200-(h),16,h,'#E6ECF7',2) for i,h in enumerate([40,70,52,96,64]))+c(100,112,0,'#000')+p('M60 214 L80 196 L104 206 L128 176 L152 150','#E8B04A',3)+r(40,230,120,5,'#E6ECF7',2)+r(40,246,120,5,'#E8B04A',2)),
}
for f in sorted(glob.glob(os.path.join(R,'data','pe_src','pe*.json'))):
    i=os.path.basename(f)[:-5]
    x=json.load(open(f))
    rec={'id':i,'name':x['name'],'sub':x['sub'],'dates':x['dates'],'country':x['country'],'job':x['job'],'src':' || '.join(x['src']),'body':x['body']}
    PE=d['D'].setdefault('PED',[])
    k=next((n for n,y in enumerate(PE) if y['id']==i),None)
    if k is None: PE.append(rec)
    else: PE[k]=rec
    d['TH'][i]='personnes';d['YR'][i]=x['yr'];d['BLURB'][i]=x['blurb'];d['FMT'][i]=x['fmt'];d['FIN'][i]={'n':x['note']}
    t,b,lt,ac,sh=COV[i];cv[i]=S(i,t,b,lt,ac,sh)
json.dump(d,open(C,'w'),ensure_ascii=False,separators=(',',':'))
json.dump(cv,open(CV,'w'),ensure_ascii=False,separators=(',',':'))
print(len(d['D']['PED']),'récits Personnes ajoutés')
