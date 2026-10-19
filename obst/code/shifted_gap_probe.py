#!/usr/bin/env python3
"""Independent cubic/exhaustive probe before the shifted alphabetic constructor."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
from research import cubic,cost
from joint_merge_probe import enumerated,oracle
from threshold_probe import key_bound,threshold_bound,external_min


def main():
    rng=random.Random(317209);checks=Counter();examples=[]
    for n in range(1,17):
        for trial in range(60):
            p=[rng.randrange(1,10) for _ in range(n)]
            q=[rng.randrange(10) for _ in range(n+1)]
            m=min(p);gap,tree=cubic([0]*n,[x+m for x in q])
            lower=key_bound([x-m for x in p])+gap-m*n
            opt=cubic(p,q)[0];checks['cubic_controls']+=1
            assert key_bound(p)+threshold_bound(q)<=lower<=opt
            for a in range(-min(q),m+1):
                value=key_bound([x-a for x in p])+cubic([0]*n,[x+a for x in q])[0]-a*n
                assert value<=lower
                checks['scalar_shift_controls']+=1
            if n<=7:
                assert lower<=oracle(p,q)[0]
                for _,pd,qd in enumerated(n):
                    assert lower<=sum(x*y for x,y in zip(p,pd))+sum(x*y for x,y in zip(q,qd))
                    checks['literal_tree_inequalities']+=1
            if cost(tree,p,q)==lower:
                assert lower==opt;checks['certified']+=1
                if lower>key_bound(p)+threshold_bound(q):
                    checks['strictly_stronger_certified']+=1
                    if len(examples)<8:examples.append(dict(p=p,q=q,lower=lower,old=key_bound(p)+threshold_bound(q)))
    p=[7,1,5,8,6,4];q=[18,2,13,3,17,1,2]
    m=min(p);gap,tree=cubic([0]*len(p),[x+m for x in q])
    assert key_bound([x-m for x in p])+gap-m*len(p)==cost(tree,p,q)==213
    result=dict(seed=317209,checks=dict(checks),examples=examples,
                source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in ('shifted_gap_probe.py','joint_merge_probe.py','research.py','threshold_probe.py')})
    (Path(__file__).resolve().parents[1]/'results'/'shifted_gap_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
