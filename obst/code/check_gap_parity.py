#!/usr/bin/env python3
"""Independent exhaustive checks of the global alternating-gap lower bound."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
from research import shapes,label,cost,cubic,knuth


def main():
    rng=random.Random(381027);checks=Counter();rows=[]
    for n in range(1,10):
        h=(n+1).bit_length()-1;S=1<<h;s=n+1-S
        trees=[label(t)[0] for t in shapes(n)]
        for parity in (0,1):
            q=[int(i%2==parity) for i in range(n+1)];H=sum(q);Z=n+1-H
            ell=H.bit_length()-1;leaf_min=(ell+2)*H-(1<<(ell+1))
            lower=leaf_min+Z
            assert lower==h*H+s
            values=[cost(t,[0]*n,q) for t in trees]
            assert all(v>=lower for v in values) and min(values)==lower
            checks['parity_tree_inequalities']+=len(trees)
            rows.append(dict(n=n,parity=parity,selected=H,deleted=Z,lower=lower))
        for trial in range(10):
            p=[rng.randrange(100) for _ in range(n)];x,y=rng.randrange(100),rng.randrange(100)
            q=[x if i%2 else y for i in range(n+1)]
            lower=sum(v*(i+1).bit_length() for i,v in enumerate(sorted(p,reverse=True)))
            lower+=h*sum(q)+s*(x+y)
            assert all(cost(t,p,q)>=lower for t in trees)
            checks['mixed_tree_inequalities']+=len(trees)
    # A perfect-size alternating-key input need not attain the key bound.
    p=[100,1,100];q=[0,0,0,0]
    full=cubic(p,q)[0]
    balanced=cost((1,(0,None,None),(2,None,None)),p,q)
    assert full==knuth(p,q)[0]==303 and balanced==401
    result=dict(seed=381027,checks=dict(checks),rows=rows,
                perfect_size_counterexample=dict(p=p,q=q,full=full,balanced=balanced),
                source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in ('check_gap_parity.py','research.py')})
    (Path(__file__).resolve().parents[1]/'results'/'gap_parity.json').write_text(json.dumps(result,indent=2)+'\n')
    print(dict(checks),flush=True)


if __name__=='__main__':main()
