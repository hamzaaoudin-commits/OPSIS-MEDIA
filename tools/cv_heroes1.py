from cv_engine import *
H = {}
def hero(f): H[f.__name__] = f; return f

def hl(x, y, w, h, c=CREAM, op=.5, r=2): return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" opacity="%s"/>' % (x, y, w, h, r, c, op)

# ---------------- scène, musique ----------------
@hero
def micro(p, **k):
    return ('<rect x="95" y="150" width="10" height="100" fill="#9AA0AA" %s/><path d="M70 236 Q100 262 130 236" fill="none" stroke="#9AA0AA" stroke-width="7" stroke-linecap="round"/><path d="M70 236 Q100 262 130 236" fill="none" %s opacity=".6"/>' % (ST, ST) +
            '<rect x="72" y="86" width="56" height="74" rx="28" fill="#C9CCD2" %s/>' % ST + ''.join('<path d="M%s %s H%s" stroke="%s" stroke-width="2" opacity=".5"/>' % (80, y, 120, INK) for y in (104, 116, 128, 140)) +
            '<path d="M100 88 V158" stroke="%s" stroke-width="2" opacity=".5"/>' % INK + '<path d="M84 96 Q88 90 98 90" stroke="#fff" stroke-width="3" fill="none" opacity=".7"/>')
@hero
def child_stage(p, **k):
    return ('<rect x="14" y="238" width="172" height="22" rx="4" fill="%s" %s/>' % (mix(p['a'], INK, .45), ST) + ''.join('<circle cx="%s" cy="249" r="5" fill="%s"/>' % (28 + i * 24, GOLD2) for i in range(7)) +
            '<circle cx="100" cy="124" r="15" fill="%s"/><path d="M85 112 Q100 96 115 112 Q108 106 100 107 Q92 106 85 112Z" fill="%s"/><path d="M100 98 l16 -8 l0 16 Z M100 98 l-16 -8 l0 16 Z" fill="%s"/>' % (INK, INK, p['a']) +
            '<path d="M82 148 Q100 138 118 148 L126 200 L74 200Z" fill="%s"/><rect x="86" y="200" width="9" height="36" fill="%s"/><rect x="105" y="200" width="9" height="36" fill="%s"/>' % (INK, INK, INK) +
            '<path d="M74 156 Q58 164 52 150 M126 156 Q144 170 150 154" stroke="%s" stroke-width="7" stroke-linecap="round" fill="none"/>' % INK)
@hero
def balance(p, **k):
    return ('<rect x="52" y="104" width="96" height="140" rx="16" fill="%s" %s/>' % (CREAM, ST) + hl(60, 112, 10, 120, WHITE, .5, 5) +
            '<rect x="70" y="120" width="60" height="30" rx="6" fill="%s" %s/>' % (INK, ST) + txt(100, 143, k.get('t', '38'), 24, p['a2']) + '<path d="M76 190 Q100 170 124 190" stroke="%s" stroke-width="3" fill="none" opacity=".5"/>' % INK +
            '<path d="M76 222 h48" stroke="%s" stroke-width="3" opacity=".4"/><circle cx="64" cy="232" r="4" fill="%s"/><circle cx="136" cy="232" r="4" fill="%s"/>' % (INK, INK, INK))
@hero
def arc_ciel(p, **k):
    o = ''
    for i, c in enumerate(('#D2232C', '#F08A24', '#F2C14E', '#4C9A5A', '#3F78C2', '#7A4BA8')):
        r = 88 - i * 11; o += '<path d="M%s 236 A%s %s 0 0 1 %s 236" fill="none" stroke="%s" stroke-width="11"/>' % (100 - r, r, r, 100 + r, c)
    o += '<path d="M12 236 A88 88 0 0 1 188 236" fill="none" %s opacity=".0"/>' % ST
    for x in (26, 168): o += '<ellipse cx="%s" cy="240" rx="30" ry="13" fill="%s" %s/><ellipse cx="%s" cy="236" rx="22" ry="9" fill="%s" opacity=".8"/>' % (x, CREAM, ST2, x + 4, WHITE)
    return o
