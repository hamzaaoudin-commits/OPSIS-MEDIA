#!/usr/bin/env python3
"""Couvertures des épisodes des « vies » : une affiche par épisode, dessinée en SVG
selon la scène que l'épisode raconte (motif choisi à la main dans ASSIGN).
Écrit les clés ptNNeK dans data/covers.json. Idempotent. À lancer avant tools/build.js."""
import json, re, colorsys, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIV = json.load(open(R + '/data/lives.json'))
COV = json.load(open(R + '/data/covers.json'))

def hx(c):
    c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))

def palette(pid):
    svg = COV[pid]
    cols = re.findall(r'#([0-9A-Fa-f]{6})', svg)
    stops = re.findall(r'stop-color="#([0-9A-Fa-f]{6})"', svg)
    b0 = '#' + (stops[0] if stops else '3A1410'); b1 = '#' + (stops[1] if len(stops) > 1 else '0A0708')
    cnt = {}
    for c in cols:
        r, g, b = hx(c); h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s > .35 and v > .6: cnt[c.upper()] = cnt.get(c.upper(), 0) + 1
    br = sorted(cnt, key=lambda k: -cnt[k])
    a = '#' + (br[0] if br else 'E8B04A'); a2 = '#' + (br[1] if len(br) > 1 else br[0] if br else 'F2C14E')
    return dict(b0=b0, b1=b1, a=a, a2=a2, l='#F4E6C8', d='#0B0B0C')

def person(x, y, s=1, c='#0B0B0C', op=1):
    return ('<g fill="%s" opacity="%s"><circle cx="%s" cy="%s" r="%s"/><path d="M%s %s Q%s %s %s %s L%s %s H%s Z"/></g>'
            % (c, op, x, y, 9 * s, x - 17 * s, y + 14 * s, x, y + 5 * s, x + 17 * s, y + 14 * s, x + 20 * s, y + 70 * s, x - 20 * s))

def fl(c, op=1): return 'fill="%s" opacity="%s"' % (c, op)

# ---------- motifs : chacun reçoit la palette p et rend du SVG (zone utile : y 70-270) ----------
M = {}
def motif(f): M[f.__name__] = f; return f

@motif
def stage(p):
    return ('<polygon points="100,62 38,262 162,262" %s/><ellipse cx="100" cy="262" rx="64" ry="10" %s/>' % (fl(p['l'], .16), fl(p['a'], .75)) +
            person(100, 150, 1.3) + '<rect x="123" y="178" width="2.5" height="80" %s/><rect x="119" y="168" width="10" height="16" rx="5" %s/>' % (fl(p['l'], .8), fl(p['l'], .8)))
@motif
def mic(p):
    return ('<rect x="96" y="160" width="8" height="70" %s/><path d="M70 214 Q100 250 130 214" fill="none" stroke="%s" stroke-width="5"/>' % (fl(p['l'], .85), p['l']) +
            '<ellipse cx="100" cy="124" rx="26" ry="38" %s/><path d="M76 124 H124 M78 110 H122 M78 138 H122 M100 86 V162" stroke="%s" stroke-width="1.5" opacity=".5"/>' % (fl(p['a']), p['d']) +
            '<rect x="82" y="248" width="36" height="6" rx="3" %s/>' % fl(p['l'], .6))
@motif
def guitar(p):
    return ('<g transform="rotate(-32 100 170)"><rect x="95" y="64" width="10" height="106" %s/><rect x="92" y="52" width="16" height="18" rx="3" %s/>' % (fl(p['l'], .8), fl(p['l'], .8)) +
            '<circle cx="100" cy="196" r="30" %s/><circle cx="100" cy="236" r="38" %s/><circle cx="100" cy="206" r="11" %s/>' % (fl(p['a']), fl(p['a']), fl(p['d'])) +
            '<path d="M98 70 V212 M102 70 V212" stroke="%s" stroke-width=".8" opacity=".7"/></g>' % p['l'])
@motif
def piano(p):
    o = '<rect x="22" y="150" width="156" height="100" rx="4" %s/>' % fl(p['l'], .92)
    for i in range(8): o += '<rect x="%s" y="150" width="1.4" height="100" %s/>' % (22 + i * 19.5, fl(p['d'], .5))
    for i in (0, 1, 3, 4, 5): o += '<rect x="%s" y="150" width="12" height="60" rx="2" %s/>' % (36 + i * 19.5, fl(p['d']))
    return o + '<ellipse cx="100" cy="255" rx="84" ry="8" %s/>' % fl(p['a'], .5)
@motif
def vinyl(p):
    o = '<circle cx="100" cy="165" r="70" %s/>' % fl(p['d'])
    for r in (60, 50, 40, 30): o += '<circle cx="100" cy="165" r="%s" fill="none" stroke="%s" stroke-width="1" opacity=".35"/>' % (r, p['l'])
    return o + '<circle cx="100" cy="165" r="20" %s/><circle cx="100" cy="165" r="3" %s/><path d="M50 120 A64 64 0 0 1 100 100" fill="none" stroke="%s" stroke-width="3" opacity=".5"/>' % (fl(p['a']), fl(p['d']), p['l'])
@motif
def tv(p):
    return ('<rect x="34" y="104" width="132" height="102" rx="10" %s/><rect x="42" y="112" width="116" height="86" rx="6" %s/>' % (fl(p['d']), fl(p['a'], .9)) +
            '<circle cx="100" cy="155" r="26" %s/><path d="M88 142 L116 155 L88 168Z" %s/>' % (fl(p['l'], .35), fl(p['l'])) +
            '<path d="M80 206 L72 232 H128 L120 206Z" %s/><path d="M82 104 L66 80 M118 104 L134 80" stroke="%s" stroke-width="3"/>' % (fl(p['d']), p['l']))
@motif
def clapper(p):
    o = '<rect x="38" y="140" width="124" height="92" rx="4" %s/><g transform="rotate(-12 38 138)"><rect x="38" y="112" width="124" height="26" rx="3" %s/>' % (fl(p['d']), fl(p['l']))
    for i in range(6): o += '<polygon points="%s,112 %s,112 %s,138 %s,138" %s/>' % (50 + i * 21, 64 + i * 21, 52 + i * 21, 38 + i * 21, fl(p['d']))
    return o + '</g><path d="M52 164 H148 M52 182 H130 M52 200 H140" stroke="%s" stroke-width="2.5" opacity=".6"/>' % p['l']
@motif
def phone(p):
    return ('<rect x="62" y="82" width="76" height="150" rx="12" %s/><rect x="68" y="94" width="64" height="124" rx="6" %s/>' % (fl(p['d']), fl(p['a'], .9)) +
            '<circle cx="100" cy="150" r="22" %s/><path d="M100 138 V152 L110 158" stroke="%s" stroke-width="3" fill="none"/>' % (fl(p['l'], .3), p['l']) +
            '<rect x="88" y="222" width="24" height="4" rx="2" %s/>' % fl(p['l'], .5))
@motif
def news(p):
    o = '<rect x="46" y="86" width="108" height="150" rx="3" %s/><rect x="56" y="96" width="88" height="14" %s/>' % (fl(p['l'], .95), fl(p['d']))
    o += '<rect x="56" y="118" width="44" height="40" %s/>' % fl(p['a'])
    for i in range(4): o += '<rect x="106" y="%s" width="38" height="3" %s/>' % (120 + i * 9, fl(p['d'], .7))
    for i in range(5): o += '<rect x="56" y="%s" width="88" height="3" %s/>' % (168 + i * 10, fl(p['d'], .55))
    return o
@motif
def flashes(p):
    o = person(100, 150, 1.25)
    for (x, y, s) in ((40, 110, 16), (160, 130, 20), (52, 200, 12), (150, 206, 14), (100, 96, 10)):
        o += '<polygon points="%s,%s %s,%s %s,%s %s,%s %s,%s %s,%s %s,%s %s,%s" %s/>' % (x, y - s, x + s * .25, y - s * .25, x + s, y, x + s * .25, y + s * .25, x, y + s, x - s * .25, y + s * .25, x - s, y, x - s * .25, y - s * .25, fl(p['l'], .95))
    return o
@motif
def car(p):
    return ('<path d="M0 238 H200 V300 H0Z" %s/><path d="M96 238 L104 238 L120 300 L80 300Z" %s/>' % (fl(p['d'], .85), fl(p['l'], .25)) +
            '<path d="M30 218 Q34 188 62 184 L84 160 Q90 154 100 154 H126 Q138 154 146 166 L156 184 Q176 188 176 210 V224 H30Z" %s/>' % fl(p['a']) +
            '<path d="M92 164 H122 L134 184 H88Z" %s/><circle cx="62" cy="226" r="15" %s/><circle cx="146" cy="226" r="15" %s/>' % (fl(p['d'], .8), fl(p['d']), fl(p['d'])) +
            '<circle cx="62" cy="226" r="6" %s/><circle cx="146" cy="226" r="6" %s/><polygon points="176,206 200,190 200,222" %s/>' % (fl(p['l'], .6), fl(p['l'], .6), fl(p['l'], .3)))
