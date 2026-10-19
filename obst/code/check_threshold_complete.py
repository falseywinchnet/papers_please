#!/usr/bin/env python3
"""Independent checks specified before threshold_complete implementation."""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
from research import cost,cubic,knuth,label,shapes
from threshold_probe import depth_vectors,key_bound,threshold_bound


def family(h,s):
    """Reference tree and positive multilevel weights; no solver witness input."""
    S=1<<h
    assert 0<=s<=S//2
    expanded=set(range(1,2*s,2));q=[]
    n=S-1+s;Q=n*n+2
    def shape(lo,hi):
        if hi-lo==1:
            if lo in expanded:q.extend([1,1]);return (None,None)
            q.append(Q if lo%2==0 else 2+lo);return None
        mid=(lo+hi)//2
        return shape(lo,mid),shape(mid,hi)
    tree=label(shape(0,S))[0]
    pd,qd=depth_vectors(tree,n)
    p=[(h+2-d)*(n+1)+i for i,d in enumerate(pd)]
    return p,q,tree


def iterative_cost(tree,p,q):
    stack=[(tree,0,len(p),0)];value=0;seen=[]
    while stack:
        node,lo,hi,d=stack.pop()
        if node is None:
            assert lo==hi;value+=q[lo]*d;continue
        r,left,right=node
        assert lo<=r<hi;seen.append(r);value+=p[r]*(d+1)
        stack.extend([(left,lo,r,d+1),(right,r+1,hi,d+1)])
    assert sorted(seen)==list(range(len(p)))
    return value


def main():
    from threshold_complete import attempt,gap_bound,solve,portfolio_solve,ranked_external
    rng=random.Random(317205);checks=Counter();routes=Counter();scale=[]
    def check(p,q,exhaust=False):
        n=len(p);oracle,tree=cubic(p,q)
        assert oracle==knuth(p,q)[0]
        if exhaust:assert oracle==min(cost(label(s)[0],p,q) for s in shapes(n))
        lower=key_bound(p)+threshold_bound(q)
        stats=Counter();g=gap_bound(q,stats)
        assert g==threshold_bound(q) and lower<=oracle
        candidate,t,sc=attempt(p,q)
        routes.update({k:v for k,v in sc.items() if k in ('certified','key_profile_rejected','gap_profile_rejected','gap_linear_formula','gap_selection_formula')})
        if candidate is not None:assert candidate==oracle==lower==iterative_cost(t,p,q)
        for solver in (solve,portfolio_solve):
            v,t,st=solver(p,q)
            assert v==oracle==iterative_cost(t,p,q)
            checks[solver.__name__]+=1
        checks['cubic_controls']+=1;checks['literal_controls']+=int(exhaust)
    for n in range(4):
        for ws in itertools.product(range(3),repeat=2*n+1):check(list(ws[:n]),list(ws[n:]),True)
    for n in range(1,19):
        for trial in range(30):
            if trial%3==0:p=[100+rng.randrange(3) for _ in range(n)];q=[100+rng.randrange(3) for _ in range(n+1)]
            elif trial%3==1:p=[1<<rng.randrange(14) for _ in range(n)];q=[1<<rng.randrange(14) for _ in range(n+1)]
            else:p=[rng.randrange(100) for _ in range(n)];q=[rng.randrange(100) for _ in range(n+1)]
            check(p,q,n<=5)
    # Both formulas must match the independent layer sum, including every
    # small gap vector, zeros, ties, arbitrary extrema multiplicities.
    for N in range(1,8):
        for q in itertools.product(range(4),repeat=N):
            st=Counter();assert gap_bound(q,st)==threshold_bound(q)
            ordered=sorted(q,reverse=True)
            assert ranked_external(q,Counter())==sum((r.bit_length()+1)*v for r,v in enumerate(ordered) if r)
            checks['gap_formula_controls']+=1
    selection_scale=[]
    for N in (100,1000,10000,100000):
        for kind in ('random','ascending','descending','duplicates','organpipe'):
            if kind=='random':q=[rng.randrange(N*N) for _ in range(N)]
            elif kind=='ascending':q=list(range(N))
            elif kind=='descending':q=list(range(N,0,-1))
            elif kind=='duplicates':q=[rng.randrange(7) for _ in range(N)]
            else:q=[min(i,N-i) for i in range(N)]
            st=Counter();actual=ranked_external(q,st);ordered=sorted(q,reverse=True)
            assert actual==sum((r.bit_length()+1)*v for r,v in enumerate(ordered) if r)
            assert st['rank_level_items']<=3*N
            selection_scale.append(dict(N=N,kind=kind,stats=dict(st)))
    for h in range(1,6):
        for s in range((1<<h)//2+1):
            p,q,t=family(h,s);v,out,st=attempt(p,q)
            assert v==cost(t,p,q)==cost(out,p,q)==knuth(p,q)[0]
            assert st['gap_linear_formula']==1 and not st['bound_weight_comparisons']
            checks['positive_multilevel_controls']+=1
    # A valid lower bound need not be attained; ties can hide an attaining
    # shape from this deterministic Cartesian candidate.
    p=[2,1,1];q=[100,10,1,10]
    assert attempt(p,q)[0] is None
    assert key_bound(p)+threshold_bound(q)==158<cubic(p,q)[0]==160
    assert attempt([1]*3,[1]*4)[0] is None
    assert solve([1]*3,[1]*4)[0]==13
    v,t,st=portfolio_solve([1]*3,[1]*4)
    assert v==13 and st['previous_profile_certified']==1
    assert not st['candidate_key_visits']
    for h in (8,10,12,14,16,18):
        p,q,t=family(h,(1<<h)//4);n=len(p)
        v,out,st=attempt(p,q)
        assert v==iterative_cost(t,p,q)==iterative_cost(out,p,q)
        assert st['certified']==st['gap_linear_formula']==1
        assert st['constructed_keys']==n and not st['bound_weight_comparisons']
        assert st['cartesian_comparisons']<=2*n
        assert len(set(p))==n and len(set(q))==(1<<h)//4+2
        scale.append(dict(n=n,cost=v,key_levels=len(set(p)),gap_levels=len(set(q)),stats=dict(st)))
    # Linear-height, zero-padded exact tree: recursion must not be required.
    n=20000;p=[7]+[0]*(n-1);q=[11]+[0]*n
    v,t,st=attempt(p,q)
    assert v==18==iterative_cost(t,p,q)
    checks['deep_iterative_control']=1
    result=dict(seed=317205,checks=dict(checks),routes=dict(routes),scaling=scale,selection_scaling=selection_scale,
                source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in ('check_threshold_complete.py','threshold_complete.py','threshold_probe.py','research.py')})
    (Path(__file__).resolve().parents[1]/'results'/'threshold_complete.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
