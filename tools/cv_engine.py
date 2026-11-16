"""Moteur des couvertures d'épisodes : cadre (dégradé, ambiance, décor, grain, vignette), outils de dessin.
Style maison : aplats, contours encre #0B0909, reflets crème, grain, vignette — comme les affiches de base."""
import re, json, math, colorsys

INK = '#0B0909'; CREAM = '#F4E6C8'; RED = '#D2232C'; GOLD = '#E8B04A'; GOLD2 = '#F2C14E'; WHITE = '#FFFFFF'
ST = 'stroke="%s" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"' % INK
ST2 = 'stroke="%s" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"' % INK

def hx(c):
    c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
def rgb(t): return '#%02X%02X%02X' % tuple(max(0, min(255, int(round(v)))) for v in t)
def mix(a, b, t):
    A, B = hx(a), hx(b); return rgb([A[i] + (B[i] - A[i]) * t for i in range(3)])

def palette(svg):
    stops = re.findall(r'stop-color="#([0-9A-Fa-f]{6})"', svg)
    b0 = '#' + stops[0]; b1 = '#' + (stops[1] if len(stops) > 1 else '0A0708')
    cnt = {}
    for c in re.findall(r'#([0-9A-Fa-f]{6})', svg):
        r, g, b = hx(c); h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s > .38 and v > .55 and c.upper() not in ('F4E6C8',): cnt[c.upper()] = cnt.get(c.upper(), 0) + 1
    br = sorted(cnt, key=lambda k: -cnt[k])
    a = '#' + br[0] if br else GOLD; a2 = '#' + br[1] if len(br) > 1 else mix(a, CREAM, .35)
    return dict(b0=b0, b1=b1, a=a, a2=a2, l=CREAM, d=INK)

MOODS = {
    'nuit':   lambda p: dict(p, b0=mix(p['b0'], '#0B1030', .55), b1='#05060F'),
    'aube':   lambda p: dict(p, b0=mix(p['b0'], '#F0A25A', .45), b1=mix(p['b1'], '#3A1A22', .4)),
    'jour':   lambda p: dict(p, b0=mix(p['b0'], '#E8D3A0', .38), b1=mix(p['b1'], p['b0'], .3)),
    'alerte': lambda p: dict(p, b0=mix(p['b0'], '#A81420', .6), b1='#1A0305'),
    'froid':  lambda p: dict(p, b0=mix(p['b0'], '#5C7A92', .55), b1='#0A1018'),
    'cendre': lambda p: dict(p, b0=mix(p['b0'], '#6E6A66', .6), b1='#121110'),
    'or':     lambda p: dict(p, b0=mix(p['b0'], '#B9801E', .5), b1=mix(p['b1'], '#2A1606', .5)),
    'vert':   lambda p: dict(p, b0=mix(p['b0'], '#1E6B44', .55), b1='#04120B'),
    'violet': lambda p: dict(p, b0=mix(p['b0'], '#5A2A86', .55), b1='#0C0614'),
    'standard': lambda p: p,
}

def F(c, op=1): return 'fill="%s"%s' % (c, '' if op == 1 else ' opacity="%s"' % op)
def person(x, y, s=1.0, c=INK, op=1):
    return ('<g fill="%s" opacity="%s"><circle cx="%.1f" cy="%.1f" r="%.1f"/><path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %.1f H%.1f Z"/></g>'
            % (c, op, x, y, 11 * s, x - 22 * s, y + 18 * s, x, y + 8 * s, x + 22 * s, y + 18 * s, x + 26 * s, y + 92 * s, x - 26 * s))
def poly(pts, fill, extra=''): return '<polygon points="%s" fill="%s" %s/>' % (' '.join('%s,%s' % (round(x, 1), round(y, 1)) for x, y in pts), fill, extra)
def txt(x, y, s, size, fill, anchor='middle', ls=1, weight=800, font="Big Shoulders Display,Impact,Arial Narrow,sans-serif", extra=''):
    s = s.replace('&', '&amp;')
    return '<text x="%s" y="%s" text-anchor="%s" font-family="%s" font-weight="%s" font-size="%s" letter-spacing="%s" fill="%s" %s>%s</text>' % (x, y, anchor, font, weight, size, ls, fill, extra, s)
def sparkle(x, y, s, c=CREAM, op=.95):
    return '<polygon points="%s,%s %s,%s %s,%s %s,%s %s,%s %s,%s %s,%s %s,%s" fill="%s" opacity="%s"/>' % (
        x, y - s, x + s * .22, y - s * .22, x + s, y, x + s * .22, y + s * .22, x, y + s, x - s * .22, y + s * .22, x - s, y, x - s * .22, y - s * .22, c, op)
