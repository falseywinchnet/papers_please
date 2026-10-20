#!/usr/bin/env python3
"""Independent word/tree oracles precede the parity-interval constructor."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

from complete import parameters,best_complete
from check_ramp_complete import enumerate_class
from profile_interval_probe import literal
from research import cost,cubic,knuth


def valid_word(pattern,word,m):
    assert len(pattern)==len(word) and sum(word)==m
    rank=0;last=1
    for high,x in zip(pattern,word):
        assert x or last
        assert not high or x
        if x:
            rank+=1
            assert high or rank%2
        last=x


def fixture(n,rng,baseline=True,alternating=False):
    if not n:return [],[0]
    h,S,s=parameters(n);chosen=set(rng.sample(range(S),s));pattern=[]
    for j in range(S):
        if j in chosen:pattern.append(0)
        if j<S-1:pattern.append(1 if (j+1)%2==0 else rng.randrange(2))
    if alternating:pattern=[i%2 for i in range(n)]
    M=max(1,n*n);B=4*(n+1)**2*M if baseline else 0
    p=[B+(M if x else 0) for x in pattern]
    q=[B+(M//3 if i%2 else M) for i in range(n+1)]
    return p,q


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--oracle-only',action='store_true')
    ap.add_argument('--max-n',type=int,default=768);ap.add_argument('--scale-n',type=int,default=393216)
    args=ap.parse_args();rng=random.Random(640291);checks=Counter();rows=[]
    sys.setrecursionlimit(10000)
    for n in range(1,10):
        h,S,s=parameters(n);m=S-1;trees=[t for _,t in enumerate_class(n)]
        for pattern in itertools.product((0,1),repeat=n):
            state=literal(pattern);attained=bool(((state[0]|state[1])>>m)&1)
            if not args.oracle_only:
                from profile_complete import recognize
                word,stats=recognize(pattern,m)
                assert (word is not None)==attained
                if word is not None:valid_word(pattern,word,m)
                checks['recognizer_checks']+=1
            if S//2-1<=sum(pattern)<=m:
                p=[17 if x else 2 for x in pattern];q=[3 if i%2 else 11 for i in range(n+1)]
                lower=sum(v*(i+1).bit_length() for i,v in enumerate(sorted(p,reverse=True)))+h*sum(q)+14*s
                actual=min(cost(t,p,q) for t in trees)
                assert (actual==lower)==attained
                checks['independent_profile_checks']+=1
    print('oracles',dict(checks),flush=True)
    if args.oracle_only:return
    from profile_complete import solve,attempt,portfolio_solve
    def check(p,q):
        n=len(p);v,t,st=solve(p,q);ev,_,ks=knuth(p,q)
        assert v==ev==cost(t,p,q),(p,q,v,ev)
        checks['full_solves']+=1;checks['certified']+=st['certified']
        checks['profile_certified']+=st['profile_certified'];checks['mixed_certified']+=st['mixed_certified']
        pv,pt,pc=portfolio_solve(p,q)
        assert pv==v==cost(pt,p,q)
        checks['portfolio_solves']+=1
        checks['portfolio_profile_routes']+=pc['route_to_profile']
        checks['portfolio_previous_routes']+=pc['route_to_previous']
        for key in ('unsupported_keys','unsupported_gaps','unsupported_high_count','profile_unattained','gate_rejected'):
            checks[key]+=st[key]
        if n<=12:assert v==cubic(p,q)[0];checks['cubic_controls']+=1
        cv,ct,cs=attempt(p,q,certify=False)
        if cv is not None:
            assert cv==best_complete(p,q)[0]==cost(ct,p,q)
            checks['shape_controls']+=1
        return dict(n=n,value=v,counts=dict(st),knuth_candidates=ks)
    for n in range(5):
        for values in itertools.product((0,1),repeat=2*n+1):check(list(values[:n]),list(values[n:]))
    for n in range(1,10):
        for pattern in itertools.product((0,1),repeat=n):
            for B in (0,4*(n+1)**2*19):
                p=[B+(19 if x else 0) for x in pattern];q=[B+(7 if i%2 else 3) for i in range(n+1)]
                check(p,q)
    row=check([100,1,100],[0,0,0,0]);row['family']='perfect_size_counterexample';rows.append(row)
    assert row['value']==303 and row['counts']['gate_rejected']
    for n in range(1,41):
        for family in range(10):
            if family<4:p,q=fixture(n,rng,baseline=family%2==0,alternating=family>=2)
            elif family==4:p=[rng.randrange(32) for _ in range(n)];q=[rng.randrange(32) for _ in range(n+1)]
            elif family==5:p=[1<<rng.randrange(20) for _ in range(n)];q=[1<<rng.randrange(20) for _ in range(n+1)]
            elif family==6:p=[10**50+rng.randrange(2) for _ in range(n)];q=[10**50+(i%2) for i in range(n+1)]
            elif family==7:p=[rng.choice((0,10**30)) for _ in range(n)];q=[i%2 for i in range(n+1)]
            elif family==8:p=[13]*n;q=[3 if i%2 else 7 for i in range(n+1)]
            else:p=[i%2 for i in range(n)];q=[rng.randrange(4) for _ in range(n+1)]
            check(p,q)
        print('fuzz',n,flush=True)
    for n in (48,96,192,384,768):
        if n>args.max_n:continue
        for family in ('witness_pattern','alternating','no_baseline','unattained','ordinary_random','affine'):
            p,q=fixture(n,rng,baseline=family!='no_baseline',alternating=family=='alternating')
            if family=='unattained':p=sorted(p)
            elif family=='ordinary_random':p=[rng.randrange(100) for _ in range(n)];q=[rng.randrange(100) for _ in range(n+1)]
            elif family=='affine':p=[4*(n+1)**3+i for i in range(n)];q=[4*(n+1)**3+i for i in range(n+1)]
            row=check(p,q);row['family']=family;rows.append(row)
            print('fixture',n,family,row['counts'].get('certified',0),flush=True)
    scales=[]
    for n in (1536,6144,24576,98304,393216):
        if n>args.scale_n:continue
        for alternating in (False,True):
            p,q=fixture(n,rng,baseline=False,alternating=alternating);v,t,st=solve(p,q)
            assert st['certified'] and cost(t,p,q)==v
            pv,pt,pc=portfolio_solve(p,q)
            assert pv==v==cost(pt,p,q) and pc['route_to_profile']
            checks['portfolio_scaling_controls']+=1
            if n==1536:
                assert v==knuth(p,q)[0]==best_complete(p,q)[0]
                checks['large_dense_controls']+=1
            k=1+sum((p[i],q[i]+q[i+1])!=(p[i-1],q[i-1]+q[i]) for i in range(1,n))
            scales.append(dict(n=n,alternating=alternating,signature_runs=k,value=v,counts=dict(st)))
            print('scale',n,alternating,k,st['interval_transitions'],flush=True)
    names=('profile_complete.py','check_profile_complete.py','profile_interval_probe.py','complete.py','research.py','check_ramp_complete.py','run_complete.py','ramp_complete.py','ordered_complete.py','ruler_barrier.py','sparse.py')
    root=Path(__file__).resolve().parents[1]
    result=dict(seed=640291,checks=dict(checks),rows=rows,scaling=scales,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in names})
    (root/'results'/'profile_complete.json').write_text(json.dumps(result,indent=2)+'\n')
    print(dict(checks),flush=True)


if __name__=='__main__':main()
