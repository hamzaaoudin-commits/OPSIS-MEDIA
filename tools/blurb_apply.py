import json,glob
p='data/content.json';d=json.load(open(p,encoding='utf-8'))
n=0
for f in sorted(glob.glob('data/blurb_new/*.json')):
    for k,v in json.load(open(f,encoding='utf-8')).items():
        assert k in d['BLURB'],k
        d['BLURB'][k]={'b':v['b'],'h':v['h']};n+=1
json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print(n,'appliqués')