@motif
def chase(p):
    return (car(p) + '<polygon points="60,40 36,180 84,180" %s/><polygon points="140,40 116,180 164,180" %s/>' % (fl(p['l'], .14), fl(p['l'], .14)) +
            '<circle cx="60" cy="64" r="5" %s/><circle cx="140" cy="64" r="5" %s/>' % (fl(p['l']), fl(p['l'])))
@motif
def plane(p):
    return ('<ellipse cx="60" cy="236" rx="52" ry="12" %s/><ellipse cx="146" cy="248" rx="50" ry="11" %s/>' % (fl(p['l'], .18), fl(p['l'], .14)) +
            '<g transform="rotate(-22 100 150)"><path d="M28 150 Q60 140 150 144 Q176 146 180 150 Q176 154 150 156 Q60 160 28 150Z" %s/>' % fl(p['l']) +
            '<path d="M92 148 L66 108 L84 108 L124 146Z" %s/><path d="M92 154 L66 194 L84 194 L124 156Z" %s/><path d="M40 148 L28 126 L42 126 L56 146Z" %s/></g>' % (fl(p['a']), fl(p['a']), fl(p['a'])))
@motif
def ship(p):
    o = '<path d="M30 190 H170 L150 232 H52Z" %s/><rect x="70" y="150" width="60" height="40" %s/><rect x="82" y="124" width="18" height="30" %s/><rect x="104" y="124" width="14" height="30" %s/>' % (fl(p['d']), fl(p['l'], .9), fl(p['a']), fl(p['a']))
    for i in range(4): o += '<circle cx="%s" cy="170" r="4" %s/>' % (80 + i * 13, fl(p['d']))
    for i in range(3): o += '<path d="M0 %s Q25 %s 50 %s T100 %s T150 %s T200 %s" fill="none" stroke="%s" stroke-width="3" opacity="%s"/>' % (240 + i * 14, 230 + i * 14, 240 + i * 14, 240 + i * 14, 240 + i * 14, 240 + i * 14, p['a'], .8 - i * .2)
    return o
@motif
def ocean(p):
    o = '<circle cx="100" cy="150" r="34" %s/>' % fl(p['a'], .9)
    for i in range(6):
        y = 176 + i * 16; o += '<path d="M0 %s Q25 %s 50 %s T100 %s T150 %s T200 %s V300 H0Z" %s/>' % (y, y - 10, y, y, y, y, fl(p['d'], .16 + i * .12))
        o += '<path d="M0 %s Q25 %s 50 %s T100 %s T150 %s T200 %s" fill="none" stroke="%s" stroke-width="1.6" opacity=".5"/>' % (y, y - 10, y, y, y, y, p['l'])
    return o
@motif
def mountain(p):
    return ('<circle cx="140" cy="116" r="22" %s/><polygon points="0,260 56,130 92,190 118,150 200,260" %s/><polygon points="40,260 110,100 176,260" %s/>' % (fl(p['l'], .85), fl(p['d'], .55), fl(p['d'], .9)) +
            '<polygon points="110,100 94,134 104,128 110,140 118,126 128,134" %s/><path d="M0 260 H200 V300 H0Z" %s/>' % (fl(p['l'], .9), fl(p['d'])))
@motif
def desert(p):
    return ('<circle cx="100" cy="150" r="40" %s/><path d="M0 210 Q60 160 120 200 T200 190 V300 H0Z" %s/><path d="M0 240 Q70 200 140 236 T200 230 V300 H0Z" %s/>' % (fl(p['a'], .9), fl(p['d'], .55), fl(p['d'], .9)))
@motif
def city(p):
    o = ''
    for i, (x, h) in enumerate(((10, 110), (38, 150), (66, 90), (90, 176), (120, 120), (146, 160), (172, 100))):
        o += '<rect x="%s" y="%s" width="26" height="%s" %s/>' % (x, 262 - h, h, fl(p['d'], .55 + (i % 3) * .15))
        for j in range(int(h / 18)): o += '<rect x="%s" y="%s" width="5" height="7" %s/>' % (x + 5 + (j % 2) * 11, 270 - h + j * 18, fl(p['a'], .7))
    return o + '<rect x="0" y="262" width="200" height="38" %s/>' % fl(p['d'])
@motif
def night(p):
    return '<circle cx="146" cy="104" r="22" %s/><circle cx="154" cy="98" r="19" %s/>' % (fl(p['l'], .9), fl(p['b0'])) + city(p)
@motif
def tower(p):
    o = '<polygon points="84,262 116,262 110,110 90,110" %s/><rect x="98" y="72" width="4" height="40" %s/>' % (fl(p['d']), fl(p['d']))
    for j in range(10): o += '<rect x="93" y="%s" width="14" height="5" %s/>' % (122 + j * 13, fl(p['a'], .75))
    o += '<rect x="56" y="190" width="30" height="72" %s/><rect x="116" y="170" width="34" height="92" %s/>' % (fl(p['d'], .7), fl(p['d'], .7))
    return o + '<rect x="0" y="262" width="200" height="38" %s/>' % fl(p['d'])
@motif
def house(p):
    return ('<polygon points="100,110 40,164 160,164" %s/><rect x="52" y="164" width="96" height="80" %s/><rect x="84" y="190" width="32" height="54" %s/>' % (fl(p['d']), fl(p['d'], .85), fl(p['a'])) +
            '<rect x="60" y="178" width="18" height="18" %s/><rect x="122" y="178" width="18" height="18" %s/><rect x="0" y="244" width="200" height="56" %s/>' % (fl(p['a'], .8), fl(p['a'], .8), fl(p['d'])) +
            '<polygon points="84,244 116,244 140,300 60,300" %s/>' % fl(p['a'], .3))
@motif
def door(p):
    return ('<polygon points="100,70 160,40 160,262 100,262" %s/><rect x="58" y="80" width="84" height="182" %s/><path d="M64 86 H136 V262 H64Z" %s/>' % (fl(p['l'], .13), fl(p['d']), fl(p['a'], .92)) +
            '<polygon points="64,86 100,98 100,250 64,262" %s/><circle cx="92" cy="176" r="3" %s/><polygon points="64,262 136,262 190,300 10,300" %s/>' % (fl(p['d'], .9), fl(p['l']), fl(p['a'], .28)))
@motif
def window(p):
    o = '<rect x="46" y="84" width="108" height="150" rx="3" %s/><rect x="54" y="92" width="92" height="134" %s/><path d="M100 92 V226 M54 160 H146" stroke="%s" stroke-width="4"/>' % (fl(p['d']), fl(p['a'], .55), p['d'])
    for i in range(14): o += '<path d="M%s %s l-4 14" stroke="%s" stroke-width="1.5" opacity=".7"/>' % (60 + (i * 37) % 84, 98 + (i * 53) % 110, p['l'])
    return o + '<rect x="40" y="234" width="120" height="8" %s/>' % fl(p['d'])
@motif
def clock(p):
    o = '<circle cx="100" cy="160" r="68" %s/><circle cx="100" cy="160" r="60" %s/>' % (fl(p['d']), fl(p['l'], .93))
    for i in range(12):
        import math; a = i * math.pi / 6; o += '<path d="M%s %s L%s %s" stroke="%s" stroke-width="3"/>' % (round(100 + 52 * math.sin(a), 1), round(160 - 52 * math.cos(a), 1), round(100 + 58 * math.sin(a), 1), round(160 - 58 * math.cos(a), 1), p['d'])
    return o + '<path d="M100 160 V118 M100 160 L130 176" stroke="%s" stroke-width="5" stroke-linecap="round"/><circle cx="100" cy="160" r="5" %s/>' % (p['d'], fl(p['a']))
@motif
def money(p):
    o = ''
    for i in range(4):
        for j in range(3): o += '<rect x="%s" y="%s" width="92" height="22" rx="3" %s/><circle cx="%s" cy="%s" r="6" %s/>' % (36 + j * 8 + (i % 2) * 6, 246 - i * 26 - j * 6, fl(p['l'] if (i + j) % 2 else p['a'], .95), 82 + j * 8 + (i % 2) * 6, 257 - i * 26 - j * 6, fl(p['d'], .55))
    return o + '<circle cx="146" cy="104" r="22" %s/><text x="146" y="112" text-anchor="middle" font-family="Big Shoulders Display,Impact,sans-serif" font-weight="800" font-size="26" %s>$</text>' % (fl(p['a']), fl(p['d']))
@motif
def safe(p):
    return ('<rect x="44" y="92" width="112" height="150" rx="8" %s/><rect x="54" y="102" width="92" height="130" rx="4" %s/><circle cx="100" cy="166" r="30" %s/><circle cx="100" cy="166" r="22" %s/>' % (fl(p['d']), fl(p['a'], .35), fl(p['d']), fl(p['l'], .9)) +
            '<path d="M100 148 V166 L112 174" stroke="%s" stroke-width="3" fill="none"/><rect x="56" y="242" width="14" height="10" %s/><rect x="130" y="242" width="14" height="10" %s/>' % (p['d'], fl(p['d']), fl(p['d'])))
