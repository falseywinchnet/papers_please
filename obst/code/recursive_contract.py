#!/usr/bin/env python3
"""Exact recursive contraction with a certified-cost shortcut and DP fallback."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import random
import sys
import time

from block_contract import candidate_blocks
from contract import reduce_instance
from research import cost,cubic,knuth
from sparse import FAMILIES,SparseSolver,weights


def solve(p,q):
    stats=Counter()

    def expand(t,keys,leaves,lo=0):
        if t is None:
            return leaves[lo]
        r,a,b=t
        stats['reconstructed_nodes']+=1
        return keys[r],expand(a,keys,leaves,lo),expand(b,keys,leaves,r+1)

    def visit(p,q,depth):
        n=len(p)
        stats['calls']+=1
        stats['processed_keys']+=n
        stats['max_recursion_depth']=max(stats['max_recursion_depth'],depth)
        cp,cq,ids,leaves,offset,counts=reduce_instance(p,q)
        stats['single_predicate_checks']+=counts['predicate_checks']
        stats['single_queue_pops']+=counts['queue_pops']
        stats['single_contractions']+=counts['contractions']
        m=len(cp)
        if not m:
            return offset,leaves[0]
        helper=SparseSolver(cp,cq)
        lower=helper.lower(0,m)
        upper,tree=helper.upper(0,m)
        for k,v in helper.stats.items():
            stats[k]+=v
        helper.lower.cache_clear()
        helper.upper.cache_clear()
        if lower==upper:
            stats['certified_components']+=1
            return offset+upper,expand(tree,ids,leaves)

        blocks=[]
        if m>8:
            blocks,scan=candidate_blocks(cp,cq)
            stats['cartesian_nodes']+=m
            stats['block_predicate_checks']+=scan['predicate_checks']
            stats['selection_events']+=scan['selection_events']
        sizes=[j-i for i,j in blocks]
        remaining=m-sum(sizes)
        score=remaining*(remaining+1)//2+sum(k*(k+1)//2 for k in sizes)
        # This fixed fractional decrease gives logarithmic recursive depth.
        if not blocks or 4*score>3*m*(m+1)//2:
            value,tree,scans=knuth(cp,cq)
            stats['dp_states']+=m*(m+1)//2
            stats['root_candidates']+=scans
            stats['dp_components']+=1
            return offset+value,expand(tree,ids,leaves)

        stats['decompositions']+=1
        stats['selected_blocks']+=len(blocks)
        alive=[True]*m
        gap=list(cq)
        payload=[None]*(m+1)
        block_cost=0
        for i,j in blocks:
            value,t=visit(cp[i:j],cq[i:j+1],depth+1)
            block_cost+=value
            payload[j]=expand(t,list(range(i,j)),[None]*(j-i+1))
            gap[j]=sum(cp[i:j])+sum(cq[i:j+1])
            alive[i:j]=[False]*(j-i)
        core_ids=[k for k in range(m) if alive[k]]
        core_leaves=core_ids+[m]
        value,t=visit([cp[k] for k in core_ids],[gap[k] for k in core_leaves],depth+1)
        tree=expand(t,core_ids,[payload[k] for k in core_leaves])
        return offset+block_cost+value,expand(tree,ids,leaves)

    value,t=visit(p,q,0)
    return value,t,dict(stats)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-n',type=int,default=1024)
    args=parser.parse_args()
    sys.setrecursionlimit(20000)
    rng=random.Random(0xAEC0)
    verified=0
    for n in range(1,31):
        for trial in range(100):
            p=[1<<rng.randrange(20) if trial%2 else rng.randrange(100) for _ in range(n)]
            q=[1<<rng.randrange(20) if trial%3 else rng.randrange(5) for _ in range(n+1)]
            value,t,_=solve(p,q)
            ref,_=cubic(p,q)
            assert value==ref==cost(t,p,q),(p,q,value,ref)
            verified+=1
    nested_rng=random.Random(0xAE57)
    observed_depth=0
    for _ in range(20):
        p=[]
        # With 32 groups the global state score favors contracting whole
        # groups; their interior reductions must occur in recursive calls.
        for group in range(32):
            if group: p.append(10**7)
            p.extend([1]*5+[1000]+[1]*5)
        q=[nested_rng.randrange(1,6) for _ in range(len(p)+1)]
        value,t,counts=solve(p,q)
        ref,_,_=knuth(p,q)
        assert value==ref==cost(t,p,q)
        observed_depth=max(observed_depth,counts['max_recursion_depth'])
    assert observed_depth>=2,observed_depth
    rows=[]
    for n in (32,64,128,256,512,1024):
        if n>args.max_n: break
        inputs=[(f,*weights(n,f,rng)) for f in FAMILIES]
        p=[rng.randrange(1,4) for _ in range(n)]
        q=[rng.randrange(1,4) for _ in range(n+1)]
        for k in rng.sample(range(n),max(1,math.isqrt(n))): p[k]=1000000
        inputs.append(('heavy_separators',p,q))
        inputs.append(('hierarchical',
                       [100**((i+1 & -(i+1)).bit_length()-1) for i in range(n)],
                       [rng.randrange(1,4) for _ in range(n+1)]))
        for family,p,q in inputs:
            started=time.perf_counter()
            ref,_,scans=knuth(p,q)
            baseline_seconds=time.perf_counter()-started
            started=time.perf_counter()
            value,t,counts=solve(p,q)
            seconds=time.perf_counter()-started
            assert value==ref==cost(t,p,q),(n,family,value,ref)
            assert counts.get('dp_states',0)<=n*(n+1)//2
            row=dict(n=n,family=family,baseline_states=n*(n+1)//2,
                     baseline_candidates=scans,baseline_seconds=baseline_seconds,
                     seconds=seconds,**counts)
            rows.append(row)
            if n==args.max_n:
                print(family,counts.get('dp_states',0),round(seconds/baseline_seconds,3),flush=True)
    target=Path(__file__).resolve().parents[1]/'results/recursive_contraction.json'
    target.write_text(json.dumps(dict(random_verification=verified,
                                     nested_verification=20,
                                     verified_nested_depth=observed_depth,
                                     rows=rows),indent=2)+'\n')


if __name__=='__main__':
    main()
