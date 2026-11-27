import json,sys
d=json.load(open('data/content.json'));D=d['D'];B=d['BLURB']
idx={}
for s,v in D.items():
    if isinstance(v,list):
        for e in v:
            if isinstance(e,dict) and 'id' in e: idx[e['id']]=e
done=set()
import glob
for f in glob.glob('data/blurb_new/*.json'): done|=set(json.load(open(f)).keys())
ids=[k for k in B if k not in done]
n=int(sys.argv[1]); 
for i in ids[:n]:
    e=idx.get(i,{});body=e.get('body','');t=' '.join(body) if isinstance(body,list) else str(body)
    print('##',i,'|',e.get('name',''),'|',e.get('dates',''));print('B:',B[i]['b']);print('T:',t[:300].replace('#',' / '));print()
print(len(ids),'restants')