@motif
def cuffs(p):
    return ('<circle cx="66" cy="170" r="38" fill="none" stroke="%s" stroke-width="12"/><circle cx="134" cy="170" r="38" fill="none" stroke="%s" stroke-width="12"/>' % (p['l'], p['l']) +
            '<rect x="92" y="164" width="16" height="12" %s/><rect x="56" y="124" width="20" height="14" rx="3" %s/><rect x="124" y="124" width="20" height="14" rx="3" %s/>' % (fl(p['a']), fl(p['a']), fl(p['a'])))
@motif
def bars(p):
    o = '<rect x="0" y="0" width="200" height="300" %s/><rect x="30" y="70" width="140" height="190" %s/><circle cx="100" cy="120" r="30" %s/>' % (fl(p['d'], .35), fl(p['a'], .55), fl(p['l'], .9))
    for i in range(7): o += '<rect x="%s" y="64" width="7" height="206" %s/>' % (30 + i * 21, fl(p['d']))
    return o + '<rect x="24" y="64" width="152" height="8" %s/><rect x="24" y="262" width="152" height="8" %s/>' % (fl(p['d']), fl(p['d']))
@motif
def gavel(p):
    return ('<g transform="rotate(-30 100 150)"><rect x="56" y="112" width="88" height="40" rx="6" %s/><rect x="46" y="108" width="14" height="48" rx="4" %s/><rect x="140" y="108" width="14" height="48" rx="4" %s/>' % (fl(p['l']), fl(p['a']), fl(p['a'])) +
            '<rect x="94" y="152" width="12" height="100" rx="5" %s/></g><rect x="40" y="244" width="120" height="14" rx="3" %s/><rect x="56" y="258" width="88" height="10" %s/>' % (fl(p['l'], .85), fl(p['a']), fl(p['a'], .7)))
@motif
def scales(p):
    return ('<rect x="97" y="96" width="6" height="150" %s/><rect x="68" y="244" width="64" height="10" rx="3" %s/><rect x="36" y="104" width="128" height="6" %s/><circle cx="100" cy="96" r="8" %s/>' % (fl(p['l']), fl(p['l']), fl(p['l']), fl(p['a'])) +
            '<path d="M40 108 L24 168 H56Z M160 108 L144 168 H176Z" stroke="%s" stroke-width="1.5" fill="none"/>' % p['l'] +
            '<path d="M22 168 Q40 192 58 168Z M142 168 Q160 192 178 168Z" %s/>' % fl(p['a']))
@motif
def court(p):
    o = '<polygon points="100,78 30,116 170,116" %s/><rect x="30" y="116" width="140" height="8" %s/>' % (fl(p['l']), fl(p['a']))
    for i in range(5): o += '<rect x="%s" y="126" width="14" height="98" %s/>' % (38 + i * 28, fl(p['l'], .92))
    return o + '<rect x="24" y="224" width="152" height="10" %s/><rect x="16" y="234" width="168" height="12" %s/>' % (fl(p['l']), fl(p['a']))
@motif
def fire(p):
    return ('<path d="M100 66 Q140 120 128 160 Q150 150 152 120 Q184 170 160 220 Q148 256 100 262 Q52 256 40 220 Q18 170 54 132 Q56 160 74 166 Q56 116 100 66Z" %s/>' % fl(p['a']) +
            '<path d="M100 130 Q128 170 120 206 Q114 234 100 238 Q84 234 80 206 Q74 172 100 130Z" %s/><path d="M100 188 Q112 206 106 224 Q100 232 94 224 Q88 206 100 188Z" %s/>' % (fl(p['a2']), fl(p['l'])))
@motif
def flask(p):
    return ('<path d="M84 84 H116 V132 L152 226 Q160 250 134 250 H66 Q40 250 48 226 L84 132Z" %s/><path d="M62 200 H138 L152 226 Q160 250 134 250 H66 Q40 250 48 226Z" %s/>' % (fl(p['l'], .22), fl(p['a'], .9)) +
            '<rect x="80" y="76" width="40" height="10" rx="3" %s/><circle cx="90" cy="180" r="5" %s/><circle cx="112" cy="164" r="7" %s/><circle cx="100" cy="144" r="4" %s/>' % (fl(p['l']), fl(p['l'], .8), fl(p['l'], .7), fl(p['l'], .8)))
@motif
def cross(p):
    return ('<path d="M82 80 H118 V130 H168 V166 H118 V216 H82 V166 H32 V130 H82Z" %s/><path d="M0 250 H52 L66 226 L86 270 L106 232 L122 250 H200" fill="none" stroke="%s" stroke-width="3" opacity=".9"/>' % (fl(p['a']), p['l']))
@motif
def heart(p):
    return ('<path d="M100 224 C28 168 40 98 82 106 C94 108 100 118 100 124 C100 118 106 108 118 106 C160 98 172 168 100 224Z" %s/>' % fl(p['a']) +
            '<path d="M0 160 H70 L82 132 L100 196 L114 150 L124 160 H200" fill="none" stroke="%s" stroke-width="3.5"/>' % p['l'])
@motif
def bed(p):
    return ('<polygon points="100,70 148,70 190,262 10,262" %s/><rect x="30" y="196" width="140" height="40" rx="6" %s/><rect x="30" y="170" width="20" height="90" rx="4" %s/><rect x="150" y="186" width="20" height="74" rx="4" %s/>' % (fl(p['a'], .1), fl(p['l'], .9), fl(p['d']), fl(p['d'])) +
            '<rect x="42" y="184" width="46" height="18" rx="8" %s/><path d="M96 200 Q130 190 170 204 V236 H96Z" %s/>' % (fl(p['l']), fl(p['a'], .85)) + '<circle cx="164" cy="104" r="14" %s/>' % fl(p['a'], .9))
@motif
def letter(p):
    return ('<rect x="36" y="110" width="128" height="94" rx="4" %s/><path d="M36 114 L100 168 L164 114" fill="none" stroke="%s" stroke-width="4"/><path d="M36 204 L84 154 M164 204 L116 154" stroke="%s" stroke-width="2" opacity=".5"/>' % (fl(p['l']), p['d'], p['d']) +
            '<circle cx="100" cy="168" r="11" %s/><rect x="44" y="76" width="112" height="40" rx="3" %s transform="rotate(-6 100 96)"/>' % (fl(p['a']), fl(p['l'], .45)))
@motif
def book(p):
    return ('<path d="M100 96 Q60 74 24 90 V222 Q60 206 100 228Z" %s/><path d="M100 96 Q140 74 176 90 V222 Q140 206 100 228Z" %s/>' % (fl(p['l']), fl(p['l'], .86)) +
            '<path d="M38 112 Q70 102 90 116 M38 136 Q70 126 90 140 M38 160 Q70 150 90 164 M110 116 Q130 102 162 112 M110 140 Q130 126 162 136" stroke="%s" stroke-width="2.4" fill="none" opacity=".5"/>' % p['d'] +
            '<rect x="97" y="96" width="6" height="132" %s/><rect x="46" y="232" width="108" height="6" rx="3" %s/>' % (fl(p['a']), fl(p['a'], .6)))
@motif
def ring(p):
    return ('<circle cx="100" cy="190" r="48" fill="none" stroke="%s" stroke-width="12"/><polygon points="100,100 124,124 100,152 76,124" %s/><polygon points="76,124 100,124 100,152" %s/><polygon points="100,124 124,124 100,152" %s/>' % (p['a'], fl(p['l']), fl(p['l'], .6), fl(p['l'], .85)) +
            '<path d="M70 98 L62 84 M130 98 L138 84 M100 90 V74" stroke="%s" stroke-width="3"/>' % p['l'])
@motif
def family(p):
    return person(62, 150, 1.0) + person(140, 158, 0.95) + person(100, 184, 0.62) + '<ellipse cx="100" cy="262" rx="76" ry="9" %s/>' % fl(p['a'], .6)
@motif
def ball(p):
    return ('<path d="M0 250 H200 V300 H0Z" %s/><path d="M20 300 L70 250 M180 300 L130 250 M0 270 H200" stroke="%s" stroke-width="1.5" opacity=".45"/>' % (fl(p['d'], .8), p['l']) +
            '<circle cx="100" cy="158" r="62" %s/><polygon points="100,126 126,146 116,176 84,176 74,146" %s/>' % (fl(p['l']), fl(p['d'])) +
            '<path d="M100 126 V96 M126 146 L152 134 M116 176 L134 202 M84 176 L66 202 M74 146 L48 134" stroke="%s" stroke-width="3"/>' % p['d'])
@motif
def stadium(p):
    return ('<ellipse cx="100" cy="226" rx="94" ry="30" %s/><ellipse cx="100" cy="226" rx="70" ry="18" %s/><ellipse cx="100" cy="226" rx="30" ry="8" fill="none" stroke="%s" stroke-width="1.5" opacity=".6"/>' % (fl(p['d'], .9), fl(p['a'], .75), p['l']) +
            '<rect x="22" y="104" width="4" height="124" %s/><rect x="174" y="104" width="4" height="124" %s/><rect x="12" y="84" width="24" height="22" %s/><rect x="164" y="84" width="24" height="22" %s/>' % (fl(p['d']), fl(p['d']), fl(p['l']), fl(p['l'])) +
            '<polygon points="24,106 -10,250 90,226" %s/><polygon points="176,106 210,250 110,226" %s/>' % (fl(p['l'], .14), fl(p['l'], .14)))
