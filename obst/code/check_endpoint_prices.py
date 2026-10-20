#!/usr/bin/env python3
"""Exact two-price checks against independent arrangements and full OBSTs."""
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
from endpoint_price_probe import transformed,literal,arrangement_max,rank
from endpoint_prices import attempt,solve,oracle
from shifted_alphabetic import attempt as previous,tree_cost
from joint_merge_probe import enumerated
from research import cubic,knuth


def encode(x):
    if isinstance(x,Fraction):return str(x)
    raise TypeError(type(x))


def main():
    rng=random.Random(317211);checks=Counter();examples={};rank_rows=[];max_calls=0
    for n in range(3,9):
        vectors=[pd+qd for _,pd,qd in enumerated(n)]
        r=rank([[x-y for x,y in zip(v,vectors[0])] for v in vectors[1:]])
        assert r==2*n-2;rank_rows.append(dict(n=n,trees=len(vectors),rank=r,nullity=2*n+1-r))
        p=[rng.randrange(1,10) for _ in range(n)];q=[rng.randrange(1,10) for _ in range(n+1)]
        a=min(p[1:-1]);x=Fraction(p[0]+q[0],3);y=Fraction(p[-1]+q[-1],2)
        pp,qq=transformed(p,q,a,x,y)
        for t,pd,qd in enumerated(n):
            assert sum(v*d for v,d in zip(pp,pd))+sum(v*d for v,d in zip(qq,qd))==tree_cost(t,p,q)+a*n
            checks['literal_transfer_identities']+=1
    for n,trials in ((3,30),(4,30)):
        for _ in range(trials):
            p=[rng.randrange(10) for _ in range(n)];q=[rng.randrange(10) for _ in range(n+1)]
            expected,points=arrangement_max(p,q)
            v,t,s,d=attempt(p,q,budget=100,stop_on_certificate=False)
            assert d['max_complete'] and d['lower']==expected[0]
            checks['independent_arrangement_maxima']+=1;checks['arrangement_points']+=points
    for n in (3,4,5,6,7,8,12,20,32,64):
        for trial in range(60):
            kind=trial%5
            if kind==0:p=[rng.randrange(1,30) for _ in range(n)];q=[rng.randrange(1,30) for _ in range(n+1)]
            elif kind==1:p=[100+rng.randrange(3) for _ in range(n)];q=[100+rng.randrange(3) for _ in range(n+1)]
            elif kind==2:p=[1<<rng.randrange(12) for _ in range(n)];q=[1<<rng.randrange(12) for _ in range(n+1)]
            elif kind==3:p=[rng.randrange(2) for _ in range(n)];q=[rng.randrange(2) for _ in range(n+1)]
            else:p=[rng.randrange(1,30)]*n;p[0]=p[-1]=1;q=[rng.randrange(1,30) for _ in range(n+1)]
            expected=cubic(p,q)[0];assert expected==knuth(p,q)[0]
            v,t,s,d=attempt(p,q,budget=100,stop_on_certificate=False)
            assert d['max_complete'] and d['lower']<=expected
            old,_,oldstats=previous(p,q)
            assert d['lower']>=oldstats['global_lower_bound']
            max_calls=max(max_calls,s['oracle_calls'])
            for event in d['history']:
                x,y=event['x'],event['y'];a=min(p[1:-1]);pp,qq=transformed(p,q,a,x,y)
                scale=x.denominator*y.denominator
                gap=cubic([0]*n,[int(z*scale) for z in qq])[0]
                from threshold_probe import key_bound
                assert event['lower']==key_bound(pp)+Fraction(gap,scale)-a*n
                checks['independent_oracle_calls']+=1
                if n<=7:assert event['lower']==literal(p,q,a,x,y)
            if v is not None:assert v==expected==tree_cost(t,p,q);checks['uncapped_certified']+=1
            if v is not None and old is None:
                checks['rescued_previous_rejection']+=1
                examples.setdefault('rescued',dict(p=p,q=q,optimum=expected,old_lower=oldstats['global_lower_bound'],new_lower=d['lower'],history=d['history']))
            if d['lower'].denominator>1:
                checks['fractional_maxima']+=1
                examples.setdefault('fractional',dict(p=p,q=q,optimum=expected,lower=d['lower'],history=d['history']))
            if d['lower']<expected:
                checks['strict_bound_gaps']+=1
                examples.setdefault('strict_gap',dict(p=p,q=q,optimum=expected,lower=d['lower'],history=d['history']))
            vv,tt,ss,dd=solve(p,q)
            assert vv==expected==tree_cost(tt,p,q);checks['bounded_full_solves']+=1
            checks['bounded_certified' if ss['certified'] else 'bounded_fallback']+=1
            if ss['certified'] and old is None:checks['bounded_rescued_previous_rejection']+=1
            if old is not None and not ss['certified']:checks['bounded_lost_previous_certificate']+=1
            # Independently test monotonic clamped movement from an arbitrary
            # admissible uniform shift and endpoint-price pair to maximal a.
            lo=-min(q[1:-1]);hi=min(p[1:-1]);aa=rng.randrange(lo,hi+1)
            xx=rng.randrange(p[0]+q[0]+1);yy=rng.randrange(p[-1]+q[-1]+1);delta=hi-aa
            f0=oracle(p,q,aa,xx,yy,Counter())[0]
            f1=oracle(p,q,hi,max(0,xx-delta),max(0,yy-delta),Counter())[0]
            assert f1>=f0;checks['clamped_monotonicity_controls']+=1
        print('n',n,'checks',dict(checks),'max calls',max_calls,flush=True)
    result=dict(seed=317211,checks=dict(checks),ranks=rank_rows,max_uncapped_oracle_calls=max_calls,examples=examples,
        source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in ('check_endpoint_prices.py','endpoint_price_probe.py','endpoint_prices.py','shifted_alphabetic.py','joint_merge_probe.py','research.py','threshold_probe.py')})
    (Path(__file__).resolve().parents[1]/'results'/'endpoint_prices.json').write_text(json.dumps(result,default=encode,indent=2)+'\n')
    print(json.dumps(examples,default=encode,indent=2),flush=True)


if __name__=='__main__':main()
