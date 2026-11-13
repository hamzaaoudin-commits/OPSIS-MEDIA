#!/usr/bin/env python3
"""Génère les scènes illustrées (SVG 430x1500) des parcours de découverte."""
import random, math, sys, json
W,H=430,1500
def R(seed): return random.Random(seed)
def f(x): return ('%.1f'%x).rstrip('0').rstrip('.')
def svg(inner,defs=''):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" preserveAspectRatio="xMidYMin slice"><defs>%s'
            '<filter id="gr" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .055 0"/></filter>'
            '</defs>%s<rect width="%d" height="%d" filter="url(#gr)"/></svg>')%(W,H,W,H,defs,inner,W,H)
def stars(seed,n,y0,y1,col='#fff',rmax=1.4,op=.9):
    r=R(seed);o=''
    for _ in range(n):
        o+='<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>'%(f(r.uniform(0,W)),f(r.uniform(y0,y1)),f(r.uniform(.4,rmax)),col,f(r.uniform(.25,op)))
    return o
def lg(id,stops,x1=0,y1=0,x2=0,y2=1):
    return '<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s">%s</linearGradient>'%(id,x1,y1,x2,y2,''.join('<stop offset="%s" stop-color="%s" stop-opacity="%s"/>'%(s[0],s[1],s[2] if len(s)>2 else 1) for s in stops))
def rg(id,stops,cx=.5,cy=.5,r=.5):
    return '<radialGradient id="%s" cx="%s" cy="%s" r="%s">%s</radialGradient>'%(id,cx,cy,r,''.join('<stop offset="%s" stop-color="%s" stop-opacity="%s"/>'%(s[0],s[1],s[2] if len(s)>2 else 1) for s in stops))
def ridge(seed,y,amp,color,step=26,snow=None,base=H):
    r=R(seed);pts=[(0,y)];x=0
    while x<W+step:
        x+=step*r.uniform(.6,1.4);pts.append((x,y-r.uniform(0,amp)))
    d='M0 %d '%base+' '.join('L%s %s'%(f(a),f(b)) for a,b in pts)+' L%d %d Z'%(W+60,base)
    o='<path d="%s" fill="%s"/>'%(d,color)
    if snow:
        for (a,b) in pts:
            if b<y-amp*.55:
                o+='<path d="M%s %s l-11 15 l6 -4 l5 7 l5 -7 l6 4 z" fill="%s"/>'%(f(a),f(b),snow)
    return o
def gear(cx,cy,r,teeth,col,op=1,hole=.35):
    pts=[]
    for i in range(teeth*4):
        a=2*math.pi*i/(teeth*4);rr=r*(1.0 if i%4 in (1,2) else .86)
        pts.append('%s,%s'%(f(cx+rr*math.cos(a)),f(cy+rr*math.sin(a))))
    return '<polygon points="%s" fill="%s" opacity="%s"/><circle cx="%s" cy="%s" r="%s" fill="#000" opacity=".55"/>'%(' '.join(pts),col,op,f(cx),f(cy),f(r*hole))
def smoke(seed,x,y,n,col,op=.3):
    r=R(seed);o=''
    for i in range(n):
        o+='<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>'%(f(x+i*r.uniform(6,14)),f(y-i*r.uniform(18,28)),f(8+i*5),col,f(op*(1-i/n)))
    return o

