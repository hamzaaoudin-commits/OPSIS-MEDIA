#!/usr/bin/env python3
"""Couvertures des épisodes des « vies » : une affiche dessinée par épisode (objet central propre à
l'épisode, décor, ambiance, grain, vignette), dans le style des affiches de base.
Moteur : cv_engine.py · objets : cv_heroes1-5.py · affectation : cv_recipes1-5.py
Écrit les clés ptNNeK dans data/covers.json. Idempotent."""
import sys, os, json, re, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cv_build import make, palette, R
LIV = json.load(open(R + '/data/lives.json')); COV = json.load(open(R + '/data/covers.json'))
REC = {}
for m in ('cv_recipes1', 'cv_recipes2', 'cv_recipes3', 'cv_recipes4', 'cv_recipes5'):
    REC.update(importlib.import_module(m).REC)
for k in [k for k in COV if re.match(r'pt\d\de\d+$', k)]: del COV[k]
bad = made = 0
for pid in sorted(LIV):
    eps = LIV[pid]['eps']
    if len(REC.get(pid, [])) != len(eps): print('!', pid, len(REC.get(pid, [])), len(eps)); bad += 1; continue
    pal = palette(COV[pid])
    for i, (e, rec) in enumerate(zip(eps, REC[pid]), 1):
        COV['%se%d' % (pid, i)] = make(pid, i, len(eps), e['t'], rec, pal); made += 1
json.dump(COV, open(R + '/data/covers.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print("couvertures d'épisodes :", made, '· erreurs :', bad)
sys.exit(1 if bad else 0)
