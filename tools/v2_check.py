#!/usr/bin/env python3
"""Contrôle une histoire réécrite : python3 tools/v2_check.py <id> [<id>…]"""
import json,sys,os,re
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
B={3:(540,700),7:(1250,1560),12:(2200,2700)}
bad=0
for i in sys.argv[1:]:
    p=os.path.join(R,'data','opsis_v2',i+'.json');pb=[]
    try:x=json.load(open(p))
    except Exception as e:print(i,'ERREUR JSON',e);bad+=1;continue
    for k in('id','name','sub','fmt','body','blurb'):
        if k not in x:pb.append('champ manquant: '+k)
    if not pb:
        body=x['body'];w=sum(len(t.split()) for t in body if t[:1] not in '#@')
        f=x['fmt']
        if f not in B:pb.append('fmt doit valoir 3, 7 ou 12')
        elif not B[f][0]<=w<=B[f][1]:pb.append('%d mots, attendu %d à %d pour %d min'%(w,B[f][0],B[f][1],f))
        if not isinstance(body,list) or not all(isinstance(t,str) and t.strip() for t in body):pb.append('body doit être une liste de chaînes non vides')
        elif not body[0].startswith('#'):pb.append('le texte doit commencer par un intertitre #')
        txt='\n'.join(body)
        if '*' in txt:pb.append('astérisques interdits')
        m=re.findall(r'(?i)\b(selon (?:wikip|le site|les sources|une source|britannica)|d.après (?:wikip|le site)|les sources (?:divergent|lues))',txt)
        if m:pb.append('attributions de source dans le récit: '+', '.join(sorted(set(m))))
        if len(x['name'])>46:pb.append('titre trop long (%d)'%len(x['name']))
        if not 90<=len(x['sub'])<=200:pb.append('sub: %d caractères'%len(x['sub']))
        if x['id']!=i:pb.append('id incorrect')
        nb=len(x['blurb'].get('b','').split())
        if not 40<=nb<=70:pb.append('blurb.b: %d mots'%nb)
        print(i,'OK' if not pb else 'À CORRIGER',f,'min',w,'mots','' if not pb else '| '+' ; '.join(pb))
    else:print(i,'À CORRIGER |',' ; '.join(pb))
    bad+=bool(pb)
sys.exit(1 if bad else 0)
