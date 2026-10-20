#!/usr/bin/env python3
"""Independent exact controls, tie audit, and full mixed scaling family."""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
from shifted_alphabetic import alphabetic,attempt,solve,tree_cost
from research import cubic,knuth
from joint_merge_probe import candidate,enumerated
from threshold_probe import key_bound,threshold_bound,depth_vectors


def family(h):
    r=1<<h;n=7*r-1;p=[0]*n;q=[18,2,13,3,17,1,2]*r
    pd=[0]*n
    def build(first,count,depth):
        if count==1:
            i=7*first
            for j,d in enumerate((2,4,3,1,2,3)):pd[i+j]=depth+d-1
            return (i+3,(i,None,(i+2,(i+1,None,None),None)),(i+4,None,(i+5,None,None)))
        half=count//2;i=7*(first+half)-1;pd[i]=depth
        return i,build(first,half,depth+1),build(first+half,half,depth+1)
    tree=build(0,r,1)
    for i,d in enumerate(pd):p[i]=1 if d==h+4 else 1+(h+4-d)*(n+1)+i
    expected=sum(x*d for x,d in zip(p,pd))+sum(qi*(h+d) for qi,d in zip(q,(2,4,4,3,2,3,3)*r))
    return p,q,tree,expected


def main():
    rng=random.Random(317210);checks=Counter();scales=[]
    for n in range(8):
        for q in itertools.product(range(3),repeat=n+1):
            v,t,s=alphabetic(q);literal=candidate([0]*n,q)
            assert v==cubic([0]*n,q)[0]==tree_cost(t,[0]*n,q)
            assert depth_vectors(t,n)[1]==literal['qd']
            checks['alphabetic_exhaustive']+=1
    for n in (1,2,3,4,5,6,7,8,12,20,32,64):
        for trial in range(80):
            kind=trial%5
            if kind==0:p=[rng.randrange(30) for _ in range(n)];q=[rng.randrange(30) for _ in range(n+1)]
            elif kind==1:p=[100+rng.randrange(3) for _ in range(n)];q=[100+rng.randrange(3) for _ in range(n+1)]
            elif kind==2:p=[1<<rng.randrange(20) for _ in range(n)];q=[1<<rng.randrange(20) for _ in range(n+1)]
            elif kind==3:p=[rng.randrange(2) for _ in range(n)];q=[rng.randrange(2) for _ in range(n+1)]
            else:p=[rng.randrange(1,30)]*n;q=[rng.randrange(30) for _ in range(n+1)]
            v,t,s=solve(p,q);expected=cubic(p,q)[0]
            assert v==expected==knuth(p,q)[0]==tree_cost(t,p,q)
            checks['full_cubic_knuth_controls']+=1
            checks['certified' if s['certified'] else 'fallback']+=1
            if n<=7:
                assert expected==min(tree_cost(t,p,q) for t,_,_ in enumerated(n))
                checks['full_literal_controls']+=1
            assert s['global_lower_bound']<=expected
            if len(set(p))==1:assert s['certified'];checks['uniform_key_controls']+=1
    p=[7,1,5,8,6,4];q=[18,2,13,3,17,1,2]
    v,t,s=attempt(p,q);assert v==213 and s['certified'] and key_bound(p)+threshold_bound(q)==208
    for h in range(8):
        p,q,t,expected=family(h);v,tt,s=attempt(p,q)
        assert s['certified'] and v==expected==tree_cost(t,p,q)==tree_cost(tt,p,q)==knuth(p,q)[0]
        assert sum(x*d for x,d in zip(p,depth_vectors(t,len(p))[0]))-key_bound(p)==1<<h
        if h<=3:assert v==cubic(p,q)[0]
        checks['family_knuth_controls']+=1
    for h in (8,10,12,14,15):
        p,q,t,expected=family(h);v,tt,s=attempt(p,q)
        assert s['certified'] and v==expected==tree_cost(t,p,q)==tree_cost(tt,p,q)
        scales.append(dict(h=h,n=len(p),distinct_keys=len(set(p)),cost=v,stats=dict(s)))
        print('scale',h,len(p),v,flush=True)
    # Large skewed alphabetic input checks iterative reconstruction and traversal.
    q=[1<<i for i in range(1200)];v,t,s=alphabetic(q)
    assert v==tree_cost(t,[0]*1199,q);checks['long_chain_control']+=1
    result=dict(seed=317210,checks=dict(checks),scales=scales,
                source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in ('check_shifted_alphabetic.py','shifted_alphabetic.py','joint_merge_probe.py','threshold_probe.py','research.py')})
    (Path(__file__).resolve().parents[1]/'results'/'shifted_alphabetic.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks)),flush=True)


if __name__=='__main__':main()
