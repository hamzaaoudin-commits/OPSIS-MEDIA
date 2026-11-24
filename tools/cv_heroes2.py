from cv_engine import *
from cv_heroes1 import hl
H = {}
def hero(f): H[f.__name__] = f; return f
GREY = '#9AA0AA'

@hero
def etoile_trottoir(p, **k):
    pts = []
    for i in range(10):
        r = 78 if i % 2 == 0 else 33; a = -math.pi / 2 + i * math.pi / 5; pts.append((100 + r * math.cos(a), 166 + r * math.sin(a)))
    return ('<polygon points="%s" fill="%s" %s/>' % (' '.join('%.1f,%.1f' % q for q in pts), p['a2'], ST) + '<polygon points="%s" fill="none" stroke="%s" stroke-width="2" opacity=".5" transform="translate(100 166) scale(.72) translate(-100 -166)"/>' % (' '.join('%.1f,%.1f' % q for q in pts), INK) +
            '<circle cx="100" cy="166" r="14" fill="%s" %s/>' % (p['a'], ST2) + '<path d="M0 262 H200 M0 280 H200" stroke="%s" stroke-width="2" opacity=".4"/>' % CREAM)
@hero
def pot_peinture(p, **k):
    return ('<path d="M100 40 V96" stroke="%s" stroke-width="3"/><path d="M100 96 L66 110 H134Z" fill="none" stroke="%s" stroke-width="3"/>' % (CREAM, CREAM) + '<path d="M62 118 H138 L130 214 H70Z" fill="%s" %s/><ellipse cx="100" cy="118" rx="38" ry="9" fill="%s" %s/>' % (p['a'], ST, mix(p['a'], INK, .3), ST) +
            '<rect x="68" y="150" width="64" height="30" fill="%s" opacity=".9"/>' % CREAM + txt(100, 171, 'PEINTURE', 13, INK, ls=1.4) + '<path d="M72 126 q-4 40 0 70" stroke="#fff" stroke-width="3" fill="none" opacity=".4"/>' +
            '<path d="M84 124 q4 26 -2 40 M118 124 q-4 22 2 30" stroke="%s" stroke-width="7" stroke-linecap="round" opacity=".9" fill="none"/>' % mix(p['a'], WHITE, .2) + '<circle cx="82" cy="252" r="9" fill="#C9CCD2" %s/><circle cx="118" cy="256" r="9" fill="#C9CCD2" %s/><circle cx="150" cy="246" r="7" fill="#C9CCD2" %s/>' % (ST2, ST2, ST2))
@hero
def telephone(p, **k):
    return ('<rect x="42" y="170" width="116" height="62" rx="16" fill="%s" %s/><path d="M48 168 Q50 128 100 126 Q150 128 152 168" fill="none" stroke="%s" stroke-width="16" stroke-linecap="round"/><path d="M48 168 Q50 128 100 126 Q150 128 152 168" fill="none" %s/>' % (INK, ST, INK, ST) +
            '<circle cx="100" cy="202" r="26" fill="%s" %s/>' % (CREAM, ST) + ''.join('<circle cx="%.1f" cy="%.1f" r="3.4" fill="%s"/>' % (100 + 17 * math.cos(a), 202 + 17 * math.sin(a), INK) for a in [i * math.pi / 5 for i in range(10)]) + '<circle cx="100" cy="202" r="6" fill="%s"/>' % p['a'] +
            '<path d="M100 232 q-30 20 -50 8 q-10 20 20 30" fill="none" stroke="%s" stroke-width="3"/>' % CREAM)
@hero
def maison_fendue(p, **k):
    return ('<polygon points="100,96 30,156 100,156 92,168 104,184 92,200 104,216 96,246 30,246" fill="%s" %s/><polygon points="100,96 170,156 100,156 92,168 104,184 92,200 104,216 96,246 170,246" fill="%s" %s transform="translate(10 4)"/>' % (mix(p['b0'], CREAM, .35), ST, mix(p['b0'], CREAM, .15), ST) +
            '<rect x="50" y="176" width="22" height="22" fill="%s" opacity=".9"/><rect x="132" y="180" width="22" height="22" fill="%s" opacity=".9"/>' % (p['a2'], p['a2']) + '<path d="M100 150 V250" stroke="%s" stroke-width="5" opacity=".55"/>' % INK)
