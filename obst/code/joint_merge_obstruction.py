#!/usr/bin/env python3
"""Find and verify a positive, strict-choice compatible-merge obstruction."""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
from joint_merge_probe import candidate,oracle
from research import cubic,knuth,cost
from threshold_probe import key_bound,threshold_bound


def check(p,q):
    if min(p+q)<1 or len(set(p))!=len(p):return None
    actual=candidate(p,q)
    if not actual['valid'] or actual['charges']!=actual['value']:return None
    if any(x['pair_margin']==0 for x in actual['trace']):return None
    expected,witness=oracle(p,q)
    if expected>=actual['value']:return None
    return expected,witness,actual


def main():
    rng=random.Random(317207);checks=Counter();answer=None
    for trial in range(20000):
        p=sorted(rng.sample(range(1,61),6));q=[rng.randrange(1,61) for _ in range(7)]
        checks['search_cases']+=1;answer=check(p,q)
        if answer:break
    assert answer is not None
    # Coordinate descent is only counterexample minimization, not a solver.
    changed=True
    while changed:
        changed=False
        for k in range(13):
            ws=p+q
            for v in range(1,ws[k]):
                trial=ws[:];trial[k]=v;checks['shrink_cases']+=1
                test=check(sorted(trial[:6]),trial[6:])
                if test:
                    p,q=sorted(trial[:6]),trial[6:];answer=test;changed=True;break
    expected,witness,actual=answer
    positions=sorted(range(6),key=lambda i:(witness['pd'][i],i))
    ordered=[0]*6
    for i,v in zip(positions,sorted(p,reverse=True)):ordered[i]=v
    assert cost(witness['tree'],ordered,q)==expected==cubic(ordered,q)[0]==knuth(ordered,q)[0]
    assert candidate(ordered,q)['value']>expected
    scaled=[]
    for scale in (1,2,3,10,100,10000,10**30):
        pp=[scale*x for x in ordered];qq=[scale*x for x in q]
        got=candidate(pp,qq)
        assert got['value']==scale*actual['value']>scale*expected==cubic(pp,qq)[0]
        scaled.append(dict(scale=scale,candidate=got['value'],optimum=scale*expected))
    corner_min=None
    for signs in itertools.product((-1,1),repeat=13):
        ws=[1000*x+e for x,e in zip(ordered+q,signs)]
        got=candidate(ws[:6],ws[6:]);upper=cost(witness['tree'],ws[:6],ws[6:])
        assert got['valid'] and got['qd']==actual['qd']
        assert all(x['pair_margin'] is None or x['pair_margin']>0 for x in got['trace'])
        gap=got['value']-upper;assert gap>=996
        corner_min=gap if corner_min is None else min(corner_min,gap)
        checks['positive_box_corners']+=1
    assert corner_min==996
    def shifted(t):
        return None if t is None else (t[0]+1,shifted(t[1]),shifted(t[2]))
    embedded=[];pp=ordered[:];qq=q[:];tree=witness['tree'];upper=expected
    for n in range(6,257):
        if n in (6,7,8,16,32,64,128,256):
            got=candidate(pp,qq);value=knuth(pp,qq)[0]
            assert got['valid'] and got['charges']==got['value']==value+1
            assert value==upper==cost(tree,pp,qq)
            if n<=16:assert value==cubic(pp,qq)[0]
            assert all(x['pair_margin'] is None or x['pair_margin']>0 for x in got['trace'])
            embedded.append(dict(n=n,optimum=value,candidate=got['value'],max_weight_bits=max(pp+qq).bit_length(),pair_evaluations=got['pair_evaluations']))
        if n<256:
            W=sum(pp)+sum(qq);A=W+upper+1;P=2*A
            pp=[P]+pp;qq=[A]+qq;tree=(0,None,shifted(tree));upper=4*A-1
    result=dict(seed=317207,checks=dict(checks),key_multiset=p,p=ordered,q=q,
                optimum=expected,oracle=witness,candidate=actual,
                separate_bound=key_bound(ordered)+threshold_bound(q),scaled=scaled,
                perturbation_min_gap_scaled=corner_min,embedded=embedded,
                source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in ('joint_merge_obstruction.py','joint_merge_probe.py','research.py','threshold_probe.py')})
    (Path(__file__).resolve().parents[1]/'results'/'joint_merge_obstruction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
