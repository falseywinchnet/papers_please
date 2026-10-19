#!/usr/bin/env python3
"""Fixed-mass binary search distinguishes weight variation from positional effects."""
from collections import Counter
from pathlib import Path
import argparse,hashlib,json,random,subprocess
from penalty_layers import solve


def main():
    ap=argparse.ArgumentParser();ap.add_argument('binary');ap.add_argument('--steps',type=int,default=2000)
    ap.add_argument('--sizes',default='16,32,64,128,256,512,1024');args=ap.parse_args()
    root=Path(__file__).resolve().parents[1];checks=Counter();rng=random.Random(29019);rows=[]
    proc=subprocess.Popen([args.binary],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
    def audit(w):
        n=(len(w)-1)//2
        proc.stdin.write(' '.join(map(str,[n,*w]))+'\n');proc.stdin.flush();a=json.loads(proc.stdout.readline())
        b=solve(w[:n],w[n:],checks,deep=n<=5)
        assert a['cost']==b['cost'] and a['cores'][1:]==[n+x['nonzero_core'] for x in b['layers']]
        checks['independent_vectors']+=1
    for n in (2,3,4,5,8,15,16,31,32,63,64):
        for mode in ('mixed','keys','gaps'):
            slots=list(range(2*n+1)) if mode=='mixed' else list(range(n)) if mode=='keys' else list(range(n,2*n+1))
            rng.shuffle(slots);w=[0]*(2*n+1)
            for i in slots[:len(slots)//2]:w[i]=1
            audit(w)
    files=['binary_core_search.cpp','binary_core_search.py','core_size_search.cpp','penalty_layers.py','research.py']
    report=dict(scope='Diagnostic only. Binary weights, fixed mass within each search; no asymptotic bound inferred.',
                objective='Maximum completed core over all layers, including the completion diagonal',checks=checks,rows=rows,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    target=root/'results'/'binary_core_search.json'
    for n in map(int,args.sizes.split(',')):
        for mode in ('mixed','keys','gaps'):
            for start in ('random','alternating','center','prefix'):
                seed=29019+100*n+len(rows);steps=max(100,args.steps*min(128,n)//n)
                row=json.loads(subprocess.check_output([args.binary,str(n),str(steps),str(seed),mode,start],text=True))
                row.update(mode=mode,start=start,seed=seed,steps=steps)
                w=row['weights'];assert all(v in (0,1) for v in w)
                assert sum(w)==(n if mode=='mixed' else n//2 if mode=='keys' else (n+1)//2)
                if n<=128:audit(w)
                row['core_per_n']=row['maximum_completed_core']/n
                row['core_per_n_log2']=row['maximum_completed_core']/(n*n.bit_length())
                rows.append(row);target.write_text(json.dumps(report,indent=2)+'\n')
                print(n,mode,start,'core',row['maximum_completed_core'],'per_n',row['core_per_n'],flush=True)
    proc.stdin.close();assert proc.wait()==0
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(dict(checks),flush=True)
if __name__=='__main__':main()