@motif
def glove(p):
    return ('<path d="M64 188 Q40 140 78 112 Q122 82 148 120 Q168 152 152 192 Q140 214 120 216 V250 H72 V212 Q66 204 64 188Z" %s/><rect x="68" y="236" width="60" height="22" rx="4" %s/>' % (fl(p['a']), fl(p['l'], .9)) +
            '<path d="M70 164 Q56 158 62 144 Q74 132 90 150" %s/><path d="M96 126 Q120 112 140 132" stroke="%s" stroke-width="3" fill="none" opacity=".6"/>' % (fl(p['a2']), p['l']))
@motif
def ringbox(p):
    o = '<polygon points="0,236 200,236 200,300 0,300" %s/><polygon points="20,236 180,236 200,262 0,262" %s/>' % (fl(p['d'], .9), fl(p['a'], .6))
    o += '<rect x="30" y="100" width="6" height="140" %s/><rect x="164" y="100" width="6" height="140" %s/>' % (fl(p['l']), fl(p['l']))
    for y in (130, 164, 198): o += '<path d="M36 %s H164" stroke="%s" stroke-width="3.5"/>' % (y, p['a'])
    return o + person(100, 140, 1.2, p['d'], .9)
@motif
def trophy(p):
    return ('<path d="M62 84 H138 V128 Q138 168 100 176 Q62 168 62 128Z" %s/><path d="M62 96 H40 Q36 136 68 146 M138 96 H160 Q164 136 132 146" fill="none" stroke="%s" stroke-width="7"/>' % (fl(p['a']), p['a']) +
            '<rect x="93" y="176" width="14" height="40" %s/><rect x="70" y="216" width="60" height="16" rx="3" %s/><rect x="58" y="232" width="84" height="14" rx="3" %s/><path d="M76 100 Q80 130 92 150" stroke="%s" stroke-width="5" fill="none" opacity=".5"/>' % (fl(p['a']), fl(p['l']), fl(p['l'], .8), p['l']))
@motif
def medal(p):
    return ('<polygon points="62,60 98,60 112,150 80,150" %s/><polygon points="138,60 102,60 88,150 120,150" %s/><circle cx="100" cy="190" r="48" %s/><circle cx="100" cy="190" r="38" fill="none" stroke="%s" stroke-width="3" opacity=".6"/>' % (fl(p['l'], .85), fl(p['a'], .85), fl(p['a']), p['d']) +
            '<polygon points="100,168 107,184 124,186 111,197 115,214 100,205 85,214 89,197 76,186 93,184" %s/>' % fl(p['l']))
@motif
def track(p):
    o = '<polygon points="82,70 118,70 200,300 0,300" %s/>' % fl(p['d'], .55)
    for i in range(1, 5): o += '<path d="M%s 70 L%s 300" stroke="%s" stroke-width="2" opacity=".6"/>' % (82 + i * 9, i * 40, p['l'])
    return o + person(100, 160, 1.0, p['d']) + '<path d="M0 252 H200" stroke="%s" stroke-width="4" opacity=".7"/>' % p['a']
@motif
def bike(p):
    return ('<circle cx="56" cy="206" r="40" fill="none" stroke="%s" stroke-width="6"/><circle cx="148" cy="206" r="40" fill="none" stroke="%s" stroke-width="6"/>' % (p['l'], p['l']) +
            '<path d="M56 206 L92 146 H132 L148 206 M92 146 L104 206 H56 M104 206 L132 146" fill="none" stroke="%s" stroke-width="5"/><path d="M86 132 H104 M128 140 L124 124 H138" stroke="%s" stroke-width="5" fill="none"/>' % (p['a'], p['a']) +
            '<circle cx="104" cy="206" r="7" %s/><path d="M0 246 H200" stroke="%s" stroke-width="3" opacity=".5"/>' % (fl(p['a']), p['l']))
@motif
def rocket(p):
    return ('<path d="M100 66 Q136 108 130 188 H70 Q64 108 100 66Z" %s/><circle cx="100" cy="124" r="14" %s/><circle cx="100" cy="124" r="9" %s/><path d="M70 160 L44 204 L72 192Z M130 160 L156 204 L128 192Z" %s/>' % (fl(p['l']), fl(p['d']), fl(p['a'], .8), fl(p['a'])) +
            '<path d="M80 188 H120 L112 244 Q100 268 88 244Z" %s/><path d="M92 188 H108 L104 236 Q100 248 96 236Z" %s/>' % (fl(p['a2']), fl(p['l'])))
@motif
def chess(p):
    return ('<rect x="72" y="208" width="56" height="14" rx="3" %s/><path d="M80 208 Q88 150 84 128 H116 Q112 150 120 208Z" %s/><rect x="76" y="118" width="48" height="12" rx="3" %s/>' % (fl(p['a']), fl(p['l']), fl(p['a'])) +
            '<rect x="96" y="76" width="8" height="32" %s/><rect x="86" y="86" width="28" height="8" %s/><rect x="60" y="222" width="80" height="10" rx="3" %s/>' % (fl(p['a']), fl(p['a']), fl(p['l'])))
@motif
def mask(p):
    return ('<path d="M34 110 Q100 82 166 110 Q172 188 130 226 Q100 244 70 226 Q28 188 34 110Z" %s/><path d="M54 140 Q76 128 90 148 Q72 162 54 140Z M146 140 Q124 128 110 148 Q128 162 146 140Z" %s/>' % (fl(p['l']), fl(p['d'])) +
            '<path d="M72 196 Q100 216 128 196" fill="none" stroke="%s" stroke-width="4"/><path d="M100 150 V176" stroke="%s" stroke-width="3" opacity=".5"/>' % (p['d'], p['d']))
@motif
def crown(p):
    return ('<path d="M34 214 L26 108 L68 152 L100 92 L132 152 L174 108 L166 214Z" %s/><rect x="30" y="214" width="140" height="22" rx="4" %s/>' % (fl(p['a']), fl(p['a2'])) +
            '<circle cx="26" cy="104" r="8" %s/><circle cx="100" cy="86" r="9" %s/><circle cx="174" cy="104" r="8" %s/><circle cx="70" cy="226" r="5" %s/><circle cx="100" cy="226" r="5" %s/><circle cx="130" cy="226" r="5" %s/>' % ((fl(p['l']),) * 3 + (fl(p['d']),) * 3))
@motif
def stairs(p):
    o = ''
    for i in range(7): o += '<rect x="%s" y="%s" width="%s" height="%s" %s/>' % (20 + i * 20, 254 - i * 24, 180 - 20 - i * 20, 24 + i * 24 - i * 0, fl(p['l'] if i % 2 else p['a'], .9))
    return o + '<path d="M150 74 V100" stroke="%s" stroke-width="3"/>' % p['l'] + '<circle cx="150" cy="116" r="22" %s/>' % fl(p['a'], .9)
@motif
def bridge(p):
    o = '<rect x="0" y="206" width="200" height="12" %s/><path d="M20 206 Q100 90 180 206" fill="none" stroke="%s" stroke-width="5"/>' % (fl(p['d']), p['l'])
    for i in range(7): o += '<path d="M%s 206 V%s" stroke="%s" stroke-width="2"/>' % (40 + i * 20, 160 - abs(3 - i) * -8 - 12, p['l'])
    return o + '<rect x="0" y="230" width="200" height="70" %s/>' % fl(p['a'], .35)
@motif
def road(p):
    return ('<circle cx="100" cy="132" r="34" %s/><polygon points="94,150 106,150 200,300 0,300" %s/><path d="M100 152 V172 M100 188 V216 M100 236 V280" stroke="%s" stroke-width="4" opacity=".85"/>' % (fl(p['a'], .9), fl(p['d'], .88), p['l']) +
            '<path d="M0 150 H200" stroke="%s" stroke-width="2" opacity=".4"/>' % p['l'])
@motif
def forest(p):
    o = ''
    for i, (x, h) in enumerate(((20, 120), (56, 160), (96, 190), (140, 150), (176, 110))):
        o += '<polygon points="%s,%s %s,252 %s,252" %s/>' % (x, 252 - h, x - 28, x + 28, fl(p['d'], .55 + i % 2 * .3)) + '<rect x="%s" y="252" width="6" height="16" %s/>' % (x - 3, fl(p['d']))
    return o + '<circle cx="150" cy="98" r="18" %s/>' % fl(p['l'], .85)
@motif
def sunrise(p):
    o = ''
    import math
    for i in range(11):
        a = math.pi + i * math.pi / 10; o += '<path d="M100 220 L%s %s" stroke="%s" stroke-width="3" opacity=".45"/>' % (round(100 + 110 * math.cos(a), 1), round(220 + 110 * math.sin(a), 1), p['a'])
    return o + '<path d="M56 220 A44 44 0 0 1 144 220Z" %s/><path d="M0 220 H200 V300 H0Z" %s/><path d="M0 236 H200" stroke="%s" stroke-width="2" opacity=".3"/>' % (fl(p['a']), fl(p['d'], .88), p['l'])
