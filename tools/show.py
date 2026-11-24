import json,sys
L=json.load(open('data/lives.json'))
for pid in sys.argv[1:]:
    print('#####',pid)
    for i,e in enumerate(L[pid]['eps'],1):
        print('--- ép.%d : %s'%(i,e['t']))
        for l in e['body']:
            if l!='*': print(l)