@hero
def souliers(p, **k):
    o = ''
    for x, rot in ((72, -12), (132, 12)):
        o += ('<g transform="translate(%s 190) rotate(%s)"><path d="M-30 20 Q-34 -14 -12 -26 L10 -30 Q18 -4 40 6 Q50 12 44 22 Z" fill="%s" %s/><path d="M-30 20 H44" stroke="%s" stroke-width="3"/>' % (x, rot, RED, ST, INK) +
              ''.join('<circle cx="%s" cy="%s" r="2" fill="%s"/>' % (-8 + i * 9, -10 + (i % 2) * 8, WHITE) for i in range(4)) + '<path d="M-22 -4 Q-14 -18 0 -22" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/></g>')
    return o + sparkle(38, 120, 10) + sparkle(166, 112, 12) + sparkle(100, 96, 8)
@hero
def tramway(p, **k):
    return ('<rect x="30" y="142" width="140" height="82" rx="10" fill="%s" %s/><rect x="38" y="120" width="124" height="28" rx="6" fill="%s" %s/>' % (p['a'], ST, mix(p['a'], INK, .25), ST) +
            ''.join('<rect x="%s" y="154" width="24" height="26" rx="3" fill="%s" %s/>' % (42 + i * 30, mix(CREAM, p['a2'], .3), ST2) for i in range(4)) + '<rect x="30" y="196" width="140" height="6" fill="%s" opacity=".6"/>' % INK +
            '<path d="M100 120 V60 M60 60 H140" stroke="%s" stroke-width="3.5"/><path d="M0 52 H200" stroke="%s" stroke-width="2.4"/>' % (INK, INK) +
            '<circle cx="62" cy="230" r="11" fill="%s" %s/><circle cx="138" cy="230" r="11" fill="%s" %s/>' % (INK, ST, INK, ST) + '<path d="M0 242 H200" stroke="%s" stroke-width="5"/>' % CREAM + '<path d="M34 138 Q100 128 166 138" stroke="#fff" stroke-width="3" fill="none" opacity=".4"/>' + sparkle(100, 56, 8))
@hero
def porte_valise(p, **k):
    return ('<polygon points="100,70 164,40 164,262 100,262" fill="%s" opacity=".13"/><rect x="58" y="80" width="84" height="182" fill="%s" %s/><path d="M64 86 H136 V262 H64Z" fill="%s" opacity=".95"/>' % (CREAM, INK, ST, p['a2']) +
            '<polygon points="64,86 98,98 98,250 64,262" fill="%s" %s/><circle cx="90" cy="176" r="3" fill="%s"/>' % (mix(p['b0'], INK, .4), ST2, CREAM) +
            '<rect x="108" y="212" width="38" height="28" rx="4" fill="%s" %s/><path d="M120 212 v-6 h14 v6" stroke="%s" stroke-width="3" fill="none"/><rect x="118" y="222" width="18" height="4" fill="%s" opacity=".6"/>' % (RED if False else p['a'], ST, INK, INK))
@hero
def enseigne(p, **k):
    w = k.get('t', 'PALACE')
    o = '<rect x="24" y="110" width="152" height="70" rx="6" fill="%s" %s/><rect x="32" y="118" width="136" height="54" rx="3" fill="%s"/>' % (INK, ST, mix(p['b0'], INK, .35))
    o += txt(100, 154, w, 25 if len(w) < 9 else 17, p['a2'], ls=2)
    for i in range(14):
        x = 30 + i * 10.5; o += '<circle cx="%s" cy="114" r="2.6" fill="%s"/><circle cx="%s" cy="176" r="2.6" fill="%s"/>' % (x, GOLD2, x, GOLD2)
    o += '<rect x="96" y="180" width="8" height="70" fill="%s" %s/>' % (INK, ST2)
    return o + sparkle(18, 100, 10) + sparkle(184, 104, 12)
@hero
def salle(p, **k):
    o = '<path d="M16 256 V118 Q100 22 184 118 V256Z" fill="%s" %s/><path d="M32 256 V124 Q100 52 168 124 V256Z" fill="%s"/>' % (mix(p['b0'], INK, .3), ST, mix(p['b0'], INK, .6))
    o += '<path d="M100 50 V92" stroke="%s" stroke-width="2.4"/>' % CREAM + '<path d="M70 118 Q100 98 130 118 L120 144 H80Z" fill="%s" %s/>' % (GOLD2, ST2) + ''.join('<path d="M%s 144 v12" stroke="%s" stroke-width="2"/><circle cx="%s" cy="158" r="2.6" fill="%s"/>' % (82 + i * 9, GOLD2, 82 + i * 9, GOLD2) for i in range(5))
    o += '<path d="M32 190 H168 M32 214 H168" stroke="%s" stroke-width="3" opacity=".45"/>' % GOLD
    o += '<rect x="20" y="236" width="160" height="22" rx="3" fill="%s" %s/><polygon points="100,170 62,236 138,236" fill="%s" opacity=".2"/>' % (INK, ST, CREAM)
    o += person(100, 178, .46, CREAM, .95) + '<path d="M40 150 q4 -14 16 -8 M148 142 q12 -6 18 8" stroke="%s" stroke-width="2" fill="none" opacity=".4"/>' % CREAM
    return o
