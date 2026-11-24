#!/usr/bin/env python3
"""Affiche une histoire (texte actuel) : python3 tools/v2_show.py <id>"""
import json,sys,os
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
d=json.load(open(os.path.join(R,'data','content.json')))
i=sys.argv[1]
for v in d['D'].values():
    for x in v:
        if x['id']==i:
            L=d['LENS'].get(i,{})
            body=L.get('10') or x['body']
            print(json.dumps({'id':i,'name':x['name'],'sub':x['sub'],'dates':x.get('dates'),'country':x.get('country'),'job':x.get('job'),'body':body},ensure_ascii=False,indent=1));sys.exit()
print('introuvable')
