from cv_engine import *
from cv_heroes1 import hl
H = {}
def hero(f): H[f.__name__] = f; return f
GREY = '#9AA0AA'; SKIN = '#E0B58A'
def card(x, y, w, h, fill, r=3): return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" %s/>' % (x, y, w, h, r, fill, ST)

# ---------- génériques paramétrables ----------
@hero
def journal(p, **k):
    t = k.get('t', 'ÉDITION SPÉCIALE'); l = wrap(t, 13)
    o = '<g transform="rotate(-4 100 160)">' + card(40, 80, 120, 164, CREAM) + '<rect x="48" y="88" width="104" height="38" fill="%s"/>' % INK
    for i, ln in enumerate(l[:2]): o += txt(100, 104 + i * 15, ln, 13, CREAM, ls=1)
    o += '<rect x="48" y="134" width="46" height="40" fill="%s" opacity=".85"/>' % p['a']
    o += ''.join('<rect x="100" y="%s" width="52" height="3" fill="%s" opacity=".6"/>' % (136 + i * 9, INK) for i in range(5)) + ''.join('<rect x="48" y="%s" width="104" height="3" fill="%s" opacity=".5"/>' % (186 + i * 10, INK) for i in range(5))
    return o + '</g>'
@hero
def ecran(p, **k):
    t = k.get('t', 'LIVE')
    return ('<rect x="26" y="96" width="148" height="104" rx="10" fill="%s" %s/><rect x="34" y="104" width="132" height="88" rx="5" fill="%s"/>' % (INK, ST, mix(p['b0'], p['a'], .35)) + txt(100, 160, t, 30 if len(t) < 6 else round(min(30, 112 / (len(t) * .75)), 1), CREAM, ls=1.2) +
            '<path d="M34 112 H166" stroke="%s" stroke-width="1" opacity=".2"/><path d="M82 200 L76 228 H124 L118 200" fill="%s" %s/><rect x="62" y="228" width="76" height="8" rx="3" fill="%s" %s/>' % (CREAM, INK, ST2, INK, ST2) + '<path d="M40 112 L90 108" stroke="#fff" stroke-width="3" opacity=".25"/>' + k.get('extra', ''))
@hero
def plaque(p, **k):
    t = k.get('t', 'ENRON'); l = wrap(t, 9)
    o = '<rect x="96" y="150" width="8" height="108" fill="%s" %s/>' % (GREY, ST2) + card(24, 86, 152, 76 if len(l) > 1 else 60, k.get('c', CREAM))
    for i, ln in enumerate(l): o += txt(100, (132 if len(l) == 1 else 116) + i * 28, ln, 34 if len(l) == 1 and len(ln) < 7 else 28, INK, ls=2)
    return o
@hero
def lettre(p, **k):
    t = k.get('t', '')
    return ('<g transform="rotate(-6 100 160)">' + card(34, 100, 132, 96, CREAM) + '<path d="M34 104 L100 158 L166 104" fill="none" stroke="%s" stroke-width="3"/><circle cx="100" cy="158" r="11" fill="%s" %s/>' % (INK, p['a'], ST2) + '<path d="M34 196 L88 146 M166 196 L112 146" stroke="%s" stroke-width="1.6" opacity=".4"/>' % INK +
            ('<g transform="rotate(-3 100 80)">' + card(46, 54, 108, 54, mix(CREAM, p['a'], .15), 2) + txt(100, 87, t, 14, INK, ls=1) + '</g>' if t else '') + '</g>')
@hero
def affiche(p, **k):
    t = k.get('t', 'FILM'); l = wrap(t, 9)
    o = card(40, 70, 120, 178, mix(p['b0'], INK, .15), 4) + '<rect x="48" y="78" width="104" height="162" fill="none" stroke="%s" stroke-width="1.4" opacity=".6"/>' % p['a2']
    o += '<circle cx="100" cy="148" r="34" fill="%s" opacity=".9"/>' % p['a'] + person(100, 120, .8, INK, 1)
    for i, ln in enumerate(l): o += txt(100, 214 + i * 16, ln, 16, p['a2'], ls=2)
    return o + sparkle(58, 92, 7) + sparkle(144, 96, 6)
@hero
def chiffre(p, **k):
    t = k.get('t', '8'); c = k.get('c', p['a2'])
    return ('<circle cx="100" cy="166" r="76" fill="%s" %s/><circle cx="100" cy="166" r="64" fill="none" stroke="%s" stroke-width="2" opacity=".6"/>' % (INK, ST, c) + txt(100, 166 + (46 if len(t) < 3 else 32), t, 130 if len(t) < 2 else 96 if len(t) < 3 else 66 if len(t) < 4 else 44, c, ls=1, extra='stroke="%s" stroke-width="2"' % INK) + k.get('extra', ''))
