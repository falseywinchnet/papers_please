#!/usr/bin/env python3
"""Independent exact audit, then fixed-mass core maximization. No timings."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
import subprocess
from penalty_layers import solve

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('binary')
    ap.add_argument('--sizes',default='16,31,32,63,64,127,128,255,256,511,512,1024')
    ap.add_argument('--steps',type=int,default=1200)
    ap.add_argument('--modes',default='mixed,keys,uniform,mixed')
    ap.add_argument('--output',default='core_size_search.json')
    args=ap.parse_args(); root=Path(__file__).resolve().parents[1]
    rng=random.Random(190025);checks=Counter();rows=[]
    proc=subprocess.Popen([args.binary],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
    def audit(p,q,deep=False):
        n=len(p);proc.stdin.write(' '.join(map(str,[n,*p,*q]))+'\n');proc.stdin.flush()
        got=json.loads(proc.stdout.readline());expected=solve(p,q,checks,deep=deep)
        assert got['cost']==expected['cost']
        assert got['cores'][1:]==[n+x['nonzero_core'] for x in expected['layers']]
        checks['independent_cpp_layer_vectors']+=1
    for n in range(1,4):
        for w in itertools.product(range(2),repeat=2*n+1):audit(list(w[:n]),list(w[n:]),True)
    for n in (4,5,7,8,15,16,31,32):
        for _ in range(8):
            w=[0]*(2*n+1)
            for t in range(n):w[rng.randrange(len(w))]+=1
            audit(w[:n],w[n:],n<=7)
    files=['core_size_search.cpp','core_size_search.py','penalty_layers.py','research.py']
    report=dict(seed=190025,objective='max_h delta(E_h) / (n sqrt(W ceil(log2(n+1))))',
      mass_constraint='W=n exactly; nonnegative integer keys and gaps; keys mode restricts gaps to zero',
      scope='Dense adversarial search, not a fast OBST solver or a tightness proof. All layers including finite-completion diagonal are counted.',
      source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files},checks=checks,rows=rows)
    output=root/'results'/args.output
    output.write_text(json.dumps(report,indent=2)+'\n')
    print('independent layer audit passed',checks['independent_cpp_layer_vectors'],flush=True)
    for n in map(int,args.sizes.split(',')):
        for trial,mode in enumerate(args.modes.split(',')):
            seed=190025+n*13+trial;steps=max(80,args.steps*min(128,n)//n)
            row=json.loads(subprocess.check_output([args.binary,str(n),str(steps),str(seed),mode],text=True))
            row.update(seed=seed,mode=mode,steps=steps)
            w=row['weights'];audit(w[:n],w[n:]) if n<=128 else None
            rows.append(row);output.write_text(json.dumps(report,indent=2)+'\n')
            print(n,mode,'core',row['maximum_completed_core'],'ratio',row['ratio'],flush=True)
    proc.stdin.close();assert proc.wait()==0
    output.write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