@hero
def cle_hotel(p, **k):
    return ('<g transform="rotate(-20 100 160)"><circle cx="100" cy="92" r="26" fill="%s" %s/><circle cx="100" cy="92" r="9" fill="%s"/><rect x="92" y="116" width="16" height="86" fill="%s" %s/><rect x="108" y="170" width="16" height="9" fill="%s" %s/><rect x="108" y="188" width="12" height="9" fill="%s" %s/></g>' % (GOLD, ST, p['b0'], GOLD, ST, GOLD, ST2, GOLD, ST2) +
            '<g transform="rotate(14 128 226)"><rect x="104" y="204" width="48" height="52" rx="4" fill="%s" %s/><circle cx="128" cy="212" r="3" fill="%s"/>' % (CREAM, ST, INK) + txt(128, 244, k.get('t', '1117'), 18, INK) + '</g>')
@hero
def bougies(p, **k):
    o = ''
    for i, (x, y, h) in enumerate(((40, 226, 40), (70, 214, 54), (100, 204, 66), (132, 216, 52), (162, 228, 38))):
        o += '<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".12"/>' % (x, y - h - 4, 26, GOLD2)
        o += '<rect x="%s" y="%s" width="18" height="%s" rx="3" fill="%s" %s/>' % (x - 9, y - h, h, CREAM, ST2) + '<path d="M%s %s q8 -10 0 -22 q-8 12 0 22z" fill="%s" %s/>' % (x, y - h - 2, GOLD2, ST2)
    return o + '<rect x="20" y="244" width="160" height="10" rx="3" fill="%s" opacity=".7"/>' % INK
@hero
def maison_num(p, **k):
    return ('<polygon points="100,98 34,160 166,160" fill="%s" %s/><rect x="46" y="160" width="108" height="86" fill="%s" %s/><rect x="86" y="196" width="28" height="50" fill="%s" %s/><rect x="56" y="174" width="20" height="20" fill="%s" opacity=".9"/><rect x="124" y="174" width="20" height="20" fill="%s" opacity=".9"/>' % (INK, ST, mix(p['b0'], CREAM, .3), ST, p['a2'], ST2, p['a2'], p['a2']) +
            '<rect x="70" y="262" width="60" height="22" rx="3" fill="%s" %s/>' % (CREAM, ST) + txt(100, 279, k.get('t', '2300'), 19, INK, ls=2) + '<path d="M0 246 H200" stroke="%s" stroke-width="4"/><rect x="132" y="110" width="12" height="26" fill="%s" %s/>' % (INK, INK, ST2))
@hero
def chaise_ceinture(p, **k):
    return ('<path d="M66 146 V250 M134 146 V250" stroke="%s" stroke-width="9" stroke-linecap="round"/><rect x="56" y="196" width="88" height="14" rx="4" fill="%s" %s/><path d="M64 200 V96 Q64 84 76 84 H124 Q136 84 136 96 V200" fill="none" stroke="%s" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>' % (INK, mix(p['a'], INK, .3), ST, INK) +
            '<path d="M70 110 H130 M70 140 H130 M70 168 H130" stroke="%s" stroke-width="6"/>' % mix(p['a'], INK, .3) + '<path d="M138 205 q34 30 14 56" fill="none" stroke="#6B3E1B" stroke-width="10" stroke-linecap="round"/><rect x="144" y="254" width="12" height="10" rx="2" fill="%s" %s/>' % (GOLD, ST2))
