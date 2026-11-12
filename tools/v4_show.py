#!/usr/bin/env python3
"""Affiche la matière existante d'une histoire : python3 tools/v4_show.py <id>"""
import json,os,sys
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
d=json.load(open(os.path.join(R,'data','content.json')))
for i in sys.argv[1:]:
    s=next((x for v in d['D'].values() for x in v if x['id']==i),None)
    if not s:print(i,'introuvable');continue
    print('=====',i,'|',s['name'],'|',s.get('dates',''),'|',s.get('country',''),'|',s.get('job',''))
    print('SRC:',s.get('src',''))
    print('\n'.join(t for t in s['body']))