# ---------------------------------------------------------------- 1. guerre froide
def gf():
    d=lg('sk',[(0,'#070d1a'),(.36,'#13203a'),(.5,'#2e1620'),(.52,'#0b0d14'),(1,'#06070b')])+rg('sun',[(0,'#ff6a4a',.95),(.45,'#d2232c',.5),(1,'#d2232c',0)])+lg('bm',[(0,'#fff',.0),(.15,'#cfe3ff',.22),(1,'#cfe3ff',0)])
    o='<rect width="430" height="1500" fill="url(#sk)"/>'
    o+=stars(1,90,0,500,'#cfe0ff',1.3,.8)
    o+='<circle cx="300" cy="420" r="230" fill="url(#sun)"/><circle cx="300" cy="420" r="92" fill="#e8483f"/><circle cx="300" cy="420" r="92" fill="none" stroke="#ff9a7a" stroke-width="2" opacity=".5"/>'
    for y in (384,406,428,450,470):
        dy=y+3-420;w=2*math.sqrt(max(0,92*92-dy*dy));o+='<rect x="%s" y="%d" width="%s" height="6" fill="#13203a" opacity=".9"/>'%(f(300-w/2),y,f(w))
    # satellite et orbite
    o+='<path d="M20 190 Q215 40 410 150" fill="none" stroke="#9fb4cc" stroke-width="1" stroke-dasharray="2 6" opacity=".6"/><circle cx="118" cy="120" r="9" fill="#b9c7d9"/><path d="M118 111v-26M118 129v26M109 120h-26M127 120h26" stroke="#b9c7d9" stroke-width="1.4"/>'
    # nuages
    for (y,op) in [(300,.5),(520,.35)]:
        o+='<path d="M0 %d Q60 %d 130 %d T260 %d T430 %d V%d H0Z" fill="#0b1426" opacity="%s"/>'%(y,y-26,y,y-10,y-30,y+40,op)
    # projecteurs
    o+='<polygon points="70,740 -40,0 120,0" fill="url(#bm)"/><polygon points="360,745 460,40 300,0" fill="url(#bm)" opacity=".8"/>'
    # mur, mirador, barbelés
    o+='<rect x="0" y="738" width="430" height="150" fill="#05060a"/>'
    for i in range(0,432,36): o+='<rect x="%d" y="742" width="35" height="62" fill="#161b27"/><rect x="%d" y="744" width="35" height="2" fill="#2a3346"/>'%(i,i)
    o+='<rect x="52" y="640" width="46" height="100" fill="#0a0d14"/><rect x="44" y="620" width="62" height="26" fill="#0a0d14"/><polygon points="40,620 75,596 110,620" fill="#05060a"/><rect x="56" y="628" width="38" height="10" fill="#ffcf6a"/><rect x="56" y="628" width="38" height="10" fill="#ffcf6a" opacity=".5" filter="url(#gr)"/>'
    o+='<path d="M0 736 '+' '.join('l9 -9 l9 9' for _ in range(48))+'" fill="none" stroke="#7d8aa0" stroke-width="1.2"/>'
    for x in (150,260,360): o+='<rect x="%d" y="700" width="3" height="40" fill="#0a0d14"/><circle cx="%d" cy="698" r="5" fill="#ffe9a8"/><circle cx="%d" cy="698" r="20" fill="#ffe9a8" opacity=".12"/>'%(x,x+1,x+1)
    # carte (graticule) en bas
    r=R(11)
    for i in range(9):
        y=900+i*60;o+='<path d="M0 %d Q215 %d 430 %d" fill="none" stroke="#d2232c" stroke-width="1" opacity="%s"/>'%(y,y+r.uniform(-40,40),y+r.uniform(-30,30),f(.28-i*.02))
    for i in range(7):
        x=i*72;o+='<path d="M%d 880 Q%d 1180 %d 1500" fill="none" stroke="#9fb4cc" stroke-width=".8" opacity=".14"/>'%(x,x+r.uniform(-50,50),x+r.uniform(-90,90))
    for (x,y,rr) in [(120,1010,70),(310,1230,95)]:
        for k in (1,2,3): o+='<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#e0434b" stroke-width="1" opacity="%s"/>'%(x,y,rr*k//3,f(.35-k*.07))
        o+='<path d="M%d %d L%d %d" stroke="#e0434b" stroke-width="1.5" opacity=".4"/><circle cx="%d" cy="%d" r="4" fill="#e0434b"/>'%(x,y,x+rr*.7,y-rr*.7,x,y)
    o+=stars(3,60,880,1500,'#fff',1.6,.5)
    return svg(o,d)

# ---------------------------------------------------------------- 2. art du faux
def frame(x,y,w,h,ang,art,seed):
    r=R(seed);o='<g transform="rotate(%s %s %s)">'%(ang,f(x+w/2),f(y+h/2))
    o+='<rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="url(#gold)"/>'%(f(x),f(y),f(w),f(h))
    o+='<rect x="%s" y="%s" width="%s" height="%s" fill="#3a2410"/>'%(f(x+9),f(y+9),f(w-18),f(h-18))
    o+='<rect x="%s" y="%s" width="%s" height="%s" fill="#150e07"/>'%(f(x+16),f(y+16),f(w-32),f(h-32))
    ix,iy,iw,ih=x+16,y+16,w-32,h-32
    if art==0:  # blocs façon Rothko
        o+='<rect x="%s" y="%s" width="%s" height="%s" fill="#8a2b22"/><rect x="%s" y="%s" width="%s" height="%s" fill="#c9622a"/>'%(f(ix+8),f(iy+8),f(iw-16),f(ih*.46),f(ix+8),f(iy+ih*.52),f(iw-16),f(ih*.4))
    elif art==1:  # perle
        o+='<rect x="%s" y="%s" width="%s" height="%s" fill="#27406a"/><circle cx="%s" cy="%s" r="%s" fill="#f1ead8"/><circle cx="%s" cy="%s" r="%s" fill="#c98a3a"/>'%(f(ix),f(iy),f(iw),f(ih),f(ix+iw/2),f(iy+ih*.5),f(min(iw,ih)*.2),f(ix+iw/2),f(iy+ih*.8),f(min(iw,ih)*.28))
    elif art==2:  # paysage
        o+='<rect x="%s" y="%s" width="%s" height="%s" fill="#6e8aa0"/><path d="M%s %s L%s %s L%s %s L%s %s Z" fill="#3c5a3c"/>'%(f(ix),f(iy),f(iw),f(ih),f(ix),f(iy+ih),f(ix+iw*.35),f(iy+ih*.5),f(ix+iw*.7),f(iy+ih*.75),f(ix+iw),f(iy+ih))
    else:  # craquelures
        o+='<rect x="%s" y="%s" width="%s" height="%s" fill="#7a5a30"/>'%(f(ix),f(iy),f(iw),f(ih))
        for _ in range(7):
            a=r.uniform(0,iw);b=r.uniform(0,ih)
            o+='<path d="M%s %s l%s %s l%s %s l%s %s" stroke="#1a0f05" stroke-width="1" fill="none"/>'%(f(ix+a),f(iy+b),f(r.uniform(-18,18)),f(r.uniform(6,22)),f(r.uniform(-18,18)),f(r.uniform(6,22)),f(r.uniform(-14,14)),f(r.uniform(6,18)))
    for cx,cy in [(x+5,y+5),(x+w-5,y+5),(x+5,y+h-5),(x+w-5,y+h-5)]:
        o+='<circle cx="%s" cy="%s" r="6" fill="#f3d58a"/>'%(f(cx),f(cy))
    return o+'</g>'
def faux():
    d=lg('wl',[(0,'#2d1c0b'),(.5,'#1c1208'),(1,'#0b0805')])+lg('gold',[(0,'#f3d58a'),(.5,'#b8873a'),(1,'#6d4a1c')],0,0,1,1)+lg('cone',[(0,'#ffe9b0',.28),(1,'#ffe9b0',0)])
    o='<rect width="430" height="1500" fill="url(#wl)"/>'
    r=R(5)
    for y in range(0,1500,90): o+='<path d="M0 %d H430" stroke="#000" stroke-width="1" opacity=".18"/>'%y
    spots=[(20,430,120,150,-3,0,60),(250,370,160,200,2,1,61),(30,640,150,110,-4,2,62),(215,790,175,135,3,0,63),(30,860,110,150,2,3,64),(270,1050,130,170,-3,1,65),(60,1120,170,120,3,2,66),(240,1280,150,110,-2,3,67),(40,1340,120,150,3,0,68)]
    for (x,y,w,h,a,art,sd) in spots:
        o+=frame(x,y,w,h,a,art,sd)
    for (x,w) in [(80,170),(300,190)]:
        o+='<polygon points="%d,0 %d,0 %d,520 %d,520" fill="url(#cone)"/><ellipse cx="%d" cy="0" rx="14" ry="6" fill="#ffe9b0" opacity=".7"/>'%(x-6,x+6,x+w//2+90,x-w//2-90,x)
    # loupe
    o+='<g transform="rotate(35 330 220)"><rect x="318" y="300" width="24" height="120" rx="10" fill="#6d4a1c"/><circle cx="330" cy="230" r="104" fill="none" stroke="url(#gold)" stroke-width="14"/><circle cx="330" cy="230" r="96" fill="#e8c27a" opacity=".12"/></g><path d="M268 190 Q285 150 330 140" stroke="#fff" stroke-width="4" fill="none" opacity=".45" stroke-linecap="round"/>'
    # craquelures dans la loupe
    for _ in range(8): o+='<path d="M%s %s l%s %s l%s %s" stroke="#fff" stroke-width=".9" fill="none" opacity=".35"/>'%(f(270+r.uniform(0,120)),f(170+r.uniform(0,120)),f(r.uniform(-20,20)),f(r.uniform(8,26)),f(r.uniform(-20,20)),f(r.uniform(8,22)))
    # plaque, étiquettes
    return svg(o,d)

# ---------------------------------------------------------------- 3. extrêmes
def extremes():
    d=lg('c',[(0,'#010208'),(.12,'#050b1f'),(.2,'#0c2a52'),(.34,'#a9d6ee'),(.42,'#5d93b8'),(.5,'#0d3b66'),(.64,'#082a4a'),(.8,'#041424'),(1,'#02060d')])+rg('earth',[(0,'#3d86d6'),(.8,'#143c78'),(1,'#0a1d44')],.5,.4,.6)+lg('au',[(0,'#6dffb0',0),(.5,'#6dffb0',.45),(1,'#8a6dff',0)])
    o='<rect width="430" height="1500" fill="url(#c)"/>'
    o+=stars(7,140,0,300,'#fff',1.5,.95)
    # Terre vue de l'espace
    o+='<circle cx="215" cy="610" r="470" fill="url(#earth)"/><path d="M-255 610 A470 470 0 0 1 685 610" fill="none" stroke="#9fe0ff" stroke-width="3" opacity=".7"/><circle cx="215" cy="610" r="478" fill="none" stroke="#6ab8ff" stroke-width="10" opacity=".14"/>'
    o+='<path d="M60 170 Q120 140 190 175 T330 160 M110 205 Q210 185 300 215" stroke="#fff" stroke-width="5" fill="none" opacity=".25" stroke-linecap="round"/>'
    # fusée / station
    o+='<g transform="translate(335 90) rotate(25)"><rect x="-5" y="-26" width="10" height="46" rx="5" fill="#e8eef6"/><polygon points="-5,-26 5,-26 0,-40" fill="#d2232c"/><polygon points="-5,12 -14,24 -5,20" fill="#d2232c"/><polygon points="5,12 14,24 5,20" fill="#d2232c"/><polygon points="-4,20 4,20 0,44" fill="#ffb347" opacity=".9"/></g>'
    # sommets
    o+=ridge(21,520,150,'#8fb2cf',34,'#fff')+ridge(22,585,120,'#4c7596',30,'#e8f2fa')+ridge(23,640,80,'#274a6a',26)
    o+=''
    # banquise + aurore
    o+='<path d="M-20 620 Q120 560 240 590 T450 570 V700 H-20Z" fill="url(#au)" opacity=".7"/><path d="M-20 700 Q140 650 260 680 T450 650 V760 H-20Z" fill="url(#au)" opacity=".5"/>'
    for (x,y,w) in [(30,790,130),(210,770,170),(110,850,150),(290,840,120)]:
        o+='<path d="M%d %d l%d -22 l%d 12 l%d -8 l%d 24 z" fill="#d6eefa" opacity=".9"/><path d="M%d %d l%d 22 l-%d 8 l-%d -6z" fill="#4c7ea0" opacity=".6"/>'%(x,y,w*.25,w*.3,w*.25,w*.2,x,y,w*.35,w*.2,w*.1)
    # océan + navire
    o+='<rect y="900" width="430" height="260" fill="#0a3a64" opacity=".0"/>'
    for i in range(9):
        y=930+i*26;o+='<path d="M-10 %d Q30 %d 70 %d T150 %d T230 %d T310 %d T390 %d T470 %d" fill="none" stroke="#7fc4ef" stroke-width="1.4" opacity="%s"/>'%(y,y-9,y,y-9,y,y-9,y,y,f(.5-i*.045))
    o+='<g transform="translate(215 905)"><path d="M-58 8 Q0 36 58 8 L46 -6 H-46 Z" fill="#0a0d14"/><path d="M-2 -6 V-96" stroke="#0a0d14" stroke-width="3"/><path d="M-2 -90 L40 -66 L-2 -34 Z" fill="#f1ead8"/><path d="M-2 -60 L-38 -44 L-2 -24 Z" fill="#f1ead8" opacity=".9"/><path d="M-2 -96 l16 5 l-16 5" fill="#d2232c"/></g>'
    o+='<ellipse cx="215" cy="960" rx="110" ry="6" fill="#ffe9b0" opacity=".25"/>'
    # abysses
    r=R(9)
    for _ in range(46): 
        x=r.uniform(0,W);y=r.uniform(1180,1500);rr=r.uniform(1.5,6);o+='<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#7fd4ff" stroke-width="1" opacity="%s"/>'%(f(x),f(y),f(rr),f(r.uniform(.15,.5)))
    o+='<g transform="translate(130 1260)"><ellipse rx="40" ry="22" fill="#e0a82e"/><circle cx="12" cy="-4" r="9" fill="#bfeaff"/><circle cx="12" cy="-4" r="9" fill="#bfeaff" opacity=".6"/><rect x="-46" y="-3" width="10" height="6" fill="#e0a82e"/><polygon points="12,-4 -30,-60 120,-40" fill="#bfeaff" opacity=".08"/></g>'
    o+='<g transform="translate(330 1390)"><path d="M0 0 Q30 -24 60 0 Q30 14 0 0Z" fill="#0b1a2a"/><path d="M40 -8 Q50 -34 62 -28" stroke="#0b1a2a" stroke-width="3" fill="none"/><circle cx="62" cy="-28" r="5" fill="#9bff6a"/><circle cx="62" cy="-28" r="18" fill="#9bff6a" opacity=".2"/></g>'
    return svg(o,d)

# ---------------------------------------------------------------- 4. géants
def geants():
    d=lg('c',[(0,'#1b1420'),(.2,'#5a2a1a'),(.36,'#c4612a'),(.44,'#e89a4e'),(.45,'#1d1410'),(1,'#0a0908')])+rg('sun',[(0,'#ffd08a',.95),(1,'#ffd08a',0)])
    o='<rect width="430" height="1500" fill="url(#c)"/>'
    o+='<circle cx="120" cy="540" r="190" fill="url(#sun)"/><circle cx="120" cy="560" r="58" fill="#ffe0a8"/>'
    o+=gear(380,160,110,16,'#3a2418',.9)+gear(300,310,64,12,'#52301c',.8)+gear(40,360,70,12,'#42261a',.8)
    # skyline derrière
    r=R(31);x=0
    while x<W:
        w=r.uniform(26,50);h=r.uniform(60,180);o+='<rect x="%s" y="%s" width="%s" height="%s" fill="#6b3a22" opacity=".7"/>'%(f(x),f(620-h),f(w),f(h+50));x+=w+r.uniform(0,4)
    # cheminées + fumées
    for (cx,hh) in [(60,150),(330,190),(250,120)]:
        o+='<rect x="%d" y="%d" width="22" height="%d" fill="#17100c"/><rect x="%d" y="%d" width="30" height="8" fill="#2a1a12"/>'%(cx,640-hh,hh+20,cx-4,640-hh)+smoke(cx,cx+11,640-hh,7,'#2a1c16',.7)
    # gratte-ciel central éclairé
    o+='<rect x="168" y="330" width="62" height="330" fill="#120d0b"/><polygon points="168,330 199,296 230,330" fill="#120d0b"/><rect x="198" y="270" width="2" height="30" fill="#120d0b"/>'
    for i in range(14):
        for j in range(3):
            if r.random()>.35: o+='<rect x="%d" y="%d" width="10" height="10" fill="#ffd36a" opacity="%s"/>'%(176+j*18,345+i*22,f(r.uniform(.5,1)))
    # usine premier plan
    x=0
    while x<W:
        w=r.uniform(40,70);h=r.uniform(40,90);o+='<polygon points="%s,%s %s,%s %s,%s %s,%s" fill="#0a0807"/>'%(f(x),f(700),f(x),f(660-h*.4),f(x+w),f(640-h*.6),f(x+w),f(700));x+=w
    o+='<rect y="700" width="430" height="800" fill="#0a0908"/>'
    # plan technique
    for i in range(0,430,40): o+='<path d="M%d 720 V1500" stroke="#4a8fd0" stroke-width=".6" opacity=".16"/>'%i
    for j in range(720,1500,40): o+='<path d="M0 %d H430" stroke="#4a8fd0" stroke-width=".6" opacity=".16"/>'%j
    o+='<g fill="none" stroke="#6fb0f0" stroke-width="1.4" opacity=".42"><circle cx="110" cy="900" r="60"/><circle cx="110" cy="900" r="38"/><path d="M30 900 H190 M110 820 V980"/><rect x="250" y="840" width="130" height="110" rx="4"/><path d="M250 870 H380"/><circle cx="315" cy="1150" r="80"/><circle cx="315" cy="1150" r="52"/><path d="M60 1100 h120 v110 h-120z M60 1140 h120"/><path d="M200 1320 h190" marker-end="url(#ar)"/></g>'
    o+='<g stroke="#6fb0f0" stroke-width="1" opacity=".4"><path d="M30 1050 H190 M30 1044 v12 M190 1044 v12"/><path d="M240 1300 H390 M240 1294 v12 M390 1294 v12"/></g>'
    for i in range(36): o+='<circle cx="%s" cy="%s" r="2.4" fill="#e89a4e" opacity=".5"/>'%(f(r.uniform(10,420)),f(r.uniform(740,1480)))
    o+=gear(330,1400,90,14,'#e89a4e',.12)+gear(60,1330,52,10,'#e89a4e',.1)
    return svg(o,d)

# ---------------------------------------------------------------- 5. révolution
def revolution():
    d=lg('c',[(0,'#1a0610'),(.25,'#4a0e1c'),(.42,'#7a1624'),(.46,'#0e0a14'),(1,'#06060f')])+rg('gl',[(0,'#ff8a5a',.5),(1,'#ff8a5a',0)])+lg('gd',[(0,'#f3d58a'),(1,'#b8873a')])+lg('fd',[(0,'#fff'),(.6,'#fff'),(1,'#000')])
    o='<rect width="430" height="1500" fill="url(#c)"/>'
    r=R(41)
    for i in range(7):
        y=60+i*56;o+='<path d="M-20 %d Q80 %d 200 %d T450 %d V%d H-20Z" fill="#12060c" opacity="%s"/>'%(y,y-30,y+10,y-18,y+120,f(.22+i*.06))
    o+='<circle cx="215" cy="560" r="260" fill="url(#gl)"/>'
    # drapeau tricolore ondulant
    o+='<mask id="fm"><rect width="430" height="400" fill="url(#fd)"/></mask><g mask="url(#fm)">'
    for k,(col,off) in enumerate([('#2b5db8',0),('#f2efe6',40),('#d2232c',80)]):
        o+='<path d="M%d 0 Q%d 120 %d 240 Q%d 330 %d 400 L%d 400 Q%d 330 %d 240 Q%d 120 %d 0Z" fill="%s" opacity=".5"/>'%(250+off,300+off,230+off,260+off,300+off,340+off,300+off,270+off,350+off,290+off,col)
    o+='</g>'
    # balance de la justice
    o+='<g stroke="url(#gd)" stroke-width="4" fill="none" opacity=".85" transform="translate(110 130)"><path d="M0 0 V150 M-50 150 H50 M-100 30 H100"/><path d="M-100 30 L-130 100 H-70 Z M100 30 L70 100 H130 Z"/><circle cx="0" cy="-8" r="9" fill="#f3d58a"/></g>'
    # palais de justice
    o+='<rect x="30" y="610" width="370" height="30" fill="#0c0810"/><polygon points="20,610 215,520 410,610" fill="#0c0810"/><polygon points="62,602 215,534 368,602" fill="none" stroke="#7a1624" stroke-width="2"/>'
    for i in range(7):
        x=50+i*52;o+='<rect x="%d" y="640" width="26" height="200" fill="#0c0810"/><rect x="%d" y="636" width="34" height="9" fill="#17101e"/><rect x="%d" y="838" width="34" height="9" fill="#17101e"/>'%(x,x-4,x-4)
    for i in range(6):
        x=76+i*52;o+='<rect x="%d" y="660" width="26" height="160" fill="#ffb25a" opacity="%s"/>'%(x,f(.5+.1*(i%3)))
    for k in range(6): o+='<rect x="%d" y="%d" width="%d" height="14" fill="#17101e"/>'%(20+k*6,846+k*14,390-k*12)
    # torches
    for x in (36,394): o+='<rect x="%d" y="760" width="5" height="60" fill="#0c0810"/><path d="M%d 760 q-9 -22 2 -40 q12 18 4 40z" fill="#ffb25a"/><circle cx="%d" cy="745" r="38" fill="#ffb25a" opacity=".16"/>'%(x,x,x+2)
    # foule, silhouettes
    for row,(y,sc,col) in enumerate([(960,1,'#0a0710'),(1060,1.2,'#08060d'),(1170,1.5,'#06050a')]):
        x=-10
        while x<W+20:
            w=r.uniform(26,40)*sc;o+='<circle cx="%s" cy="%s" r="%s" fill="%s"/><path d="M%s %s q%s -%s %s 0 v200 h-%s z" fill="%s"/>'%(f(x),f(y),f(9*sc),col,f(x-w/2),f(y+10*sc),f(w/2),f(18*sc),f(w),f(w),col);x+=w*.9
            if r.random()>.8: o+='<rect x="%s" y="%s" width="2" height="%s" fill="%s"/><path d="M%s %s l22 6 l-22 8z" fill="#d2232c"/>'%(f(x),f(y-60*sc),f(60*sc),col,f(x),f(y-60*sc))
    # papiers, plume
    for i in range(14): o+='<g transform="translate(%s %s) rotate(%s)" opacity=".18"><rect width="22" height="30" fill="#f2efe6"/><path d="M4 8h14M4 14h14M4 20h10" stroke="#222" stroke-width="1.2"/></g>'%(f(r.uniform(10,400)),f(r.uniform(1240,1480)),f(r.uniform(-30,30)))
    o+=stars(5,40,0,180,'#fff',1.2,.5)
    return svg(o,d)

# ---------------------------------------------------------------- 6. évasion
def evasion():
    d=lg('c',[(0,'#04100c'),(.3,'#0b2a1f'),(.5,'#0a1a16'),(1,'#030605')])+rg('mn',[(0,'#e8f6e0',.5),(1,'#e8f6e0',0)])+lg('bm',[(0,'#d6ffd8',.34),(1,'#d6ffd8',0)],0,0,1,0)+rg('lamp',[(0,'#ffd88a',.9),(1,'#ffd88a',0)])
    o='<rect width="430" height="1500" fill="url(#c)"/>'+stars(2,90,0,420,'#e8f6e0',1.2,.7)
    o+='<circle cx="330" cy="190" r="170" fill="url(#mn)"/><circle cx="330" cy="190" r="56" fill="#eaf7e2"/><circle cx="314" cy="176" r="10" fill="#c9dccb" opacity=".6"/><circle cx="344" cy="206" r="14" fill="#c9dccb" opacity=".5"/>'
    for (x,y) in [(60,150),(110,200),(40,230)]: o+='<path d="M%d %d q8 -8 14 0 q6 -8 14 0" fill="none" stroke="#0a1a16" stroke-width="2.4"/>'%(x,y)
    # toits de Venise lointains
    r=R(51);x=0
    while x<W:
        w=r.uniform(24,44);h=r.uniform(20,50);o+='<polygon points="%s,560 %s,%s %s,%s %s,560" fill="#0a1d17"/>'%(f(x),f(x),f(560-h),f(x+w/2),f(540-h),f(x+w));x+=w
    o+='<rect x="355" y="470" width="14" height="92" fill="#0a1d17"/><polygon points="350,470 362,440 374,470" fill="#0a1d17"/>'
    # mur de prison
    o+='<rect y="600" width="430" height="210" fill="#0a0f0d"/>'
    for j in range(0,210,14):
        o+='<path d="M0 %d H430" stroke="#17241f" stroke-width="1"/>'%(612+j)
    for j in range(15):
        for i in range(0,432,40): o+='<path d="M%d %d v14" stroke="#17241f" stroke-width="1"/>'%(i+(20 if j%2 else 0),612+j*14)
    # mirador et faisceau
    o+='<rect x="40" y="478" width="54" height="124" fill="#07100c"/><rect x="30" y="456" width="74" height="30" fill="#07100c"/><polygon points="26,456 67,430 108,456" fill="#050a08"/><rect x="48" y="464" width="38" height="10" fill="#ffd88a"/>'
    o+='<polygon points="94,470 560,640 560,300" fill="url(#bm)" transform="rotate(-8 94 470)"/><polygon points="94,470 560,720 560,560" fill="url(#bm)" opacity=".55"/>'
    # barbelés
    o+='<path d="M0 598 '+' '.join('q5 -14 10 0 q5 14 10 0' for _ in range(22))+'" fill="none" stroke="#7a8a82" stroke-width="1.6"/>'
    for x in range(0,430,60): o+='<rect x="%d" y="572" width="3" height="30" fill="#07100c"/>'%x
    # échelle de corde
    o+='<g stroke="#c9a46a" stroke-width="3" opacity=".9"><path d="M250 596 V840 M274 596 V840"/>'+''.join('<path d="M250 %d H274"/>'%(612+i*20) for i in range(12))+'</g>'
    # sol + tunnel en coupe
    o+='<rect y="810" width="430" height="690" fill="#0a0907"/><path d="M0 812 H430" stroke="#1c2a22" stroke-width="3"/>'
    for i in range(30): o+='<rect x="%s" y="%s" width="%s" height="%s" fill="#14100c"/>'%(f(r.uniform(0,420)),f(r.uniform(830,1480)),f(r.uniform(6,20)),f(r.uniform(4,10)))
    o+='<path d="M-10 1000 H300 Q330 1000 330 1040 V1070 H-10Z" fill="#030302"/><rect x="-10" y="996" width="320" height="5" fill="#5a3f22"/><rect x="-10" y="1068" width="340" height="5" fill="#5a3f22"/>'
    for x in range(30,330,60): o+='<rect x="%d" y="996" width="8" height="76" fill="#5a3f22"/>'%x
    o+='<circle cx="360" cy="1050" r="70" fill="url(#lamp)"/><circle cx="360" cy="1050" r="10" fill="#ffe9b0"/><path d="M345 1038 q15 -22 30 0" stroke="#9a7a3a" stroke-width="2" fill="none"/>'
    o+='<path d="M10 1032 q40 -4 80 0 t80 0 t80 0" stroke="#e8c27a" stroke-width="2" fill="none" stroke-dasharray="1 8" opacity=".6"/>'
    # pelles / silhouette qui rampe
    o+='<path d="M60 1050 q20 -22 44 -8 l16 8 q-10 12 -30 8z" fill="#17100c"/>'
    # clés, grilles
    for x in (60,160,260,360):
        o+='<g stroke="#2a3a32" stroke-width="3" fill="none" opacity=".7"><rect x="%d" y="1180" width="60" height="90"/>'%x+''.join('<path d="M%d 1180 v90"/>'%(x+10+k*10) for k in range(5))+'</g>'
    for i in range(24): o+='<circle cx="%s" cy="%s" r="1.6" fill="#d6ffd8" opacity="%s"/>'%(f(r.uniform(0,430)),f(r.uniform(1300,1500)),f(r.uniform(.1,.4)))
    return svg(o,d)

# ---------------------------------------------------------------- 7. chute
def chute():
    d=lg('c',[(0,'#3a1410'),(.22,'#7a2a1a'),(.4,'#2a1210'),(.6,'#14090a'),(1,'#070405')])+rg('sun',[(0,'#ffcf7a',.9),(1,'#ffcf7a',0)])+lg('bar',[(0,'#f6c96a'),(1,'#a8541e')])+lg('ash',[(0,'#6e5a56',0),(.15,'#6e5a56',.5),(1,'#241a19',.3)])
    o='<rect width="430" height="1500" fill="url(#c)"/>'
    o+='<circle cx="320" cy="300" r="240" fill="url(#sun)"/><circle cx="320" cy="300" r="62" fill="#ffe6a8"/>'
    # escalier ascendant (barres)
    xs=[24,88,152,216,280];hs=[110,170,240,330,430]
    for x,h in zip(xs,hs): o+='<rect x="%d" y="%d" width="52" height="%d" fill="url(#bar)" opacity=".95"/><rect x="%d" y="%d" width="52" height="4" fill="#fff3c8" opacity=".6"/>'%(x,720-h,h,x,720-h)
    # couronne au sommet
    # barres qui se brisent et tombent
    r=R(71)
    for k,(x,h) in enumerate([(344,360),(388,300)]):
        y=720-h+k*20
        o+='<g transform="rotate(%s %s %s)"><rect x="%d" y="%d" width="40" height="%d" fill="url(#bar)" opacity=".8"/></g>'%(14+k*10,x,y,x,y,h)
    # éclats de verre qui chutent
    for i in range(40):
        x=r.uniform(150,430);y=r.uniform(380,1100);s=r.uniform(8,34);a=r.uniform(0,360)
        o+='<polygon transform="rotate(%s %s %s)" points="%s,%s %s,%s %s,%s" fill="%s" opacity="%s"/>'%(f(a),f(x),f(y),f(x),f(y),f(x+s),f(y+s*.4),f(x+s*.3),f(y+s*1.2),r.choice(['#e8b878','#c4623a','#f2d9b0','#8a3a28']),f(r.uniform(.25,.7)))
    # fissures
    o+='<path d="M215 720 L196 790 L232 850 L204 930 L246 1010 L218 1100 L260 1190 L236 1290" fill="none" stroke="#ff6a3a" stroke-width="3" opacity=".85"/><path d="M215 720 L196 790 L232 850 L204 930 L246 1010 L218 1100 L260 1190 L236 1290" fill="none" stroke="#ffb27a" stroke-width="1" opacity=".9"/>'
    for (x,y,dx,dy) in [(232,850,70,30),(204,930,-80,40),(246,1010,90,50),(218,1100,-70,36),(260,1190,60,44)]:
        o+='<path d="M%d %d l%d %d l%d %d" stroke="#ff6a3a" stroke-width="2" fill="none" opacity=".6"/>'%(x,y,dx*.5,dy*.5,dx*.5,dy*.8)
    o+='<rect y="640" width="430" height="860" fill="url(#ash)"/>'
    # braises
    for i in range(70): o+='<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>'%(f(r.uniform(0,430)),f(r.uniform(700,1500)),f(r.uniform(1,3.2)),r.choice(['#ff8a3a','#ffd08a','#ff5a3a']),f(r.uniform(.2,.8)))
    # silhouette qui tombe
    o+='<g transform="translate(110 520) rotate(160)" fill="#0a0506" opacity=".9"><circle cy="-24" r="9"/><path d="M-9 -12 h18 l5 30 h-6 l-3 24 h-8 l-3 -24 h-6z"/><path d="M-9 -10 l-20 -16 M9 -10 l22 -14" stroke="#0a0506" stroke-width="5" stroke-linecap="round"/></g>'
    return svg(o,d)

SCENES={'gf':gf,'faux':faux,'extremes':extremes,'geants':geants,'revolution':revolution,'evasion':evasion,'chute':chute}
if __name__=='__main__':
    out=sys.argv[1]
    for k,fn in SCENES.items():
        open('%s/%s.svg'%(out,k),'w').write(fn())