@motif
def moon(p):
    o = '<circle cx="100" cy="150" r="56" %s/><circle cx="122" cy="134" r="50" %s/>' % (fl(p['l'], .95), fl(p['b0']))
    for (x, y, r) in ((40, 100, 1.8), (160, 90, 1.5), (150, 200, 2), (50, 220, 1.4), (120, 80, 1.2), (34, 170, 1.6)): o += '<circle cx="%s" cy="%s" r="%s" %s/>' % (x, y, r, fl(p['l']))
    return o
@motif
def rain(p):
    o = '<path d="M50 130 Q40 100 70 98 Q78 72 108 82 Q134 66 148 96 Q176 98 168 130Z" %s/>' % fl(p['l'], .8)
    for i in range(16): o += '<path d="M%s %s l-5 16" stroke="%s" stroke-width="2.2" opacity=".75"/>' % (52 + (i * 23) % 100, 146 + (i * 41) % 90, p['a'])
    return o + '<rect x="0" y="262" width="200" height="38" %s/>' % fl(p['d'], .8)
@motif
def candle(p):
    return ('<path d="M100 82 Q124 116 112 138 Q100 146 88 138 Q76 116 100 82Z" %s/><path d="M100 104 Q110 122 104 134 Q100 138 96 134 Q90 122 100 104Z" %s/>' % (fl(p['a']), fl(p['l'])) +
            '<rect x="82" y="146" width="36" height="96" rx="3" %s/><path d="M100 140 V148" stroke="%s" stroke-width="2"/><ellipse cx="100" cy="246" rx="48" ry="8" %s/><circle cx="100" cy="116" r="70" %s/>' % (fl(p['l'], .92), p['d'], fl(p['l'], .3), fl(p['a'], .1)))
@motif
def blocks(p):
    o = ''
    def cube(x, y, s, c):
        return ('<polygon points="%s,%s %s,%s %s,%s %s,%s" %s/><polygon points="%s,%s %s,%s %s,%s %s,%s" %s/><polygon points="%s,%s %s,%s %s,%s %s,%s" %s/>'
                % (x, y, x + s, y - s * .5, x + 2 * s, y, x + s, y + s * .5, fl(p['l']), x, y, x + s, y + s * .5, x + s, y + s * 1.5, x, y + s, fl(p['a']), x + s, y + s * .5, x + 2 * s, y, x + 2 * s, y + s, x + s, y + s * 1.5, fl(p['a2'], .75)))
    return cube(36, 190, 32, p) + cube(100, 190, 32, p) + cube(68, 150, 32, p) + cube(68, 110, 32, p)
@motif
def chartup(p):
    return ('<path d="M24 78 V250 H178" fill="none" stroke="%s" stroke-width="3" opacity=".6"/><path d="M36 232 L76 190 L104 208 L142 138 L160 120" fill="none" stroke="%s" stroke-width="6"/><polygon points="170,106 142,112 162,136" %s/>' % (p['l'], p['a'], fl(p['a'])) +
            '<rect x="44" y="212" width="16" height="38" %s/><rect x="84" y="196" width="16" height="54" %s/><rect x="124" y="170" width="16" height="80" %s/>' % (fl(p['l'], .5), fl(p['l'], .5), fl(p['l'], .5)))
@motif
def chartdown(p):
    return ('<path d="M24 78 V250 H178" fill="none" stroke="%s" stroke-width="3" opacity=".6"/><path d="M36 116 L76 150 L104 136 L142 210 L160 226" fill="none" stroke="%s" stroke-width="6"/><polygon points="172,236 144,230 164,208" %s/>' % (p['l'], p['a'], fl(p['a'])) +
            '<rect x="44" y="140" width="16" height="110" %s/><rect x="84" y="170" width="16" height="80" %s/><rect x="124" y="214" width="16" height="36" %s/>' % (fl(p['l'], .5), fl(p['l'], .5), fl(p['l'], .5)))
@motif
def mirror(p):
    return ('<ellipse cx="100" cy="160" rx="54" ry="84" %s/><ellipse cx="100" cy="160" rx="46" ry="76" %s/>' % (fl(p['a']), fl(p['b1'])) +
            person(100, 150, .95, p['l'], .9) + '<path d="M62 120 L96 90 M58 160 L110 100" stroke="%s" stroke-width="3" opacity=".35"/><rect x="88" y="244" width="24" height="16" %s/>' % (p['l'], fl(p['a'])))
@motif
def crowd(p):
    o = ''
    for row, (y, s, op) in enumerate(((200, 1.0, .95), (164, .8, .7), (134, .62, .5))):
        for i in range(7 - row):
            o += '<circle cx="%s" cy="%s" r="%s" %s/><path d="M%s %s Q%s %s %s %s V%s H%s Z" %s/>' % (20 + i * (170 / (6 - row)) + row * 4, y, 9 * s, fl(p['d'], op), 20 + i * (170 / (6 - row)) + row * 4 - 16 * s, y + 14 * s, 20 + i * (170 / (6 - row)) + row * 4, y + 6 * s, 20 + i * (170 / (6 - row)) + row * 4 + 16 * s, y + 14 * s, 300, 20 + i * (170 / (6 - row)) + row * 4 - 16 * s, fl(p['d'], op))
    return '<ellipse cx="100" cy="120" rx="70" ry="50" %s/>' % fl(p['a'], .35) + o + '<polygon points="100,60 70,150 130,150" %s/>' % fl(p['l'], .15)
@motif
def key(p):
    return ('<circle cx="64" cy="150" r="36" %s/><circle cx="64" cy="150" r="14" %s/><rect x="96" y="144" width="86" height="14" %s/><rect x="150" y="158" width="10" height="24" %s/><rect x="168" y="158" width="10" height="16" %s/>' % (fl(p['a']), fl(p['b1']), fl(p['a']), fl(p['a']), fl(p['a'])))
@motif
def lock(p):
    return ('<path d="M66 150 V116 Q66 76 100 76 Q134 76 134 116 V150" fill="none" stroke="%s" stroke-width="12"/><rect x="48" y="146" width="104" height="94" rx="10" %s/><circle cx="100" cy="186" r="11" %s/><rect x="96" y="190" width="8" height="26" rx="3" %s/>' % (p['l'], fl(p['a']), fl(p['d']), fl(p['d'])))
@motif
def cards(p):
    return ('<g transform="rotate(-18 100 170)"><rect x="52" y="96" width="70" height="104" rx="8" %s/></g><g transform="rotate(14 100 170)"><rect x="80" y="96" width="70" height="104" rx="8" %s/>' % (fl(p['l'], .8), fl(p['l'])) +
            '<text x="115" y="150" text-anchor="middle" font-family="Georgia,serif" font-size="46" %s>♠</text></g>' % fl(p['d']) + '<ellipse cx="100" cy="254" rx="70" ry="8" %s/>' % fl(p['a'], .5))
@motif
def bottle(p):
    return ('<path d="M88 76 H112 V118 Q128 140 128 170 V236 Q128 246 118 246 H82 Q72 246 72 236 V170 Q72 140 88 118Z" %s/><rect x="90" y="66" width="20" height="14" rx="2" %s/><rect x="72" y="170" width="56" height="44" %s/>' % (fl(p['a'], .9), fl(p['d']), fl(p['l'], .85)) +
            '<path d="M82 130 V228" stroke="%s" stroke-width="3" opacity=".5"/>' % p['l'])
@motif
def paint(p):
    return ('<path d="M24 210 Q50 140 100 150 Q150 160 176 100" fill="none" stroke="%s" stroke-width="22" stroke-linecap="round"/><path d="M34 240 Q80 200 120 222 Q160 244 180 196" fill="none" stroke="%s" stroke-width="14" stroke-linecap="round"/>' % (p['a'], p['l']) +
            '<circle cx="40" cy="110" r="10" %s/><circle cx="64" cy="86" r="5" %s/><circle cx="150" cy="248" r="8" %s/><g transform="rotate(30 150 100)"><rect x="146" y="60" width="8" height="70" %s/><rect x="144" y="126" width="12" height="16" %s/><path d="M142 142 H158 L152 164 H148Z" %s/></g>' % (fl(p['a2']), fl(p['l']), fl(p['a2']), fl(p['l'], .9), fl(p['d']), fl(p['a'])))
@motif
def lens(p):
    o = ''
    for r, c, op in ((70, p['d'], 1), (58, p['a'], .9), (44, p['d'], 1), (32, p['b1'], 1), (14, p['l'], .8)): o += '<circle cx="100" cy="160" r="%s" fill="%s" opacity="%s"/>' % (r, c, op)
    return o + '<circle cx="82" cy="140" r="8" %s/><path d="M40 160 H60 M140 160 H160 M100 90 V108 M100 212 V230" stroke="%s" stroke-width="3" opacity=".7"/>' % (fl(p['l'], .6), p['l'])
