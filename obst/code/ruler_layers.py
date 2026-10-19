#!/usr/bin/env python3
"""Exact dense diagnostic for saturated partial-tree layers.

This is not a subquadratic constructor. Independent subsequence and all-shape
oracles test the ruler-pattern identity; density differences audit a possible
representation. Counts include the dense work used to discover that structure.
"""
from collections import Counter
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random

from research import check_weights, cubic, knuth, label, shapes


def valuation(t):
    return (t & -t).bit_length()-1


def sequence_score(p, h, stats):
    """Maximum score of a length-(2**h-1) subsequence, independently of trees."""
    c=(1<<h)-1
    assert len(p)>=c
    dp=[0]+[None]*c
    for r,x in enumerate(p):
        for t in range(min(c,r+1),0,-1):
            if dp[t-1] is not None:
                z=dp[t-1]+valuation(t)*x
                if dp[t] is None or z>dp[t]:dp[t]=z
                stats['subsequence_transitions']+=1
    return dp[c]


def density_counts(a, min_distance=1):
    n=len(a)-1
    d={(i,j):a[i][j+1]+a[i+1][j]-a[i][j]-a[i+1][j+1]
       for i in range(n-1) for j in range(i+1,n)}
    assert all(x>=0 for x in d.values())
    eligible=[(i,j) for i,j in d if j-i>=min_distance]
    fourth=[d[i,j+1]+d[i+1,j]-d[i,j]-d[i+1,j+1]
            for i,j in eligible if (i+1,j) in d and (i+1,j+1) in d and (i,j+1) in d]
    row_changes=sum(d[i,j]!=d[i,j-1] for i,j in eligible
                    if (i,j-1) in d and j-1-i>=min_distance)
    return dict(cells=len(eligible),core=sum(d[k]>0 for k in eligible),
                row_changes=row_changes,fourth_cells=len(fourth),
                fourth_nonzero=sum(x!=0 for x in fourth))


def layers(p,q,limit,stats,deep=False,formula=False):
    check_weights(p,q);n=len(p);w=sum(p)+sum(q);M=(limit+1)*w+1
    prefix=[0]
    for x,y in zip(p,q[1:]):prefix.append(prefix[-1]+x+y)
    mass=lambda i,j:prefix[j]-prefix[i]+q[i]
    old=[[M*max(0,j-i) for j in range(n+1)] for i in range(n+1)]
    result=[]
    for h in range(1,limit+1):
        c=(1<<h)-1
        a=[[0]*(n+1) for _ in range(n+1)];rr=[[0]*(n+1) for _ in range(n+1)]
        for k in range(1,n+1):
            for i in range(n-k+1):
                j=i+k;lo=i if k==1 else rr[i][j-1];hi=j-1 if k==1 else rr[i+1][j]
                v,r=min((old[i][r]+old[r+1][j],r) for r in range(lo,hi+1))
                a[i][j]=mass(i,j)+v;rr[i][j]=r
                stats['dense_layer_states']+=1;stats['dense_layer_candidates']+=hi-lo+1
                if deep:
                    assert (v,r)==min((old[i][r]+old[r+1][j],r) for r in range(i,j))
                    stats['all_root_checks']+=1
                if formula and k>=c:
                    score=sequence_score(p[i:j],h,stats)
                    assert a[i][j]==M*(k-c)+h*mass(i,j)-score,(p,q,h,i,j)
                    stats['ruler_interval_checks']+=1
                    if h==2:
                        assert score==max(p[i+1:j-1]);stats['range_max_checks']+=1
        if deep:
            def trunc(t,i,j,budget):
                if i==j:return 0
                if not budget:return M*(j-i)
                r,l,z=t
                return mass(i,j)+trunc(l,i,r,budget-1)+trunc(z,r+1,j,budget-1)
            assert a[0][n]==min(trunc(label(s)[0],0,n,h) for s in shapes(n))
            stats['all_shape_checks']+=1
        result.append(dict(h=h,value=a[0][n],density=density_counts(a),
                           saturated_density=density_counts(a,c+1)))
        old=a
    stats['layer_solves']+=1
    return result


