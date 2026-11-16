import sys, json, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cv_build import *
import importlib
LIV = json.load(open(R + '/data/lives.json')); COV = json.load(open(R + '/data/covers.json'))
REC = {}
for m in ('cv_recipes1','cv_recipes2','cv_recipes3','cv_recipes4','cv_recipes5','cv_recipes6'):
    try: REC.update(importlib.import_module(m).REC)
    except ImportError: pass
pids = sys.argv[1:] or sorted(REC)
h = '<meta charset=utf-8><body style="background:#111;margin:0;display:flex;flex-wrap:wrap;gap:5px;padding:5px">'
i = 0
for pid in pids:
    eps = LIV[pid]['eps']; pal = palette(COV[pid])
    assert len(REC[pid]) == len(eps), (pid, len(REC[pid]), len(eps))
    for n, (e, rec) in enumerate(zip(eps, REC[pid]), 1):
        s = make(pid, n, len(eps), e['t'], rec, pal); i += 1
        s = re.sub(r'(id="|url\(#)(\w+)', lambda m: m.group(1) + m.group(2) + '_%d' % i, s)
        h += '<div style="width:190px;height:285px">%s</div>' % s.replace('<svg', '<svg width="190" height="285"', 1)
open('/tmp/claude-0/try.html', 'w').write(h)