def stars(p, n=18, seed=3, y0=0, y1=170):
    o = ''; r = seed
    for i in range(n):
        r = (r * 1103515245 + 12345) & 0x7fffffff; x = r % 200
        r = (r * 1103515245 + 12345) & 0x7fffffff; y = y0 + r % max(1, (y1 - y0))
        o += '<circle cx="%d" cy="%d" r="%.1f" fill="%s" opacity=".%d"/>' % (x, y, .7 + (r % 3) * .5, CREAM, 4 + r % 5)
    return o
def ground(p, y=250, col=None, h=None):
    return '<rect x="-2" y="%s" width="204" height="%s" fill="%s"/>' % (y, 304 - y, col or INK) + '<ellipse cx="100" cy="%s" rx="62" ry="7" fill="%s" opacity=".45"/>' % (y + 1, INK)
def halo(p, cx=100, cy=140, r=62, op=.2, col=None):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>' % (cx, cy, r, col or CREAM, op)

# ------------------------------------------------------------------ décors (derrière le héros)
BG = {}
def bg(f): BG[f.__name__] = f; return f

@bg
def nu(p): return ''
@bg
def spot(p): return '<polygon points="70,0 130,0 176,262 24,262" fill="%s" opacity=".17"/>' % CREAM
@bg
def scene(p): return ('<path d="M0 0 H56 Q42 120 30 300 H0Z" fill="%s" opacity=".85"/><path d="M200 0 H144 Q158 120 170 300 H200Z" fill="%s" opacity=".85"/>' % (mix(p['b0'], INK, .45), mix(p['b0'], INK, .45)) +
                      '<polygon points="76,0 124,0 168,262 32,262" fill="%s" opacity=".17"/><ellipse cx="100" cy="262" rx="72" ry="11" fill="%s" opacity=".6"/>' % (CREAM, p['a']))
@bg
def brique(p):
    o = '<rect width="200" height="300" fill="%s" opacity=".35"/>' % mix(p['b0'], INK, .2)
    for r in range(15):
        y = r * 20
        o += '<path d="M0 %s H200" stroke="%s" stroke-width="1.6" opacity=".35"/>' % (y, INK)
        for c in range(6): o += '<path d="M%s %s v20" stroke="%s" stroke-width="1.6" opacity=".35"/>' % ((c * 40 + (20 if r % 2 else 0)), y, INK)
    return o
@bg
def ville_nuit(p):
    o = stars(p, 22, 7, 0, 130) + '<circle cx="152" cy="82" r="20" fill="%s" opacity=".92"/><circle cx="160" cy="76" r="17" fill="%s"/>' % (CREAM, p['b0'])
    xs = [(-6, 70, 34), (26, 110, 30), (54, 84, 34), (86, 134, 30), (114, 96, 36), (148, 122, 30), (176, 80, 34)]
    for i, (x, h, w) in enumerate(xs):
        o += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s" opacity="%s"/>' % (x, 262 - h, w, h, INK, .55 + (i % 3) * .15)
        for j in range(int(h / 17)):
            if (i + j) % 3: o += '<rect x="%s" y="%s" width="4" height="6" fill="%s" opacity=".75"/>' % (x + 6 + (j % 2) * 12, 268 - h + j * 17, p['a2'])
    return o
@bg
def ville_aube(p):
    o = '<circle cx="100" cy="196" r="58" fill="%s" opacity=".75"/>' % p['a2'] + '<circle cx="100" cy="196" r="92" fill="%s" opacity=".15"/>' % p['a']
    for i, (x, h, w) in enumerate([(-4, 70, 36), (30, 104, 30), (58, 84, 30), (90, 120, 28), (116, 90, 34), (148, 112, 28), (174, 74, 34)]):
        o += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s" opacity="%s"/>' % (x, 262 - h, w, h, INK, .5 + (i % 3) * .18)
    return o
@bg
def horizon_mer(p):
    o = '<circle cx="100" cy="170" r="42" fill="%s" opacity=".8"/>' % p['a2']
    for i in range(7):
        y = 176 + i * 15
        o += '<path d="M-10 %s Q15 %s 40 %s T90 %s T140 %s T190 %s T240 %s V310 H-10Z" fill="%s" opacity="%s"/>' % (y, y - 7, y, y, y, y, y, INK, .12 + i * .1)
    return o
@bg
def rayons(p):
    o = ''
    for i in range(18):
        a = math.pi + i * math.pi / 17 * 1.0
        o += '<path d="M100 250 L%.1f %.1f L%.1f %.1f Z" fill="%s" opacity="%s"/>' % (100 + 260 * math.cos(a - .06), 250 + 260 * math.sin(a - .06), 100 + 260 * math.cos(a + .06), 250 + 260 * math.sin(a + .06), p['a'] if i % 2 else CREAM, .13 if i % 2 else .07)
    return o + '<circle cx="100" cy="250" r="44" fill="%s" opacity=".5"/>' % p['a2']