@hero
def echelle_taille(p, **k):
    o = '<rect x="58" y="62" width="84" height="204" fill="%s" %s/><rect x="70" y="62" width="60" height="204" fill="%s"/>' % (mix(CREAM, INK, .25), ST, mix(p['b0'], INK, .5))
    for i in range(9):
        y = 246 - i * 20; o += '<path d="M%s %s H%s" stroke="%s" stroke-width="3"/>' % (70, y, 70 + (24 if i % 2 else 34), CREAM) + txt(108 + (i % 2) * 0, y + 4, str(5 + i), 8, CREAM, anchor='start', weight=700) if False else '<path d="M70 %s H%s" stroke="%s" stroke-width="3"/>' % (y, 70 + (22 if i % 2 else 34), p['a2'])
    return o + '<path d="M70 246 l60 -0" stroke="%s" stroke-width="3" opacity="0"/>' % INK + '<rect x="70" y="86" width="30" height="5" fill="%s"/><polygon points="136,100 156,92 156,108" fill="%s" %s/>' % (RED, RED, ST2)
@hero
def chaise_vide(p, **k):
    return ('<path d="M70 160 V252 M130 160 V252" stroke="%s" stroke-width="9" stroke-linecap="round"/><rect x="60" y="196" width="80" height="14" rx="4" fill="%s" %s/><path d="M70 196 V100 Q70 90 80 90 H120 Q130 90 130 100 V196" fill="none" stroke="%s" stroke-width="10" stroke-linecap="round"/>' % (INK, mix(p['a'], INK, .3), ST, INK) +
            '<path d="M78 112 H122 M78 144 H122" stroke="%s" stroke-width="5"/>' % mix(p['a'], INK, .3) + '<ellipse cx="100" cy="262" rx="60" ry="8" fill="%s" opacity=".5"/>' % INK + '<path d="M120 212 q16 6 24 20" stroke="%s" stroke-width="2.2" fill="none" opacity=".4"/>' % CREAM)
@hero
def ours(p, **k):
    return ('<circle cx="64" cy="108" r="17" fill="#B88246" %s/><circle cx="136" cy="108" r="17" fill="#B88246" %s/><circle cx="100" cy="144" r="52" fill="#C99A5B" %s/>' % (ST, ST, ST) + '<ellipse cx="100" cy="162" rx="22" ry="17" fill="#EAD2A6" %s/><circle cx="100" cy="155" r="6" fill="%s"/><circle cx="80" cy="132" r="5" fill="%s"/><circle cx="120" cy="132" r="5" fill="%s"/>' % (ST2, INK, INK, INK) +
            '<path d="M100 161 v7 M90 172 q10 7 20 0" stroke="%s" stroke-width="2.4" fill="none"/><path d="M76 192 Q100 214 124 192 L130 236 H70Z" fill="%s" %s/><path d="M80 196 L100 210 L120 196 L100 224Z" fill="%s" %s/>' % (INK, RED, ST, RED, ST2))
@hero
def arbre_gene(p, **k):
    o = '<path d="M100 252 V150 M100 190 Q70 180 56 150 M100 190 Q130 180 144 150 M100 150 Q86 130 70 112 M100 150 Q114 130 130 112" fill="none" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % mix(INK, CREAM, .1)
    for x, y, r in ((56, 144, 17), (144, 144, 17), (70, 106, 17), (130, 106, 17), (100, 84, 20), (100, 126, 15)):
        o += '<circle cx="%s" cy="%s" r="%s" fill="%s" %s/><circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (x, y, r, CREAM, ST, x, y - 3, r * .38, INK) + '<path d="M%s %s Q%s %s %s %s" fill="%s"/>' % (x - r * .6, y + r * .7, x, y + r * .05, x + r * .6, y + r * .7, INK)
    return o + '<rect x="40" y="250" width="120" height="8" rx="3" fill="%s" %s/>' % (INK, ST2)