@hero
def guitare(p, **k):
    c = k.get('c', p['a'])
    return ('<g transform="rotate(-30 100 168)"><rect x="95" y="46" width="10" height="108" fill="#6B4A2A" %s/><rect x="90" y="30" width="20" height="22" rx="3" fill="%s" %s/>' % (ST, INK, ST) + ''.join('<circle cx="%s" cy="%s" r="2" fill="%s"/>' % (94 if i % 2 else 106, 36 + i * 5, CREAM) for i in range(4)) +
            '<path d="M100 148 Q60 140 62 182 Q44 200 58 228 Q70 258 100 252 Q130 258 142 228 Q156 200 138 182 Q140 140 100 148Z" fill="%s" %s/>' % (c, ST) + '<circle cx="100" cy="196" r="13" fill="%s" %s/><rect x="82" y="226" width="36" height="7" rx="2" fill="%s" %s/>' % (INK, ST2, INK, ST2) +
            '<path d="M97 54 V226 M103 54 V226" stroke="%s" stroke-width=".9" opacity=".8"/>' % CREAM + '<path d="M72 168 Q74 154 90 154" stroke="#fff" stroke-width="3" fill="none" opacity=".5"/></g>')
@hero
def cerveau(p, **k):
    return ('<path d="M100 92 Q60 66 44 108 Q20 128 44 154 Q32 190 68 196 Q86 224 100 214 Q114 224 132 196 Q168 190 156 154 Q180 128 156 108 Q140 66 100 92Z" fill="%s" %s/>' % (mix(p['a'], CREAM, .45), ST) +
            '<path d="M100 92 V214 M66 120 Q86 130 78 154 M134 120 Q114 130 122 154 M56 168 Q80 164 88 186 M144 168 Q120 164 112 186" stroke="%s" stroke-width="3" fill="none" opacity=".6"/>' % INK + k.get('extra', '<path d="M118 100 L108 130 L126 142 L112 170" stroke="%s" stroke-width="4" fill="none" stroke-linejoin="round"/>' % INK))
@hero
def trophee(p, **k):
    return ('<path d="M62 84 H138 V128 Q138 170 100 178 Q62 170 62 128Z" fill="%s" %s/><path d="M62 96 H40 Q36 138 68 148 M138 96 H160 Q164 138 132 148" fill="none" stroke="%s" stroke-width="7"/><path d="M62 96 H40 Q36 138 68 148 M138 96 H160 Q164 138 132 148" fill="none" %s/>' % (GOLD, ST, GOLD, ST2) +
            '<rect x="92" y="178" width="16" height="38" fill="%s" %s/><rect x="68" y="216" width="64" height="16" rx="3" fill="%s" %s/><rect x="56" y="232" width="88" height="14" rx="3" fill="%s" %s/>' % (GOLD, ST2, mix(INK, CREAM, .2), ST, INK, ST) + '<path d="M76 100 Q80 132 92 152" stroke="#fff" stroke-width="5" fill="none" opacity=".55" stroke-linecap="round"/>' + k.get('extra', ''))
@hero
def gants(p, **k):
    o = ''
    for x, s in ((64, -1), (136, 1)):
        o += ('<g transform="translate(%s 168) scale(%s 1)"><path d="M-24 40 Q-44 -2 -14 -28 Q26 -52 44 -14 Q58 14 42 44 Q32 62 14 62 V84 H-18 V58 Q-22 52 -24 40Z" fill="%s" %s/><rect x="-18" y="72" width="34" height="16" rx="3" fill="%s" %s/>' % (x, s, k.get('c', p['a']), ST, CREAM, ST2) +
              '<path d="M-22 14 Q-34 8 -28 -4 Q-18 -14 -6 -2" fill="%s" %s/><path d="M-6 -22 Q10 -34 28 -14" stroke="#fff" stroke-width="3" fill="none" opacity=".5"/></g>' % (mix(k.get('c', p['a']), WHITE, .1), ST2))
    return o
