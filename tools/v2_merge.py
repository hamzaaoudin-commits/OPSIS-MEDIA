#!/usr/bin/env python3
"""Intègre les histoires réécrites (data/opsis_v2/*.json) dans data/content.json. Ne prend que celles qui passent le contrôle."""
import json,glob,os,subprocess,sys
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
d=json.load(open(os.path.join(R,'data','content.json')))
idx={x['id']:x for v in d['D'].values() for x in v}
d.setdefault('FMT',{})
ok=skip=0
for f in sorted(glob.glob(os.path.join(R,'data','opsis_v2','*.json'))):
    i=os.path.basename(f)[:-5]
    if i.startswith('_') or i not in idx:continue
    if subprocess.run([sys.executable,os.path.join(R,'tools','v2_check.py'),i],capture_output=True).returncode:skip+=1;print('ignorée',i);continue
    x=json.load(open(f));s=idx[i]
    s['name']=x['name'];s['sub']=x['sub'];s['body']=x['body']
    d['BLURB'][i]=x['blurb'];d['LENS'].pop(i,None);d['FMT'][i]=x['fmt'];ok+=1
json.dump(d,open(os.path.join(R,'data','content.json'),'w'),ensure_ascii=False,separators=(',',':'))
print(ok,'intégrées,',skip,'ignorées')