@hero
def vinyle(p, **k):
    o = '<circle cx="100" cy="164" r="76" fill="%s" %s/>' % (INK, ST)
    for r in (66, 56, 46, 36): o += '<circle cx="100" cy="164" r="%s" fill="none" stroke="%s" stroke-width="1.2" opacity=".28"/>' % (r, CREAM)
    return o + '<circle cx="100" cy="164" r="25" fill="%s" %s/><circle cx="100" cy="164" r="4" fill="%s"/>' % (k.get('c', p['a']), ST, INK) + '<path d="M44 124 A64 64 0 0 1 90 98" fill="none" stroke="%s" stroke-width="5" opacity=".35" stroke-linecap="round"/>' % WHITE + txt(100, 160, k.get('t', ''), 7, INK)
@hero
def miroir_gant(p, **k):
    return ('<rect x="54" y="74" width="92" height="170" rx="46" fill="%s" %s/><rect x="64" y="84" width="72" height="150" rx="36" fill="%s"/>' % (GOLD, ST, mix(p['b0'], CREAM, .25)) +
            '<path d="M72 130 L110 96 M70 180 L128 112" stroke="#fff" stroke-width="4" opacity=".28"/>' + '<path d="M92 190 V152 Q92 144 100 144 Q108 144 108 152 V190 Z" fill="#fff" %s opacity=".95"/>' % ST2 +
            '<path d="M84 180 H116 V204 H84Z" fill="%s" %s/>' % (p['a'], ST2) + ''.join('<circle cx="%s" cy="%s" r="2" fill="%s"/>' % (86 + i * 8, 192, GOLD2) for i in range(4)) + sparkle(120, 140, 9, WHITE) + '<rect x="70" y="244" width="60" height="14" rx="3" fill="%s" %s/>' % (GOLD, ST))
@hero
def pyro(p, **k):
    o = ''
    for x in (46, 100, 154):
        o += '<path d="M%s 252 L%s 120" stroke="%s" stroke-width="2.4" opacity=".6"/>' % (x, x, CREAM)
        for a in range(-4, 5):
            ang = -math.pi / 2 + a * .22; L = 72 + (a % 3) * 10
            o += '<path d="M%s 252 L%.1f %.1f" stroke="%s" stroke-width="3.2" stroke-linecap="round" opacity=".85"/><circle cx="%.1f" cy="%.1f" r="2.8" fill="%s"/>' % (x, x + L * math.cos(ang) * .6, 252 + L * 1.8 * math.sin(ang), p['a2'] if a % 2 else CREAM, x + L * math.cos(ang) * .6, 252 + L * 1.8 * math.sin(ang), CREAM)
    return o + '<rect x="20" y="248" width="160" height="10" fill="%s"/>' % INK
@hero
def veste(p, **k):
    return ('<path d="M72 92 L52 104 L34 204 L58 210 L66 150 L70 250 H130 L134 150 L142 210 L166 204 L148 104 L128 92 L100 126Z" fill="%s" %s/>' % (INK, ST) +
            '<path d="M72 92 L100 126 L128 92 L116 88 L100 104 L84 88Z" fill="%s" %s/><path d="M100 126 V250" stroke="%s" stroke-width="2" opacity=".4"/>' % (mix(INK, CREAM, .2), ST2, CREAM) +
            ''.join('<rect x="%s" y="%s" width="10" height="7" rx="2" fill="#C9CCD2" %s/>' % (a, b, ST2) for a, b in ((96, 150), (96, 176), (96, 202), (44, 176), (150, 176))) + '<path d="M66 110 L52 200" stroke="#fff" stroke-width="2" opacity=".25"/>')
@hero
def papier_stylo(p, **k):
    t = k.get('t', 'ACCORD')
    return ('<g transform="rotate(-5 100 160)"><rect x="44" y="82" width="112" height="152" rx="3" fill="%s" %s/>' % (CREAM, ST) + txt(100, 108, t, round(min(14, 96 / (len(t) * .95)), 1), INK, ls=1.6) + ''.join('<rect x="56" y="%s" width="%s" height="3" fill="%s" opacity=".5"/>' % (122 + i * 12, 88 - (i % 3) * 14, INK) for i in range(6)) +
            '<path d="M60 214 q10 -16 18 -2 t18 -4 t20 2" fill="none" stroke="%s" stroke-width="2.4"/></g>' % INK + '<g transform="rotate(34 150 220)"><rect x="140" y="170" width="12" height="70" rx="2" fill="%s" %s/><polygon points="140,240 152,240 146,256" fill="%s" %s/></g>' % (p['a'], ST, GOLD, ST2))
