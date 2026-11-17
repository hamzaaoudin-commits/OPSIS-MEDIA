#!/usr/bin/env python3
"""Intègre les récits Sport ajoutés (data/sp_src/sp*.json) : D.SPD, TH, YR, BLURB, FMT, FIN, couvertures."""
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
'sp01':('#1E6B4F','#04120C','#E4F4EA','#FF8A3D', p('M30 96 L170 96','#E4F4EA',4)+r(28,80,6,40,'#E4F4EA')+r(166,80,6,40,'#E4F4EA')+p('M44 190 Q100 40 156 190','#FF8A3D',4)+c(100,92,9,'#FF8A3D')+r(40,206,120,24,'#2F9E6E',4)+r(40,206,120,6,'#E4F4EA',2)+r(40,250,120,5,'#E4F4EA',2)),
'sp02':('#8A4B1A','#140903','#F8E4C4','#F2C14E', r(30,214,140,32,'#E8C887',3)+p('M26 214 Q110 20 172 214','#F8E4C4',3)+c(108,64,7,'#F8E4C4')+r(30,252,140,8,'#F8E4C4',2)+''.join(r(30+i*14,252,2,13 if i%2==0 else 9,'#14100A') for i in range(10))+p('M40 214 L150 214','#F2C14E',3)),
'sp03':('#7A1F2E','#130408','#FBE4DA','#F2A33A', p('M20 280 Q100 150 180 280','#FBE4DA',3)+p('M40 280 Q100 176 160 280','#FBE4DA',3)+p('M60 280 Q100 200 140 280','#FBE4DA',3)+pg('62,110 92,130 62,150','#F2A33A')+pg('100,110 130,130 100,150','#FBE4DA')+r(56,186,88,8,'#F2A33A',3)+c(100,230,6,'#FBE4DA')),
'sp04':('#2A4E7A','#050C16','#E4EEF9','#F2C14E', pg('20,70 120,150 120,160 20,90','#E4EEF9')+p('M28 82 L120 156','#2A4E7A',2)+p('M120 154 Q160 160 176 220','#F2C14E',3)+r(112,212,70,7,'#E4EEF9',3,'rotate(-8 147 215)')+r(112,226,70,7,'#E4EEF9',3,'rotate(-8 147 229)')+'<circle cx="74" cy="96" r="12" fill="none" stroke="#2A4E7A" stroke-width="3"/><circle cx="100" cy="100" r="12" fill="none" stroke="#2A4E7A" stroke-width="3"/>'+r(30,262,140,5,'#E4EEF9',2)),
'sp05':('#0E5C7A','#02111A','#D6F0FA','#7AE0FF', ''.join(p('M30 %s L170 %s'%(y,y),'#D6F0FA',2) for y in (140,170,200,230))+''.join(c(40+i*20,140,3,'#FF8A3D') for i in range(7))+''.join(c(40+i*20,230,3,'#FF8A3D') for i in range(7))+p('M60 186 Q100 170 140 186','#7AE0FF',3)+p('M70 192 Q100 180 130 192','#7AE0FF',2)+c(100,206,5,'#D6F0FA')),
'sp06':('#7A2A4E','#12040C','#FBE4EE','#F2C14E', r(36,84,6,150,'#FBE4EE')+r(158,84,6,150,'#FBE4EE')+p('M42 104 L158 128','#F2C14E',5)+p('M42 168 L158 150','#FBE4EE',5)+p('M70 52 Q100 22 130 52','#F2C14E',3)+r(40,248,120,6,'#FBE4EE',3)+c(100,40,5,'#F2C14E')),
}
for f in sorted(glob.glob(os.path.join(R,'data','sp_src','sp*.json'))):
    i=os.path.basename(f)[:-5]
    x=json.load(open(f))
    rec={'id':i,'name':x['name'],'sub':x['sub'],'dates':x['dates'],'country':x['country'],'job':x['job'],'src':' || '.join(x['src']),'body':x['body']}
    PE=d['D'].setdefault('SPD',[])
    k=next((n for n,y in enumerate(PE) if y['id']==i),None)
    if k is None: PE.append(rec)
    else: PE[k]=rec
    d['TH'][i]='sport';d['YR'][i]=x['yr'];d['BLURB'][i]=x['blurb'];d['FMT'][i]=x['fmt'];d['FIN'][i]={'n':x['note']}
    t,b,lt,ac,sh=COV[i];cv[i]=S(i,t,b,lt,ac,sh)
json.dump(d,open(C,'w'),ensure_ascii=False,separators=(',',':'))
json.dump(cv,open(CV,'w'),ensure_ascii=False,separators=(',',':'))
print(len(d['D']['SPD']),'récits Sport ajoutés')