@bg
def stores(p):
    o = '<rect width="200" height="300" fill="%s" opacity=".3"/>' % mix(p['b0'], INK, .4)
    for i in range(0, 300, 14): o += '<rect x="0" y="%s" width="200" height="6" fill="%s" opacity=".5"/>' % (i, INK)
    return o + '<polygon points="0,40 200,0 200,120 0,170" fill="%s" opacity=".13"/>' % CREAM
@bg
def pluie(p):
    o = ''
    for i in range(46): o += '<path d="M%s %s l-6 20" stroke="%s" stroke-width="1.6" opacity=".5"/>' % ((i * 37) % 210, (i * 53) % 270, CREAM)
    return '<rect width="200" height="300" fill="%s" opacity=".25"/>' % INK + o
@bg
def brume(p):
    return ''.join('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" opacity=".11"/>' % (x, y, rx, ry, CREAM) for x, y, rx, ry in ((40, 220, 90, 20), (170, 190, 80, 16), (100, 250, 120, 24), (30, 120, 70, 12)))
@bg
def diag(p):
    o = ''
    for i in range(-3, 9): o += '<polygon points="%s,0 %s,0 %s,300 %s,300" fill="%s" opacity=".08"/>' % (i * 34, i * 34 + 14, i * 34 - 70 + 14, i * 34 - 70, CREAM)
    return o
@bg
def pellicule(p):
    o = '<rect x="0" y="0" width="30" height="300" fill="%s" opacity=".7"/><rect x="170" y="0" width="30" height="300" fill="%s" opacity=".7"/>' % (INK, INK)
    for i in range(0, 300, 22): o += '<rect x="8" y="%s" width="14" height="12" rx="2" fill="%s" opacity=".7"/><rect x="178" y="%s" width="14" height="12" rx="2" fill="%s" opacity=".7"/>' % (i + 4, CREAM, i + 4, CREAM)
    return o
@bg
def presse(p):
    o = '<rect width="200" height="300" fill="%s" opacity=".28"/>' % CREAM
    for i in range(0, 300, 9): o += '<rect x="%s" y="%s" width="%s" height="2.4" fill="%s" opacity=".13"/>' % (10 + (i * 7) % 20, i, 120 + (i * 13) % 60, INK)
    return o