@hero
def balance_justice(p, **k):
    return ('<rect x="96" y="92" width="8" height="150" fill="%s" %s/><rect x="66" y="238" width="68" height="14" rx="3" fill="%s" %s/><circle cx="100" cy="90" r="9" fill="%s" %s/><path d="M32 112 H168" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (GOLD, ST2, GOLD, ST, GOLD2, ST2, GOLD) +
            '<path d="M34 114 L18 176 M34 114 L52 176 M166 114 L148 176 M166 114 L182 176" stroke="%s" stroke-width="2"/>' % CREAM + '<path d="M14 176 Q35 202 56 176Z M144 176 Q165 202 186 176Z" fill="%s" %s/>' % (GOLD, ST2))
@hero
def compteur(p, **k):
    t = k.get('t', '50')
    return ('<ellipse cx="100" cy="246" rx="80" ry="12" fill="%s" opacity=".6"/>' % p['a'] + '<rect x="30" y="102" width="140" height="132" rx="18" fill="%s" %s/><rect x="38" y="110" width="124" height="116" rx="12" fill="none" stroke="%s" stroke-width="2" opacity=".6"/>' % (INK, ST, p['a2']) +
            txt(100, 206, t, 96, p['a2'], ls=2, extra='stroke="%s" stroke-width="2"' % INK) + sparkle(30, 96, 12) + sparkle(172, 92, 9))
@hero
def palais(p, **k):
    o = '<polygon points="100,78 28,122 172,122" fill="%s" %s/><rect x="28" y="122" width="144" height="10" fill="%s" %s/>' % (CREAM, ST, mix(CREAM, INK, .2), ST)
    for i in range(5): o += '<rect x="%s" y="132" width="16" height="92" fill="%s" %s/>' % (36 + i * 28, CREAM, ST2) + hl(39 + i * 28, 134, 3, 88, WHITE, .5, 1)
    o += '<rect x="20" y="224" width="160" height="10" fill="%s" %s/><rect x="10" y="234" width="180" height="12" fill="%s" %s/>' % (CREAM, ST, mix(CREAM, INK, .2), ST) + '<circle cx="100" cy="106" r="8" fill="%s" %s/>' % (p['a'], ST2)
    return o
@hero
def foule(p, **k):
    o = ''
    for row, (y, s, op) in enumerate(((236, 1.1, 1), (210, .9, .8), (188, .7, .6))):
        for i in range(6 - row):
            x = 20 + i * (180 / (5 - row + .001 if False else (5 - row + 1))) + row * 10
            o += person(x, y - 60 * s, s, INK, op)
    return o
@hero
def casiers(p, **k):
    o = '<rect x="22" y="88" width="156" height="164" fill="%s" %s/>' % (mix(p['a'], INK, .35), ST)
    for i in range(4):
        x = 26 + i * 38; o += '<rect x="%s" y="94" width="32" height="152" fill="%s" %s/>' % (x, mix(p['a'], INK, .15 + i % 2 * .15), ST2) + '<path d="M%s 110 h22 M%s 118 h22 M%s 126 h22" stroke="%s" stroke-width="2" opacity=".55"/>' % (x + 5, x + 5, x + 5, INK) + '<circle cx="%s" cy="180" r="3" fill="%s"/>' % (x + 24, CREAM)
    return o + '<rect x="34" y="150" width="20" height="26" fill="%s" transform="rotate(-8 44 160)" %s/><path d="M40 160 h10" stroke="%s" stroke-width="2"/>' % (CREAM, ST2, p['a'])
@hero
def objectifs(p, **k):
    o = ''
    for x, y, r in ((52, 120, 30), (140, 108, 24), (150, 186, 30), (56, 202, 22), (100, 156, 26)):
        o += '<circle cx="%s" cy="%s" r="%s" fill="%s" %s/><circle cx="%s" cy="%s" r="%s" fill="%s"/><circle cx="%s" cy="%s" r="%s" fill="%s"/><circle cx="%s" cy="%s" r="%s" fill="#fff" opacity=".7"/>' % (x, y, r, INK, ST, x, y, r * .72, mix(p['a'], INK, .6), x, y, r * .4, p['a2'], x - r * .25, y - r * .25, r * .14)
    return o + ''.join('<path d="M%s %s L%s %s" stroke="%s" stroke-width="2" opacity=".5"/>' % (a, b, c, d, CREAM) for a, b, c, d in ((20, 40, 70, 100), (180, 50, 150, 90), (100, 30, 100, 124)))
