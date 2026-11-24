import sys, json, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cv_engine import *
import cv_heroes1
H = dict(cv_heroes1.H)
for m in ('cv_heroes2', 'cv_heroes3', 'cv_heroes4', 'cv_heroes5'):
    try: H.update(__import__(m).H)
    except ImportError: pass
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def make(pid, n, N, title, rec, pal):
    hero, args = rec['h'] if isinstance(rec['h'], tuple) else (rec['h'], {})
    p = MOODS[rec.get('m', 'standard')](pal)
    if n % 2 == 0 and rec.get('swap', 1): p = dict(p, a=p['a2'], a2=p['a'])
    body = BG[rec.get('bg', 'nu')](p) + H[hero](p, **args)
    for acc in rec.get('acc', []):
        nm, x, y, s = acc[:4]; ar = acc[4] if len(acc) > 4 else {}
        body += '<g transform="translate(%s %s) scale(%s) translate(-100 -160)">%s</g>' % (x, y, s, H[nm](p, **ar))
    defs = ('<defs><linearGradient id="gX" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
            '<radialGradient id="vgP" cx=".5" cy=".42" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>'
            '<pattern id="dtP" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#fff" opacity=".08"/></pattern></defs>') % (p['b0'], p['b1'])
    lines = wrap(re.sub(r'\s+', ' ', re.sub(r'[«»“”"]', '', title).replace('’', "'")).upper().strip())
    sc = '<g>%s</g>' % body
    if rec.get('halo', 1): sc = halo(p, 100, 150, 64, .16) + sc
    tag = txt(100, 289, 'ÉPISODE %d / %d' % (n, N), 9, CREAM, ls=2.4, extra='opacity=".85"')
    return ('<svg viewBox="0 0 200 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true">' + defs + '<rect width="200" height="300" fill="url(#gX)"/>' + sc +
            '<rect y="236" width="200" height="64" fill="#000" opacity=".0"/><rect width="200" height="300" fill="url(#dtP)"/><rect width="200" height="300" fill="url(#vgP)"/>' + labelsvg(lines, p) + tag + '</svg>')