@hero
def doigt_lumiere(p, **k):
    return ('<circle cx="100" cy="140" r="90" fill="%s" opacity=".1"/><circle cx="100" cy="140" r="60" fill="%s" opacity=".14"/>' % (p['a2'], p['a2']) +
            '<path d="M58 250 Q52 190 70 176 Q86 170 90 186 L90 120 Q90 108 102 108 Q114 108 114 120 V176 Q130 168 142 178 Q152 190 144 250Z" fill="#E0B58A" %s/>' % ST +
            '<ellipse cx="102" cy="104" rx="13" ry="16" fill="%s" %s/><ellipse cx="102" cy="104" rx="26" ry="30" fill="%s" opacity=".35"/>' % (WHITE, ST2, p['a2']) + sparkle(138, 84, 12) + sparkle(64, 92, 9) + '<path d="M96 150 v22 M108 156 v16" stroke="%s" stroke-width="2" opacity=".4"/>' % INK)
@hero
def boule_disco(p, **k):
    o = '<path d="M100 40 V96" stroke="%s" stroke-width="3"/><circle cx="100" cy="150" r="58" fill="#B8BEC9" %s/>' % (CREAM, ST)
    for i in range(7):
        for j in range(7):
            x = 56 + i * 14.6; y = 106 + j * 14.6
            if (x - 100) ** 2 + (y - 150) ** 2 < 52 ** 2: o += '<rect x="%.1f" y="%.1f" width="12" height="12" fill="%s" opacity="%s" stroke="%s" stroke-width=".8"/>' % (x, y, [WHITE, p['a2'], '#8E96A8', p['a']][(i * 3 + j) % 4], .9, INK)
    o += '<path d="M62 120 Q80 96 108 94" stroke="#fff" stroke-width="5" fill="none" opacity=".6" stroke-linecap="round"/>'
    return o + sparkle(26, 120, 11) + sparkle(176, 110, 13) + sparkle(160, 214, 9) + sparkle(36, 216, 8) + sparkle(100, 232, 7)
@hero
def fenetre_barreaux(p, **k):
    o = '<rect x="44" y="78" width="112" height="152" rx="3" fill="%s" %s/><rect x="54" y="88" width="92" height="132" fill="%s"/>' % (INK, ST, mix(p['b0'], CREAM, .35))
    o += '<circle cx="118" cy="122" r="18" fill="%s" opacity=".9"/>' % CREAM
    for i in range(5): o += '<rect x="%s" y="78" width="6" height="152" fill="#6A6F78" %s/>' % (60 + i * 20, ST2)
    return o + '<rect x="40" y="228" width="120" height="10" fill="%s" %s/>' % (INK, ST2) + '<rect x="86" y="150" width="28" height="22" rx="3" fill="%s" %s/><path d="M92 150 v-8 q8 -10 16 0 v8" fill="none" stroke="%s" stroke-width="3"/>' % (GOLD, ST, GOLD)
@hero
def acte_dechire(p, **k):
    t = k.get('t', 'ÉMANCIPATION')
    return ('<g transform="rotate(-6 70 160)"><path d="M40 84 H112 L106 104 L114 126 L104 148 L112 172 L106 196 L112 236 H40Z" fill="%s" %s/>' % (CREAM, ST) + txt(76, 108, t[:6], 10, INK, ls=1) + ''.join('<rect x="50" y="%s" width="%s" height="3" fill="%s" opacity=".5"/>' % (122 + i * 14, 46 - (i % 3) * 8, INK) for i in range(6)) + '</g>' +
            '<g transform="rotate(8 130 160)"><path d="M122 92 L186 98 L180 130 L188 156 L178 180 L184 244 L132 240 L126 214 L134 186 L124 160 L132 130Z" fill="%s" %s/>' % (CREAM, ST) + ''.join('<rect x="138" y="%s" width="%s" height="3" fill="%s" opacity=".5"/>' % (116 + i * 14, 36 - (i % 3) * 8, INK) for i in range(8)) + '</g>')
