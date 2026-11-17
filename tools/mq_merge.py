#!/usr/bin/env python3
"""Intègre les récits Marques ajoutés (data/mq_src/mq*.json) à D.MQD, TH, YR, BLURB, FMT, FIN, couvertures."""
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
'mq21':('#B3202A','#120406','#FDE3D4','#F2C14E', r(84,60,32,34,'#1A0A0A',6)+r(88,50,24,14,'#C0C0C0',3)+pg('70,94 130,94 144,150 144,230 56,230 56,150','#1A0A0A')+r(60,150,80,40,'#FDE3D4',3)+c(80,120,4,'#FDE3D4',.8)+c(114,108,3,'#FDE3D4',.8)+c(96,100,5,'#FDE3D4',.8)+p('M52 258 L148 258','#F2C14E',4)+p('M120 270 L80 270','#FDE3D4',3)+pg('80,270 90,262 90,278','#FDE3D4')),
'mq22':('#2C4F6E','#050B12','#E3EEF7','#E8B04A', r(46,100,56,26,'#E8B04A',13,'rotate(-30 74 113)')+r(88,128,56,26,'#F7F7F2',13,'rotate(-30 116 141)')+c(100,200,28,'none')+'<circle cx="100" cy="212" r="30" fill="none" stroke="#E3EEF7" stroke-width="5"/>'+r(86,204,28,22,'#E3EEF7',4)+p('M92 204 L92 196 Q100 184 108 196 L108 204','#E3EEF7',4)+r(40,256,120,6,'#E8B04A',3)),
'mq23':('#C9A80A','#160F02','#FFF3B0','#F2C14E', r(52,70,96,96,'#FFE552',3,'rotate(-5 100 118)')+r(60,80,96,96,'#FFF176',3,'rotate(4 108 128)')+pg('136,164 156,164 156,184','#E0C400')+r(70,96,70,4,'#C9A80A',2,'rotate(4 105 98)')+r(70,110,50,4,'#C9A80A',2,'rotate(4 95 112)')+c(60,226,7,'#FFF3B0')+c(80,236,7,'#FFF3B0')+c(100,226,7,'#FFF3B0')+c(120,236,7,'#FFF3B0')+r(40,258,120,5,'#FFF3B0',2)),
'mq24':('#C2185B','#14040C','#FFE3EE','#2EC4B6', r(82,26,36,70,'#2EC4B6',6)+r(82,208,36,66,'#2EC4B6',6)+c(100,152,52,'#FFE3EE')+c(100,152,42,'#FFFFFF')+c(100,152,5,'#14040C')+p('M100 152 L100 122','#14040C',4)+p('M100 152 L124 164','#C2185B',4)+''.join(c(100+38*__import__("math").cos(a*0.5236),152+38*__import__("math").sin(a*0.5236),2.5,'#14040C') for a in range(12))),
'mq25':('#6C2F8E','#0C0414','#F8E6F2','#FF8A3D', r(46,66,84,100,'#F8E6F2',4,'rotate(-8 88 116)')+r(70,76,84,100,'#FFFFFF',4,'rotate(6 112 126)')+r(78,84,68,66,'#FF8A3D',2,'rotate(6 112 117)')+c(122,104,9,'#FFE8C2')+pg('80,148 104,118 120,138 130,126 144,148','#6C2F8E','rotate(6 112 117)')+r(40,214,120,6,'#F8E6F2',3)+c(70,240,5,'#FF8A3D')+c(100,240,5,'#F8E6F2')+c(130,240,5,'#FF8A3D')),
}
for f in sorted(glob.glob(os.path.join(R,'data','mq_src','mq*.json'))):
    i=os.path.basename(f)[:-5]
    x=json.load(open(f))
    rec={'id':i,'name':x['name'],'sub':x['sub'],'dates':x['dates'],'country':x['country'],'job':x['job'],'src':' || '.join(x['src']),'body':x['body']}
    MQ=d['D']['MQD']
    k=next((n for n,y in enumerate(MQ) if y['id']==i),None)
    if k is None: MQ.append(rec)
    else: MQ[k]=rec
    d['TH'][i]='marques';d['YR'][i]=x['yr'];d['BLURB'][i]=x['blurb'];d['FMT'][i]=x['fmt'];d['FIN'][i]={'n':x['note']}
    t,b,lt,ac,sh=COV[i];cv[i]=S(i,t,b,lt,ac,sh)
json.dump(d,open(C,'w'),ensure_ascii=False,separators=(',',':'))
json.dump(cv,open(CV,'w'),ensure_ascii=False,separators=(',',':'))
print(len([1 for y in d['D']['MQD']]),'récits Marques au total')
