#!/usr/bin/env python3
"""Convertit un récit au format modèle (docs/modeles/*.md) en data/opsis_v3/<id>.json : python3 tools/v3_from_md.py <fichier.md> <id> <fmt>"""
import re,sys,json,os
f,i,fmt=sys.argv[1],sys.argv[2],int(sys.argv[3])
L=[l.rstrip() for l in open(f,encoding='utf-8')]
title=next(l[2:].strip() for l in L if l.startswith('# '))
sub=next(l for l in L if l.startswith('**') and l.endswith('**') and len(l)>30)[2:-2]
body=[];learned=[];retain='';note='';src=[];mode='story'
sec=None
for l in L:
    s=l.strip()
    if not s or s=='---' or s.startswith('# ') or s.startswith('###') or s==('**'+sub+'**'):continue
    if s.startswith('## '):
        h=s[3:].strip()
        if h.startswith('PAGE DE FIN'):mode='fin';continue
        if h.startswith('SOURCES'):mode='src';continue
        body.append('#'+h.title().replace(' — ',' — ') if False else '#'+h);continue
    if mode=='story':
        if s.startswith('**') and s.endswith('**'):body.append('!'+s.strip('*'))
        else:body.append(s.replace('**',''))
    elif mode=='fin':
        if s.startswith('**CE QUE'):sec='l';continue
        if s.startswith('**À RETENIR'):sec='r';continue
        if s.startswith('**LA PROCHAINE'):sec='n';continue
        if sec=='l' and s.startswith('- '):learned.append(s[2:])
        elif sec=='r':retain+=(' ' if retain else '')+s
    elif mode=='src':
        if s.startswith('**NOTE'):sec='note';continue
        if sec=='note':note+=(' ' if note else '')+s
        elif re.match(r'\d+\.',s):src.append(re.sub(r'^\d+\.\s*','',s).replace('**',''))
        elif src and s.startswith('http'):src[-1]+=' '+s
os.makedirs('data/opsis_v3',exist_ok=True)
words=sum(len(t.split()) for t in body if t[0] not in '#@')
out={'id':i,'fmt':fmt,'name':title.title() if title.isupper() else title,'sub':sub,'body':body,'learned':learned,'retain':retain,'note':note,'src':src,'blurb':{'b':'','h':''}}
json.dump(out,open('data/opsis_v3/%s.json'%i,'w'),ensure_ascii=False,indent=1)
print(i,words,'mots',len(body),'lignes',len(learned),'appris',len(src),'sources')