def full_table(p,q,stats,deep=False):
    n=len(p);prefix=[0]
    for x,y in zip(p,q[1:]):prefix.append(prefix[-1]+x+y)
    a=[[0]*(n+1) for _ in range(n+1)];rr=[[0]*(n+1) for _ in range(n+1)]
    for k in range(1,n+1):
        for i in range(n-k+1):
            j=i+k;lo=i if k==1 else rr[i][j-1];hi=j-1 if k==1 else rr[i+1][j]
            v,r=min((a[i][r]+a[r+1][j],r) for r in range(lo,hi+1))
            a[i][j]=v+prefix[j]-prefix[i]+q[i];rr[i][j]=r
            stats['full_dense_states']+=1;stats['full_dense_candidates']+=hi-lo+1
    if deep:
        assert a[0][n]==cubic(p,q)[0];stats['cubic_checks']+=1
    assert a[0][n]==knuth(p,q)[0];stats['knuth_checks']+=1
    return dict(cost=a[0][n],density=density_counts(a))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--max-n',type=int,default=512)
    args=parser.parse_args();rng=random.Random(157011);stats=Counter();rows=[]
    for n in range(1,5):
        for bits in itertools.product((0,1),repeat=2*n+1):
            p=list(bits[:n]);q=list(bits[n:])
            layers(p,q,min(3,n),stats,deep=True,formula=True)
        print('exhaustive',n,flush=True)
    for n in range(1,25):
        for trial in range(8):
            p=[rng.getrandbits(rng.choice((1,4,64))) for _ in range(n)]
            q=[rng.getrandbits(rng.choice((1,4,128))) for _ in range(n+1)]
            layers(p,q,min(4,n),stats,deep=n<=7,formula=True)
            full_table(p,q,stats,deep=n<=12)
        print('fuzz',n,flush=True)
    # A three-level greedy-root counterexample, all gaps strictly positive.
    p=[0,9,0,9,10,9,0,0];q=[1]*9
    values={}
    for chosen in itertools.combinations(range(8),7):
        r=chosen[3];score=sum(valuation(t)*p[s] for t,s in enumerate(chosen,1))
        values[r]=max(values.get(r,-1),score)
    assert values=={3:36,4:29}
    layers(p,q,3,stats,deep=False,formula=True)
    greedy=dict(p=p,q=q,scores_by_root=values,selected_root=3,largest_eligible_key=4)
    n=16
    while n<=args.max_n:
        fixtures=[
            ('uniform',[1]*n,[1]*(n+1)),
            ('near_uniform',[2**80+rng.randrange(3) for _ in range(n)],
             [2**80+rng.randrange(3) for _ in range(n+1)]),
            ('random_64',[1+rng.getrandbits(64) for _ in range(n)],
             [1+rng.getrandbits(64) for _ in range(n+1)]),
            ('small_random',[rng.randrange(16) for _ in range(n)],
             [rng.randrange(16) for _ in range(n+1)]),
            ('linear',list(range(1,n+1)),list(range(1,n+2))),
            ('geometric',[1<<i for i in range(n)],[1<<i for i in range(n+1)]),
            ('folded_geometric',[1<<min(i,n-1-i) for i in range(n)],
             [1<<min(i,n-i) for i in range(n+1)]),
            ('log_uniform',[1<<rng.randrange(n) for _ in range(n)],
             [1<<rng.randrange(n) for _ in range(n+1)]),
        ]
        for name,p,q in fixtures:
            row=dict(n=n,family=name,full=full_table(p,q,stats),
                     layers=layers(p,q,4,stats,formula=n<=32))
            rows.append(row)
            print(name,n,'full',row['full']['density'],
                  'layer cores',[z['saturated_density']['core'] for z in row['layers']],flush=True)
        n*=2
    root=Path(__file__).resolve().parents[1]
    result=dict(seed=157011,max_n=args.max_n,checks=dict(stats),rows=rows,
                greedy_counterexample=greedy,
                implementation='dense diagnostic; no subquadratic constructor or timings',
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest()
                               for f in ('ruler_layers.py','research.py')})
    (root/'results'/'ruler_layers.json').write_text(json.dumps(result,indent=2)+'\n')
    print(dict(stats),flush=True)


if __name__=='__main__':main()
