#!/usr/bin/env python3
"""Harness-first root/nonroot coupling bounds for arbitrary mixed weights."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
from joint_merge_probe import enumerated
from research import cubic, knuth, cost


def capacity(values):
    return sum(w*(j+1).bit_length() for j,w in enumerate(sorted(values,reverse=True)))


def bound(p,q):
    n=len(p)
    assert n>=2
    r=max(range(n),key=lambda i:p[i])
    ranked=sorted(p,reverse=True)
    key=capacity(p)
    gap=cubic([0]*n,q)[0]
    nonroot=key+ranked[0]-ranked[1]+gap
    fixed=sum(p)+sum(q)+capacity(p[:r])+capacity(p[r+1:])
    fixed+=cubic([0]*r,q[:r+1])[0]+cubic([0]*(n-r-1),q[r+1:])[0]
    return min(nonroot,fixed),dict(r=r,key=key,gap=gap,nonroot=nonroot,fixed=fixed)


def main():
    rng=random.Random(317218);checks=Counter();examples={}
    fixture_p=[0,0,1,0];fixture_q=[2,3,2,2,2]
    v,m=bound(fixture_p,fixture_q)
    assert v==28==cubic(fixture_p,fixture_q)[0]
    for n in range(2,9):
        trees=enumerated(n)
        for trial in range(120):
            kind=trial%4
            if kind==0:p=[rng.randrange(20) for _ in range(n)];q=[rng.randrange(20) for _ in range(n+1)]
            elif kind==1:p=[100+rng.randrange(3) for _ in range(n)];q=[100+rng.randrange(3) for _ in range(n+1)]
            elif kind==2:p=[1<<rng.randrange(12) for _ in range(n)];q=[1<<rng.randrange(12) for _ in range(n+1)]
            else:p=[rng.randrange(2) for _ in range(n)];q=[rng.randrange(2) for _ in range(n+1)]
            v,m=bound(p,q);expected=cubic(p,q)[0]
            assert m['key']+m['gap']<=v<=expected==knuth(p,q)[0]
            rootmin=nonrootmin=None
            for tree,pd,qd in trees:
                actual=sum(x*d for x,d in zip(p,pd))+sum(x*d for x,d in zip(q,qd))
                which='fixed' if tree[0]==m['r'] else 'nonroot'
                assert m[which]<=actual
                checks['literal_conditioned_inequalities']+=1
                if which=='fixed':rootmin=actual if rootmin is None else min(rootmin,actual)
                else:nonrootmin=actual if nonrootmin is None else min(nonrootmin,actual)
            assert min(rootmin,nonrootmin)==expected
            checks['cases']+=1
            checks['strict_improvements']+=int(v>m['key']+m['gap'])
            checks['exact_bounds']+=int(v==expected)
            if v>m['key']+m['gap']:
                examples.setdefault('improved',dict(p=p,q=q,optimum=expected,lower=v,metadata=m))
        print(n,dict(checks),flush=True)
    result=dict(seed=317218,checks=dict(checks),fixture=dict(p=fixture_p,q=fixture_q,lower=28),examples=examples,
      source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest()
                    for f in ('root_partition_probe.py','joint_merge_probe.py','research.py','threshold_probe.py')})
    (Path(__file__).resolve().parents[1]/'results'/'root_partition_probe.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
