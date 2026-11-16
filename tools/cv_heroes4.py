from cv_engine import *
from cv_heroes1 import hl
from cv_heroes3 import card, GREY, SKIN, H as H3
H = {}
def hero(f): H[f.__name__] = f; return f

@hero
def casque_audio(p, **k):
    return ('<path d="M44 176 Q44 80 100 80 Q156 80 156 176" fill="none" stroke="%s" stroke-width="14" stroke-linecap="round"/><path d="M44 176 Q44 80 100 80 Q156 80 156 176" fill="none" stroke="%s" stroke-width="2" opacity=".5"/>' % (INK, CREAM) +
            '<rect x="28" y="150" width="34" height="68" rx="16" fill="%s" %s/><rect x="138" y="150" width="34" height="68" rx="16" fill="%s" %s/><rect x="36" y="164" width="12" height="40" rx="6" fill="%s" opacity=".5"/><rect x="152" y="164" width="12" height="40" rx="6" fill="%s" opacity=".5"/>' % (p['a'], ST, p['a'], ST, INK, INK) + sparkle(100, 130, 12))
@hero
def egaliseur(p, **k):
    o = ''
    hs = (50, 90, 130, 170, 120, 150, 80, 110, 60)
    for i, h in enumerate(hs):
        x = 22 + i * 18.5
        for j in range(int(h / 14)): o += '<rect x="%s" y="%s" width="14" height="10" rx="2" fill="%s" %s/>' % (x, 246 - j * 14, [p['a2'], p['a'], CREAM][j % 3] if j < int(h / 14) - 1 else CREAM, ST2)
    return o
@hero
def eclair(p, **k):
    return '<polygon points="116,60 52,170 94,170 76,252 150,128 104,128" fill="%s" %s/><polygon points="108,76 70,160 100,160" fill="#fff" opacity=".35"/>' % (p['a2'], ST) + sparkle(40, 100, 9) + sparkle(160, 200, 10)
@hero
def croix_med(p, **k):
    return ('<path d="M80 80 H120 V130 H170 V170 H120 V220 H80 V170 H30 V130 H80Z" fill="%s" %s/>' % (CREAM, ST) + '<path d="M80 80 H120 V130 H170 V170 H120 V220 H80 V170 H30 V130 H80Z" fill="%s" opacity=".0"/>' % INK + '<path d="M0 262 H44 L58 238 L76 286 L96 246 L110 262 H200" fill="none" stroke="%s" stroke-width="3.4"/>' % p['a'])
@hero
def boussole(p, **k):
    o = '<circle cx="100" cy="164" r="68" fill="%s" %s/><circle cx="100" cy="164" r="56" fill="%s" %s/>' % (GOLD, ST, mix(INK, p['a'], .2), ST2)
    for i in range(12): o += '<path d="M100 %s V%s" stroke="%s" stroke-width="2" transform="rotate(%s 100 164)"/>' % (112, 120 if i % 3 else 116, CREAM, i * 30)
    return o + '<polygon points="100,116 110,164 100,212 90,164" fill="%s" %s/><polygon points="100,116 110,164 90,164" fill="%s" %s/><circle cx="100" cy="164" r="5" fill="%s" %s/>' % (CREAM, ST2, RED, ST2, GOLD, ST2) + txt(100, 108, 'N', 12, CREAM)
@hero
def pousse(p, **k):
    return ('<path d="M100 250 Q96 200 100 150" fill="none" stroke="#5B8A4A" stroke-width="8" stroke-linecap="round"/><path d="M100 190 Q60 190 56 150 Q96 150 100 190Z" fill="#5B8A4A" %s/><path d="M100 160 Q142 160 146 118 Q106 118 100 160Z" fill="#7BB05E" %s/>' % (ST2, ST2) +
            '<path d="M40 250 Q100 226 160 250 V262 H40Z" fill="%s" %s/>' % (mix(INK, p['a'], .15), ST) + '<circle cx="100" cy="116" r="40" fill="%s" opacity=".18"/>' % GOLD2 + sparkle(142, 90, 9) + sparkle(60, 108, 7))
@hero
def couronne(p, **k):
    return ('<path d="M34 214 L26 108 L68 152 L100 92 L132 152 L174 108 L166 214Z" fill="%s" %s/><rect x="30" y="214" width="140" height="22" rx="4" fill="%s" %s/>' % (GOLD, ST, GOLD2, ST) + ''.join('<circle cx="%s" cy="%s" r="8" fill="%s" %s/>' % (x, y, c, ST2) for x, y, c in ((26, 104, CREAM), (100, 86, RED), (174, 104, CREAM))) + ''.join('<circle cx="%s" cy="226" r="5" fill="%s"/>' % (x, p['a']) for x in (66, 100, 134)) + '<path d="M46 200 L40 130" stroke="#fff" stroke-width="4" opacity=".4"/>')
@hero
def bateau(p, **k):
    return ('<path d="M24 190 H176 L150 238 H50Z" fill="%s" %s/><rect x="74" y="148" width="64" height="42" fill="%s" %s/><rect x="90" y="112" width="18" height="36" fill="%s" %s/><rect x="112" y="124" width="14" height="24" fill="%s" %s/>' % (INK, ST, CREAM, ST, p['a'], ST2, p['a'], ST2) +
            ''.join('<circle cx="%s" cy="170" r="4.4" fill="%s"/>' % (84 + i * 14, INK) for i in range(4)) + '<path d="M32 200 H168" stroke="%s" stroke-width="3" opacity=".6"/>' % p['a'] + ''.join('<path d="M-10 %s Q25 %s 60 %s T130 %s T210 %s" fill="none" stroke="%s" stroke-width="3" opacity="%s"/>' % (240 + j * 14, 232 + j * 14, 240 + j * 14, 240 + j * 14, 240 + j * 14, CREAM, .7 - j * .2) for j in range(3)))