@hero
def cle_simple(p, **k):
    return ('<g transform="rotate(-24 100 160)"><circle cx="100" cy="94" r="30" fill="%s" %s/><circle cx="100" cy="94" r="11" fill="%s"/><rect x="92" y="122" width="16" height="96" fill="%s" %s/><rect x="108" y="176" width="20" height="10" fill="%s" %s/><rect x="108" y="196" width="14" height="10" fill="%s" %s/></g>' % (GOLD, ST, p['b0'], GOLD, ST, GOLD, ST2, GOLD, ST2) +
            '<g transform="rotate(14 138 232)"><path d="M118 212 H160 V236 L152 248 H118Z" fill="%s" %s/><circle cx="126" cy="222" r="3" fill="%s"/>' % (p['a'], ST, INK) + txt(142, 240, k.get('t', 'N°1'), 12, INK) + '</g>')
@hero
def ailes(p, **k):
    o = ''
    for s in (-1, 1):
        o += '<g transform="translate(100 168) scale(%s 1)">' % s
        for i in range(6): o += '<path d="M10 %s Q%s %s %s %s Q%s %s 10 %s Z" fill="%s" %s/>' % (-10 + i * 10, 44 + i * 6, -52 + i * 10, 96 - i * 6, -34 + i * 14, 56 + i * 4, -6 + i * 12, 6 + i * 10, CREAM if i % 2 else mix(CREAM, p['a2'], .25), ST2)
        o += '</g>'
    return o + '<ellipse cx="100" cy="82" rx="26" ry="8" fill="none" stroke="%s" stroke-width="5"/><ellipse cx="100" cy="82" rx="26" ry="8" fill="none" %s opacity=".5"/>' % (GOLD2, ST2) + '<circle cx="100" cy="166" r="12" fill="%s" %s/>' % (INK, ST2)
@hero
def ballon_use(p, **k):
    return ('<circle cx="100" cy="164" r="68" fill="#D8C7A4" %s/><polygon points="100,128 128,148 118,182 82,182 72,148" fill="%s" %s/>' % (ST, mix(INK, CREAM, .12), ST) + '<path d="M100 128 V96 M128 148 L158 136 M118 182 L140 210 M82 182 L60 210 M72 148 L42 136" stroke="%s" stroke-width="3"/>' % INK +
            '<path d="M44 150 L58 156 M150 190 L162 184 M70 106 q6 8 14 4" stroke="%s" stroke-width="2" opacity=".5"/>' % INK + '<path d="M0 242 H200 V300 H0Z" fill="%s" opacity=".0"/>' % INK + '<path d="M38 112 A68 68 0 0 1 92 98" stroke="#fff" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/>')
