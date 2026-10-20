#!/usr/bin/env python3
"""Exact mixed-weight word/block identities and independent constructor checks."""
from collections import Counter
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random

from complete import parameters,best_complete
from check_ramp_complete import enumerate_class
from research import cost,cubic,knuth


def feasible_words(L,t):
    for w in itertools.product((0,1),repeat=L):
        if any(not a and not b for a,b in zip((t,)+w,w)):continue
        yield w


def independent_limits(L,t,u):
    amounts=[sum(w) for w in feasible_words(L,t) if w[-1]==u]
    return set(amounts)


def check_identities(checks,rng):
    for L in range(1,11):
        for t,u in itertools.product((0,1),repeat=2):
            lo=((L+1)//2 if t else L//2+1) if u else (L//2 if t else (L+1)//2)
            hi=L-(not u)
            assert independent_limits(L,t,u)==set(range(lo,hi+1))
            checks['boundary_count_intervals']+=1
    for n in range(1,15):
        h,S,s=parameters(n)
        for trial in range(5):
            p=[rng.randrange(21) for _ in range(n)]
            q=[rng.randrange(21) for _ in range(n+1)]
            for selected,t in enumerate_class(n):
                # Build the key word from independent slot expansion choices.
                word=[];chosen=set(selected)
                for g in range(S):
                    if g in chosen:word.append(0)
                    if g<S-1:word.append(1)
                base=(h+1)*sum(p)+h*sum(q)+sum(q[i]+q[i+1] for i in range(n))
                reward=0;r=0
                for i,x in enumerate(word):
                    if x:
                        r+=1;reward+=(1+(r&-r).bit_length()-1)*p[i]+q[i]+q[i+1]
                assert r==S-1 and base-reward==cost(t,p,q)
                checks['independent_word_costs']+=1
    for L in range(1,9):
        for t in (0,1):
            for w in feasible_words(L,t):
                a,c,r0=(rng.randrange(30),rng.randrange(30),rng.randrange(20))
                reward=0;r=r0
                for x in w:
                    if x:r+=1;reward+=(1+(r&-r).bit_length()-1)*a+c
                U=lambda j:(2*a+c)*j-a*bin(j).count('1')
                assert reward==U(r)-U(r0)
                checks['block_path_independence']+=1


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--identities-only',action='store_true')
    ap.add_argument('--max-n',type=int,default=768);ap.add_argument('--scale-n',type=int,default=98304)
    args=ap.parse_args();rng=random.Random(731086);checks=Counter();rows=[]
    check_identities(checks,rng)
    print('identities',dict(checks),flush=True)
    if args.identities_only:return
    from run_complete import (limits,transfer,optimize_shape,solve,portfolio_solve,signature_runs,
                              sorted_weights,block_word,make_fixture)
    for L in range(1,11):
        for t,u in itertools.product((0,1),repeat=2):
            lo,hi=limits(L,t,u)
            for m in range(lo,hi+1):
                w=tuple(block_word(L,m,t,u))
                assert len(w)==L and sum(w)==m and w[-1]==u
                assert all(a or b for a,b in zip((t,)+w,w))
                checks['block_reconstructions']+=1
    for trial in range(500):
        rlo=rng.randrange(8);width=rng.randrange(1,18)
        bits=[bin(j).count('1') for j in range(rlo+width)]
        L=rng.randrange(1,10);a=rng.randrange(20);c=rng.randrange(20)
        U=[(2*a+c)*r-a*bits[r] for r in range(rlo,rlo+width)]
        src=[[None if rng.randrange(4)==0 else rng.randrange(-100,101) for _ in range(width)] for _ in (0,1)]
        for backward in (False,True):
            observed=transfer(src,L,U,backward,Counter());expected=[[None]*width for _ in (0,1)]
            for j in range(width):
                for t in (0,1):
                    for w in feasible_words(L,t):
                        k=j+sum(w);u=w[-1]
                        if k>=width:continue
                        target=j if backward else k;state=t if backward else u
                        val=src[u][k] if backward else src[t][j]
                        if val is None:continue
                        v=val+U[k]-U[j]
                        old=expected[state][target]
                        if old is None or v>old:expected[state][target]=v
            assert observed==expected,(trial,backward,L,src,observed,expected)
            checks['enumerated_transfer_vectors']+=1
    def check(p,q,shape=True):
        n=len(p);value,t,stats=solve(p,q);expected,_,scans=knuth(p,q)
        assert value==expected==cost(t,p,q),(p,q,value,expected)
        checks['full_solves']+=1;checks['certified']+=stats['certified']
        checks['preflight_rejections']+=stats['preflight_rejected']
        checks['gate_rejections']+=stats['global_gate_rejected']
        pv,pt,pc=portfolio_solve(p,q)
        assert pv==value==cost(pt,p,q)
        checks['portfolio_solves']+=1;checks['portfolio_run_routes']+=pc['route_to_runs']
        checks['portfolio_affine_routes']+=pc['route_to_affine']
        if n<=12:assert value==cubic(p,q)[0];checks['cubic_checks']+=1
        blocks=signature_runs(p,q,Counter());ps,qs=sorted_weights(p,q,blocks,Counter())
        assert ps==sorted(p,reverse=True) and qs==sorted(q,reverse=True)
        checks['compressed_weight_sort_checks']+=1
        if shape:
            v,tt,st=optimize_shape(p,q,blocks=blocks)
            assert v==best_complete(p,q)[0]==cost(tt,p,q)
            checks['unrestricted_shape_controls']+=1
            if n<=10:
                assert v==min(cost(tree,p,q) for _,tree in enumerate_class(n))
                checks['independent_shape_enumerations']+=1
        return dict(n=n,value=value,counts=dict(stats),knuth_candidates=scans)
    for n in range(5):
        for v in itertools.product((0,1),repeat=2*n+1):check(list(v[:n]),list(v[n:]))
    for n in range(1,41):
        for trial in range(8):
            if trial<4:
                p=[rng.randrange(50) for _ in range(n)];q=[rng.randrange(50) for _ in range(n+1)]
                if trial==1:p=[1<<v for v in p];q=[1<<v for v in q]
                if trial==2:p=[10**25+v for v in p];q=[10**25+v for v in q]
                if trial==3:p.reverse();q.reverse()
            else:p,q=make_fixture(n,max(1,n//(trial-2)),rng,baseline=trial%2==0)
            check(p,q)
        print('fuzz',n,flush=True)
    for n in (48,96,192,384,768,1536):
        if n>args.max_n:continue
        for family,k,baseline in [('four_blocks',4,True),('many_blocks',max(2,int(n**.5)),True),
                                  ('no_baseline',4,False),('irregular',n,True)]:
            p,q=make_fixture(n,k,rng,baseline=baseline)
            row=check(p,q);row['family']=family;rows.append(row)
            print('fixture',n,family,row['counts'].get('certified',0),flush=True)
    n=min(384,args.max_n);B=4*(n+1)**3
    p=[B+i+(-1)**i for i in range(n)];q=[B+i for i in range(n+1)]
    row=check(p,q);row['family']='affine_route';rows.append(row)
    scaling=[]
    for n in (1536,6144,24576,98304):
        if n>args.scale_n:continue
        for k in (4,16):
            p,q=make_fixture(n,k,rng,baseline=True)
            value,t,stats=solve(p,q)
            assert stats['certified'] and value==cost(t,p,q)
            pv,pt,pc=portfolio_solve(p,q)
            assert pc['route_to_runs'] and pv==value==cost(pt,p,q)
            checks['portfolio_scaling_controls']+=1
            if n==1536:
                assert value==knuth(p,q)[0]==best_complete(p,q)[0]
                checks['large_dense_controls']+=1
            scaling.append(dict(n=n,requested_blocks=k,value=value,counts=dict(stats)))
            print('scale',n,k,stats['signature_runs'],stats['transfer_window_queries'],flush=True)
    names=['run_complete.py','check_run_complete.py','complete.py','research.py','sparse.py',
           'check_ramp_complete.py','ramp_complete.py','ordered_complete.py','ruler_barrier.py']
    result=dict(seed=731086,checks=dict(checks),rows=rows,constructor_scaling=scaling,
                source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in names})
    out=Path(__file__).resolve().parents[1]/'results'/'run_complete.json'
    out.write_text(json.dumps(result,indent=2)+'\n');print(dict(checks),flush=True)


if __name__=='__main__':main()