@motif
def suitcase(p):
    return ('<path d="M78 112 V96 Q78 88 86 88 H114 Q122 88 122 96 V112" fill="none" stroke="%s" stroke-width="7"/><rect x="36" y="112" width="128" height="112" rx="10" %s/><rect x="36" y="150" width="128" height="8" %s/><rect x="90" y="146" width="20" height="18" rx="3" %s/>' % (p['l'], fl(p['a']), fl(p['d'], .55), fl(p['l'])) +
            '<rect x="50" y="224" width="12" height="12" %s/><rect x="138" y="224" width="12" height="12" %s/>' % (fl(p['d']), fl(p['d'])))
@motif
def shadow(p):
    return ('<polygon points="100,262 30,262 0,300 70,300" %s/><polygon points="100,262 170,262 200,300 130,300" %s/>' % (fl(p['d'], .5), fl(p['d'], .3)) +
            '<path d="M100 262 L-20 300 H60Z" %s/>' % fl(p['d'], .0) + person(100, 136, 1.35, p['d']) + '<polygon points="64,206 100,262 140,262 100,206" %s/><circle cx="100" cy="110" r="76" %s/>' % (fl(p['d'], .45), fl(p['a'], .22)))
@motif
def emptyroom(p):
    return ('<polygon points="0,0 60,60 140,60 200,0" %s/><rect x="60" y="60" width="80" height="140" %s/><polygon points="0,300 60,200 140,200 200,300" %s/><rect x="84" y="80" width="32" height="46" %s/>' % (fl(p['d'], .55), fl(p['d'], .35), fl(p['d'], .85), fl(p['a'], .9)) +
            '<polygon points="84,126 116,126 150,262 50,262" %s/><rect x="90" y="200" width="22" height="26" rx="2" %s/><rect x="88" y="220" width="3" height="22" %s/><rect x="111" y="220" width="3" height="22" %s/>' % (fl(p['a'], .22), fl(p['l']), fl(p['l']), fl(p['l'])))
@motif
def scissors(p):
    return ('<g transform="rotate(-28 100 170)"><path d="M100 170 L152 70 L160 74 L112 176Z" %s/><path d="M100 170 L48 70 L40 74 L88 176Z" %s/><circle cx="68" cy="214" r="24" fill="none" stroke="%s" stroke-width="9"/><circle cx="132" cy="214" r="24" fill="none" stroke="%s" stroke-width="9"/><path d="M82 196 L100 170 L118 196" fill="none" stroke="%s" stroke-width="7"/></g>' % (fl(p['l']), fl(p['l']), p['a'], p['a'], p['a']) +
            '<path d="M150 256 q10 -14 22 0 M172 240 q10 -14 22 0" stroke="%s" stroke-width="3" fill="none" opacity=".5"/>' % p['l'])
@motif
def church(p):
    return ('<polygon points="100,56 118,106 82,106" %s/><rect x="82" y="106" width="36" height="46" %s/><rect x="96" y="70" width="8" height="2" %s/><rect x="97" y="40" width="6" height="26" %s/><rect x="88" y="48" width="24" height="5" %s/>' % (fl(p['l']), fl(p['l']), fl(p['d']), fl(p['a']), fl(p['a'])) +
            '<rect x="30" y="152" width="140" height="94" %s/><path d="M86 246 V196 Q100 178 114 196 V246Z" %s/><rect x="44" y="176" width="14" height="28" rx="7" %s/><rect x="142" y="176" width="14" height="28" rx="7" %s/><rect x="0" y="246" width="200" height="54" %s/>' % (fl(p['d'], .88), fl(p['a']), fl(p['a'], .8), fl(p['a'], .8), fl(p['d'])))
@motif
def kitchen(p):
    return ('<circle cx="92" cy="170" r="52" %s/><circle cx="92" cy="170" r="44" %s/><rect x="140" y="160" width="56" height="12" rx="6" %s/><path d="M62 150 Q92 120 122 150" fill="none" stroke="%s" stroke-width="3" opacity=".5"/>' % (fl(p['d']), fl(p['a'], .85), fl(p['d']), p['l']) +
            '<path d="M38 82 L78 82 L66 118 H46Z" %s opacity="0"/><g transform="rotate(34 100 90)"><rect x="96" y="40" width="8" height="48" %s/><path d="M92 86 H108 V132 Q100 146 92 132Z" %s/></g>' % (fl(p['l']), fl(p['l']), fl(p['l'])))
@motif
def dress(p):
    return ('<path d="M92 72 Q100 92 108 72 L120 84 L116 134 Q142 176 164 262 H36 Q58 176 84 134 L80 84Z" %s/><path d="M84 134 H116" stroke="%s" stroke-width="3" opacity=".6"/>' % (fl(p['a']), p['d']) +
            '<rect x="98" y="262" width="4" height="26" %s/><rect x="70" y="288" width="60" height="6" rx="3" %s/><path d="M80 84 Q100 112 120 84" fill="none" stroke="%s" stroke-width="3" opacity=".6"/>' % (fl(p['l']), fl(p['l']), p['d']))
@motif
def runway(p):
    o = '<polygon points="90,100 110,100 190,300 10,300" %s/>' % fl(p['d'], .85)
    for i in range(1, 6): o += '<path d="M%s %s L%s 300" stroke="%s" stroke-width="1.5" opacity=".25"/>' % (90 + (i - 3) * 4, 100, 10 + i * 30, p['l'])
    o += '<polygon points="40,40 20,160 70,160" %s/><polygon points="160,40 130,160 180,160" %s/><polygon points="100,40 80,150 120,150" %s/>' % (fl(p['l'], .16), fl(p['l'], .16), fl(p['l'], .2))
    return o + person(100, 170, .7, p['l'], .95) + '<path d="M60 300 L100 232 L140 300" fill="none" stroke="%s" stroke-width="2" opacity="0"/>' % p['a']
@motif
def curtain(p):
    o = '<rect x="0" y="0" width="200" height="300" %s/>' % fl(p['d'], .3)
    o += '<path d="M0 60 H200 V0 H0Z" %s/>' % fl(p['a'])
    o += '<path d="M0 60 Q40 120 50 300 H0Z" %s/><path d="M200 60 Q160 120 150 300 H200Z" %s/>' % (fl(p['a'], .9), fl(p['a'], .9))
    o += '<path d="M14 60 Q28 150 26 300 M32 60 Q44 150 40 300" stroke="%s" stroke-width="2" fill="none" opacity=".4"/>' % p['d']
    return o + '<polygon points="100,90 60,262 140,262" %s/><ellipse cx="100" cy="262" rx="56" ry="9" %s/>' % (fl(p['l'], .18), fl(p['l'], .55))
@motif
def rainbow(p):
    o = ''
    for i, c in enumerate((p['a'], p['a2'], p['l'], p['a'], p['a2'])):
        r = 84 - i * 13; o += '<path d="M%s 232 A%s %s 0 0 1 %s 232" fill="none" stroke="%s" stroke-width="12" opacity="%s"/>' % (100 - r, r, r, 100 + r, c, .95 - i * .12)
    return o + '<ellipse cx="34" cy="244" rx="30" ry="12" %s/><ellipse cx="170" cy="244" rx="30" ry="12" %s/>' % (fl(p['l'], .7), fl(p['l'], .7))
@motif
def star(p):
    import math
    pts = []
    for i in range(10):
        r = 72 if i % 2 == 0 else 30; a = -math.pi / 2 + i * math.pi / 5; pts.append('%s,%s' % (round(100 + r * math.cos(a), 1), round(160 + r * math.sin(a), 1)))
    return '<polygon points="%s" %s/><polygon points="%s" fill="none" stroke="%s" stroke-width="3" opacity=".6" transform="translate(100 160) scale(1.18) translate(-100 -160)"/>' % (' '.join(pts), fl(p['a']), ' '.join(pts), p['l'])
@motif
def neon(p):
    return ('<rect x="0" y="0" width="200" height="300" %s/><rect x="34" y="110" width="132" height="90" rx="12" fill="none" stroke="%s" stroke-width="5"/><rect x="42" y="118" width="116" height="74" rx="8" fill="none" stroke="%s" stroke-width="2" opacity=".6"/>' % (fl(p['d'], .35), p['a'], p['l']) +
            '<path d="M60 160 Q80 130 100 160 T140 160" fill="none" stroke="%s" stroke-width="5"/><circle cx="100" cy="155" r="70" %s/><circle cx="100" cy="155" r="40" %s/>' % (p['l'], fl(p['a'], .12), fl(p['a'], .12)))
@motif
def globe(p):
    return ('<circle cx="100" cy="160" r="70" %s/><ellipse cx="100" cy="160" rx="30" ry="70" fill="none" stroke="%s" stroke-width="2.5" opacity=".6"/><path d="M30 160 H170 M42 120 H158 M42 200 H158" stroke="%s" stroke-width="2.5" opacity=".6"/>' % (fl(p['a'], .9), p['d'], p['d']) +
            '<path d="M60 130 Q80 110 100 128 Q94 150 76 148Z M114 170 Q136 160 148 184 Q128 206 112 192Z" %s/><path d="M20 230 Q100 280 180 230" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="5 6" opacity=".7"/>' % (fl(p['d'], .55), p['l']))