@bg
def trame(p):
    o = ''
    for y in range(0, 300, 10):
        for x in range(0, 200, 10): o += '<circle cx="%s" cy="%s" r="%.1f" fill="%s" opacity=".09"/>' % (x + (5 if (y // 10) % 2 else 0), y, 1 + ((x + y) % 30) / 20, CREAM)
    return o
@bg
def tribunes(p):
    o = '<rect x="0" y="100" width="200" height="120" fill="%s" opacity=".45"/>' % INK
    for r in range(5):
        for i in range(24): o += '<circle cx="%s" cy="%s" r="2.2" fill="%s" opacity="%s"/>' % (4 + i * 8.4 + (r % 2) * 4, 112 + r * 20, [p['a'], CREAM, p['a2']][(i + r) % 3], .55)
    return o + '<polygon points="20,0 -20,230 60,230" fill="%s" opacity=".12"/><polygon points="180,0 220,230 140,230" fill="%s" opacity=".12"/>' % (CREAM, CREAM)
@bg
def flammes(p):
    o = ''
    for i in range(9):
        x = i * 26 - 4; h = 80 + (i * 37) % 60
        o += '<path d="M%s 300 Q%s %s %s %s Q%s %s %s 300Z" fill="%s" opacity="%s"/>' % (x, x - 10, 300 - h * .5, x + 8, 300 - h, x + 28, 300 - h * .4, x + 34, p['a'] if i % 2 else p['a2'], .4)
    return o
@bg
def montagne(p):
    return ('<circle cx="146" cy="96" r="22" fill="%s" opacity=".9"/><polygon points="-10,262 50,130 90,196 124,150 210,262" fill="%s" opacity=".55"/><polygon points="40,262 112,96 190,262" fill="%s" opacity=".85"/>' % (CREAM, INK, INK) +
            '<polygon points="112,96 96,132 106,126 112,138 120,124 130,132" fill="%s"/>' % CREAM)
@bg
def desert(p):
    return ('<circle cx="100" cy="168" r="46" fill="%s" opacity=".85"/>' % p['a2'] + '<path d="M-10 214 Q50 168 110 206 T210 196 V310 H-10Z" fill="%s" opacity=".5"/><path d="M-10 244 Q70 206 140 240 T210 232 V310 H-10Z" fill="%s" opacity=".9"/>' % (INK, INK))
@bg
def carreaux(p):
    o = '<polygon points="0,300 70,196 130,196 200,300" fill="%s" opacity=".85"/>' % INK
    for i in range(0, 9): o += '<path d="M%s 196 L%s 300" stroke="%s" stroke-width="1.4" opacity=".3"/>' % (70 + i * 7.5, i * 25, CREAM)
    for y in (214, 238, 270): o += '<path d="M%s %s H%s" stroke="%s" stroke-width="1.4" opacity=".3"/>' % (70 - (y - 196) * .7, y, 130 + (y - 196) * .7, CREAM)
    return o
@bg
def route(p):
    return ('<circle cx="100" cy="126" r="40" fill="%s" opacity=".85"/><polygon points="95,150 105,150 214,310 -14,310" fill="%s" opacity=".9"/>' % (p['a2'], INK) +
            '<path d="M100 156 V176 M100 192 V220 M100 240 V280" stroke="%s" stroke-width="4" opacity=".85"/>' % CREAM)
@bg
def cadre(p):
    return '<rect x="14" y="14" width="172" height="272" fill="none" stroke="%s" stroke-width="1.4" opacity=".45"/><rect x="22" y="22" width="156" height="256" fill="none" stroke="%s" stroke-width=".8" opacity=".3"/>' % (CREAM, CREAM)
@bg
def reseau(p):
    o = ''; pts = [(30, 90), (88, 60), (150, 100), (60, 170), (130, 190), (176, 160), (100, 130)]
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if (i * 3 + j) % 3 == 0: o += '<path d="M%s %s L%s %s" stroke="%s" stroke-width="1" opacity=".35"/>' % (pts[i] + pts[j] + (CREAM,))
    return o + ''.join('<circle cx="%s" cy="%s" r="3" fill="%s" opacity=".6"/>' % (x, y, p['a2']) for x, y in pts)
@bg
def marbre(p):
    return ('<rect y="0" width="200" height="300" fill="%s" opacity=".18"/>' % CREAM + ''.join('<rect x="%s" y="40" width="22" height="210" fill="%s" opacity=".35"/><rect x="%s" y="34" width="30" height="8" fill="%s" opacity=".4"/>' % (i * 66 - 4 + 12, INK, i * 66 - 8 + 12, INK) for i in range(4)))
@bg
def etoiles(p): return stars(p, 40, 11, 0, 260)
@bg
def lueur(p): return '<circle cx="100" cy="150" r="96" fill="%s" opacity=".16"/><circle cx="100" cy="150" r="62" fill="%s" opacity=".14"/>' % (p['a'], p['a2'])
@bg
def balayage(p):
    return '<polygon points="30,0 70,0 150,300 -10,300" fill="%s" opacity=".08"/><polygon points="170,0 130,0 50,300 210,300" fill="%s" opacity=".08"/>' % (CREAM, CREAM)

# ------------------------------------------------------------------ cadre final
def frame(p, mood, scene_svg, bgname, label_lines, tag, glowx=50):
    pm = MOODS[mood](p)
    cap = 3
    defs = ('<defs><linearGradient id="gX" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
            '<radialGradient id="vgP" cx=".5" cy=".42" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>'
            '<pattern id="dtP" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#fff" opacity=".08"/></pattern></defs>') % (pm['b0'], pm['b1'])
    return pm, defs

def wrap(t, mx=17):
    if len(t) <= mx: return [t]
    w = t.split(' '); best = None
    for i in range(1, len(w)):
        a, b = ' '.join(w[:i]), ' '.join(w[i:]); sc = max(len(a), len(b))
        if best is None or sc < best[0]: best = (sc, a, b)
    if best is None: return [t[:20]]
    a, b = best[1], best[2]
    if len(a) > 24: a = a[:23] + '…'
    if len(b) > 24: b = b[:23] + '…'
    return [a, b]

def labelsvg(lines, p):
    mx = max(len(x) for x in lines); fs = 10.5 if mx <= 17 else 9.2
    w = mx * fs * .66 + 24; h = 16 if len(lines) == 1 else 28; y0 = 36
    o = '<g><rect x="%.1f" y="%s" width="%.1f" height="%s" rx="%s" fill="#000" opacity=".62"/>' % (100 - w / 2, y0, w, h, 8 if len(lines) == 1 else 10)
    for i, ln in enumerate(lines): o += txt(100, round(y0 + 11.4 + i * 12, 1), ln, fs, CREAM, ls=1.3)
    return o + '</g>'
