#!/usr/bin/env python3
"""Contrôle un récit au format OPSIS v3 : python3 tools/v3_check.py <id>…"""
import json,sys,os,re,statistics
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
B={3:(520,760),7:(1250,1950),12:(2200,3000)}
bad=0
for i in sys.argv[1:]:
    p=os.path.join(R,'data','opsis_v3',i+'.json');pb=[]
    try:x=json.load(open(p))
    except Exception as e:print(i,'ERREUR JSON',e);bad+=1;continue
    for k in('id','name','sub','fmt','body','blurb','learned','retain','note'):
        if k not in x or not x[k]:pb.append('champ manquant: '+k)
    if not pb:
        body=x['body'];f=x['fmt']
        w=sum(len(t.split()) for t in body if t[:1] not in '#@')
        if f not in B:pb.append('fmt 3, 7 ou 12')
        elif not B[f][0]<=w<=B[f][1]:pb.append('%d mots, attendu %d à %d'%(w,*B[f]))
        H=[t for t in body if t.startswith('#')]
        if not H[0].upper().startswith('#PROLOGUE'):pb.append('premier intertitre: #PROLOGUE — lieu, date')
        if not H[-1].upper().startswith('#ÉPILOGUE'):pb.append('dernier intertitre: #ÉPILOGUE — titre')
        nums=[h for h in H if re.match(r'#\d\d — ',h)]
        mn={3:2,7:4,12:7}.get(f,3)
        if len(nums)<mn:pb.append('au moins %d chapitres numérotés « #01 — TITRE EN MAJUSCULES »'%mn)
        if any(h[1:]!=h[1:].upper() and re.match(r'#\d\d',h) for h in H):pb.append('titres de chapitres en MAJUSCULES')
        P=[len(t.split()) for t in body if t[:1] not in '#@!']
        if statistics.median(P)>32:pb.append('paragraphes trop longs (médiane %d mots, viser 8 à 28)'%statistics.median(P))
        if max(P)>90:pb.append('un paragraphe de %d mots (max 90)'%max(P))
        txt='\n'.join(body)
        if '*' in txt:pb.append('astérisques interdits')
        if re.search(r'(?i)\b(selon (?:wikip|le site|les sources|une source)|d.après (?:wikip|le site))',txt):pb.append('source citée dans le récit')
        if len(x['name'])>46:pb.append('titre trop long')
        if not 3<=len(x['learned'])<=7:pb.append('learned: 3 à 6 puces')
        if len(x['name'])>0 and x['name'].isupper():pb.append('titre en casse normale')
        nb=len(x['blurb'].get('b','').split())
        if not 40<=nb<=75:pb.append('blurb.b: %d mots'%nb)
        print(i,'OK' if not pb else 'À CORRIGER',f,'|',w,'mots, médiane',statistics.median(P),'|' if pb else '',' ; '.join(pb))
    else:print(i,'À CORRIGER |',' ; '.join(pb))
    bad+=bool(pb)
sys.exit(1 if bad else 0)