@motif
def planet(p):
    return ('<circle cx="100" cy="160" r="56" %s/><path d="M66 140 Q90 126 112 146 Q100 168 72 162Z M104 184 Q130 176 142 196 Q120 214 100 202Z" %s/><ellipse cx="100" cy="160" rx="92" ry="18" fill="none" stroke="%s" stroke-width="4" opacity=".7" transform="rotate(-18 100 160)"/>' % (fl(p['a']), fl(p['d'], .3), p['l']) +
            '<circle cx="36" cy="86" r="2" %s/><circle cx="164" cy="82" r="1.6" %s/><circle cx="170" cy="240" r="2" %s/><circle cx="30" cy="236" r="1.5" %s/>' % ((fl(p['l']),) * 4))
@motif
def ladder(p):
    o = '<circle cx="100" cy="92" r="26" %s/><circle cx="100" cy="92" r="20" %s/><path d="M0 262 Q100 236 200 262 V300 H0Z" %s/>' % (fl(p['l'], .9), fl(p['d'], .35), fl(p['d']))
    o += '<rect x="76" y="126" width="6" height="136" %s/><rect x="118" y="126" width="6" height="136" %s/>' % (fl(p['l']), fl(p['l']))
    for i in range(6): o += '<rect x="76" y="%s" width="48" height="5" %s/>' % (140 + i * 20, fl(p['a']))
    return o
@motif
def golf(p):
    return ('<ellipse cx="100" cy="250" rx="96" ry="26" %s/><ellipse cx="108" cy="244" rx="26" ry="7" %s/><rect x="106" y="108" width="3" height="136" %s/><polygon points="109,108 150,124 109,140" %s/><circle cx="70" cy="238" r="7" %s/>' % (fl(p['a'], .6), fl(p['d']), fl(p['l']), fl(p['a']), fl(p['l'])) +
            '<circle cx="150" cy="90" r="22" %s/>' % fl(p['l'], .85))
@motif
def helmet(p):
    return ('<path d="M40 178 Q36 98 100 90 Q168 92 166 170 L152 196 H110 V218 H66 Q56 200 40 178Z" %s/><path d="M100 90 V130 H160" fill="none" stroke="%s" stroke-width="3" opacity=".4"/>' % (fl(p['a']), p['d']) +
            '<path d="M110 176 H168 M110 190 H160 M110 204 H150 M130 176 V214" stroke="%s" stroke-width="5" fill="none"/><circle cx="84" cy="170" r="6" %s/><path d="M64 120 Q80 104 100 102" stroke="%s" stroke-width="4" fill="none" opacity=".6"/>' % (p['l'], fl(p['d']), p['l']))
@motif
def brain(p):
    return ('<path d="M100 96 Q60 70 44 112 Q22 130 46 156 Q34 190 70 196 Q88 224 100 214 Q112 224 130 196 Q166 190 154 156 Q178 130 156 112 Q140 70 100 96Z" %s/>' % fl(p['a']) +
            '<path d="M100 96 V214 M66 120 Q86 130 78 154 M134 120 Q114 130 122 154 M58 168 Q80 164 88 184 M142 168 Q120 164 112 184" stroke="%s" stroke-width="3" fill="none" opacity=".55"/>' % p['d'])
@motif
def ticket(p):
    return ('<g transform="rotate(-10 100 160)"><path d="M26 112 H174 V144 A14 14 0 0 0 174 172 V204 H26 V172 A14 14 0 0 0 26 144Z" %s/><path d="M132 112 V204" stroke="%s" stroke-width="2" stroke-dasharray="4 4"/>' % (fl(p['l']), p['d']) +
            '<text x="78" y="166" text-anchor="middle" font-family="Big Shoulders Display,Impact,sans-serif" font-weight="800" font-size="36" %s>$</text><text x="153" y="166" text-anchor="middle" font-family="Big Shoulders Display,Impact,sans-serif" font-weight="800" font-size="20" %s>00</text></g>' % (fl(p['a']), fl(p['d'])))
@motif
def pool(p):
    o = '<rect x="0" y="100" width="200" height="200" %s/>' % fl(p['a'], .35)
    for i in range(5): o += '<path d="M0 %s Q25 %s 50 %s T100 %s T150 %s T200 %s" fill="none" stroke="%s" stroke-width="2.2" opacity=".8"/>' % ((130 + i * 30,) * 1 + (120 + i * 30, 130 + i * 30, 130 + i * 30, 130 + i * 30, 130 + i * 30) + (p['l'],))
    o += '<path d="M0 118 H200" stroke="%s" stroke-width="5"/>' % p['l'] + '<circle cx="60" cy="170" r="7" %s/><path d="M44 184 Q70 160 100 178" stroke="%s" stroke-width="9" fill="none" stroke-linecap="round"/>' % (fl(p['l']), p['l'])
    return o
@motif
def racket(p):
    return ('<g transform="rotate(32 100 150)"><ellipse cx="100" cy="126" rx="36" ry="48" fill="none" stroke="%s" stroke-width="7"/><path d="M100 78 V174 M64 126 H136 M72 98 H128 M72 154 H128 M82 84 V168 M118 84 V168" stroke="%s" stroke-width="1" opacity=".6"/><rect x="96" y="174" width="8" height="64" rx="3" %s/><rect x="94" y="204" width="12" height="40" rx="5" %s/></g>' % (p['a'], p['l'], fl(p['l']), fl(p['d'])) +
            '<circle cx="150" cy="216" r="12" %s/><path d="M140 212 Q150 222 160 212" stroke="%s" stroke-width="1.6" fill="none"/>' % (fl(p['a2']), p['d']))
@motif
def laptop(p):
    return ('<rect x="46" y="110" width="108" height="76" rx="6" %s/><rect x="52" y="116" width="96" height="64" %s/><path d="M30 190 H170 L180 206 H20Z" %s/>' % (fl(p['d']), fl(p['a'], .85), fl(p['l'], .85)) +
            '<path d="M62 134 H98 M62 148 H120 M62 162 H88" stroke="%s" stroke-width="3" opacity=".8"/><circle cx="128" cy="148" r="14" %s/>' % (p['d'], fl(p['l'], .6)))
@motif
def cage(p):
    o = '<ellipse cx="100" cy="246" rx="92" ry="24" %s/>' % fl(p['a'], .6)
    o += '<polygon points="30,246 170,246 188,110 12,110" %s/>' % fl(p['d'], .3)
    for i in range(8): o += '<path d="M%s 246 L%s 110" stroke="%s" stroke-width="1.6" opacity=".55"/>' % (30 + i * 20, 12 + i * 25.1, p['l'])
    for y in (140, 176, 212): o += '<path d="M%s %s H%s" stroke="%s" stroke-width="1.6" opacity=".55"/>' % (20 + (y - 140) * .1, y, 180 - (y - 140) * .1, p['l'])
    return o + '<rect x="10" y="102" width="180" height="10" rx="4" %s/>' % fl(p['l'])
@motif
def reactor(p):
    o = ''
    for r, op in ((78, .12), (62, .22), (46, .4)): o += '<circle cx="100" cy="160" r="%s" %s/>' % (r, fl(p['a'], op))
    o += '<circle cx="100" cy="160" r="40" fill="none" stroke="%s" stroke-width="5"/><circle cx="100" cy="160" r="24" fill="none" stroke="%s" stroke-width="3"/><circle cx="100" cy="160" r="12" %s/>' % (p['l'], p['l'], fl(p['l']))
    for i in range(10):
        import math; a = i * math.pi / 5; o += '<path d="M%s %s L%s %s" stroke="%s" stroke-width="5"/>' % (round(100 + 26 * math.cos(a), 1), round(160 + 26 * math.sin(a), 1), round(100 + 40 * math.cos(a), 1), round(160 + 40 * math.sin(a), 1), p['l'])
    return o
@motif
def beam(p):
    return ('<rect x="14" y="170" width="172" height="16" rx="6" %s/><rect x="46" y="186" width="8" height="70" %s/><rect x="146" y="186" width="8" height="70" %s/><rect x="30" y="256" width="40" height="6" %s/><rect x="130" y="256" width="40" height="6" %s/>' % (fl(p['a']), fl(p['l'], .8), fl(p['l'], .8), fl(p['l'], .8), fl(p['l'], .8)) +
            '<circle cx="104" cy="96" r="9" %s/><path d="M104 106 L104 140 M104 118 L70 100 M104 118 L142 92 M104 140 L84 168 M104 140 L128 164" stroke="%s" stroke-width="8" stroke-linecap="round" fill="none"/>' % (fl(p['l']), p['l']))
