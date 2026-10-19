#!/usr/bin/env python3
"""Independent exhaustive threshold/run lower bounds before the constructor."""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
from research import cost,cubic,knuth,label,shapes


def external_min(H):
    if H<2:return 0
    h=H.bit_length()-1
    return (h+2)*H-(1<<(h+1))


def indicator_bound(selected):
    H=sum(selected)
    if not H:return 0
    runs=sum(not x and (i==0 or selected[i-1]) for i,x in enumerate(selected))
    return external_min(H)+runs


def threshold_bound(q):
    value=0;previous=0
    for level in sorted(set(q)):
        if not level:continue
        selected=[int(x>=level) for x in q]
        value+=(level-previous)*indicator_bound(selected);previous=level
    return value


def key_bound(p):
    return sum(v*(i+1).bit_length() for i,v in enumerate(sorted(p,reverse=True)))


def depth_vectors(t,n):
    p=[0]*n;q=[0]*(n+1)
    def visit(t,lo,hi,d):
        if t is None:
            assert lo==hi;q[lo]=d;return
        r,l,rr=t;p[r]=d+1;visit(l,lo,r,d+1);visit(rr,r+1,hi,d+1)
    visit(t,0,n,0)
    return p,q


def profile_test(p,lengths):
    selected=[(v,d) for v,d in zip(p,lengths) if v>0]
    H=len(selected)
    if sum(d for _,d in selected)!=sum(i.bit_length() for i in range(1,H+1)):return False
    return all(v>=w for v,d in selected for w,e in selected if d<e)


def main():
    rng=random.Random(317204);checks=Counter();examples=[]
    for n in range(0,9):
        trees=[label(s)[0] for s in shapes(n)]
        depths=[depth_vectors(t,n) for t in trees]
        for pattern in itertools.product((0,1),repeat=n+1):
            bound=indicator_bound(pattern)
            values=[sum(a*b for a,b in zip(pattern,qd)) for _,qd in depths]
            assert bound<=min(values),(pattern,bound,min(values))
            checks['indicator_patterns']+=1;checks['indicator_tree_inequalities']+=len(values)
            checks['indicator_tight' if bound==min(values) else 'indicator_strict']+=1
            if bound<min(values) and len(examples)<8:examples.append(dict(pattern=pattern,lower=bound,optimum=min(values)))
        for trial in range(10):
            p=[rng.randrange(9) for _ in range(n)];q=[rng.randrange(9) for _ in range(n+1)]
            lower=key_bound(p)+threshold_bound(q)
            for pd,qd in depths:
                key=sum(a*b for a,b in zip(p,pd));gap=sum(a*b for a,b in zip(q,qd))
                assert lower<=key+gap
                assert profile_test(p,pd)==(key==key_bound(p))
                checks['weighted_tree_inequalities']+=1;checks['key_profile_characterizations']+=1
    for n in range(1,13):
        for trial in range(100):
            p=[rng.randrange(100) for _ in range(n)];q=[rng.randrange(100) for _ in range(n+1)]
            lower=key_bound(p)+threshold_bound(q);actual=cubic(p,q)[0]
            assert lower<=actual==knuth(p,q)[0]
            checks['mixed_cubic_bounds']+=1
    q=[100,10,1,10];p=[2,1,1]
    gap=threshold_bound(q);mixed=key_bound(p)+gap;opt=cubic(p,q)[0]
    assert gap==152 and gap<cubic([0]*3,q)[0]
    assert mixed<opt
    result=dict(seed=317204,checks=dict(checks),indicator_strict_examples=examples,
                strict_mixed_example=dict(p=p,q=q,lower=mixed,optimum=opt,gap_lower=gap,gap_optimum=cubic([0]*3,q)[0]),
                source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in ('threshold_probe.py','research.py')})
    (Path(__file__).resolve().parents[1]/'results'/'threshold_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