@hero
def voiture(p, **k):
    c = k.get('c', CREAM)
    return ('<path d="M18 214 Q20 186 46 180 L68 154 Q74 148 84 148 H122 Q134 148 142 158 L156 180 Q180 184 182 208 V222 H18Z" fill="%s" %s/>' % (c, ST) + '<path d="M78 158 H120 L134 180 H70Z" fill="%s" %s/><path d="M100 158 V180" stroke="%s" stroke-width="2.4"/>' % (mix(INK, p['a'], .25), ST2, INK) +
            '<circle cx="54" cy="224" r="17" fill="%s" %s/><circle cx="146" cy="224" r="17" fill="%s" %s/><circle cx="54" cy="224" r="7" fill="%s"/><circle cx="146" cy="224" r="7" fill="%s"/>' % (INK, ST, INK, ST, GREY, GREY) + '<rect x="172" y="196" width="10" height="9" fill="%s"/><path d="M18 202 H40" stroke="%s" stroke-width="2.4" opacity=".4"/>' % (GOLD2, INK) + k.get('extra', ''))
@hero
def avion(p, **k):
    return ('<g transform="rotate(-18 100 160)"><path d="M16 160 Q50 148 150 152 Q180 154 186 160 Q180 166 150 168 Q50 172 16 160Z" fill="%s" %s/><path d="M96 156 L58 108 L82 108 L128 154Z" fill="%s" %s/><path d="M96 164 L58 214 L82 214 L128 166Z" fill="%s" %s/><path d="M26 156 L12 128 L32 128 L50 154Z" fill="%s" %s/>' % (CREAM, ST, mix(CREAM, p['a'], .3), ST, mix(CREAM, p['a'], .3), ST, mix(CREAM, p['a'], .3), ST) +
            ''.join('<circle cx="%s" cy="158" r="3" fill="%s"/>' % (110 + i * 12, INK) for i in range(4)) + '</g><path d="M10 232 Q60 214 100 226" stroke="%s" stroke-width="4" opacity=".35" fill="none"/>' % CREAM)
@hero
def valise(p, **k):
    return ('<path d="M78 112 V96 Q78 88 86 88 H114 Q122 88 122 96 V112" fill="none" stroke="%s" stroke-width="8"/><rect x="34" y="112" width="132" height="114" rx="10" fill="%s" %s/><rect x="34" y="150" width="132" height="8" fill="%s" opacity=".5"/><rect x="88" y="144" width="24" height="20" rx="3" fill="%s" %s/>' % (INK, k.get('c', p['a']), ST, INK, GOLD, ST2) +
            '<rect x="48" y="226" width="14" height="12" fill="%s"/><rect x="138" y="226" width="14" height="12" fill="%s"/>' % (INK, INK) + hl(42, 118, 7, 100, WHITE, .3, 3))
@hero
def foule_dos(p, **k):
    o = '<ellipse cx="100" cy="120" rx="74" ry="46" fill="%s" opacity=".3"/>' % p['a']
    for row, (y, s, op) in enumerate(((214, 1.0, 1), (188, .8, .75), (166, .62, .55))):
        n = 6 - row
        for i in range(n): o += person(18 + i * (164 / (n - 1)) + row * 6, y - 66 * s, s, INK, op)
    return o
@hero
def estrade(p, **k):
    return '<polygon points="100,60 62,220 138,220" fill="%s" opacity=".2"/><rect x="20" y="220" width="160" height="26" rx="3" fill="%s" %s/><rect x="20" y="246" width="160" height="8" fill="%s"/>' % (CREAM, mix(p['a'], INK, .4), ST, INK) + person(100, 120, 1.05, INK, 1) + k.get('extra', '')