@motif
def beehive(p):
    return ('<ellipse cx="100" cy="112" rx="32" ry="52" %s/><path d="M70 150 Q68 190 80 200 L84 262 H116 L120 200 Q132 190 130 150Z" %s/>' % (fl(p['d']), fl(p['d'])) +
            '<path d="M70 124 H130 M74 100 H126 M82 78 H118" stroke="%s" stroke-width="3" opacity=".35"/><path d="M80 152 Q100 168 120 152" fill="none" stroke="%s" stroke-width="3"/>' % (p['a'], p['l']) +
            '<circle cx="100" cy="132" r="64" %s/><path d="M82 142 Q84 150 94 148 M108 148 Q116 150 118 142" stroke="%s" stroke-width="2" fill="none"/>' % (fl(p['a'], .15), p['l']))
@motif
def pizza(p):
    import math
    o = '<circle cx="100" cy="160" r="70" %s/><circle cx="100" cy="160" r="60" %s/>' % (fl(p['a2']), fl(p['a']))
    for i in range(8):
        a = i * math.pi / 4; o += '<path d="M100 160 L%s %s" stroke="%s" stroke-width="2.4" opacity=".7"/>' % (round(100 + 60 * math.cos(a), 1), round(160 + 60 * math.sin(a), 1), p['d'])
    for (x, y) in ((76, 130), (124, 134), (96, 180), (130, 182), (72, 176)): o += '<circle cx="%s" cy="%s" r="8" %s/>' % (x, y, fl(p['d'], .7))
    return o
@motif
def shoe(p):
    return ('<path d="M28 214 V150 Q28 140 38 140 H70 Q80 160 100 164 Q130 170 146 192 H176 Q186 196 184 214 Z" %s/><rect x="22" y="214" width="170" height="14" rx="6" %s/>' % (fl(p['a']), fl(p['l'])) +
            '<path d="M80 168 L92 156 M96 174 L108 162 M112 180 L124 168" stroke="%s" stroke-width="3"/><path d="M40 150 H66" stroke="%s" stroke-width="3" opacity=".6"/>' % (p['l'], p['l']))
@motif
def sun(p):
    import math
    o = ''
    for i in range(16):
        a = i * math.pi / 8; o += '<path d="M%s %s L%s %s" stroke="%s" stroke-width="4" opacity=".7"/>' % (round(100 + 52 * math.cos(a), 1), round(160 + 52 * math.sin(a), 1), round(100 + 72 * math.cos(a), 1), round(160 + 72 * math.sin(a), 1), p['a'])
    return o + '<circle cx="100" cy="160" r="40" %s/>' % fl(p['a'])

ALIAS = {'tree': 'forest'}

# ---------- affectation motif -> épisode (ordre des épisodes de chaque vie) ----------
ASSIGN = {
 'pt01': 'stage clapper rainbow ring door trophy curtain window candle',
 'pt02': 'house emptyroom vinyl mirror fire crown scales court stage',
 'pt03': 'court book flashes scissors bars crowd sunrise',
 'pt04': 'star house money gavel mirror rain family',
 'pt05': 'cross moon neon door court road lens',
 'pt06': 'ball family stadium trophy crowd shadow heart candle',
 'pt07': 'ringbox glove trophy ring bars ringbox chartdown stage',
 'pt08': 'ocean bike mountain flask shadow road crowd',
 'pt09': 'ocean helmet emptyroom brain court',
 'pt10': 'mic stadium city family crowd moon',
 'pt11': 'guitar vinyl bottle beehive flashes trophy door candle',
 'pt12': 'house guitar tv crowd window emptyroom',
 'pt13': 'church trophy vinyl clapper flashes stage candle',
 'pt14': 'laptop stage cross bed ocean sunrise',
 'pt15': 'house crown heart dress rain clapper emptyroom sunrise',
 'pt16': 'flashes ring family book ocean scales',
 'pt17': 'tv rain crowd church guitar house',
 'pt18': 'car vinyl stage chartdown sunrise phone',
 'pt19': 'laptop blocks money shadow',
 'pt20': 'door guitar lock ring vinyl plane',
 'pt21': 'ticket money neon family tv',
 'pt22': 'car crowd moon letter trophy',
 'pt23': 'door clapper mountain cards star emptyroom',
 'pt24': 'kitchen book globe mirror suitcase candle',
 'pt25': 'book paint stairs lens court',
 'pt26': 'runway scissors tower rain dress',
 'pt27': 'sunrise cross crown dress desert church',
 'pt28': 'ladder rocket globe bottle shadow planet',
 'pt29': 'emptyroom pool medal sunrise heart',
 'pt30': 'racket crown shadow chartup',
 'pt31': 'letter mirror chartdown crowd book',
 'pt32': 'stadium cage trophy ringbox',
 'pt33': 'letter mask tower flask chartdown book',
 'pt34': 'ocean chartup safe gavel scales',
 'pt35': 'desert tower money house',
 'pt36': 'bars house plane letter gavel tv',
 'pt37': 'medal pizza shoe money fire',
 'pt38': 'phone chartup safe chartdown court bars',
 'pt39': 'sunrise mask letter lock chartdown tv',
 'pt40': 'suitcase crown cuffs night',
 'pt41': 'tower chartup money letter family bars candle',
 'pt42': 'clapper phone ship stage',
 'pt43': 'tv cross bike shadow chartdown',
 'pt44': 'chase helmet door gavel book bars',
 'pt45': 'news lock gavel',
 'pt46': 'phone track gavel',
 'pt47': 'golf car cross car',
 'pt48': 'house bars ocean reactor trophy',
 'pt49': 'ocean tv house mic',
 'pt50': 'mic vinyl rain crowd',
 'pt51': 'beam family door sunrise',
 'pt52': 'road mic track family',
}

def label(title):
    t = re.sub(r'[«»“”"]', '', title).replace('’', "'").upper().strip()
    t = re.sub(r'\s+', ' ', t)
    return t

def wrap(t, mx=18):
    if len(t) <= mx: return [t]
    w = t.split(' '); best = None
    for i in range(1, len(w)):
        a, b = ' '.join(w[:i]), ' '.join(w[i:])
        sc = max(len(a), len(b))
        if best is None or sc < best[0]: best = (sc, a, b)
    a, b = best[1], best[2]
    if len(a) > 24: a = a[:23] + '…'
    if len(b) > 24: b = b[:23] + '…'
    return [a, b]

def build(pid, n, N, title, name):
    p = palette(pid)
    if n % 2 == 0: p = dict(p, a=p['a2'], a2=p['a'])
    gx = (60, 100, 140)[n % 3]
    scene = M[ALIAS.get(name, name)](p)
    lines = wrap(label(title))
    fs = 10.5 if max(len(x) for x in lines) <= 18 else 9
    w = max(len(x) for x in lines) * fs * .68 + 22
    h = 16 if len(lines) == 1 else 28
    y0 = 36
    lab = '<g><rect x="%.1f" y="%s" width="%.1f" height="%s" rx="%s" %s/>' % (100 - w / 2, y0, w, h, 8 if len(lines) == 1 else 10, fl('#000', .62))
    for i, ln in enumerate(lines):
        lab += '<text x="100" y="%.1f" text-anchor="middle" font-family="Big Shoulders Display,Impact,Arial Narrow,sans-serif" font-weight="800" font-size="%s" letter-spacing="1.1" fill="%s">%s</text>' % (y0 + 11.4 + i * 12, fs, p['l'], ln.replace('&', '&amp;'))
    lab += '</g>'
    ep = '<text x="100" y="288" text-anchor="middle" font-family="Big Shoulders Display,Impact,Arial Narrow,sans-serif" font-weight="800" font-size="9" letter-spacing="2.4" fill="%s" opacity=".85">ÉPISODE %s / %s</text>' % (p['l'], n, N)
    return ('<svg viewBox="0 0 200 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs><linearGradient id="gX" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="#0A0708"/></linearGradient>'
            '<radialGradient id="gY" cx="%s%%" cy="46%%" r="62%%"><stop offset="0" stop-color="%s" stop-opacity=".34"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient></defs>'
            '<rect width="200" height="300" fill="url(#gX)"/><rect width="200" height="300" fill="url(#gY)"/>%s'
            '<rect y="236" width="200" height="64" fill="url(#gX)" opacity="0"/><rect width="200" height="300" fill="none"/>%s%s</svg>') % (p['b0'], gx / 2, p['a'], p['a'], scene, lab, ep)

def main():
    bad = 0; made = 0
    for k in [k for k in COV if re.match(r'pt\d\de\d+$', k)]: del COV[k]
    for pid in sorted(LIV):
        eps = LIV[pid]['eps']; names = ASSIGN.get(pid, '').split()
        if len(names) != len(eps):
            print('! %s : %d motifs pour %d épisodes' % (pid, len(names), len(eps))); bad += 1; continue
        for i, (e, nm) in enumerate(zip(eps, names), 1):
            if ALIAS.get(nm, nm) not in M: print('! motif inconnu', nm, pid, i); bad += 1; continue
            COV['%se%d' % (pid, i)] = build(pid, i, len(eps), e['t'], nm); made += 1
    json.dump(COV, open(R + '/data/covers.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    print('couvertures d\'épisodes :', made, '· erreurs :', bad)
    return bad

if __name__ == '__main__':
    sys.exit(1 if main() else 0)
