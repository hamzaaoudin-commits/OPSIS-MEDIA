#!/usr/bin/env python3
"""Intègre les récits Science (data/sc_src/*.json) : D.SCD, TH, YR, BLURB, FMT, FIN, couvertures."""
import json,glob,os,subprocess,sys
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
C=os.path.join(R,'data','content.json');CV=os.path.join(R,'data','covers.json')
d=json.load(open(C));cv=json.load(open(CV))
for k in('TH','YR','FMT','FIN','BLURB'):d.setdefault(k,{})
D=[]
# (haut, bas, clair, accent, formes)
def S(i,top,bot,lt,ac,shapes):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300"><defs><linearGradient id="g%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs><rect width="200" height="300" fill="url(#g%s)"/><circle cx="100" cy="112" r="70" fill="%s" opacity=".9"/>%s</svg>'%(i,top,bot,i,lt,shapes))
def c(x,y,r,f,o=1):return '<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>'%(x,y,r,f,o)
def r(x,y,w,h,f,rx=0,t=''):return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"%s/>'%(x,y,w,h,rx,f,(' transform="%s"'%t if t else ''))
def e(x,y,rx,ry,f,o=1):return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" opacity="%s"/>'%(x,y,rx,ry,f,o)
def p(dd,s,w,f='none',t=''):return '<path d="%s" stroke="%s" stroke-width="%s" fill="%s" stroke-linecap="round"%s/>'%(dd,s,w,f,(' transform="%s"'%t if t else ''))
def pg(pts,f,t=''):return '<polygon points="%s" fill="%s"%s/>'%(pts,f,(' transform="%s"'%t if t else ''))
COV={
'sc01':('#1F4E5F','#06141A','#DDF1F2','#7FD1D6', e(100,170,62,18,'#F4FAFA')+e(100,166,50,11,'#7FD1D6')+r(62,100,28,70,'#F4D9C6',12,'rotate(-12 76 135)')+r(110,100,28,70,'#F4D9C6',12,'rotate(12 124 135)')+c(84,214,6,'#7FD1D6')+c(116,224,5,'#7FD1D6')+c(100,238,7,'#7FD1D6')+r(40,252,120,6,'#F4FAFA',3)),
'sc02':('#7A3B1D','#120704','#F6E0C4','#E0A458', r(92,86,16,130,'#2B1608',3)+r(70,86,60,12,'#2B1608',4)+p('M108 100 L170 70','#2B1608',8)+c(170,70,8,'#E0A458')+p('M70 98 L70 150','#2B1608',6)+e(100,222,46,10,'#E0A458',.6)+e(100,222,28,6,'#F6E0C4',.7)+c(60,252,5,'#E0A458')+c(100,258,5,'#E0A458')+c(140,252,5,'#E0A458')),
'sc03':('#1E5C4A','#06130F','#D8EEDF','#F0C060', pg('30,120 96,100 104,150 84,190 40,180','#2E8B6A')+pg('112,104 174,124 168,184 128,198 120,150','#C9A24A')+p('M100 90 L100 240','#F4F7EE',3,'none')+c(100,262,5,'#F0C060')+p('M30 250 Q100 224 170 250','#F0C060',3)),
'sc04':('#5B2A74','#10061A','#F0E1F5','#F2C14E', ''.join(c(52+i*24,112+(i%2)*8,10,['#F2C14E','#C77AD6','#E8590C','#6C94E0'][i%4]) for i in range(6))+''.join(c(60+i*24,170-(i%2)*10,10,['#6C94E0','#F2C14E','#C77AD6','#E8590C'][i%4]) for i in range(5))+p('M40 220 Q100 170 160 220','#F0E1F5',3)+pg('160,220 148,208 150,228','#F0E1F5')+r(44,240,112,8,'#F2C14E',3)),
'sc05':('#2B2F4A','#07080F','#E6E8F5','#F4EFD6', r(48,58,104,104,'#0A0C16',2)+e(100,110,34,34,'#0A0C16',0)+c(100,110,36,'none')+'<circle cx="100" cy="110" r="36" fill="none" stroke="#F4EFD6" stroke-width="3"/><circle cx="100" cy="110" r="18" fill="none" stroke="#F4EFD6" stroke-width="2" opacity=".6"/>'+''.join(c(100+dx,110+dy,4,'#F4EFD6') for dx,dy in [(-24,-24),(24,-24),(-24,24),(24,24),(-40,-40),(40,-40),(-40,40),(40,40)])+r(70,200,60,50,'#F4EFD6',2,'rotate(-4 100 225)')),
'sc06':('#3B6B2E','#08140A','#E4F1D2','#F2D14E', ''.join(e(70+i*30,120+(i%2)*30,14,28,'#6FBF4E',.95)+c(70+i*30,112+(i%2)*30,5,'#E4F1D2') for i in range(3))+''.join(c(54+i*18,214,8,'#F2D14E' if i%2 else '#6FBF4E') for i in range(7))+p('M40 244 L160 244','#E4F1D2',3)),
'sc07':('#14183A','#03040C','#FFF4D6','#F6C85F', c(100,112,70,'#FFF4D6')+c(100,112,58,'#0A0B18')+p('M100 22 L100 6','#FFF4D6',3)+p('M170 112 L194 112','#FFF4D6',3)+p('M30 112 L6 112','#FFF4D6',3)+p('M150 62 L168 46','#FFF4D6',3)+p('M50 62 L32 46','#FFF4D6',3)+c(60,222,4,'#F6C85F')+c(100,232,4,'#F6C85F')+c(140,222,4,'#F6C85F')+p('M60 252 Q100 236 140 252','#F6C85F',2)),
'sc08':('#6B1F2E','#14050A','#F7DCE0','#E58BA0', e(100,150,64,64,'#FBEAEC',.15)+'<circle cx="100" cy="150" r="64" fill="none" stroke="#F7DCE0" stroke-width="3"/>'+''.join(c(100+dx,150+dy,s,'#E58BA0',.9) for dx,dy,s in [(-24,-20,12),(10,-34,9),(30,0,14),(-10,12,10),(-34,26,8),(20,34,9),(0,-8,6)])+r(72,238,56,8,'#F7DCE0',3)),
'sc09':('#16294F','#030812','#DCE6FA','#F5E27A', c(100,112,0,'#000')+p('M30 230 Q100 90 170 60','#F5E27A',2.5)+''.join(c(x,y,s,'#F5E27A') for x,y,s in [(40,222,4),(66,190,5),(92,160,7),(122,120,9),(150,84,12)])+''.join(c(x,y,2,'#DCE6FA') for x,y in [(40,60),(70,90),(160,200),(30,150)])+r(36,252,128,3,'#DCE6FA',1)),
'sc10':('#13595E','#03161A','#D6F4F0','#FF7A59', p('M30 110 Q65 40 100 110 T170 110','#FF7A59',6)+p('M30 150 Q65 220 100 150 T170 150','#D6F4F0',6)+''.join(c(x,130,5,'#F5E27A') for x in [48,82,118,152])+r(62,226,76,28,'#D6F4F0',14)+r(70,234,60,12,'#13595E',6)),
'sc11':('#27496B','#050D18','#E1EEF8','#F2A33A', c(100,112,34,'#F2A33A')+c(100,112,24,'#FFD27A')+p('M100 112 L100 80 M100 112 L128 112 M100 112 L100 144 M100 112 L72 112','#F2A33A',2)+pg('36,212 164,212 146,252 54,252','#6B3A1C')+r(98,150,4,62,'#E1EEF8')+pg('102,156 140,196 102,196','#E1EEF8')+p('M20 262 Q60 250 100 262 T180 262','#8FB8D8',3)),
'sc12':('#4A2B6E','#0B0614','#EADFF7','#6FE0C3', c(100,100,26,'#6FE0C3')+c(60,170,22,'#EADFF7')+c(140,170,22,'#EADFF7')+p('M88 124 L68 150','#EADFF7',3)+p('M112 124 L132 150','#EADFF7',3)+p('M40 220 L160 220','#6FE0C3',4)+''.join(c(50+i*25,244,3,'#6FE0C3') for i in range(5))),
'sc13':('#6A4B1C','#130C03','#F6E6C6','#9CCFE8', e(76,170,40,30,'#D9A04A')+e(76,160,34,18,'#E8BA6A')+pg('130,100 150,100 160,200 120,200','#9CCFE8')+r(130,80,20,24,'#9CCFE8',3)+p('M122 150 L158 150','#F6E6C6',2)+''.join(c(140+(i%2)*6,126+i*12,3,'#F6E6C6') for i in range(3))+r(36,236,128,8,'#F6E6C6',3)),
'sc14':('#1B2B5E','#03060F','#D9E3FA','#5EA8FF', c(100,112,36,'#5EA8FF')+'<ellipse cx="100" cy="112" rx="84" ry="26" fill="none" stroke="#D9E3FA" stroke-width="2" transform="rotate(-18 100 112)"/>'+c(172,92,6,'#D9E3FA')+p('M44 232 L150 206','#D9E3FA',4)+pg('150,206 140,198 140,214','#D9E3FA')+r(36,238,70,6,'#5EA8FF',3)+''.join(c(x,y,2,'#D9E3FA') for x,y in [(30,40),(170,40),(40,180),(165,170)])),
'sc15':('#2B4A5E','#060F14','#DDF3F7','#FF8A3D', pg('78,70 122,70 122,130 160,222 40,222 78,130','#DDF3F7',)+pg('62,190 138,190 160,222 40,222','#FF8A3D')+r(94,50,12,110,'#9AA7AE',2)+''.join(c(x,y,s,'#FFFFFF',.9) for x,y,s in [(84,170,5),(110,160,4),(98,146,3)])+r(60,240,80,8,'#DDF3F7',3)),
'sc16':('#6B2410','#120503','#FFE1A8','#FF6B2C', c(100,112,52,'#FF6B2C')+c(100,112,40,'#FFD27A')+p('M146 70 Q190 40 176 12','#FFE1A8',5)+p('M52 76 Q20 50 30 20','#FFE1A8',4)+p('M30 230 L170 230','#FFE1A8',3)+r(50,200,6,50,'#FFE1A8')+r(144,200,6,50,'#FFE1A8')+p('M30 214 Q100 244 170 214','#FFE1A8',2)),
'sc17':('#1B2E4A','#040810','#DCEBFF','#7AE0FF', ''.join(p('M20 %s L180 %s'%(90+i*18,90+i*18),'#7AE0FF',2.5) for i in range(5))+''.join(c(150-i*18,90+i*18,4,'#FFFFFF') for i in range(5))+'<circle cx="100" cy="232" r="22" fill="none" stroke="#DCEBFF" stroke-width="3"/>'+p('M100 232 L100 218 M100 232 L112 238','#DCEBFF',3)),
'sc18':('#3C3C3C','#0A0A0A','#F0EDE6','#E8B04A', ''.join(r(40+i*18,170-i*14,12,20+i*14,'#E8B04A' if i<6 else '#C0392B',2) for i in range(7))+r(40,196,128,6,'#F0EDE6',2)+'<circle cx="100" cy="64" r="24" fill="none" stroke="#F0EDE6" stroke-width="4"/>'+p('M100 64 L116 48','#C0392B',4)+r(72,230,56,20,'#F0EDE6',4)),
}
for f in sorted(glob.glob(os.path.join(R,'data','sc_src','sc*.json'))):
    i=os.path.basename(f)[:-5]
    if subprocess.run([sys.executable,os.path.join(R,'tools','v4_check.py'),i],capture_output=True).returncode and 0:continue
    x=json.load(open(f))
    D.append({'id':i,'name':x['name'],'sub':x['sub'],'dates':x['dates'],'country':x['country'],'job':x['job'],'src':' || '.join(x['src']),'body':x['body']})
    d['TH'][i]='science';d['YR'][i]=x['yr'];d['BLURB'][i]=x['blurb'];d['FMT'][i]=x['fmt'];d['FIN'][i]={'n':x['note']}
    t,b,lt,ac,sh=COV[i];cv[i]=S(i,t,b,lt,ac,sh)
d_=d['D'];d_['SCD']=D
json.dump(d,open(C,'w'),ensure_ascii=False,separators=(',',':'))
json.dump(cv,open(CV,'w'),ensure_ascii=False,separators=(',',':'))
print(len(D),'récits Science intégrés')
