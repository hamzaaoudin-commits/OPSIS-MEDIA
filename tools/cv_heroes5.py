from cv_engine import *
from cv_heroes1 import hl
from cv_heroes3 import card, GREY, SKIN
H = {}
def hero(f): H[f.__name__] = f; return f

@hero
def perruque(p, **k):
    return ('<path d="M34 170 Q22 84 100 70 Q178 84 166 170 Q158 120 100 118 Q42 120 34 170Z" fill="%s" %s/>' % ('#C9A45A', ST) + ''.join('<path d="M%s %s q-6 30 -2 62" stroke="%s" stroke-width="4" fill="none" stroke-linecap="round"/>' % (40 + i * 20, 130 + (i % 2) * 6, '#B38A3C') for i in range(7)) +
            '<path d="M50 100 Q80 82 120 84" stroke="#fff" stroke-width="5" fill="none" opacity=".4" stroke-linecap="round"/>' + '<ellipse cx="100" cy="250" rx="46" ry="8" fill="%s" opacity=".45"/><path d="M60 232 Q100 246 140 232" fill="none" stroke="%s" stroke-width="7" opacity="0"/>' % (INK, INK))
@hero
def octogone(p, **k):
    pts = [(100 + 74 * math.cos(math.pi / 8 + i * math.pi / 4), 164 + 74 * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    o = '<polygon points="%s" fill="%s" %s/>' % (' '.join('%.1f,%.1f' % q for q in pts), mix(INK, p['a'], .3), ST)
    o += '<polygon points="%s" fill="none" stroke="%s" stroke-width="3" transform="translate(100 164) scale(.78) translate(-100 -164)"/>' % (' '.join('%.1f,%.1f' % q for q in pts), CREAM)
    for i in range(8):
        x, y = pts[i]; o += '<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="1.4" opacity=".45"/>' % (x, y, 100 + (x - 100) * .78, 164 + (y - 164) * .78, CREAM)
    return o + '<polygon points="%s" fill="none" %s/>' % (' '.join('%.1f,%.1f' % q for q in pts), ST2) + '<circle cx="100" cy="164" r="14" fill="%s" opacity=".9"/>' % p['a2']
@hero
def ring(p, **k):
    o = '<polygon points="10,236 190,236 200,270 0,270" fill="%s" %s/><polygon points="30,236 170,236 190,252 10,252" fill="%s" opacity=".7"/>' % (INK, ST, p['a'])
    o += ''.join('<path d="M%s 236 L%s 100" stroke="%s" stroke-width="5"/>' % (x, x2, CREAM) for x, x2 in ((34, 40), (166, 160)))
    for y in (130, 164, 198): o += '<path d="M40 %s H160" stroke="%s" stroke-width="4" opacity=".95"/><path d="M40 %s H160" fill="none" stroke="%s" stroke-width="1.4" opacity=".5"/>' % (y, [p['a'], CREAM, p['a']][(y // 34) % 3], y, INK)
    return o + person(100, 134, .8, INK, .95)
@hero
def col_roule(p, **k):
    return ('<path d="M34 252 L44 188 Q64 160 100 156 Q136 160 156 188 L166 252Z" fill="%s" %s/><path d="M76 160 Q100 140 124 160 V186 Q100 196 76 186Z" fill="%s" %s/><path d="M76 168 Q100 180 124 168 M76 176 Q100 188 124 176" stroke="%s" stroke-width="2" fill="none" opacity=".4"/>' % (INK, ST, mix(INK, CREAM, .12), ST2, CREAM) +
            '<ellipse cx="100" cy="100" rx="38" ry="46" fill="%s" %s/><path d="M62 94 Q60 56 100 54 Q140 56 138 94 Q130 74 100 74 Q70 74 62 94Z" fill="#C9A45A" %s/>' % (SKIN, ST, ST2) + '<path d="M82 104 h8 M110 104 h8 M90 128 Q100 134 110 128" stroke="%s" stroke-width="2.4" fill="none" stroke-linecap="round"/>' % INK + '<path d="M100 74 V90" stroke="%s" stroke-width="0"/>' % INK)
@hero
def table_reunion(p, **k):
    o = '<ellipse cx="100" cy="190" rx="86" ry="36" fill="%s" %s/><ellipse cx="100" cy="186" rx="70" ry="26" fill="%s" opacity=".6"/>' % (mix(INK, p['a'], .25), ST, p['a'])
    for i, (x, y) in enumerate(((38, 150), (70, 128), (130, 128), (162, 150), (38, 230), (70, 250), (130, 250), (162, 230))): o += '<rect x="%s" y="%s" width="22" height="26" rx="8" fill="%s" %s/>' % (x - 11, y - 13, INK, ST2)
    return o + '<rect x="84" y="176" width="32" height="14" rx="3" fill="%s" %s/>' % (CREAM, ST2) + ''.join('<rect x="%s" y="168" width="12" height="9" fill="%s" opacity=".9"/>' % (x, CREAM) for x in (50, 140)) + '<path d="M0 86 H200" stroke="%s" stroke-width="2" opacity="0"/>' % INK
@hero
def courbe_haute(p, **k):
    return ('<path d="M24 70 V246 H182" fill="none" stroke="%s" stroke-width="3" opacity=".6"/>' % CREAM + ''.join('<rect x="%s" y="%s" width="20" height="%s" fill="%s" opacity=".6"/>' % (36 + i * 30, 214 - i * 26, 32 + i * 26, p['a']) for i in range(5)) + '<path d="M34 220 L72 196 L102 206 L140 140 L168 102" fill="none" stroke="%s" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/><polygon points="178,92 148,98 170,124" fill="%s" %s/>' % (CREAM, CREAM, ST2) + sparkle(160, 70, 9))
@hero
def trou(p, **k):
    return ('<ellipse cx="100" cy="214" rx="78" ry="26" fill="%s" %s/><ellipse cx="100" cy="214" rx="62" ry="18" fill="#000"/>' % (mix(INK, CREAM, .18), ST) + ''.join('<circle cx="%s" cy="%s" r="9" fill="%s" %s/>' % (x, y, GOLD, ST2) + '<path d="M%s %s v4" stroke="%s" stroke-width="1.6"/>' % (x, y - 3, INK) for x, y in ((70, 96), (112, 124), (90, 160), (128, 178), (82, 196))) + '<path d="M70 60 V84 M112 88 V112 M90 126 V148" stroke="%s" stroke-width="2" opacity=".3" stroke-dasharray="3 5"/>' % CREAM)
@hero
def menottes(p, **k):
    return ('<circle cx="66" cy="170" r="38" fill="none" stroke="#C9CCD2" stroke-width="12"/><circle cx="134" cy="170" r="38" fill="none" stroke="#C9CCD2" stroke-width="12"/><circle cx="66" cy="170" r="38" fill="none" %s/><circle cx="134" cy="170" r="38" fill="none" %s/>' % (ST2, ST2) +
            '<rect x="92" y="164" width="16" height="12" fill="#9AA0AA" %s/><rect x="54" y="122" width="24" height="16" rx="3" fill="#9AA0AA" %s/><rect x="122" y="122" width="24" height="16" rx="3" fill="#9AA0AA" %s/>' % (ST2, ST2, ST2) + '<path d="M80 168 H120" stroke="#9AA0AA" stroke-width="5" stroke-dasharray="8 4"/>' + '<path d="M42 150 A38 38 0 0 1 70 132" stroke="#fff" stroke-width="4" fill="none" opacity=".6"/>')
@hero
def plante_bureau(p, **k):
    o = '<path d="M62 190 H138 L128 248 H72Z" fill="%s" %s/>' % (mix(p['a'], INK, .2), ST)
    for ang, h in ((-50, 110), (-24, 130), (0, 140), (24, 128), (50, 108)): o += '<g transform="rotate(%s 100 190)"><path d="M100 190 Q86 %s 100 %s Q114 %s 100 190Z" fill="#5B8A4A" %s/></g>' % (ang, 190 - h * .5, 190 - h, 190 - h * .5, ST2)
    return o + '<path d="M80 204 H120" stroke="%s" stroke-width="3" opacity=".4"/>' % CREAM
@hero
def parachute(p, **k):
    o = '<path d="M20 130 Q100 20 180 130 Q160 116 140 130 Q120 114 100 130 Q80 114 60 130 Q40 116 20 130Z" fill="%s" %s/>' % (GOLD, ST)
    o += ''.join('<path d="M%s 130 Q%s 90 100 36" stroke="%s" stroke-width="1.6" fill="none" opacity=".4"/>' % (x, x + (100 - x) * .3, INK) for x in (20, 60, 100, 140, 180))
    o += ''.join('<path d="M%s 130 L100 214" stroke="%s" stroke-width="1.8" opacity=".9"/>' % (x, CREAM) for x in (20, 60, 100, 140, 180))
    return o + '<rect x="78" y="214" width="44" height="32" rx="4" fill="%s" %s/>' % (p['a'], ST) + '<circle cx="100" cy="230" r="8" fill="%s" %s/>' % (GOLD2, ST2) + txt(100, 234, '$', 11, INK)
@hero
def ferme(p, **k):
    return ('<polygon points="30,130 100,84 170,130 170,236 30,236" fill="%s" %s/><polygon points="30,130 100,84 170,130" fill="%s" %s/><path d="M66 236 V160 H134 V236 M66 160 L134 236 M134 160 L66 236" fill="%s" stroke="%s" stroke-width="3" opacity=".9"/>' % (RED if False else mix(p['a'], INK, .15), ST, mix(p['a'], INK, .4), ST, CREAM, CREAM) +
            '<circle cx="100" cy="130" r="9" fill="%s" %s/><path d="M0 236 H200 M10 252 H190" stroke="%s" stroke-width="3" opacity=".6"/><rect x="170" y="150" width="20" height="86" fill="%s" %s/><path d="M170 150 Q180 130 190 150" fill="%s" %s/>' % (CREAM, ST2, INK, mix(CREAM, INK, .2), ST2, GREY, ST2))
@hero
def badge_pins(p, **k):
    o = ''
    for x, y, r, c, t in ((60, 120, 34, p['a'], '☺'), (140, 130, 30, CREAM, ''), (82, 196, 32, p['a2'], ''), (150, 210, 26, mix(CREAM, p['a'], .3), '')):
        o += '<circle cx="%s" cy="%s" r="%s" fill="%s" %s/><circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="1.6" opacity=".5"/>' % (x, y, r, c, ST, x, y, r * .72, INK)
    o += '<path d="M40 100 L48 112 M168 112 L158 124" stroke="%s" stroke-width="1" opacity="0"/>' % INK
    o += txt(60, 130, 'Z', 28, INK) + txt(140, 140, 'ZAP', 14, INK) + '<path d="M70 190 l8 -8 l8 8 l8 -8 l8 8" stroke="%s" stroke-width="3" fill="none"/>' % INK
    return o + '<rect x="30" y="248" width="140" height="8" rx="3" fill="%s" %s/>' % (INK, ST2)
@hero
def pizza(p, **k):
    o = '<circle cx="100" cy="164" r="72" fill="#E8B04A" %s/><circle cx="100" cy="164" r="60" fill="#D2412C" %s/><circle cx="100" cy="164" r="56" fill="#F2C14E" opacity=".9"/>' % (ST, ST2)
    for i in range(8): o += '<path d="M100 164 L%.1f %.1f" stroke="%s" stroke-width="2.4" opacity=".7"/>' % (100 + 60 * math.cos(i * math.pi / 4), 164 + 60 * math.sin(i * math.pi / 4), INK)
    for x, y in ((76, 134), (124, 138), (96, 186), (132, 188), (72, 180), (100, 150)): o += '<circle cx="%s" cy="%s" r="8" fill="#B3262A" %s/>' % (x, y, ST2)
    return o + '<path d="M46 130 A60 60 0 0 1 90 108" stroke="#fff" stroke-width="4" fill="none" opacity=".4" stroke-linecap="round"/>'
@hero
def cheque(p, **k):
    t = k.get('t', '2 000 $')
    return ('<g transform="rotate(-6 100 164)">' + card(22, 108, 156, 88, CREAM) + '<rect x="30" y="116" width="52" height="8" fill="%s" opacity=".5"/>' % p['a'] + txt(150, 134, t, 14, INK, anchor='end', ls=1) + '<path d="M34 150 H150" stroke="%s" stroke-width="1.6" opacity=".5"/>' % INK + '<path d="M96 180 q10 -18 18 -2 t16 -2 t18 2" fill="none" stroke="%s" stroke-width="2.4"/>' % INK + '<circle cx="46" cy="172" r="10" fill="%s" opacity=".7"/>' % GOLD + '</g>' + sparkle(168, 98, 10) + sparkle(30, 100, 7))
@hero
def spirale(p, **k):
    pts = []
    for i in range(0, 260, 4):
        a = i * math.pi / 40; r = 4 + i * .27; pts.append('%.1f,%.1f' % (100 + r * math.cos(a), 160 + r * math.sin(a)))
    return '<polyline points="%s" fill="none" stroke="%s" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><polyline points="%s" fill="none" stroke="%s" stroke-width="2" opacity=".5"/>' % (' '.join(pts), p['a'], ' '.join(pts), CREAM) + '<circle cx="100" cy="160" r="9" fill="%s" %s/>' % (CREAM, ST2) + sparkle(168, 84, 9)
@hero
def coffres(p, **k):
    o = ''
    for i, (s, c) in enumerate(((150, mix(INK, p['a'], .3)), (112, mix(INK, p['a'], .5)), (76, mix(INK, p['a'], .7)), (44, p['a2']))):
        o += '<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="%s" %s/>' % (100 - s / 2, 168 - s / 2 + i * 6, s, s * .8, c, ST2) + '<circle cx="%s" cy="%s" r="3.4" fill="%s"/>' % (100, 168 - s / 2 + i * 6 + s * .8 - 12, CREAM)
    return o + '<rect x="94" y="156" width="12" height="14" rx="2" fill="%s" %s/>' % (GOLD, ST2)
@hero
def horloge(p, **k):
    o = '<circle cx="100" cy="164" r="70" fill="%s" %s/><circle cx="100" cy="164" r="60" fill="%s"/>' % (INK, ST, CREAM)
    for i in range(12): o += '<path d="M100 112 V%s" stroke="%s" stroke-width="3" transform="rotate(%s 100 164)"/>' % (118 if i % 3 else 122, INK, i * 30)
    return o + '<path d="M100 164 V122 M100 164 L132 180" stroke="%s" stroke-width="6" stroke-linecap="round"/><path d="M100 164 L70 134" stroke="%s" stroke-width="2.4"/><circle cx="100" cy="164" r="6" fill="%s" %s/>' % (INK, p['a'], p['a'], ST2) + '<path d="M44 128 A60 60 0 0 1 80 106" stroke="#fff" stroke-width="4" fill="none" opacity=".5"/>'
@hero
def laptop(p, **k):
    return ('<rect x="44" y="104" width="112" height="80" rx="6" fill="%s" %s/><rect x="52" y="112" width="96" height="64" fill="%s"/><path d="M26 186 H174 L184 206 H16Z" fill="%s" %s/>' % (INK, ST, mix(p['b0'], p['a'], .3), CREAM, ST) + '<path d="M60 130 H100 M60 144 H120 M60 158 H90" stroke="%s" stroke-width="3" opacity=".8"/><circle cx="130" cy="146" r="12" fill="%s" opacity=".7"/>' % (CREAM, p['a']) + '<rect x="78" y="192" width="44" height="6" rx="3" fill="%s" opacity=".5"/>' % INK + txt(130, 151, '₿', 14, INK))
@hero
def calendrier(p, **k):
    o = card(36, 84, 128, 156, CREAM) + '<rect x="36" y="84" width="128" height="30" rx="3" fill="%s" %s/>' % (p['a'], ST) + ''.join('<rect x="%s" y="74" width="8" height="20" rx="3" fill="%s" %s/>' % (x, INK, ST2) for x in (62, 96, 130))
    for r in range(4):
        for c in range(5):
            d = r * 5 + c
            if d < 18: o += '<path d="M%s %s l14 14 M%s %s l-14 14" stroke="%s" stroke-width="3"/>' % (46 + c * 22, 126 + r * 24, 60 + c * 22, 126 + r * 24, RED) if d < 12 else '<circle cx="%s" cy="%s" r="3" fill="%s" opacity=".5"/>' % (53 + c * 22, 133 + r * 24, INK)
    return o + txt(100, 106, 'NOVEMBRE', 12, CREAM, ls=2)
@hero
def portefeuille(p, **k):
    return ('<path d="M26 120 H174 Q184 120 184 132 V222 Q184 234 172 234 H28 Q16 234 16 222 V132 Q16 120 28 120Z" fill="%s" %s/><path d="M16 150 H184" stroke="%s" stroke-width="3"/><path d="M142 164 H184 V200 H142 Q126 200 126 182 Q126 164 142 164Z" fill="%s" %s/><circle cx="148" cy="182" r="6" fill="%s" %s/>' % (mix(INK, p['a'], .3), ST, INK, mix(INK, p['a'], .5), ST, GOLD, ST2) +
            '<path d="M60 112 q8 -18 20 -8 M90 108 q6 -16 18 -6" stroke="%s" stroke-width="2.4" fill="none" opacity=".5"/><path d="M76 160 q6 12 0 24" stroke="#fff" stroke-width="3" fill="none" opacity="0"/>' % CREAM + '<g transform="translate(50 190)"><ellipse cx="0" cy="0" rx="13" ry="7" fill="%s" opacity=".6" transform="rotate(-18)"/><ellipse cx="14" cy="-4" rx="13" ry="7" fill="%s" opacity=".5" transform="rotate(12)"/></g>' % (CREAM, CREAM))
@hero
def loupe(p, **k):
    return ('<circle cx="86" cy="130" r="52" fill="%s" opacity=".4" %s/><circle cx="86" cy="130" r="52" fill="none" stroke="%s" stroke-width="12"/><circle cx="86" cy="130" r="52" fill="none" %s/><path d="M124 168 L178 232" stroke="%s" stroke-width="16" stroke-linecap="round"/><path d="M124 168 L178 232" stroke="%s" stroke-width="3" opacity=".5"/>' % (CREAM, ST2, GOLD, ST2, INK, CREAM) + '<path d="M56 112 A36 36 0 0 1 84 96" stroke="#fff" stroke-width="5" fill="none" opacity=".7" stroke-linecap="round"/>' + txt(86, 140, k.get('t', '0 ₿'), 22, INK))
@hero
def caisse_musique(p, **k):
    return ('<rect x="28" y="116" width="144" height="112" rx="6" fill="%s" %s/><rect x="28" y="116" width="144" height="16" fill="%s" %s/><rect x="28" y="214" width="144" height="14" fill="%s" %s/>' % (INK, ST, mix(INK, GREY, .3), ST2, mix(INK, GREY, .3), ST2) + ''.join('<rect x="%s" y="%s" width="14" height="14" fill="#C9CCD2" %s/>' % (x, y, ST2) for x, y in ((28, 116), (158, 116), (28, 214), (158, 214))) +
            '<rect x="84" y="136" width="32" height="16" rx="2" fill="#C9CCD2" %s/><rect x="92" y="130" width="16" height="8" fill="%s" %s/>' % (ST2, INK, ST2) + '<circle cx="64" cy="244" r="9" fill="%s" %s/><circle cx="136" cy="244" r="9" fill="%s" %s/>' % (INK, ST, INK, ST) + txt(100, 190, 'FRAGILE', 18, p['a'], ls=2) + '<path d="M0 262 H200" stroke="%s" stroke-width="4"/>' % CREAM)
@hero
def usine(p, **k):
    o = '<rect x="22" y="150" width="156" height="100" fill="%s" %s/>' % (mix(INK, p['a'], .25), ST)
    for i in range(4): o += '<polygon points="%s,150 %s,112 %s,150" fill="%s" %s/>' % (22 + i * 39, 22 + i * 39, 61 + i * 39, mix(INK, p['a'], .25), ST2)
    o += ''.join('<rect x="%s" y="168" width="22" height="20" fill="%s" opacity=".9"/>' % (34 + i * 38, p['a2']) for i in range(4)) + '<rect x="132" y="60" width="22" height="92" fill="%s" %s/><rect x="128" y="54" width="30" height="10" fill="%s" %s/>' % (mix(INK, p['a'], .35), ST, INK, ST2)
    return o + '<path d="M144 50 q-10 -16 6 -26 q14 -10 4 -22" stroke="%s" stroke-width="6" fill="none" stroke-linecap="round" opacity=".5"/><rect x="82" y="206" width="36" height="44" fill="%s" %s/>' % (CREAM, INK, ST2)
@hero
def cedre(p, **k):
    o = '<path d="M100 250 V190" stroke="%s" stroke-width="12" %s/>' % ('#6B4A2A', 'stroke-linecap="round"')
    for i, (y, w) in enumerate(((190, 80), (160, 66), (132, 54), (106, 40))): o += '<path d="M%s %s Q100 %s %s %s Q100 %s %s %s Z" fill="#3F7A4A" %s/>' % (100 - w, y, y - 24, 100 + w, y, y + 12, 100 - w, y, ST2)
    return o + '<circle cx="150" cy="84" r="20" fill="%s" opacity=".9"/>' % CREAM + '<path d="M0 252 H200" stroke="%s" stroke-width="4"/>' % INK
@hero
def pyramide_ponzi(p, **k):
    o = '<polygon points="100,70 24,240 176,240" fill="%s" %s/>' % (p['a'], ST)
    for i, y in enumerate((110, 150, 190)): o += '<path d="M%s %s H%s" stroke="%s" stroke-width="2.4"/>' % (100 - (y - 70) * .45, y, 100 + (y - 70) * .45, INK)
    return o + '<path d="M100 70 V240" stroke="%s" stroke-width="2.4" opacity=".4"/>' % INK + '<circle cx="100" cy="150" r="14" fill="%s" %s/>' % (GOLD2, ST2) + txt(100, 156, '$', 16, INK) + ''.join('<circle cx="%s" cy="252" r="8" fill="%s" %s/>' % (x, GOLD, ST2) for x in (40, 70, 130, 160))
@hero
def tapis_rouge(p, **k):
    return ('<polygon points="86,40 114,40 200,300 0,300" fill="%s" %s/>' % (RED, ST) + ''.join('<path d="M%s 40 L%s 300" stroke="%s" stroke-width="1.4" opacity=".3"/>' % (90 + i * 4, i * 50, INK) for i in range(1, 5)) + ''.join('<rect x="%s" y="%s" width="5" height="22" fill="%s" opacity=".9"/><circle cx="%s" cy="%s" r="4" fill="%s"/>' % (x, y, GOLD, x + 2.5, y - 4, GOLD2) for x, y in ((66, 120), (128, 120), (44, 190), (150, 190))) +
            '<path d="M68 142 q-10 30 -8 58 M132 142 q10 30 8 58" stroke="%s" stroke-width="3" fill="none" opacity="0"/>' % CREAM + '<path d="M70 124 H130" stroke="%s" stroke-width="3"/><path d="M48 194 H152" stroke="%s" stroke-width="3"/>' % (GOLD, GOLD) + sparkle(30, 90, 10) + sparkle(170, 100, 12))
@hero
def stylo(p, **k):
    return ('<g transform="rotate(-38 100 164)"><rect x="92" y="38" width="16" height="150" rx="4" fill="%s" %s/><rect x="92" y="38" width="16" height="30" rx="4" fill="%s" %s/><polygon points="92,188 108,188 100,224" fill="#C9CCD2" %s/><polygon points="96,212 104,212 100,224" fill="%s"/><rect x="108" y="52" width="4" height="60" fill="%s" %s/><path d="M96 74 V176" stroke="#fff" stroke-width="3" opacity=".5"/></g>' % (p['a'], ST, INK, ST, ST, INK, GOLD, ST2) +
            '<path d="M40 250 q30 -20 60 0 t60 0" fill="none" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % CREAM + sparkle(150, 100, 11))
@hero
def deux_fauteuils(p, **k):
    o = ''
    for x, s in ((50, 1), (150, -1)):
        o += '<g transform="translate(%s 176) scale(%s 1)"><rect x="-34" y="-62" width="46" height="108" rx="14" fill="%s" %s/><rect x="-34" y="0" width="68" height="40" rx="12" fill="%s" %s/><rect x="-44" y="-12" width="22" height="56" rx="10" fill="%s" %s/><rect x="-28" y="40" width="8" height="18" fill="%s"/><rect x="18" y="40" width="8" height="18" fill="%s"/></g>' % (x, s, mix(p['a'], INK, .35), ST, mix(p['a'], INK, .2), ST, mix(p['a'], INK, .45), ST, INK, INK)
    return o + '<ellipse cx="100" cy="240" rx="80" ry="9" fill="%s" opacity=".5"/>' % INK + '<polygon points="70,60 130,60 150,240 50,240" fill="%s" opacity=".1"/>' % CREAM + '<rect x="90" y="214" width="20" height="26" rx="2" fill="%s" opacity=".9"/>' % CREAM
@hero
def bracelet(p, **k):
    return ('<ellipse cx="100" cy="164" rx="72" ry="30" fill="none" stroke="#F2C14E" stroke-width="22"/><ellipse cx="100" cy="164" rx="72" ry="30" fill="none" %s/><ellipse cx="100" cy="164" rx="50" ry="14" fill="none" %s/>' % (ST, ST) + '<path d="M44 150 Q100 188 156 150" fill="none" stroke="%s" stroke-width="0"/>' % INK + txt(100, 198, k.get('t', 'FORCE'), 12, INK, ls=2) + '<path d="M40 150 Q60 130 100 134" stroke="#fff" stroke-width="4" fill="none" opacity=".5"/>' + '<ellipse cx="100" cy="164" rx="72" ry="30" fill="none" stroke="%s" stroke-width="22" opacity="0"/>' % INK)
@hero
def maillot_jaune(p, **k):
    return ('<path d="M70 96 L40 112 L52 150 L72 138 L72 240 H128 V138 L148 150 L160 112 L130 96 Q100 116 70 96Z" fill="#F2C93A" %s/><path d="M70 96 Q100 116 130 96 L124 90 Q100 106 76 90Z" fill="%s" %s/><path d="M100 118 V240" stroke="%s" stroke-width="2.4" opacity=".6"/>' % (ST, INK, ST2, INK) + ''.join('<rect x="%s" y="%s" width="12" height="9" rx="2" fill="%s" %s/>' % (x, y, CREAM, ST2) for x, y in ((84, 156), (104, 156), (84, 188), (104, 188))) + '<circle cx="100" cy="136" r="9" fill="%s" opacity=".9"/>' % INK + sparkle(34, 96, 9) + sparkle(168, 100, 10))
@hero
def gant_cuir(p, **k):
    return ('<path d="M66 244 L58 176 Q54 150 70 146 L74 110 Q76 98 88 100 Q98 102 96 116 L98 100 Q100 90 112 92 Q122 96 118 112 L122 100 Q126 92 136 96 Q144 102 138 120 L142 112 Q150 108 154 118 Q156 140 140 168 L136 244Z" fill="%s" %s/>' % (INK, ST) + '<path d="M76 130 V150 M100 120 V150 M122 124 V150" stroke="%s" stroke-width="2" opacity=".35"/>' % CREAM + '<rect x="64" y="236" width="76" height="14" rx="3" fill="%s" %s/>' % (mix(INK, CREAM, .2), ST2) + hl(80, 108, 6, 34, WHITE, .25, 3))
@hero
def prothese(p, **k):
    return ('<path d="M96 40 H120 Q124 86 112 124 Q100 150 118 180 Q140 214 150 244 H132 Q116 214 96 190 Q74 160 80 120 Q90 86 96 40Z" fill="%s" %s/>' % (CREAM, ST) + '<path d="M104 52 Q110 100 98 134" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/><path d="M150 244 H122 Q114 252 124 256 H160 Q164 246 150 244Z" fill="%s" %s/>' % (INK, ST2) + '<rect x="90" y="40" width="36" height="18" rx="4" fill="%s" %s/>' % (p['a'], ST2) + '<path d="M0 262 H200" stroke="%s" stroke-width="4"/>' % CREAM + '<g transform="translate(150 220) scale(.5)"></g>')
@hero
def veste_verte(p, **k):
    return ('<path d="M70 92 L48 106 L32 214 L58 220 L66 150 L70 250 H130 L134 150 L142 220 L168 214 L152 106 L130 92 L100 124Z" fill="#2E7A4A" %s/><path d="M70 92 L100 124 L130 92 L118 88 L100 106 L82 88Z" fill="#245F3A" %s/><path d="M100 124 V250" stroke="%s" stroke-width="2.4" opacity=".5"/>' % (ST, ST2, INK) +
            ''.join('<circle cx="100" cy="%s" r="3.6" fill="%s" %s/>' % (146 + i * 28, GOLD, ST2) for i in range(3)) + '<rect x="112" y="146" width="16" height="12" rx="2" fill="%s" opacity=".9"/><path d="M62 112 L50 200" stroke="#fff" stroke-width="2" opacity=".25"/>' % GOLD2)
@hero
def hydrant(p, **k):
    return ('<rect x="68" y="214" width="64" height="30" rx="4" fill="%s" %s/><path d="M74 214 V130 Q74 104 100 104 Q126 104 126 130 V214Z" fill="%s" %s/><rect x="64" y="146" width="72" height="14" rx="3" fill="%s" %s/><rect x="46" y="168" width="28" height="24" rx="4" fill="%s" %s/><rect x="126" y="168" width="28" height="24" rx="4" fill="%s" %s/>' % (INK, ST, RED, ST, mix(RED, INK, .3), ST2, mix(RED, INK, .2), ST, mix(RED, INK, .2), ST) +
            '<circle cx="100" cy="92" r="12" fill="%s" %s/><circle cx="50" cy="180" r="3" fill="%s"/><path d="M82 116 Q80 160 84 206" stroke="#fff" stroke-width="4" fill="none" opacity=".4"/>' % (RED, ST2, CREAM) + '<path d="M0 252 H200" stroke="%s" stroke-width="4"/>' % CREAM)
@hero
def cannes(p, **k):
    o = ''
    for x, r in ((70, -10), (134, 10)):
        o += '<g transform="translate(%s 170) rotate(%s)"><path d="M-6 -90 H36" stroke="%s" stroke-width="12" stroke-linecap="round"/><path d="M-6 -90 H36" stroke="%s" stroke-width="2" opacity=".5"/><rect x="2" y="-90" width="10" height="170" rx="4" fill="#C9CCD2" %s/><rect x="-2" y="-30" width="18" height="22" rx="4" fill="%s" %s/><path d="M-4 80 H20" stroke="%s" stroke-width="6" stroke-linecap="round"/></g>' % (x, r, INK, CREAM, ST2, p['a'], ST2, INK)
    return o
@hero
def hamburger(p, **k):
    return ('<path d="M34 142 Q34 82 100 82 Q166 82 166 142Z" fill="#D8A24C" %s/>' % ST + ''.join('<ellipse cx="%s" cy="%s" rx="3.4" ry="2" fill="%s"/>' % (60 + i * 22, 112 + (i % 2) * 10, CREAM) for i in range(5)) + '<path d="M30 148 Q50 138 66 148 T100 148 T134 148 T170 148 V158 H30Z" fill="#6DB04A" %s/>' % ST2 +
            '<rect x="30" y="158" width="140" height="14" rx="3" fill="#D2412C" %s/><rect x="26" y="172" width="148" height="22" rx="10" fill="#6B3E1B" %s/><path d="M34 196 H166 Q168 222 140 224 H60 Q32 222 34 196Z" fill="#D8A24C" %s/>' % (ST2, ST, ST) + hl(48, 96, 30, 6, WHITE, .4, 3))
@hero
def reacteur(p, **k):
    o = ''.join('<circle cx="100" cy="164" r="%s" fill="%s" opacity="%s"/>' % (r, '#7FD0F0', op) for r, op in ((80, .1), (64, .18)))
    o += '<circle cx="100" cy="164" r="52" fill="%s" %s/><circle cx="100" cy="164" r="42" fill="none" stroke="#7FD0F0" stroke-width="7"/><circle cx="100" cy="164" r="26" fill="none" stroke="#BFEAFB" stroke-width="3"/><circle cx="100" cy="164" r="12" fill="#FFFFFF" opacity=".95"/>' % (INK, ST)
    for i in range(10): o += '<path d="M%.1f %.1f L%.1f %.1f" stroke="#7FD0F0" stroke-width="6"/>' % (100 + 26 * math.cos(i * math.pi / 5), 164 + 26 * math.sin(i * math.pi / 5), 100 + 40 * math.cos(i * math.pi / 5), 164 + 40 * math.sin(i * math.pi / 5))
    return o
@hero
def statuette(p, **k):
    return ('<rect x="64" y="236" width="72" height="22" rx="3" fill="%s" %s/><rect x="74" y="224" width="52" height="14" fill="%s" %s/><path d="M84 224 Q80 190 86 166 Q74 150 80 124 Q84 104 100 104 Q116 104 120 124 Q126 150 114 166 Q120 190 116 224Z" fill="%s" %s/><circle cx="100" cy="86" r="17" fill="%s" %s/>' % (INK, ST, GOLD, ST2, GOLD2, ST, GOLD2, ST) + '<path d="M90 132 Q86 160 94 196" stroke="#fff" stroke-width="4" fill="none" opacity=".6"/>' + '<path d="M82 126 L60 100 M118 126 L140 100" stroke="%s" stroke-width="0"/>' % INK + sparkle(40, 100, 12) + sparkle(160, 90, 14) + sparkle(150, 190, 9))
@hero
def obelisque(p, **k):
    return ('<polygon points="100,40 112,52 118,240 82,240 88,52" fill="%s" %s/><polygon points="100,40 112,52 88,52" fill="%s" %s/><path d="M100 52 V240" stroke="%s" stroke-width="2" opacity=".3"/>' % (CREAM, ST, mix(CREAM, INK, .15), ST2, INK) + '<rect x="70" y="240" width="60" height="12" fill="%s" %s/><path d="M0 252 H200" stroke="%s" stroke-width="4"/>' % (mix(CREAM, INK, .25), ST2, INK) + ''.join('<circle cx="%s" cy="268" r="1.6" fill="%s"/>' % (30 + i * 16, CREAM) for i in range(10)) + hl(92, 60, 4, 170, WHITE, .45, 2))
@hero
def racine(p, **k):
    return ('<path d="M34 120 H58 L74 200 L92 80 H170" fill="none" stroke="%s" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><path d="M34 120 H58 L74 200 L92 80 H170" fill="none" stroke="%s" stroke-width="2.4" opacity=".5"/>' % (CREAM, INK) + txt(130, 150, '²', 56, p['a2'], ls=0) + txt(120, 190, 'x', 46, p['a2']) if False else
            '<path d="M30 160 H54 L72 230 L94 90 H172" fill="none" stroke="%s" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/><path d="M30 160 H54 L72 230 L94 90 H172" fill="none" stroke="%s" stroke-width="2.4" opacity=".5"/>' % (CREAM, INK) + txt(133, 150, 'A²', 36, p['a2'], extra='stroke="%s" stroke-width="1.4"' % INK))
@hero
def noeud_papillon(p, **k):
    return ('<path d="M100 150 L36 116 Q26 150 36 188 Z" fill="%s" %s/><path d="M100 150 L164 116 Q174 150 164 188 Z" fill="%s" %s/><rect x="84" y="132" width="32" height="38" rx="8" fill="%s" %s/>' % (p['a'], ST, p['a'], ST, mix(p['a'], INK, .3), ST) + '<path d="M50 130 L90 148 M50 170 L90 152 M150 130 L110 148 M150 170 L110 152" stroke="%s" stroke-width="2" opacity=".4"/>' % INK + hl(44, 124, 20, 5, WHITE, .35, 2) + '<path d="M96 170 q-6 40 -22 70 M104 170 q6 40 22 70" stroke="%s" stroke-width="7" stroke-linecap="round" fill="none"/>' % INK)
@hero
def poutre(p, **k):
    return ('<rect x="14" y="170" width="172" height="16" rx="6" fill="%s" %s/><rect x="46" y="186" width="8" height="70" fill="%s" %s/><rect x="146" y="186" width="8" height="70" fill="%s" %s/><rect x="30" y="256" width="40" height="6" fill="%s"/><rect x="130" y="256" width="40" height="6" fill="%s"/>' % (p['a'], ST, GREY, ST2, GREY, ST2, GREY, GREY) +
            '<circle cx="106" cy="90" r="10" fill="%s" %s/><path d="M106 102 L106 142 M106 114 L72 98 M106 114 L142 94 M106 142 L86 168 M106 142 L130 166" stroke="%s" stroke-width="9" stroke-linecap="round" fill="none"/>' % (INK, ST2, INK) + sparkle(40, 120, 9) + sparkle(168, 130, 11))
@hero
def cadenas(p, **k):
    return ('<path d="M64 150 V112 Q64 70 100 70 Q136 70 136 112 V150" fill="none" stroke="#C9CCD2" stroke-width="14"/><path d="M64 150 V112 Q64 70 100 70 Q136 70 136 112 V150" fill="none" %s/><rect x="44" y="146" width="112" height="100" rx="12" fill="%s" %s/><circle cx="100" cy="190" r="13" fill="%s"/><rect x="95" y="196" width="10" height="28" rx="3" fill="%s"/>' % (ST2, GOLD, ST, INK, INK) + hl(52, 154, 8, 84, WHITE, .4, 4))
@hero
def masque_hockey(p, **k):
    return ('<path d="M44 96 Q100 66 156 96 Q168 170 138 226 Q100 250 62 226 Q32 170 44 96Z" fill="%s" %s/><path d="M62 128 Q78 120 90 134 L84 150 Q68 150 62 128Z M138 128 Q122 120 110 134 L116 150 Q132 150 138 128Z" fill="%s" %s/>' % (CREAM, ST, INK, ST2) + '<circle cx="100" cy="176" r="3" fill="%s"/><circle cx="82" cy="190" r="3" fill="%s"/><circle cx="118" cy="190" r="3" fill="%s"/><circle cx="100" cy="204" r="3" fill="%s"/><circle cx="100" cy="150" r="3" fill="%s"/>' % ((INK,) * 5) +
            '<path d="M100 98 V122 M62 108 L150 108" stroke="%s" stroke-width="0"/><path d="M50 168 L64 176 M150 168 L136 176" stroke="%s" stroke-width="3"/>' % (INK, INK) + '<path d="M56 104 Q78 92 100 94" stroke="%s" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/>' % p['a'] + '<path d="M72 112 l6 20 M112 112 l6 20" stroke="%s" stroke-width="5" opacity="0"/>' % RED)
@hero
def reveil(p, **k):
    return ('<circle cx="52" cy="92" r="26" fill="%s" %s/><circle cx="148" cy="92" r="26" fill="%s" %s/><circle cx="100" cy="170" r="66" fill="%s" %s/><circle cx="100" cy="170" r="54" fill="%s"/>' % (GOLD, ST, GOLD, ST, p['a'], ST, CREAM) + ''.join('<path d="M100 122 V%s" stroke="%s" stroke-width="3" transform="rotate(%s 100 170)"/>' % (128 if i % 3 else 132, INK, i * 30) for i in range(12)) +
            '<path d="M100 170 V130 M100 170 L124 184" stroke="%s" stroke-width="6" stroke-linecap="round"/><circle cx="100" cy="170" r="6" fill="%s" %s/><rect x="60" y="232" width="14" height="20" rx="3" fill="%s" %s/><rect x="126" y="232" width="14" height="20" rx="3" fill="%s" %s/>' % (INK, p['a'], ST2, INK, ST2, INK, ST2) + '<path d="M18 86 l-10 -10 M182 86 l10 -10 M14 112 h-12 M186 112 h12" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % CREAM)
@hero
def epave(p, **k):
    return ('<path d="M18 218 Q22 190 48 186 L72 166 Q80 160 90 160 H130 Q142 160 150 170 L162 186 Q184 192 184 214 V226 H18Z" fill="%s" %s/><path d="M82 172 H126 L138 186 H76Z" fill="%s" %s/><path d="M110 160 L100 186 L120 196 L108 226" stroke="%s" stroke-width="3" fill="none" opacity=".0"/>' % (CREAM, ST, mix(INK, p['a'], .25), ST2, INK) +
            '<circle cx="56" cy="228" r="16" fill="%s" %s/><circle cx="148" cy="228" r="16" fill="%s" %s/><path d="M150 190 L184 178 M162 206 L190 206" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (INK, ST, INK, ST, INK) + '<path d="M170 176 q12 -20 4 -40 M150 168 q8 -18 0 -34" stroke="%s" stroke-width="6" fill="none" stroke-linecap="round" opacity=".45"/>' % CREAM + '<path d="M0 246 H200" stroke="%s" stroke-width="4"/>' % CREAM)
@hero
def bouteille(p, **k):
    return ('<path d="M88 66 H112 V112 Q128 134 128 164 V238 Q128 250 116 250 H84 Q72 250 72 238 V164 Q72 134 88 112Z" fill="%s" %s/><rect x="90" y="56" width="20" height="14" rx="2" fill="%s" %s/><rect x="72" y="164" width="56" height="52" fill="%s" %s/>' % (p['a'], ST, INK, ST2, CREAM, ST2) + txt(100, 196, k.get('t', 'XO'), 20, INK) + hl(80, 124, 6, 100, WHITE, .35, 3))
@hero
def chaise_bureau(p, **k):
    return ('<path d="M70 120 Q70 84 100 84 Q130 84 130 120 V172 H70Z" fill="%s" %s/><rect x="62" y="172" width="76" height="22" rx="8" fill="%s" %s/><path d="M100 194 V234 M72 246 H128 M72 246 L100 234 L128 246" stroke="%s" stroke-width="7" stroke-linecap="round" fill="none"/><circle cx="72" cy="254" r="6" fill="%s"/><circle cx="128" cy="254" r="6" fill="%s"/>' % (mix(p['a'], INK, .25), ST, mix(p['a'], INK, .4), ST, INK, INK, INK) + hl(76, 96, 6, 60, WHITE, .3, 3))