@hero
def assiettes(p, **k):
    o = ''
    for i in range(8):
        x = 38 + (i % 4) * 41; y = 126 + (i // 4) * 62
        o += '<circle cx="%s" cy="%s" r="19" fill="%s" %s/><circle cx="%s" cy="%s" r="12" fill="none" stroke="%s" stroke-width="1.6" opacity=".4"/>' % (x, y, CREAM, ST, x, y, INK)
        if i < 3: o += '<circle cx="%s" cy="%s" r="5" fill="%s"/>' % (x, y, p['a'])
    return o + '<rect x="14" y="238" width="172" height="10" rx="3" fill="%s" %s/>' % (INK, ST2)
@hero
def vesuve_ballon(p, **k):
    return ('<polygon points="0,250 70,150 92,126 108,126 130,150 200,250" fill="%s" %s/><polygon points="92,126 108,126 114,138 86,138" fill="%s"/>' % (mix(INK, p['a'], .2), ST, p['a']) +
            '<path d="M94 128 Q80 90 96 60 M106 128 Q124 96 108 52" fill="none" stroke="%s" stroke-width="8" stroke-linecap="round" opacity=".55"/>' % CREAM +
            '<circle cx="100" cy="204" r="30" fill="%s" %s/><polygon points="100,190 112,198 108,212 92,212 88,198" fill="%s"/>' % (CREAM, ST, INK) + '<path d="M0 250 H200 V300 H0Z" fill="%s" opacity=".0"/>')
@hero
def main_ballon(p, **k):
    return ('<circle cx="100" cy="82" r="38" fill="%s" %s/><polygon points="100,64 116,76 110,94 90,94 84,76" fill="%s"/>' % (CREAM, ST, INK) + '<path d="M62 250 L72 188 Q64 170 76 162 Q82 156 88 164 L92 150 Q96 140 104 144 L108 150 Q116 140 122 148 L124 158 Q134 152 140 162 Q148 176 138 190 L142 250Z" fill="#E0B58A" %s/>' % ST +
            '<path d="M92 160 v28 M106 154 v30 M120 162 v24" stroke="%s" stroke-width="2" opacity=".4"/>' % INK + sparkle(150, 112, 12))
@hero
def maillot_halo(p, **k):
    return ('<ellipse cx="100" cy="74" rx="34" ry="9" fill="none" stroke="%s" stroke-width="6"/>' % GOLD2 + '<path d="M70 96 L40 112 L52 148 L72 136 L72 238 H128 V136 L148 148 L160 112 L130 96 Q100 116 70 96Z" fill="%s" %s/>' % (CREAM, ST) +
            ''.join('<rect x="%s" y="100" width="12" height="140" fill="#7EC3F2" opacity=".85"/>' % (74 + i * 24) for i in range(0, 3)) + txt(100, 190, k.get('t', '10'), 44, INK, extra='opacity=".9"') + sparkle(34, 90, 9) + sparkle(168, 96, 10))
@hero
def ballon_creve(p, **k):
    return ('<path d="M44 190 Q36 120 100 100 Q164 120 156 190 Q150 232 100 236 Q50 232 44 190Z" fill="%s" %s/>' % (CREAM, ST) + '<path d="M58 150 L84 170 L74 206 M146 160 L120 182 L130 210" stroke="%s" stroke-width="3" fill="none"/>' % INK +
            '<path d="M100 100 L92 128 L110 146 L96 176" fill="none" stroke="%s" stroke-width="4" stroke-linejoin="round"/>' % INK + '<path d="M30 238 Q100 258 170 238" fill="none" stroke="%s" stroke-width="3" opacity=".5"/>' % CREAM)
@hero
def coeur_ecg(p, **k):
    return ('<path d="M100 232 C28 176 34 100 78 104 C92 106 100 116 100 124 C100 116 108 106 122 104 C166 100 172 176 100 232Z" fill="%s" %s/>' % (p['a'], ST) + '<path d="M28 160 H66 L80 132 L100 200 L116 150 L126 160 H172" fill="none" stroke="%s" stroke-width="4.5" stroke-linejoin="round"/>' % CREAM + '<path d="M62 118 Q70 108 84 112" stroke="#fff" stroke-width="4" fill="none" opacity=".5" stroke-linecap="round"/>')
@hero
def maison_isolee(p, **k):
    return ('<polygon points="100,112 50,158 150,158" fill="%s" %s/><rect x="58" y="158" width="84" height="66" fill="%s" %s/><rect x="92" y="184" width="16" height="40" fill="%s" %s/><rect x="68" y="172" width="16" height="14" fill="%s"/><rect x="116" y="172" width="16" height="14" fill="%s"/>' % (INK, ST, mix(p['b0'], CREAM, .25), ST, p['a2'], ST2, p['a2'], p['a2']) +
            '<path d="M0 224 H200" stroke="%s" stroke-width="3"/><path d="M20 224 q10 -40 20 0 M160 224 q12 -50 22 0" fill="%s" opacity=".8"/><circle cx="154" cy="82" r="18" fill="%s" opacity=".9"/><circle cx="162" cy="76" r="15" fill="%s"/>' % (INK, INK, CREAM, p['b0']) + stars(p, 10, 5, 0, 120))
@hero
def pigeon_immeuble(p, **k):
    o = '<rect x="36" y="86" width="128" height="170" fill="%s" %s/>' % (mix(p['a'], INK, .55), ST)
    for r in range(6):
        for c in range(4): o += '<rect x="%s" y="%s" width="18" height="20" fill="%s" opacity="%s" %s/>' % (48 + c * 30, 98 + r * 26, p['a2'] if (r + c) % 3 == 0 else INK, .85, ST2)
    return o + '<rect x="26" y="78" width="148" height="12" fill="%s" %s/>' % (INK, ST) + '<path d="M118 78 q-6 -22 8 -26 q10 -4 16 6 l14 -2 l-12 10 q2 12 -12 12Z" fill="%s" %s/><circle cx="130" cy="58" r="1.8" fill="%s"/><path d="M148 62 l8 3 l-8 2z" fill="%s"/>' % (CREAM, ST2, INK, GOLD)
@hero
def sac_boxe(p, **k):
    return ('<path d="M100 40 V84" stroke="%s" stroke-width="5"/><path d="M100 84 L72 100 M100 84 L128 100" stroke="%s" stroke-width="3"/>' % (INK, INK) + '<rect x="64" y="96" width="72" height="140" rx="20" fill="%s" %s/><path d="M64 126 H136 M64 206 H136" stroke="%s" stroke-width="3"/>' % (p['a'], ST, INK) +
            hl(72, 106, 8, 120, WHITE, .35, 4) + '<path d="M64 146 V190 M136 146 V190" stroke="%s" stroke-width="2" opacity=".35"/>' % INK + '<ellipse cx="100" cy="252" rx="46" ry="6" fill="%s" opacity=".5"/>' % INK + '<path d="M138 140 q22 -4 30 16 M142 170 q14 0 22 12" stroke="%s" stroke-width="2" fill="none" opacity=".45"/>' % CREAM)
@hero
def ceinture(p, **k):
    return ('<rect x="14" y="146" width="172" height="40" rx="8" fill="%s" %s/>' % (INK, ST) + ''.join('<rect x="%s" y="150" width="14" height="32" fill="%s" opacity=".9"/>' % (20 + i * 22, p['a'] if i % 2 else GOLD) for i in range(0, 8) if abs(20 + i * 22 - 100) > 44) +
            '<ellipse cx="100" cy="166" rx="52" ry="48" fill="%s" %s/><ellipse cx="100" cy="166" rx="42" ry="38" fill="%s" %s/><ellipse cx="100" cy="166" rx="26" ry="23" fill="%s" %s/>' % (GOLD, ST, GOLD2, ST2, p['a'], ST2) + sparkle(100, 166, 14, WHITE) + sparkle(56, 120, 9) + sparkle(150, 122, 10))
@hero
def alliance_fissuree(p, **k):
    return ('<circle cx="100" cy="184" r="52" fill="none" stroke="%s" stroke-width="16"/><circle cx="100" cy="184" r="52" fill="none" %s/><circle cx="100" cy="184" r="44" fill="none" %s/>' % (GOLD, ST, ST2) + '<path d="M98 126 L108 148 L94 160 L106 178" stroke="%s" stroke-width="4" fill="none" stroke-linejoin="round"/>' % INK +
            '<polygon points="100,92 118,112 100,134 82,112" fill="%s" %s/><polygon points="82,112 100,112 100,134" fill="#fff" opacity=".4"/>' % (CREAM, ST2) + '<path d="M60 90 l-10 -12 M140 90 l10 -12 M100 80 v-14" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % CREAM)
@hero
def porte_cellule(p, **k):
    return ('<rect x="46" y="70" width="108" height="190" fill="#6A6F78" %s/><rect x="56" y="80" width="88" height="170" fill="#7A808A" %s/>' % (ST, ST2) + ''.join('<rect x="56" y="%s" width="88" height="3" fill="%s" opacity=".4"/>' % (100 + i * 22, INK) for i in range(7)) +
            '<rect x="70" y="106" width="60" height="18" rx="2" fill="%s" %s/><circle cx="130" cy="188" r="6" fill="%s" %s/><rect x="120" y="196" width="22" height="12" fill="%s" %s/>' % (INK, ST2, GOLD, ST2, INK, ST2) + '<path d="M100 124 v10" stroke="%s" stroke-width="2"/>' % CREAM + txt(100, 238, k.get('t', '№ 922335'), 11, CREAM, ls=1.4))
@hero
def protege_dents(p, **k):
    return ('<path d="M38 164 Q38 108 100 106 Q162 108 162 164 Q162 200 140 206 Q124 196 100 198 Q76 196 60 206 Q38 200 38 164Z" fill="%s" %s/><path d="M50 160 Q100 138 150 160" fill="none" stroke="%s" stroke-width="3" opacity=".4"/>' % (p['a2'], ST, INK) +
            ''.join('<path d="M%s 176 v16" stroke="%s" stroke-width="3" opacity=".6"/>' % (66 + i * 17, INK) for i in range(5)) + '<path d="M132 168 L146 160 L140 176 L152 178" stroke="%s" stroke-width="3" fill="none"/>' % INK + hl(56, 120, 26, 6, WHITE, .5, 3))
@hero
def tigre(p, **k):
    o = '<ellipse cx="100" cy="164" rx="66" ry="60" fill="#E79A2F" %s/><polygon points="52,126 40,96 74,110" fill="#E79A2F" %s/><polygon points="148,126 160,96 126,110" fill="#E79A2F" %s/>' % (ST, ST, ST)
    o += '<ellipse cx="100" cy="190" rx="30" ry="24" fill="%s" %s/><path d="M100 168 v20" stroke="%s" stroke-width="3"/><polygon points="90,170 110,170 100,180" fill="%s"/>' % (CREAM, ST2, INK, INK)
    o += ''.join('<path d="M%s %s q%s 14 %s 28" stroke="%s" stroke-width="5" fill="none" stroke-linecap="round"/>' % (x, y, d, d * .6, INK) for x, y, d in ((60, 128, 8), (74, 114, 6), (140, 128, -8), (126, 114, -6), (100, 108, 0)))
    return o + '<circle cx="78" cy="156" r="6" fill="%s"/><circle cx="122" cy="156" r="6" fill="%s"/><circle cx="79" cy="156" r="2.4" fill="%s"/><circle cx="121" cy="156" r="2.4" fill="%s"/>' % (GOLD2, GOLD2, INK, INK) + '<path d="M70 196 H30 M70 202 L34 214 M130 196 H170 M130 202 L166 214" stroke="%s" stroke-width="1.6" opacity=".8"/>' % CREAM
@hero
def tabouret_scene(p, **k):
    return ('<polygon points="70,40 130,40 176,262 24,262" fill="%s" opacity=".14"/>' % CREAM + '<ellipse cx="100" cy="250" rx="60" ry="9" fill="%s" opacity=".55"/>' % p['a'] +
            '<path d="M80 168 L68 248 M120 168 L132 248 M100 170 V250" stroke="%s" stroke-width="7" stroke-linecap="round"/><ellipse cx="100" cy="166" rx="34" ry="9" fill="%s" %s/>' % (INK, mix(p['a'], INK, .3), ST) +
            '<rect x="124" y="124" width="18" height="40" rx="3" fill="#6FB2E0" %s/><rect x="128" y="116" width="10" height="9" rx="2" fill="%s" %s/><rect x="72" y="118" width="26" height="46" rx="3" fill="%s" opacity="0"/>' % (ST2, INK, ST2, INK) +
            '<path d="M70 124 q6 -8 16 -2 v30 h-16z" fill="%s" %s/>' % (CREAM, ST2))
