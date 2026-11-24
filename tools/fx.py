"""Correction de faits : python3 tools/fx.py PID 'ancien' 'nouveau'
Remplace une occurrence unique dans content.json (texte d'origine) ou dans tools/lives_*.py (ajouts)."""
import json,sys,glob
pid,old,new=sys.argv[1:4]
p='data/content.json'
c=json.load(open(p,encoding='utf-8'))
port=[x for x in c['BOOK']['portraits'] if x['id']==pid][0]
n=sum(l.count(old) for l in port['body'])
if n==1:
    port['body']=[l.replace(old,new) for l in port['body']]
    open(p,'w',encoding='utf-8').write(json.dumps(c,ensure_ascii=False))
    print('OK content.json',pid); sys.exit()
if n>1: sys.exit('ERREUR : %d occurrences dans content.json'%n)
for f in sorted(glob.glob('tools/lives_add_*.py'))+sorted(glob.glob('tools/lives_ins_*.py'))+['tools/lives_build.py']:
    s=open(f,encoding='utf-8').read()
    if s.count(old)==1:
        open(f,'w',encoding='utf-8').write(s.replace(old,new)); print('OK',f); sys.exit()
    if s.count(old)>1: sys.exit('ERREUR : %d occurrences dans %s'%(s.count(old),f))
sys.exit('INTROUVABLE : '+old[:50])
