#!/usr/bin/env python3
"""Exchange-certified minimum-IPL shapes, followed by the existing global gate.

The local condition proves only optimality within the minimum-IPL shape class.
The residual Huffman gate separately certifies full mixed-weight optimality.
Failure delegates to Knuth. A wide last level does not require a shape DP.
"""
from collections import Counter
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

from complete import parameters, minimum_ipl, residual_huffman, best_complete
from research import check_weights, cost, cubic, knuth, label, shapes
from ruler_barrier import construct
from sparse import Counted


def exchange_condition(p,q,stats):
    n=len(p);h,slots,s=parameters(n)
    if not s:return True
    for i in range(n-1):
        d=p[i]-p[i+1]
        stats['exchange_checks']+=1
        if max(d,h*d)>q[i+2]-q[i]:return False
    return True


def shape_candidate(p,q,stats):
    n=len(p)
    if exchange_condition(p,q,stats):
        t=construct(0,n,stats);stats['left_shape']+=1
    elif exchange_condition(p[::-1],q[::-1],stats):
        t=construct(0,n,stats);stats['right_shape']+=1
        def reflect(t):
            if t is None:return None
            r,l,z=t;stats['reflection_nodes']+=1
            return n-1-r,reflect(z),reflect(l)
        t=reflect(t)
    else:
        stats['exchange_rejected']+=1
        return None,None
    stats['candidate_cost_nodes']+=n
    return cost(t,p,q),t


def sorted_desc(a,stats):
    increasing=True;decreasing=True
    for i in range(len(a)-1):
        increasing &= a[i]<=a[i+1];decreasing &= a[i]>=a[i+1]
        stats['order_scan_pairs']+=1
    if increasing:stats['presorted_items']+=len(a);return a[::-1]
    if decreasing:stats['presorted_items']+=len(a);return list(a)
    stats['sorted_items']+=len(a)
    return [v.value for v in sorted((Counted(v,stats) for v in a),reverse=True)]


def attempt(p,q):
    check_weights(p,q);n=len(p);stats=Counter(input_keys=n)
    value,t=shape_candidate(p,q,stats)
    if value is None:return None,None,stats
    stats['candidate_cost']=value
    if not n:stats['certified']=1;return value,t,stats
    ps=sorted_desc(p,stats);qs=sorted_desc(q,stats);a=ps[-1];b=qs[-1]
    residual=residual_huffman(ps,qs,a,b,stats)
    lower=(a+b)*(minimum_ipl(n)+1)+(a+2*b)*n+residual
    stats['nonminimal_lower_bound']=lower;stats['residual_lower_bound']=residual
    if value<=lower:
        stats['certified']=1
        return value,t,stats
    stats['global_gate_rejected']=1
    return None,None,stats


def solve(p,q):
    value,t,stats=attempt(p,q)
    if value is None:
        value,t,scans=knuth(p,q)
        stats['fallback_dense_states']=len(p)*(len(p)+1)//2
        stats['fallback_root_candidates']=scans
        stats['fallback_constructed_keys']=len(p)
    return value,t,stats


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--max-n',type=int,default=768)
    args=parser.parse_args();sys.setrecursionlimit(10000)
    rng=random.Random(740177);checks=Counter();rows=[]
    def check(p,q,shape_oracle=False):
        n=len(p);value,t,stats=solve(p,q);ref,_,scans=knuth(p,q)
        assert value==ref==cost(t,p,q)
        if n<=12:assert value==cubic(p,q)[0];checks['cubic_checks']+=1
        checks['solves']+=1;checks['certified']+=stats['certified']
        checks['exchange_rejected']+=stats['exchange_rejected']
        checks['global_gate_rejected']+=stats['global_gate_rejected']
        if shape_oracle:
            candidate,tt=shape_candidate(p,q,Counter())
            if candidate is not None:
                assert candidate==best_complete(p,q)[0]
                checks['shape_dp_checks']+=1
                if n<=7:
                    values=[]
                    for sh in shapes(n):
                        tr=label(sh)[0]
                        if cost(tr,[1]*n,[0]*(n+1))-n==minimum_ipl(n):
                            values.append(cost(tr,p,q));checks['minimum_ipl_shapes']+=1
                    assert candidate==min(values);checks['shape_enumeration_checks']+=1
        return dict(n=n,value=value,counts=dict(stats),knuth_candidates=scans)
    for n in range(5):
        for v in itertools.product((0,1),repeat=2*n+1):
            check(list(v[:n]),list(v[n:]),shape_oracle=True)
    for n in range(1,41):
        for trial in range(12):
            p=[rng.randrange(32) for _ in range(n)];q=[rng.randrange(32) for _ in range(n+1)]
            if trial%3==0:p.sort();q.sort()
            if trial%3==1:p.sort(reverse=True);q.sort(reverse=True)
            if trial>=6:
                B=4*(n+1)**3;p=[B+x for x in p];q=[B+x for x in q]
            check(p,q,shape_oracle=True)
    for n in (64,96,128,192,256,384,512,768):
        if n>args.max_n:continue
        B=4*(n+1)**3;h=parameters(n)[0]
        pp=[B+(i%3) for i in range(n)]
        qq=[B+4*h*i+(i%2)*h for i in range(n+1)]
        fixtures=[
            ('positive_ramp',[B+i for i in range(n)],[B+i for i in range(n+1)]),
            ('positive_ramp_reverse',[B+i for i in reversed(range(n))],[B+i for i in reversed(range(n+1))]),
            ('jagged_keys',pp,qq),
            ('sorted_small',sorted(rng.randrange(64) for _ in range(n)),sorted(rng.randrange(64) for _ in range(n+1))),
            ('geometric',[1<<i for i in range(n)],[1<<i for i in range(n+1)]),
            ('random',[rng.randrange(64) for _ in range(n)],[rng.randrange(64) for _ in range(n+1)]),
        ]
        for name,p,q in fixtures:
            row=check(p,q);row['family']=name;rows.append(row)
            if name in ('positive_ramp','positive_ramp_reverse','jagged_keys'):assert row['counts'].get('certified')==1
            print(name,n,'certified',row['counts'].get('certified',0),'fallback states',row['counts'].get('fallback_dense_states',0),flush=True)
    scaling=[]
    for n in (1536,6144,24576,98304):
        B=4*(n+1)**3;p=[B+i for i in range(n)];q=[B+i for i in range(n+1)]
        value,t,stats=attempt(p,q)
        assert stats['certified']==1 and value==cost(t,p,q)
        from ruler_barrier import formula
        assert value==formula(0,n,B,Counter())
        scaling.append(dict(n=n,value=value,counts=dict(stats)))
        print('linear complete construction',n,dict(stats),flush=True)
    root=Path(__file__).resolve().parents[1]
    result=dict(seed=740177,checks=dict(checks),rows=rows,constructor_scaling=scaling,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest()
                               for f in ('ordered_complete.py','complete.py','sparse.py','research.py','ruler_barrier.py')})
    (root/'results'/'ordered_complete.json').write_text(json.dumps(result,indent=2)+'\n')
    print(dict(checks),flush=True)


if __name__=='__main__':main()