@hero
def masque_theatre(p, **k):
    return ('<path d="M34 100 Q100 74 166 100 Q172 170 132 210 Q100 228 68 210 Q28 170 34 100Z" fill="%s" %s/><path d="M54 128 Q76 114 90 136 Q72 150 54 128Z M146 128 Q124 114 110 136 Q128 150 146 128Z" fill="%s" %s/><path d="M72 182 Q100 204 128 182" fill="none" stroke="%s" stroke-width="4"/><path d="M168 100 Q196 120 186 164" fill="none" stroke="%s" stroke-width="3" opacity="0"/>' % (CREAM, ST, INK, ST2, INK, INK) + '<path d="M44 112 Q56 104 70 110" stroke="#fff" stroke-width="4" fill="none" opacity=".5"/>' + '<path d="M120 60 Q150 40 166 60" stroke="%s" stroke-width="3" fill="none"/>' % p['a'])
@hero
def chapeau(p, **k):
    c = k.get('c', INK)
    return ('<ellipse cx="100" cy="196" rx="76" ry="18" fill="%s" %s/><path d="M56 196 Q54 118 100 112 Q146 118 144 196Z" fill="%s" %s/><path d="M58 182 Q100 196 142 182 V196 Q100 210 58 196Z" fill="%s" %s/>' % (c, ST, c, ST, p['a'], ST2) + hl(64, 130, 8, 46, WHITE, .25, 4) + k.get('extra', '<path d="M138 170 q22 -50 36 -40 q-14 6 -22 40Z" fill="%s" %s/>' % (CREAM, ST2)))
@hero
def fenetre_paris(p, **k):
    return ('<rect x="46" y="70" width="108" height="178" rx="3" fill="%s" %s/><path d="M54 78 H146 V240 H54Z" fill="%s"/><path d="M100 78 V240" stroke="%s" stroke-width="4"/><path d="M54 150 H146" stroke="%s" stroke-width="4"/>' % (CREAM, ST, mix(p['b0'], p['a2'], .3), INK, INK) +
            '<path d="M36 224 H164 V240 H36Z M44 214 V240 M156 214 V240 M70 224 V240 M100 224 V240 M130 224 V240" fill="%s" %s/>' % (INK, ST2) + '<circle cx="124" cy="108" r="14" fill="%s" opacity=".9"/>' % CREAM + '<path d="M60 130 q10 -10 20 0 v20 h-20z" fill="%s" opacity=".6"/>' % INK)
@hero
def cadre_photo(p, **k):
    return ('<rect x="38" y="74" width="124" height="164" rx="3" fill="%s" %s/><rect x="50" y="86" width="100" height="140" fill="%s"/>' % (GOLD, ST, mix(INK, p['b0'], .5)) + '<circle cx="100" cy="152" r="52" fill="%s" opacity=".45"/>' % p['a'] + person(100, 128, .9, CREAM, .95) +
            '<path d="M50 86 L150 86 L150 226 L50 226Z" fill="none" %s/>' % ST2 + '<path d="M62 100 L100 100 L62 140Z" fill="#fff" opacity=".12"/>' + '<rect x="30" y="248" width="140" height="8" rx="3" fill="%s" %s/>' % (INK, ST2))
@hero
def tiare(p, **k):
    o = '<path d="M26 200 Q100 170 174 200 L168 220 Q100 196 32 220Z" fill="%s" %s/>' % (GOLD, ST)
    for x, h in ((44, 40), (72, 62), (100, 84), (128, 62), (156, 40)): o += '<path d="M%s %s L%s %s L%s %s" fill="%s" %s/><circle cx="%s" cy="%s" r="6" fill="%s" %s/>' % (x - 12, 198 - (abs(x - 100) * .2), x, 198 - h, x + 12, 198 - (abs(x - 100) * .2), GOLD2, ST2, x, 198 - h - 4, CREAM, ST2)
    return o + ''.join('<circle cx="%s" cy="206" r="3.6" fill="%s"/>' % (50 + i * 25, CREAM) for i in range(6)) + sparkle(30, 100, 10) + sparkle(172, 96, 12) + sparkle(100, 76, 8)
