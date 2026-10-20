#!/usr/bin/env python3
"""Probe explicit fixed-mass patterns, retaining every layer (no fit claims)."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import random
import subprocess
import sys
from penalty_layers import solve

def patterns(n):
    rng=random.Random(251019+n)
    for name in ('cluster_ramp','cluster_random','spaced_ramp','single_key',
                 'single_gap','binary_blocks','ruler_mass','random_units'):
        w=[0]*(2*n+1)
        if name in ('cluster_ramp','cluster_random','spaced_ramp'):
            k=math.isqrt(n);left=n//2-k//2
            for t in range(n):
                if name=='cluster_random':pos=left+rng.randrange(k)
                else:
                    # Sample the same integer triangular profile by rank.
                    rank=t%(k*(k+1)//2);j=0
                    while rank>=j+1:rank-=j+1;j+=1
                    pos=left+j if name=='cluster_ramp' else (j*n//k+n//(2*k))
                w[min(n-1,pos)]+=1
        elif name=='single_key':w[n//2]=n
        elif name=='single_gap':w[n+n//2]=n
        elif name=='binary_blocks':
            slots=[i for i in range(n) if (i//max(1,math.isqrt(n)))%2==0]
            for t in range(n):w[slots[t%len(slots)]]+=1
        elif name=='ruler_mass':
            slots=[]
            for i in range(n):slots.extend([i]*((i+1 & -(i+1)).bit_length()))
            for t in range(n):w[slots[t*len(slots)//n]]+=1
        else:
            for _ in range(n):w[rng.randrange(2*n+1)]+=1
        assert sum(w)==n
        yield name,w

def main():
    root=Path(__file__).resolve().parents[1];checks=Counter();rows=[]
    proc=subprocess.Popen([sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
    for n in (16,31,32,63,64,127,128,255,256,511,512,1023,1024,2048,4096):
        for name,w in patterns(n):
            proc.stdin.write(' '.join(map(str,[n,*w]))+'\n');proc.stdin.flush()
            row=json.loads(proc.stdout.readline());row['family']=name
            if n<=128:
                ref=solve(w[:n],w[n:],checks)
                assert row['cores'][1:]==[n+x['nonzero_core'] for x in ref['layers']]
                assert row['cost']==ref['cost']
            rows.append(row)
            print(n,name,row['maximum_completed_core'],row['ratio'],flush=True)
    proc.stdin.close();assert proc.wait()==0
    files=['core_size_patterns.py','core_size_search.cpp','penalty_layers.py','research.py']
    result=dict(scope='Explicit-pattern dense diagnostic; W=n exactly; no asymptotic fitting or tightness claim',
                checks=checks,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results'/'core_size_patterns.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
