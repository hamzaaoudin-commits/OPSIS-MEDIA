#!/usr/bin/env python3
"""Intègre les récits au format v3 (data/opsis_v3/*.json) dans data/content.json."""
import json,glob,os,subprocess,sys
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
d=json.load(open(os.path.join(R,'data','content.json')))
idx={x['id']:x for v in d['D'].values() for x in v}
d.setdefault('FMT',{});d.setdefault('FIN',{})
ok=skip=0
for f in sorted(glob.glob(os.path.join(R,'data','opsis_v3','*.json'))):
    i=os.path.basename(f)[:-5]
    if i.startswith('_') or i not in idx:continue
    if subprocess.run([sys.executable,os.path.join(R,'tools','v3_check.py'),i],capture_output=True).returncode:skip+=1;print('ignorée',i);continue
    x=json.load(open(f));s=idx[i]
    s['name']=x['name'];s['sub']=x['sub'];s['body']=x['body']
    if x.get('src'):s['src']=' || '.join(x['src']) if isinstance(x['src'],list) else x['src']
    d['BLURB'][i]=x['blurb'];d['LENS'].pop(i,None);d['FMT'][i]=x['fmt']
    d['FIN'][i]={'l':x['learned'],'r':x['retain'],'n':x['note']};ok+=1
json.dump(d,open(os.path.join(R,'data','content.json'),'w'),ensure_ascii=False,separators=(',',':'))
print(ok,'intégrées,',skip,'ignorées')