@hero
def tondeuse(p, **k):
    return ('<g transform="rotate(-18 100 160)"><rect x="76" y="92" width="48" height="110" rx="14" fill="%s" %s/>' % (INK, ST) + hl(82, 100, 6, 92, CREAM, .3, 3) + '<rect x="70" y="196" width="60" height="22" rx="3" fill="#C9CCD2" %s/>' % ST + ''.join('<rect x="%s" y="214" width="4" height="12" fill="#C9CCD2" %s/>' % (72 + i * 7.6, ST2) for i in range(8)) +
            '<circle cx="100" cy="126" r="7" fill="%s" %s/></g>' % (p['a'], ST2) + ''.join('<path d="M%s %s q%s 14 %s 30" stroke="%s" stroke-width="5" fill="none" stroke-linecap="round"/>' % (x, y, d, d * 2, GOLD) for x, y, d in ((40, 200, -8), (150, 226, 9), (60, 236, 7), (168, 190, -6))))
@hero
def cage(p, **k):
    o = '<path d="M100 70 V92" stroke="%s" stroke-width="3"/><circle cx="100" cy="66" r="6" fill="none" stroke="%s" stroke-width="3"/><path d="M52 110 Q100 70 148 110Z" fill="%s" %s/>' % (GOLD, GOLD, GOLD, ST)
    for i in range(9):
        x = 56 + i * 11; o += '<path d="M%s 110 Q%s 160 %s 232" fill="none" stroke="%s" stroke-width="3"/>' % (x, 56 + (i - 4) * 14 + 48 if False else x + (i - 4) * 3, x + (i - 4) * 3.5, GOLD)
    return o + '<ellipse cx="100" cy="236" rx="52" ry="10" fill="%s" %s/>' % (GOLD, ST) + '<path d="M98 200 q10 -26 22 -4 q-8 14 -22 4z" fill="%s" %s opacity=".9"/><path d="M120 196 l12 -4" stroke="%s" stroke-width="3"/>' % (CREAM, ST2, INK)
@hero
def pancarte(p, **k):
    t = k.get('t', '#FREE')
    return ('<rect x="95" y="150" width="10" height="106" fill="%s" %s/><rect x="26" y="78" width="148" height="78" rx="5" fill="%s" %s/>' % (mix(CREAM, INK, .3), ST2, CREAM, ST) + txt(100, 132, t, 38 if len(t) < 7 else 26, p['a'], ls=1, extra='stroke="%s" stroke-width="1.4"' % INK) +
            '<path d="M36 148 h128" stroke="%s" stroke-width="2.5" opacity=".4"/>' % INK + sparkle(24, 66, 10) + sparkle(176, 70, 8))
@hero
def chaine_brisee(p, **k):
    o = ''
    for i, (x, y, rot) in enumerate(((32, 166, 0), (58, 166, 90), (84, 166, 0))):
        o += '<g transform="translate(%s %s) rotate(%s)"><rect x="-16" y="-10" width="34" height="20" rx="10" fill="none" stroke="#9AA0AA" stroke-width="7"/><rect x="-16" y="-10" width="34" height="20" rx="10" fill="none" %s/></g>' % (x, y, rot, ST2)
    for i, (x, y, rot) in enumerate(((118, 176, 0), (146, 176, 90), (172, 176, 0))):
        o += '<g transform="translate(%s %s) rotate(%s)"><rect x="-16" y="-10" width="34" height="20" rx="10" fill="none" stroke="#9AA0AA" stroke-width="7"/><rect x="-16" y="-10" width="34" height="20" rx="10" fill="none" %s/></g>' % (x, y, rot, ST2)
    o += '<path d="M96 150 l8 22 l-12 8 l12 22" stroke="%s" stroke-width="3" fill="none"/>' % CREAM
    o += '<g transform="translate(100 108)"><path d="M0 0 Q-34 -34 -44 -4 Q-36 28 0 14Z" fill="%s" %s/><path d="M0 0 Q34 -34 44 -4 Q36 28 0 14Z" fill="%s" %s/><path d="M0 14 Q-24 40 -14 52 Q-4 48 0 24 Q4 48 14 52 Q24 40 0 14Z" fill="%s" %s/><rect x="-2" y="-6" width="4" height="26" rx="2" fill="%s"/></g>' % (p['a'], ST, p['a2'], ST, p['a'], ST2, INK)
    return o
