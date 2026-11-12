#!/usr/bin/env python3
"""Contrôle un récit OPSIS v4 : python3 tools/v4_check.py <id>…  (garde-fous légers : la qualité narrative se juge à la lecture)"""
import json,sys,os,re,statistics
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
B={3:(520,850),7:(1100,2000),12:(2000,3200)}
bad=0
for i in sys.argv[1:]:
    p=os.path.join(R,'data','opsis_v4',i+'.json');pb=[]
    try:x=json.load(open(p))
    except Exception as e:print(i,'ERREUR JSON',e);bad+=1;continue
    for k in('id','name','sub','fmt','body','blurb','note'):
        if k not in x or not x[k]:pb.append('champ manquant: '+k)
    if not pb:
        body=x['body'];f=x['fmt']
        w=sum(len(t.split()) for t in body if t[:1] not in '#@')
        if f not in B:pb.append('fmt 3, 7 ou 12')
        elif not B[f][0]<=w<=B[f][1]:pb.append('%d mots, attendu %d à %d'%(w,*B[f]))
        if body[0][:1] in '#@!':pb.append('le récit doit commencer par un paragraphe (pas de dateline ni d\'intertitre)')
        H=[t for t in body if t.startswith('#')]
        if re.search(r'(?i)^#(prologue|épilogue|\d\d)',' \n'.join(H),re.M):pb.append('pas de PROLOGUE/ÉPILOGUE/chapitres numérotés')
        if len(H)>{3:3,7:6,12:9}.get(f,6):pb.append('trop d\'intertitres (%d)'%len(H))
        if any(t.startswith(('@','!')) for t in body):pb.append('pas de dateline @ ni d\'exergue !')
        P=[len(t.split()) for t in body if t[:1] not in '#@!']
        med=statistics.median(P)
        if med<22:pb.append('paragraphes trop courts (médiane %d mots, viser 35 à 90) : style télégraphique'%med)
        short=sum(1 for n in P if n<9)
        if short>max(3,len(P)//8):pb.append('trop de paragraphes d\'une courte phrase isolée (%d)'%short)
        if max(P)>170:pb.append('un paragraphe de %d mots (max 170)'%max(P))
        txt='\n'.join(body)
        if '*' in txt:pb.append('astérisques interdits')
        if re.search(r'(?i)\b(selon (?:wikip|le site|les sources|une source)|d.après (?:wikip|le site))',txt):pb.append('source citée dans le récit')
        if len(x['name'])>46 or x['name'].isupper():pb.append('titre ≤ 46 caractères, casse normale')
        nb=len(x['blurb'].get('b','').split())
        if not 40<=nb<=75:pb.append('blurb.b: %d mots'%nb)
        if not x['blurb'].get('h'):pb.append('blurb.h manquant')
        if not 60<=len(x['sub'])<=220:pb.append('sub: 60 à 220 caractères')
        print(i,'OK' if not pb else 'À CORRIGER',f,'|',w,'mots, médiane',med,'|' if pb else '',' ; '.join(pb))
    else:print(i,'À CORRIGER |',' ; '.join(pb))
    bad+=bool(pb)
sys.exit(1 if bad else 0)
