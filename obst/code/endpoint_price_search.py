#!/usr/bin/env python3
"""Retain reduced global-dual obstruction and search for fractional optima."""
from collections import Counter
from fractions import Fraction
import hashlib,json
from pathlib import Path
import random
from endpoint_prices import attempt
from research import cubic


def main():
    p=[2,6,21,22];q=[8,9,3,5,28];checks=Counter()
    def test(p,q):
        _,_,_,d=attempt(p,q,budget=100,stop_on_certificate=False)
        assert d['max_complete']
        opt,tree=cubic(p,q);checks['shrink_controls']+=1
        return (opt,tree,d) if d['lower']<=opt-1 else None
    result=test(p,q);changed=True
    while changed:
        changed=False
        for i in range(9):
            ws=p+q
            for x in range(1,ws[i]):
                trial=ws[:];trial[i]=x;got=test(trial[:4],trial[4:])
                if got:p=trial[:4];q=trial[4:];result=got;changed=True;break
    obstruction=dict(p=p,q=q,optimum=result[0],tree=result[1],dual=result[2])
    print('obstruction',obstruction,flush=True)
    rng=random.Random(317212);fractional=None;maxcalls=0
    for trial in range(6000):
        n=rng.randrange(4,13);p=[rng.randrange(1,80) for _ in range(n)];q=[rng.randrange(1,80) for _ in range(n+1)]
        _,_,s,d=attempt(p,q,budget=100,stop_on_certificate=False);assert d['max_complete']
        checks['fractional_search_cases']+=1;maxcalls=max(maxcalls,s['oracle_calls'])
        if d['lower'].denominator!=1:
            fractional=dict(p=p,q=q,optimum=cubic(p,q)[0],dual=d);print('fractional',fractional,flush=True);break
        if trial%1000==0:print('trial',trial,'maxcalls',maxcalls,flush=True)
    data=dict(seed=317212,checks=dict(checks),obstruction=obstruction,fractional=fractional,maxcalls=maxcalls,
        source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in ('endpoint_price_search.py','endpoint_prices.py','shifted_alphabetic.py','research.py')})
    (Path(__file__).resolve().parents[1]/'results'/'endpoint_price_search.json').write_text(json.dumps(data,default=str,indent=2)+'\n')


if __name__=='__main__':main()