@hero
def soleil_ecran(p, **k):
    return '<circle cx="100" cy="160" r="52" fill="%s" %s/>' % (p['a2'], ST) + ''.join('<path d="M100 160 L%.1f %.1f" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % (100 + 80 * math.cos(i * math.pi / 8), 160 + 80 * math.sin(i * math.pi / 8), p['a']) for i in range(16))

# ---------- pt08 Pantani ----------
@hero
def velo(p, **k):
    o = '<circle cx="54" cy="206" r="40" fill="none" stroke="%s" stroke-width="7"/><circle cx="146" cy="206" r="40" fill="none" stroke="%s" stroke-width="7"/>' % (INK, INK) + '<circle cx="54" cy="206" r="40" fill="none" stroke="%s" stroke-width="2" opacity=".5"/><circle cx="146" cy="206" r="40" fill="none" stroke="%s" stroke-width="2" opacity=".5"/>' % (CREAM, CREAM)
    for cx in (54, 146):
        for i in range(8): o += '<path d="M%s 206 L%.1f %.1f" stroke="%s" stroke-width="1" opacity=".6"/>' % (cx, cx + 38 * math.cos(i * math.pi / 4), 206 + 38 * math.sin(i * math.pi / 4), CREAM)
    return o + '<path d="M54 206 L88 144 H130 L146 206 M88 144 L100 206 H54 M100 206 L130 144" fill="none" stroke="%s" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/><path d="M84 130 H104 M126 138 L122 120 H140" stroke="%s" stroke-width="6" fill="none" stroke-linecap="round"/><circle cx="100" cy="206" r="8" fill="%s" %s/>' % (k.get('c', p['a']), INK, GOLD2, ST2) + k.get('extra', '')
@hero
def bandana(p, **k):
    return ('<path d="M30 130 Q100 80 170 130 Q150 200 100 220 Q50 200 30 130Z" fill="%s" %s/>' % (p['a'], ST) + ''.join('<circle cx="%s" cy="%s" r="3.4" fill="%s"/>' % (60 + (i % 5) * 20, 130 + (i // 5) * 22 + (i % 2) * 6, CREAM) for i in range(15) if True) +
            '<path d="M168 128 L196 108 L190 150Z" fill="%s" %s/><path d="M32 128 L4 106 L10 152Z" fill="%s" %s/>' % (p['a'], ST, p['a'], ST) + '<path d="M44 128 Q100 92 156 128" stroke="#fff" stroke-width="4" fill="none" opacity=".4"/>' + '<path d="M70 232 H130" stroke="%s" stroke-width="3" opacity="0"/>' % INK)
@hero
def mont_pluie(p, **k):
    o = '<polygon points="-10,262 60,120 100,190 130,140 210,262" fill="%s" %s/><polygon points="30,262 112,84 190,262" fill="%s" %s/><polygon points="112,84 94,126 106,120 114,134 124,118 134,128" fill="%s"/>' % (mix(INK, p['b0'], .3), ST, INK, ST, CREAM)
    for i in range(40): o += '<path d="M%s %s l-6 20" stroke="%s" stroke-width="1.8" opacity=".6"/>' % ((i * 29) % 210, (i * 47) % 260, CREAM)
    return o + '<path d="M0 250 Q100 232 200 250" stroke="%s" stroke-width="4" fill="none" opacity=".5"/>' % CREAM
@hero
def tube_essai(p, **k):
    return ('<g transform="rotate(18 100 160)"><path d="M86 60 H114 V196 Q114 230 100 230 Q86 230 86 196Z" fill="%s" opacity=".9" %s/><path d="M86 130 H114 V196 Q114 230 100 230 Q86 230 86 196Z" fill="%s"/><rect x="82" y="54" width="36" height="12" rx="4" fill="%s" %s/><path d="M92 70 V190" stroke="#fff" stroke-width="3" opacity=".5"/></g>' % (CREAM, ST, RED, p['a'], ST2) +
            '<rect x="44" y="236" width="112" height="12" rx="4" fill="%s" %s/>' % (INK, ST2) + '<circle cx="146" cy="100" r="26" fill="%s" %s/><path d="M134 100 H158 M146 88 V112" stroke="%s" stroke-width="5"/>' % (CREAM, ST, RED))
@hero
def ombre_velo(p, **k):
    return ('<ellipse cx="100" cy="240" rx="80" ry="12" fill="%s" opacity=".6"/>' % INK + '<g transform="translate(0 -6)">' + velo(p, c=mix(p['a'], INK, .4)) + '</g>' + '<g transform="translate(34 66) scale(.7)" opacity=".9">' + person(100, 100, 1.0, INK, 1) + '</g>')
@hero
def fleurs_route(p, **k):
    o = '<polygon points="96,150 104,150 214,310 -14,310" fill="%s" %s/><path d="M100 160 V180 M100 196 V222 M100 240 V280" stroke="%s" stroke-width="3.4" opacity=".8"/>' % (INK, ST2, CREAM)
    for i, (x, y, c) in enumerate(((44, 250, p['a']), (66, 226, CREAM), (136, 232, p['a2']), (158, 258, CREAM), (84, 268, p['a2']), (120, 262, p['a']))):
        o += '<path d="M%s %s V%s" stroke="#3F7A4A" stroke-width="3"/>' % (x, y, y + 20) + ''.join('<circle cx="%.1f" cy="%.1f" r="6" fill="%s" %s/>' % (x + 7 * math.cos(a), y + 7 * math.sin(a), c, ST2) for a in [j * math.pi / 2.5 for j in range(5)]) + '<circle cx="%s" cy="%s" r="4.4" fill="%s" %s/>' % (x, y, GOLD2, ST2)
    return '<circle cx="100" cy="122" r="36" fill="%s" opacity=".9"/>' % p['a2'] + o + '<g transform="translate(76 96) scale(.5)">' + velo(p, c=INK) + '</g>'
# ---------- pt09 Seau ----------
@hero
def buste(p, **k):
    return ('<path d="M52 250 L58 202 Q70 180 100 176 Q130 180 142 202 L148 250Z" fill="#B88246" %s/><rect x="84" y="156" width="32" height="26" fill="#B88246" %s/><ellipse cx="100" cy="130" rx="32" ry="40" fill="#C99A5B" %s/><path d="M70 120 Q72 84 100 84 Q128 84 130 120 Q116 100 100 102 Q84 100 70 120Z" fill="#8A5A2B" %s/>' % (ST, ST2, ST, ST2) +
            '<rect x="50" y="250" width="100" height="20" rx="3" fill="%s" %s/>' % (INK, ST) + txt(100, 264, k.get('t', '1990-2012'), 9, GOLD2, ls=1.4) + '<path d="M76 122 Q84 118 92 124 M108 124 Q116 118 124 122" stroke="%s" stroke-width="2.4" fill="none"/>' % INK + '<path d="M90 150 Q100 156 110 150" stroke="%s" stroke-width="2.4" fill="none"/>' % INK + '<path d="M72 112 q-4 20 2 38" stroke="#fff" stroke-width="3" opacity=".35" fill="none"/>')
@hero
def casque(p, **k):
    return ('<path d="M38 178 Q32 96 100 88 Q168 92 166 170 L152 198 H110 V220 H66 Q56 202 38 178Z" fill="%s" %s/>' % (k.get('c', p['a']), ST) + '<path d="M100 88 V128 H160" fill="none" stroke="%s" stroke-width="3" opacity=".4"/>' % INK + '<path d="M112 178 H168 M112 192 H160 M112 206 H150 M132 178 V214" stroke="%s" stroke-width="5" fill="none" stroke-linecap="round"/>' % CREAM +
            '<circle cx="84" cy="170" r="7" fill="%s" %s/><path d="M62 124 Q80 104 100 102" stroke="#fff" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/>' % (INK, ST2) + k.get('extra', ''))
@hero
def palmier_valise(p, **k):
    return ('<path d="M120 246 Q112 180 96 120" fill="none" stroke="#6B4A2A" stroke-width="12" stroke-linecap="round"/>' + ''.join('<path d="M96 120 Q%s %s %s %s Q%s %s 96 122Z" fill="#3F7A4A" %s/>' % (96 + dx * .6, 84, 96 + dx, 112 + dy, 96 + dx * .5, 112 + dy * .3, ST2) for dx, dy in ((-70, 14), (-52, -6), (-20, -18), (30, -16), (58, 0), (72, 24))) +
            '<g transform="translate(18 188) scale(.5)">' + valise(p) + '</g>' + '<path d="M0 252 H200" stroke="%s" stroke-width="4"/>' % INK)
# ---------- pt10 Enke ----------
@hero
def micros(p, **k):
    o = ''
    for i, (x, y, r) in enumerate(((50, 130, -14), (100, 108, 0), (150, 130, 14), (74, 190, -6), (128, 192, 6))):
        o += '<g transform="translate(%s %s) rotate(%s)"><rect x="-9" y="0" width="18" height="46" rx="8" fill="#9AA0AA" %s/><rect x="-12" y="-26" width="24" height="32" rx="12" fill="%s" %s/><rect x="-5" y="44" width="10" height="34" fill="%s" %s/></g>' % (x, y, r, ST2, [INK, p['a'], INK, p['a2'], INK][i], ST, INK, ST2)
    return o
@hero
def minarets(p, **k):
    o = '<path d="M30 252 V190 Q100 96 170 190 V252Z" fill="%s" %s/><path d="M100 98 V76 M94 82 H106" stroke="%s" stroke-width="3"/>' % (mix(INK, p['a'], .25), ST, GOLD2)
    for x in (24, 176): o += '<rect x="%s" y="120" width="9" height="132" fill="%s" %s/><polygon points="%s,120 %s,90 %s,120" fill="%s" %s/>' % (x - 4, mix(INK, p['a'], .2), ST2, x - 4, x + .5, x + 5, GOLD2, ST2)
    return o + '<circle cx="152" cy="92" r="16" fill="%s"/><circle cx="159" cy="86" r="13" fill="%s"/>' % (CREAM, p['b0']) + '<rect x="84" y="206" width="32" height="46" rx="16" fill="%s" opacity=".8"/>' % INK
@hero
def echarpes(p, **k):
    o = ''
    for i, (x, c) in enumerate(((44, p['a']), (82, CREAM), (118, p['a2']), (156, CREAM))):
        o += '<path d="M%s 96 Q%s 150 %s 214 H%s Q%s 150 %s 96Z" fill="%s" %s/>' % (x - 14, x - 22, x - 14, x + 14, x + 22, x + 14, c, ST) + ''.join('<rect x="%s" y="%s" width="%s" height="7" fill="%s" opacity=".7"/>' % (x - 16, 120 + j * 20, 32, INK) for j in range(4)) + ''.join('<path d="M%s 214 v14" stroke="%s" stroke-width="2.4"/>' % (x - 12 + j * 6, c) for j in range(5))
    return o + '<rect x="16" y="84" width="168" height="10" rx="4" fill="%s" %s/>' % (INK, ST)
@hero
def tunnel(p, **k):
    return ('<path d="M0 0 H200 V300 H0Z" fill="%s" opacity=".0"/><path d="M-10 300 V90 Q100 20 210 90 V300Z" fill="%s" %s/><path d="M30 300 V120 Q100 66 170 120 V300Z" fill="%s"/><path d="M62 300 V148 Q100 112 138 148 V300Z" fill="%s"/>' % (INK, mix(INK, p['b0'], .3), ST, mix(INK, p['b0'], .5), CREAM) +
            '<path d="M62 300 V148 Q100 112 138 148 V300Z" fill="%s" opacity=".9"/>' % p['a2'] + '<polygon points="100,160 62,300 138,300" fill="%s" opacity=".4"/>' % WHITE + person(100, 196, .5, INK, 1))
@hero
def maillot_gardien(p, **k): return H['gants'](p, c=p['a2'])
# ---------- pt11 Winehouse ----------
@hero
def pub(p, **k):
    return (card(30, 100, 140, 120, mix(INK, p['a'], .2), 4) + '<rect x="40" y="112" width="120" height="36" rx="3" fill="%s" %s/>' % (CREAM, ST2) + txt(100, 138, k.get('t', 'THE PUB'), 20, INK, ls=2) + '<rect x="46" y="160" width="40" height="50" fill="%s" opacity=".9" %s/><rect x="112" y="160" width="42" height="60" fill="%s" %s/>' % (p['a2'], ST2, INK, ST2) +
            '<path d="M100 100 V76 M84 76 H116" stroke="%s" stroke-width="3"/><circle cx="100" cy="66" r="10" fill="%s" %s/><rect x="26" y="220" width="148" height="10" fill="%s" %s/>' % (INK, GOLD2, ST2, INK, ST))
@hero
def choucroute(p, **k):
    return ('<path d="M42 150 Q34 70 100 60 Q166 70 158 150 Q150 130 100 130 Q50 130 42 150Z" fill="%s" %s/>' % (INK, ST) + ''.join('<path d="M%s %s q8 -10 16 0" stroke="%s" stroke-width="2" fill="none" opacity=".3"/>' % (54 + (i % 4) * 26, 84 + (i // 4) * 16, CREAM) for i in range(8)) +
            '<ellipse cx="100" cy="190" rx="50" ry="58" fill="%s" %s/><path d="M54 176 Q100 152 146 176 L138 184 Q100 168 62 184Z" fill="%s" %s/><path d="M74 170 q10 -8 22 0 M104 170 q12 -8 22 0" stroke="%s" stroke-width="3" fill="none"/><path d="M78 216 Q100 226 122 216" stroke="%s" stroke-width="4" fill="%s"/>' % (SKIN, ST, INK, ST2, INK, RED, RED))
@hero
def gramophone(p, **k):
    return ('<path d="M100 60 L64 128 Q60 150 76 154 H124 Q140 150 136 128Z" fill="%s" %s/><path d="M76 154 H124" stroke="%s" stroke-width="2" opacity=".5"/><path d="M92 154 V210 H108 V154" fill="%s" %s/><path d="M70 210 H130 L138 236 H62Z" fill="%s" %s/><rect x="56" y="236" width="88" height="14" rx="3" fill="%s" %s/>' % (GOLD, ST, INK, GOLD, ST2, GOLD2, ST, INK, ST) +
            '<path d="M78 126 Q70 100 92 78" stroke="#fff" stroke-width="4" fill="none" opacity=".5" stroke-linecap="round"/>' + sparkle(40, 92, 11) + sparkle(160, 100, 14) + sparkle(150, 190, 9))
@hero
def vautour(p, **k):
    return ('<path d="M20 240 Q50 150 98 140 Q110 120 104 100 Q96 80 118 76 Q142 76 140 100 Q136 120 120 130 Q170 150 182 240 L146 214 L128 244 L108 214 L90 244 L72 214Z" fill="%s" %s/>' % (INK, ST) + '<path d="M138 92 L158 100 L140 104Z" fill="%s" %s/><circle cx="124" cy="92" r="3.4" fill="%s"/><path d="M104 118 Q96 132 108 138 Q114 130 112 118Z" fill="%s" %s/>' % (GOLD2, ST2, CREAM, CREAM, ST2) + '<path d="M0 252 H200" stroke="%s" stroke-width="5"/><path d="M-10 252 Q40 212 90 252" fill="none" stroke="%s" stroke-width="4"/>' % (CREAM, CREAM))
@hero
def ballerines(p, **k):
    o = ''
    for x, r in ((70, -14), (130, 14)):
        o += '<g transform="translate(%s 190) rotate(%s)"><path d="M-22 36 Q-30 0 -8 -26 Q8 -34 14 -14 Q24 4 34 12 Q40 26 30 36Z" fill="%s" %s/><path d="M-8 -22 Q4 -8 -2 6" stroke="%s" stroke-width="3" fill="none"/><path d="M-22 36 H30" stroke="%s" stroke-width="4"/></g>' % (x, r, p['a'], ST, CREAM, INK)
    return o + '<path d="M60 90 Q100 70 140 90" fill="none" stroke="%s" stroke-width="4" opacity=".5"/>' % CREAM + sparkle(100, 102, 9)
# ---------- pt12 Cobain ----------
@hero
def pont(p, **k):
    o = '<rect x="0" y="206" width="200" height="14" fill="%s" %s/><path d="M-10 206 Q100 90 210 206" fill="none" stroke="%s" stroke-width="6"/>' % (INK, ST, CREAM)
    for i in range(9): o += '<path d="M%s 206 V%s" stroke="%s" stroke-width="2.4"/>' % (14 + i * 21, 150 + abs(4 - i) * 14, CREAM)
    return o + ''.join('<path d="M-10 %s Q25 %s 60 %s T130 %s T210 %s" fill="none" stroke="%s" stroke-width="3" opacity="%s"/>' % (236 + j * 14, 228 + j * 14, 236 + j * 14, 236 + j * 14, 236 + j * 14, CREAM, .6 - j * .15) for j in range(3))
@hero
def hamecon(p, **k):
    return ('<path d="M100 30 V150" stroke="%s" stroke-width="2.4"/><path d="M100 150 q0 40 -22 40 q-22 -4 -10 -26" fill="none" stroke="%s" stroke-width="6" stroke-linecap="round"/><g transform="rotate(-8 100 104)">' % (CREAM, GREY) + card(60, 96, 80, 40, '#7FB07C', 3) + '<circle cx="100" cy="116" r="12" fill="none" stroke="%s" stroke-width="2"/>' % INK + txt(100, 122, '$', 16, INK) + '</g>' +
            ''.join('<path d="M%s %s Q%s %s %s %s T%s %s" fill="none" stroke="%s" stroke-width="3" opacity="%s"/>' % (-10, 214 + j * 16, 25, 204 + j * 16, 60, 214 + j * 16, 210, 214 + j * 16, CREAM, .7 - j * .15) for j in range(4)) + '<rect x="-4" y="224" width="208" height="90" fill="%s" opacity=".35"/>' % p['a'])
@hero
def smiley(p, **k):
    return ('<circle cx="100" cy="160" r="68" fill="%s" %s/><circle cx="78" cy="144" r="8" fill="%s"/><path d="M118 138 l16 12 M134 138 l-16 12" stroke="%s" stroke-width="5" stroke-linecap="round"/><path d="M70 200 Q100 176 130 200" fill="none" stroke="%s" stroke-width="6" stroke-linecap="round"/>' % (GOLD2, ST, INK, INK, INK) + '<path d="M44 130 A58 58 0 0 1 88 104" stroke="#fff" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/>')
@hero
def cassette(p, **k):
    return ('<rect x="26" y="106" width="148" height="100" rx="10" fill="%s" %s/><rect x="38" y="118" width="124" height="38" rx="4" fill="%s" %s/><circle cx="70" cy="178" r="16" fill="%s" %s/><circle cx="130" cy="178" r="16" fill="%s" %s/><circle cx="70" cy="178" r="6" fill="%s"/><circle cx="130" cy="178" r="6" fill="%s"/>' % (INK, ST, CREAM, ST2, CREAM, ST2, CREAM, ST2, INK, INK) +
            txt(100, 144, k.get('t', 'IN UTERO'), 15, INK, ls=2) + '<rect x="84" y="196" width="32" height="10" fill="%s" opacity=".6"/>' % CREAM + '<path d="M54 156 H146" stroke="%s" stroke-width="2" opacity=".3"/>' % p['a'])
@hero
def cardigan(p, **k):
    return ('<path d="M68 90 L46 104 L30 214 L58 220 L66 150 L70 252 H130 L134 150 L142 220 L170 214 L154 104 L132 90 L100 122Z" fill="%s" %s/>' % (mix(p['a'], '#8A8A6A', .5), ST) + '<path d="M68 90 L100 122 L132 90" fill="none" stroke="%s" stroke-width="2.4" opacity=".8"/><path d="M100 122 V252" stroke="%s" stroke-width="2.4"/>' % (INK, INK) +
            ''.join('<circle cx="100" cy="%s" r="3.6" fill="%s"/>' % (146 + i * 26, CREAM) for i in range(4)) + ''.join('<path d="M%s %s h40" stroke="%s" stroke-width="2" opacity=".25"/>' % (x, y, INK) for x, y in ((34, 150), (34, 170), (130, 150), (130, 170), (76, 190), (116, 190))))
# ---------- pt13 Houston ----------
@hero
def eglise(p, **k):
    return ('<polygon points="100,52 122,104 78,104" fill="%s" %s/><rect x="78" y="104" width="44" height="52" fill="%s" %s/><rect x="96" y="34" width="8" height="26" fill="%s" %s/><rect x="88" y="42" width="24" height="7" fill="%s" %s/>' % (CREAM, ST, mix(CREAM, INK, .1), ST, GOLD2, ST2, GOLD2, ST2) +
            '<rect x="26" y="156" width="148" height="96" fill="%s" %s/><path d="M84 252 V198 Q100 178 116 198 V252Z" fill="%s" %s/>' % (mix(CREAM, INK, .15), ST, p['a'], ST) + ''.join('<rect x="%s" y="176" width="14" height="30" rx="7" fill="%s" %s/>' % (x, p['a2'], ST2) for x in (42, 144)) + '<path d="M0 252 H200" stroke="%s" stroke-width="4"/>' % INK)
@hero
def robe(p, **k):
    c = k.get('c', CREAM)
    return ('<path d="M90 72 Q100 94 110 72 L124 84 L118 134 Q148 180 172 260 H28 Q52 180 82 134 L76 84Z" fill="%s" %s/>' % (c, ST) + '<path d="M82 134 H118" stroke="%s" stroke-width="3" opacity=".5"/><path d="M76 84 Q100 118 124 84" fill="none" stroke="%s" stroke-width="2.4" opacity=".5"/>' % (INK, INK) + ''.join('<path d="M%s 150 L%s 260" stroke="%s" stroke-width="1.6" opacity=".25"/>' % (100 + i * 8, 100 + i * 28, INK) for i in range(-3, 4)) + hl(80, 90, 6, 40, WHITE, .5, 3) + k.get('extra', ''))
@hero
def micro_casse(p, **k):
    return ('<g transform="rotate(-24 100 160)"><rect x="95" y="150" width="10" height="100" fill="#9AA0AA" %s/><rect x="72" y="66" width="56" height="74" rx="28" fill="#C9CCD2" %s/></g>' % (ST, ST) + '<path d="M96 70 L88 100 L104 114 L90 140" fill="none" stroke="%s" stroke-width="4" stroke-linejoin="round"/>' % INK + ''.join('<circle cx="%s" cy="%s" r="2.6" fill="%s"/>' % (x, y, CREAM) for x, y in ((56, 90), (150, 120), (64, 154), (138, 70), (160, 160))))
@hero
def roses(p, **k):
    o = ''
    for x, y, r, c in ((62, 140, 26, CREAM), (112, 120, 30, CREAM), (150, 156, 24, CREAM), (86, 178, 22, mix(CREAM, p['a'], .15))):
        o += '<path d="M%s %s Q%s %s %s 250" fill="none" stroke="#3F7A4A" stroke-width="4"/>' % (x, y + r, x + 4, y + 70, 100 + (x - 100) * .3) + '<circle cx="%s" cy="%s" r="%s" fill="%s" %s/><path d="M%s %s a%s %s 0 1 1 %s 0 a%s %s 0 1 0 %s 0" fill="none" stroke="%s" stroke-width="2" opacity=".5"/>' % (x, y, r, c, ST, x - r * .4, y, r * .4, r * .4, r * .8, r * .2, r * .2, -r * .4, INK)
    return o + '<path d="M60 250 H140" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % INK