@hero
def balancoire(p, **k):
    return ('<rect x="30" y="54" width="140" height="10" rx="4" fill="%s" %s/><path d="M54 64 V204 M146 64 V204" stroke="%s" stroke-width="3"/><rect x="38" y="204" width="32" height="9" rx="3" fill="%s" %s/><rect x="130" y="204" width="32" height="9" rx="3" fill="%s" %s/>' % (INK, ST2, CREAM, p['a'], ST2, p['a2'], ST2) +
            '<path d="M30 54 L10 252 M170 54 L190 252" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % INK + person(54, 140, .42, INK, 1) + person(146, 142, .42, INK, 1) + '<path d="M0 252 H200" stroke="%s" stroke-width="4"/>' % INK)
@hero
def trio(p, **k):
    return ('<ellipse cx="100" cy="250" rx="80" ry="9" fill="%s" opacity=".5"/>' % INK + person(46, 120, .95, INK) + person(154, 120, .95, INK) + person(100, 138, .62, CREAM, .95) + '<path d="M82 124 Q100 100 118 124" fill="none" stroke="%s" stroke-width="3" opacity=".0"/>' % INK + '<circle cx="100" cy="86" r="5" fill="%s"/>' % p['a'] + '<path d="M70 200 H130" stroke="%s" stroke-width="2.4" stroke-dasharray="4 5" opacity=".6"/>' % CREAM)
@hero
def larme(p, **k):
    return ('<circle cx="100" cy="150" r="80" fill="%s" opacity=".12"/>' % p['a2'] + '<path d="M100 62 Q150 130 146 176 Q142 232 100 232 Q58 232 54 176 Q50 130 100 62Z" fill="#8EC8E8" %s/><path d="M80 130 Q70 160 78 192" stroke="#fff" stroke-width="7" fill="none" opacity=".7" stroke-linecap="round"/>' % ST + '<path d="M100 232 Q80 252 100 262 Q120 252 100 232Z" fill="#8EC8E8" opacity="0"/><ellipse cx="100" cy="256" rx="40" ry="6" fill="%s" opacity=".5"/><ellipse cx="100" cy="256" rx="24" ry="3" fill="none" stroke="%s" stroke-width="1.6" opacity=".7"/>' % (INK, CREAM))
@hero
def pouce_bas(p, **k):
    return ('<g transform="rotate(180 100 164)"><path d="M62 236 Q54 176 74 162 L92 120 Q100 90 118 96 Q132 104 124 130 L120 152 H156 Q176 154 170 174 Q180 184 172 198 Q178 212 166 222 Q168 236 152 238Z" fill="%s" %s/><rect x="38" y="148" width="26" height="92" rx="4" fill="%s" %s/></g>' % (SKIN, ST, p['a'], ST) + ''.join('<path d="M%s %s l-3 12" stroke="%s" stroke-width="2" opacity=".5"/>' % (30 + i * 28, 60 + (i % 2) * 14, CREAM) for i in range(7)))
@hero
def croix(p, **k):
    return ('<rect x="86" y="66" width="28" height="170" rx="3" fill="%s" %s/><rect x="50" y="110" width="100" height="28" rx="3" fill="%s" %s/>' % (CREAM, ST, CREAM, ST) + '<rect x="94" y="74" width="5" height="154" fill="#fff" opacity=".4"/>' + '<circle cx="100" cy="124" r="70" fill="%s" opacity=".14"/>' % p['a2'] + '<path d="M40 250 H160" stroke="%s" stroke-width="5"/>' % INK)
@hero
def col_pretre(p, **k):
    return ('<path d="M40 252 L52 178 Q70 156 100 152 Q130 156 148 178 L160 252Z" fill="%s" %s/><rect x="82" y="138" width="36" height="26" fill="%s" %s/><rect x="90" y="150" width="20" height="12" fill="%s" %s/><path d="M100 170 V248" stroke="%s" stroke-width="2.4" opacity=".4"/>' % (INK, ST, SKIN, ST2, CREAM, ST2, CREAM) + '<circle cx="100" cy="106" r="32" fill="%s" %s/>' % (SKIN, ST) + '<path d="M62 98 Q62 72 100 70 Q138 72 138 98" fill="none" stroke="%s" stroke-width="2" opacity="0"/>' % INK + '<path d="M86 108 h6 M108 108 h6 M92 126 q8 4 16 0" stroke="%s" stroke-width="2.4" fill="none" stroke-linecap="round"/>' % INK + '<g transform="translate(100 214) scale(.5)"><rect x="-5" y="-26" width="10" height="52" fill="%s" %s/><rect x="-18" y="-12" width="36" height="9" fill="%s" %s/></g>' % (GOLD2, ST2, GOLD2, ST2))
@hero
def pantalon(p, **k):
    return ('<path d="M52 82 H148 L156 130 Q172 198 152 250 L112 250 L100 168 L88 250 L48 250 Q28 198 44 130Z" fill="%s" %s/><rect x="52" y="82" width="96" height="16" fill="%s" %s/><path d="M44 130 Q72 148 100 130 Q128 148 156 130" stroke="%s" stroke-width="2.4" fill="none" opacity=".5"/>' % (p['a'], ST, GOLD2, ST2, INK) + '<path d="M100 98 V168" stroke="%s" stroke-width="2.4" opacity=".6"/>' % INK + hl(60, 110, 6, 90, WHITE, .3, 3) + sparkle(30, 110, 9) + sparkle(172, 118, 11))
@hero
def courbe_baisse(p, **k):
    return ('<path d="M24 70 V246 H182" fill="none" stroke="%s" stroke-width="3" opacity=".6"/>' % CREAM + ''.join('<rect x="%s" y="%s" width="20" height="%s" fill="%s" opacity=".55"/>' % (36 + i * 30, 90 + i * 24, 156 - i * 24, p['a']) for i in range(5)) + '<path d="M34 96 L72 126 L102 110 L140 178 L168 214" fill="none" stroke="%s" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/><polygon points="178,226 146,222 170,194" fill="%s" %s/>' % (CREAM, CREAM, ST2))
@hero
def sneaker(p, **k):
    return ('<path d="M24 210 V144 Q24 132 36 132 H68 Q80 156 104 160 Q136 168 150 192 H182 Q194 196 192 214Z" fill="%s" %s/><rect x="16" y="210" width="182" height="16" rx="7" fill="%s" %s/>' % (p['a'], ST, CREAM, ST) + '<path d="M80 164 L94 150 M98 172 L112 158 M116 180 L130 166" stroke="%s" stroke-width="4"/>' % CREAM + '<path d="M36 144 H66" stroke="%s" stroke-width="3" opacity=".6"/><path d="M34 184 Q80 160 140 200" fill="none" stroke="%s" stroke-width="3" opacity=".7"/>' % (CREAM, CREAM) + hl(30, 140, 6, 44, WHITE, .3, 3))
@hero
def telephone_app(p, **k):
    return ('<rect x="58" y="70" width="84" height="170" rx="14" fill="%s" %s/><rect x="66" y="86" width="68" height="132" rx="4" fill="%s"/><rect x="88" y="76" width="24" height="5" rx="2.5" fill="%s"/>' % (INK, ST, mix(p['b0'], CREAM, .2), CREAM) + ''.join('<rect x="%s" y="%s" width="18" height="18" rx="5" fill="%s" %s/>' % (72 + (i % 3) * 21, 96 + (i // 3) * 24, [p['a'], p['a2'], CREAM][i % 3], ST2) for i in range(6)) + '<circle cx="100" cy="190" r="15" fill="%s" %s/><path d="M95 183 L109 190 L95 197Z" fill="%s"/>' % (RED, ST2, CREAM) + sparkle(160, 88, 10))
@hero
def casquette(p, **k):
    return ('<path d="M46 170 Q42 100 100 92 Q158 100 154 170Z" fill="%s" %s/><path d="M46 170 Q100 150 154 170 Q196 176 190 196 Q150 188 96 188 Q50 188 46 170Z" fill="%s" %s/><circle cx="100" cy="94" r="5" fill="%s" %s/>' % (INK, ST, mix(INK, p['a'], .25), ST, p['a2'], ST2) + '<path d="M66 128 Q80 108 100 106" stroke="#fff" stroke-width="4" fill="none" opacity=".3"/>' + '<rect x="78" y="122" width="44" height="24" rx="3" fill="%s" opacity=".9"/>' % CREAM + txt(100, 140, k.get('t', 'M'), 18, INK))
@hero
def cube_herbe(p, **k):
    return ('<polygon points="100,78 172,114 100,150 28,114" fill="#6AAE45" %s/><polygon points="28,114 100,150 100,242 28,206" fill="#8A5A2B" %s/><polygon points="172,114 100,150 100,242 172,206" fill="#6E4521" %s/>' % (ST, ST, ST) +
            ''.join('<rect x="%s" y="%s" width="9" height="9" fill="%s" opacity=".5"/>' % (x, y, c) for x, y, c in ((120, 164, INK), (140, 190, INK), (112, 204, CREAM), (50, 150, INK), (66, 184, INK), (46, 188, CREAM), (80, 214, INK))) + '<path d="M28 114 L100 150 L172 114" fill="none" stroke="%s" stroke-width="12" opacity="0"/>' % INK + '<path d="M30 124 L100 160 L170 124" stroke="#4E8A32" stroke-width="12" fill="none" opacity=".7"/>')
@hero
def ascenseur(p, **k):
    return ('<rect x="46" y="72" width="108" height="184" fill="%s" %s/><rect x="56" y="82" width="42" height="168" fill="#8A8F99" %s/><rect x="102" y="82" width="42" height="168" fill="#9AA0AA" %s/><path d="M98 82 V250" stroke="%s" stroke-width="3"/>' % (INK, ST, ST2, ST2, INK) +
            '<rect x="78" y="40" width="44" height="20" rx="3" fill="%s" %s/>' % (INK, ST2) + txt(100, 55, '-1', 14, p['a2']) + '<circle cx="168" cy="160" r="6" fill="%s" %s/><circle cx="168" cy="178" r="6" fill="%s" %s/>' % (p['a'], ST2, GREY, ST2) + '<polygon points="60,250 140,250 150,286 50,286" fill="%s" opacity=".25"/>' % CREAM)
@hero
def visage_mot(p, **k):
    t = k.get('t', 'SLAVE')
    return ('<ellipse cx="100" cy="150" rx="58" ry="74" fill="%s" %s/><path d="M44 130 Q46 74 100 70 Q154 74 156 130 Q130 100 100 100 Q70 100 44 130Z" fill="%s" %s/>' % (SKIN, ST, INK, ST2) + '<path d="M72 150 h14 M114 150 h14 M90 196 Q100 202 110 196" stroke="%s" stroke-width="3" fill="none" stroke-linecap="round"/>' % INK +
            '<g transform="rotate(-8 100 172)">' + txt(100, 182, t, 17, INK, ls=2) + '</g>' + '<path d="M56 120 Q70 124 76 140" stroke="#fff" stroke-width="3" fill="none" opacity="0"/>')
@hero
def coeur_brise(p, **k):
    return ('<path d="M100 232 C28 176 34 100 78 104 C92 106 100 116 100 124 L88 150 L112 170 L98 196 L108 214Z" fill="%s" %s/><path d="M100 232 C172 176 166 100 122 104 C108 106 100 116 100 124 L112 150 L90 172 L106 198 L98 214Z" fill="%s" %s transform="translate(10 6) rotate(6 100 160)"/>' % (p['a'], ST, p['a2'], ST))
@hero
def cd_journal(p, **k):
    return ('<g transform="rotate(-8 100 170)">' + card(34, 84, 132, 150, CREAM) + txt(100, 114, 'À OFFRIR', 15, INK, ls=2) + ''.join('<rect x="46" y="%s" width="108" height="3" fill="%s" opacity=".4"/>' % (196 + i * 9, INK) for i in range(3)) + '</g>' +
            '<circle cx="104" cy="160" r="40" fill="%s" %s/><circle cx="104" cy="160" r="38" fill="none" stroke="%s" stroke-width="3" opacity=".5"/><circle cx="104" cy="160" r="10" fill="%s" %s/><path d="M76 140 Q90 124 108 124" stroke="#fff" stroke-width="4" fill="none" opacity=".7"/>' % (p['a2'], ST, WHITE, p['b0'], ST2) + sparkle(160, 100, 10))
@hero
def billet_loto(p, **k):
    o = '<g transform="rotate(-6 100 164)">' + card(36, 80, 128, 168, CREAM) + '<rect x="44" y="88" width="112" height="28" fill="%s"/>' % p['a'] + txt(100, 108, 'POWERBALL', 14, CREAM, ls=1.5)
    for r in range(3):
        for c in range(5): o += '<circle cx="%s" cy="%s" r="8" fill="none" stroke="%s" stroke-width="1.6"/>' % (58 + c * 21, 138 + r * 26, INK)
    o += ''.join('<circle cx="%s" cy="%s" r="8" fill="%s" opacity=".85"/>' % (58 + c * 21, 138 + r * 26, INK) for r, c in ((0, 1), (0, 3), (1, 0), (1, 4), (2, 2)))
    return o + txt(100, 238, '$314,9 M', 15, p['a'], ls=1) + '</g>'
@hero
def bonnet(p, **k):
    return ('<path d="M40 188 Q50 100 120 84 Q160 80 170 118 Q150 112 140 130 Q116 168 160 188Z" fill="%s" %s/><rect x="34" y="180" width="140" height="36" rx="18" fill="%s" %s/><circle cx="170" cy="118" r="17" fill="%s" %s/>' % (RED, ST, CREAM, ST, CREAM, ST) + ''.join('<circle cx="%s" cy="198" r="4" fill="%s" opacity=".4"/>' % (52 + i * 17, INK) for i in range(7)) + '<path d="M60 150 Q80 116 120 104" stroke="#fff" stroke-width="4" fill="none" opacity=".35"/>')
@hero
def lunettes(p, **k):
    return ('<circle cx="66" cy="160" r="38" fill="%s" %s/><circle cx="134" cy="160" r="38" fill="%s" %s/><path d="M104 150 Q100 144 96 150" stroke="%s" stroke-width="5" fill="none"/><path d="M28 152 L8 140 M172 152 L192 140" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (mix(INK, p['a'], .25), ST, mix(INK, p['a'], .25), ST, INK, INK) +
            '<path d="M44 140 Q56 128 72 128" stroke="#fff" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/><path d="M112 140 Q124 128 140 128" stroke="#fff" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/>' + '<circle cx="66" cy="160" r="38" fill="none" stroke="%s" stroke-width="2" opacity=".6"/><circle cx="134" cy="160" r="38" fill="none" stroke="%s" stroke-width="2" opacity=".6"/>' % (p['a2'], p['a2']))
@hero
def colombe_guitare(p, **k):
    return H3['guitare'](p, c=p['a2']) + '<g transform="translate(40 100)"><path d="M0 20 Q-10 0 14 -6 Q26 -8 34 4 L52 -6 L44 14 Q40 30 18 32Z" fill="%s" %s/><circle cx="30" cy="4" r="1.8" fill="%s"/><path d="M52 -6 L64 -10 L54 0" fill="%s" %s/></g>' % (CREAM, ST2, INK, GOLD, ST2) if False else H3['guitare'](p, c=p['a2']) + '<path d="M26 92 Q14 74 40 68 Q54 66 62 78 L82 66 L72 88 Q66 106 44 108Z" fill="%s" %s/><circle cx="56" cy="76" r="2" fill="%s"/><path d="M82 66 L96 62 L84 72" fill="%s" %s/>' % (CREAM, ST2, INK, GOLD, ST2)
@hero
def tente(p, **k):
    return ('<polygon points="100,80 30,236 170,236" fill="%s" %s/><polygon points="100,80 100,236 170,236" fill="%s" opacity=".35"/><polygon points="100,150 78,236 122,236" fill="%s" %s/>' % (p['a'], ST, INK, INK, ST2) + '<path d="M100 80 V54 M100 54 L124 62 L100 70" fill="%s" %s/>' % (CREAM, ST2) + '<path d="M0 236 H200" stroke="%s" stroke-width="4"/>' % INK + stars(p, 12, 4, 0, 120) + '<path d="M20 236 L60 190 L100 236" fill="%s" opacity="0"/>' % INK)
@hero
def lit_hotel(p, **k):
    return ('<rect x="30" y="196" width="140" height="40" rx="6" fill="%s" %s/><rect x="24" y="150" width="14" height="96" rx="3" fill="%s" %s/><rect x="162" y="176" width="14" height="70" rx="3" fill="%s" %s/><rect x="38" y="176" width="124" height="28" rx="12" fill="%s" %s/>' % (CREAM, ST, INK, ST, INK, ST, mix(CREAM, p['a'], .2), ST2) +
            '<path d="M60 204 Q100 186 160 204 V228 H60Z" fill="%s" %s/>' % (p['a'], ST2) + '<rect x="74" y="84" width="52" height="42" rx="3" fill="%s" %s/>' % (mix(INK, p['a'], .2), ST) + '<polygon points="100,126 70,196 130,196" fill="%s" opacity=".18"/>' % GOLD2 + '<path d="M100 72 V84" stroke="%s" stroke-width="3"/>' % INK)
@hero
def carte_joker(p, **k):
    return ('<g transform="rotate(-10 100 164)">' + card(52, 78, 96, 150, CREAM, 8) + '<path d="M62 92 q8 -8 16 0 q8 -8 16 0 q8 -8 16 0" fill="none" stroke="%s" stroke-width="3"/>' % p['a'] + txt(76, 108, 'J', 18, p['a']) + '<circle cx="100" cy="150" r="22" fill="%s" opacity=".9"/><path d="M80 142 L86 124 L100 138 L114 124 L120 142Z" fill="%s" %s/>' % (CREAM, p['a'], ST2) +
            '<path d="M88 150 h6 M106 150 h6 M90 162 Q100 172 110 162" stroke="%s" stroke-width="2.4" fill="none"/>' % INK + '</g>' + '<g transform="rotate(12 100 170)" opacity=".55">' + card(64, 86, 96, 150, CREAM, 8) + '</g>')
@hero
def casserole(p, **k):
    return ('<ellipse cx="94" cy="170" rx="62" ry="22" fill="%s" %s/><path d="M32 170 V198 Q32 222 94 222 Q156 222 156 198 V170" fill="%s" %s/><rect x="152" y="166" width="42" height="12" rx="6" fill="%s" %s/>' % (INK, ST, mix(INK, GREY, .35), ST, INK, ST) + '<ellipse cx="94" cy="170" rx="50" ry="16" fill="%s"/><circle cx="76" cy="168" r="6" fill="%s"/><circle cx="104" cy="172" r="5" fill="%s"/>' % (p['a'], CREAM, GOLD2) +
            '<path d="M60 134 q-8 -14 4 -26 q10 -12 -2 -26 M96 130 q-8 -14 4 -26 q10 -12 -2 -26 M130 134 q-8 -14 4 -26" stroke="%s" stroke-width="5" fill="none" stroke-linecap="round" opacity=".5"/>' % CREAM)
@hero
def livre(p, **k):
    return ('<path d="M100 96 Q60 74 24 90 V222 Q60 206 100 228Z" fill="%s" %s/><path d="M100 96 Q140 74 176 90 V222 Q140 206 100 228Z" fill="%s" %s/>' % (CREAM, ST, mix(CREAM, INK, .08), ST) + '<path d="M38 112 Q70 102 90 116 M38 136 Q70 126 90 140 M38 160 Q70 150 90 164 M110 116 Q130 102 162 112 M110 140 Q130 126 162 136" stroke="%s" stroke-width="2.4" fill="none" opacity=".5"/>' % INK + '<rect x="97" y="96" width="6" height="132" fill="%s" %s/>' % (p['a'], ST2) + k.get('extra', ''))
@hero
def globe(p, **k):
    return ('<circle cx="100" cy="156" r="68" fill="%s" %s/><ellipse cx="100" cy="156" rx="28" ry="68" fill="none" stroke="%s" stroke-width="2.4" opacity=".6"/><path d="M32 156 H168 M42 118 H158 M42 194 H158" stroke="%s" stroke-width="2.4" opacity=".6"/>' % (mix('#3F78C2', p['a'], .2), ST, INK, INK) +
            '<path d="M58 124 Q80 104 100 122 Q94 144 76 142Z M112 164 Q136 154 148 178 Q128 200 112 186Z" fill="#6AAE45" %s/>' % ST2 + '<path d="M54 232 H146 M100 224 V246" stroke="%s" stroke-width="6" stroke-linecap="round"/><path d="M20 120 Q100 40 180 120" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="5 6" opacity=".7"/>' % (INK, CREAM) + sparkle(172, 80, 9))
@hero
def divan(p, **k):
    return ('<rect x="24" y="170" width="152" height="52" rx="14" fill="%s" %s/><rect x="24" y="130" width="40" height="92" rx="14" fill="%s" %s/><rect x="136" y="130" width="40" height="92" rx="14" fill="%s" %s/><rect x="52" y="150" width="96" height="40" rx="10" fill="%s" %s/>' % (mix(p['a'], INK, .35), ST, mix(p['a'], INK, .45), ST, mix(p['a'], INK, .45), ST, mix(p['a'], INK, .2), ST) +
            '<rect x="34" y="222" width="12" height="18" fill="%s"/><rect x="154" y="222" width="12" height="18" fill="%s"/>' % (INK, INK) + '<path d="M70 110 q10 -16 24 -8 q-4 14 -2 30" stroke="%s" stroke-width="3" fill="none" opacity=".6"/>' % CREAM + '<circle cx="100" cy="86" r="30" fill="%s" opacity=".16"/>' % CREAM)
@hero
def couteau(p, **k):
    return ('<g transform="rotate(-38 100 164)"><path d="M92 40 Q132 48 140 150 L100 156 Z" fill="#C9CCD2" %s/><path d="M92 40 Q112 80 112 154" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/><rect x="94" y="154" width="12" height="24" fill="%s" %s/><rect x="90" y="176" width="20" height="62" rx="9" fill="%s" %s/><circle cx="100" cy="190" r="2.6" fill="%s"/><circle cx="100" cy="212" r="2.6" fill="%s"/></g>' % (ST, GOLD, ST2, INK, ST, CREAM, CREAM) + '<ellipse cx="100" cy="258" rx="60" ry="7" fill="%s" opacity=".4"/>' % INK + sparkle(52, 90, 8))
@hero
def graffiti(p, **k):
    t = k.get('t', 'SAMO©')
    return ('<rect x="14" y="78" width="172" height="176" fill="%s" %s/>' % (mix(INK, CREAM, .12), ST) + ''.join('<path d="M14 %s H186" stroke="%s" stroke-width="1.4" opacity=".3"/>' % (96 + i * 22, CREAM) for i in range(7)) + '<g transform="rotate(-5 100 170)">' + txt(100, 182, t, 46, p['a2'], ls=2, extra='stroke="%s" stroke-width="2.4" paint-order="stroke"' % INK) + '</g>' +
            '<path d="M40 112 l10 -14 l10 14 l10 -14 l10 14" fill="none" stroke="%s" stroke-width="3.4"/>' % CREAM + '<path d="M130 222 q16 -18 32 0 q-16 12 -32 0" fill="none" stroke="%s" stroke-width="3"/>' % p['a'])
@hero
def platine(p, **k):
    return ('<rect x="22" y="110" width="156" height="126" rx="8" fill="%s" %s/><circle cx="88" cy="174" r="50" fill="%s" %s/><circle cx="88" cy="174" r="40" fill="none" stroke="%s" stroke-width="1.4" opacity=".3"/><circle cx="88" cy="174" r="16" fill="%s" %s/><circle cx="88" cy="174" r="3" fill="%s"/>' % (mix(INK, p['a'], .25), ST, INK, ST, CREAM, p['a'], ST2, INK) +
            '<path d="M158 122 V186" stroke="#C9CCD2" stroke-width="6" stroke-linecap="round"/><path d="M158 186 L132 158" stroke="#C9CCD2" stroke-width="5" stroke-linecap="round"/><circle cx="158" cy="124" r="9" fill="#C9CCD2" %s/>' % ST2 + '<circle cx="158" cy="214" r="6" fill="%s"/>' % p['a2'] + sparkle(36, 96, 9))
@hero
def boite_conserve(p, **k):
    return ('<path d="M52 100 V232 Q100 250 148 232 V100" fill="%s" %s/><ellipse cx="100" cy="100" rx="48" ry="12" fill="#C9CCD2" %s/><rect x="52" y="140" width="96" height="62" fill="%s"/>' % (p['a'], ST, ST, CREAM) + txt(100, 178, k.get('t', 'SOUP'), 24, p['a'], ls=2) + '<path d="M52 140 H148 M52 202 H148" stroke="%s" stroke-width="2.4"/>' % INK + hl(60, 110, 8, 116, WHITE, .35, 3) + '<ellipse cx="100" cy="102" rx="34" ry="7" fill="none" stroke="%s" stroke-width="1.6" opacity=".4"/>' % INK)
@hero
def podium(p, **k):
    o = '<polygon points="84,40 116,40 190,262 10,262" fill="%s" opacity=".18"/><polygon points="82,70 118,70 190,300 10,300" fill="%s" %s/>' % (CREAM, mix(INK, p['a'], .15), ST2) + '<path d="M100 70 V300" stroke="%s" stroke-width="3" opacity=".5"/>' % CREAM
    for y in (130, 184, 252): o += '<path d="M%s %s H%s" stroke="%s" stroke-width="1.6" opacity=".3"/>' % (100 - (y - 70) * .3, y, 100 + (y - 70) * .3, CREAM)
    return o + person(100, 130, .7, INK, 1) + '<path d="M60 70 H140" stroke="%s" stroke-width="5"/>' % p['a'] + ''.join('<circle cx="%s" cy="54" r="5" fill="%s"/>' % (30 + i * 28, GOLD2) for i in range(6))
@hero
def ciseaux(p, **k):
    return ('<g transform="rotate(-28 100 160)"><path d="M100 160 L150 62 L160 68 L112 168Z" fill="#C9CCD2" %s/><path d="M100 160 L50 62 L40 68 L88 168Z" fill="#C9CCD2" %s/><circle cx="66" cy="214" r="26" fill="none" stroke="%s" stroke-width="10"/><circle cx="134" cy="214" r="26" fill="none" stroke="%s" stroke-width="10"/><circle cx="66" cy="214" r="26" fill="none" %s/><circle cx="134" cy="214" r="26" fill="none" %s/><circle cx="100" cy="164" r="5" fill="%s" %s/></g>' % (ST, ST, p['a'], p['a'], ST2, ST2, GOLD, ST2) +
            '<path d="M150 250 q10 -14 22 0 M170 230 q10 -14 22 0" stroke="%s" stroke-width="3" fill="none" opacity=".5"/>' % CREAM)
@hero
def sac_luxe(p, **k):
    return ('<path d="M62 120 Q62 70 100 70 Q138 70 138 120" fill="none" stroke="%s" stroke-width="9"/><path d="M62 120 Q62 70 100 70 Q138 70 138 120" fill="none" %s/><path d="M36 120 H164 L176 238 H24Z" fill="%s" %s/>' % (INK, ST2, p['a'], ST) + '<path d="M36 120 H164 L158 158 H42Z" fill="%s" opacity=".5"/><circle cx="100" cy="164" r="14" fill="%s" %s/>' % (INK, GOLD, ST2) + txt(100, 170, 'G', 14, INK) + ''.join('<path d="M%s 176 V230" stroke="%s" stroke-width="2" opacity=".2"/>' % (44 + i * 14, INK) for i in range(9)) + hl(40, 132, 7, 96, WHITE, .3, 3))
@hero
def fil_aiguille(p, **k):
    return ('<g transform="rotate(32 100 160)"><rect x="95" y="50" width="10" height="170" rx="5" fill="#C9CCD2" %s/><ellipse cx="100" cy="68" rx="3.4" ry="12" fill="%s"/><polygon points="95,220 105,220 100,246" fill="#C9CCD2" %s/></g>' % (ST, INK, ST2) + '<path d="M96 76 Q20 80 40 140 Q70 190 130 140 Q170 100 130 70 Q96 56 80 100 Q70 160 134 200 Q170 226 150 262" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % p['a'])
@hero
def planete(p, **k):
    return ('<circle cx="100" cy="164" r="62" fill="%s" %s/><path d="M62 144 Q88 128 112 148 Q100 172 70 166Z M106 190 Q134 180 146 202 Q124 222 100 208Z" fill="%s" opacity=".7"/>' % (RED if k.get('red') else p['a'], ST, INK) + '<ellipse cx="100" cy="164" rx="94" ry="18" fill="none" stroke="%s" stroke-width="4" opacity=".7" transform="rotate(-20 100 164)"/>' % CREAM + stars(p, 14, 9, 0, 280) + '<path d="M46 124 A62 62 0 0 1 94 104" stroke="#fff" stroke-width="5" fill="none" opacity=".4" stroke-linecap="round"/>')
@hero
def module_lunaire(p, **k):
    return ('<path d="M0 262 Q100 236 200 262 V300 H0Z" fill="#B8B4AC" %s/><ellipse cx="46" cy="276" rx="22" ry="6" fill="#8E8A82"/><ellipse cx="150" cy="282" rx="16" ry="5" fill="#8E8A82"/>' % ST2 + '<path d="M64 212 L52 258 M136 212 L148 258" stroke="%s" stroke-width="5" stroke-linecap="round"/><ellipse cx="52" cy="260" rx="12" ry="4" fill="%s"/><ellipse cx="148" cy="260" rx="12" ry="4" fill="%s"/>' % (GOLD, GOLD, GOLD) +
            '<path d="M70 172 L84 130 H116 L130 172 V212 H70Z" fill="%s" %s/><rect x="70" y="196" width="60" height="20" fill="%s" %s/><circle cx="100" cy="156" r="11" fill="%s" %s/>' % (GOLD2, ST, GOLD, ST2, INK, ST2) + '<path d="M96 130 V106 M104 130 V106" stroke="%s" stroke-width="3"/>' % INK + stars(p, 24, 12, 0, 220) + '<circle cx="164" cy="80" r="16" fill="#5C8FD0" %s/>' % ST2)
@hero
def lunettes_nage(p, **k):
    return ('<path d="M20 160 H40 M160 160 H180" stroke="%s" stroke-width="10" stroke-linecap="round"/><ellipse cx="66" cy="160" rx="34" ry="28" fill="%s" %s/><ellipse cx="134" cy="160" rx="34" ry="28" fill="%s" %s/><path d="M96 158 H104" stroke="%s" stroke-width="8"/>' % (p['a'], '#8EC8E8', ST, '#8EC8E8', ST, INK) + '<path d="M46 148 Q58 136 76 140" stroke="#fff" stroke-width="5" fill="none" opacity=".7" stroke-linecap="round"/>' + ''.join('<path d="M-10 %s Q25 %s 60 %s T130 %s T210 %s" fill="none" stroke="%s" stroke-width="3" opacity="%s"/>' % (222 + j * 14, 214 + j * 14, 222 + j * 14, 222 + j * 14, 222 + j * 14, CREAM, .7 - j * .2) for j in range(3)))
@hero
def bouee(p, **k):
    o = '<circle cx="100" cy="164" r="66" fill="%s" %s/>' % (CREAM, ST) + ''.join('<path d="M100 164 L%.1f %.1f A66 66 0 0 1 %.1f %.1f Z" fill="%s"/>' % (100 + 66 * math.cos(a), 164 + 66 * math.sin(a), 100 + 66 * math.cos(a + math.pi / 4), 164 + 66 * math.sin(a + math.pi / 4), RED) for a in (0, math.pi / 2, math.pi, 3 * math.pi / 2))
    return o + '<circle cx="100" cy="164" r="66" fill="none" %s/><circle cx="100" cy="164" r="30" fill="%s" %s/>' % (ST, p['b0'], ST) + '<path d="M54 130 A56 56 0 0 1 90 108" stroke="#fff" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/>'
@hero
def raquette(p, **k):
    return ('<g transform="rotate(30 100 164)"><ellipse cx="100" cy="116" rx="40" ry="52" fill="none" stroke="%s" stroke-width="9"/><ellipse cx="100" cy="116" rx="40" ry="52" fill="none" %s/>' % (k.get('c', p['a']), ST2) + ''.join('<path d="M%s 70 V162" stroke="%s" stroke-width="1" opacity=".7"/>' % (68 + i * 8, CREAM) for i in range(9)) + ''.join('<path d="M62 %s H138" stroke="%s" stroke-width="1" opacity=".7"/>' % (84 + i * 10, CREAM) for i in range(8)) +
            '<rect x="95" y="166" width="10" height="34" fill="%s" %s/><rect x="92" y="196" width="16" height="48" rx="6" fill="%s" %s/></g>' % (k.get('c', p['a']), ST2, INK, ST) + '<circle cx="154" cy="220" r="13" fill="#D8E84A" %s/><path d="M142 216 Q154 226 166 216" stroke="%s" stroke-width="1.8" fill="none"/>' % (ST2, CREAM))
@hero
def etiquette(p, **k):
    return ('<path d="M100 40 V80" stroke="%s" stroke-width="2.4"/><g transform="rotate(8 100 160)"><path d="M48 90 H152 V240 H48Z" fill="%s" %s/><circle cx="100" cy="106" r="7" fill="%s" %s/>' % (CREAM, CREAM, ST, p['b0'], ST2) + txt(100, 164, k.get('t', 'BJÖRN'), 28, p['a'], ls=2) + txt(100, 190, k.get('t2', 'BORG'), 28, INK, ls=2) + '<path d="M60 214 H140" stroke="%s" stroke-width="3" opacity=".5"/></g>' % INK)
@hero
def bandeau(p, **k):
    return ('<path d="M22 130 Q100 96 178 130 V176 Q100 142 22 176Z" fill="%s" %s/><path d="M22 140 Q100 106 178 140" stroke="%s" stroke-width="5" fill="none" opacity=".5"/><path d="M22 166 Q100 132 178 166" stroke="%s" stroke-width="5" fill="none" opacity=".5"/>' % (p['a'], ST, CREAM, CREAM) + '<circle cx="100" cy="170" r="52" fill="none" stroke="%s" stroke-width="2" opacity="0"/>' % INK + '<path d="M172 134 q22 -6 20 22 M172 150 q18 6 14 28" stroke="%s" stroke-width="6" fill="none" stroke-linecap="round"/>' % p['a'])
