#!/usr/bin/env python3
"""Independent enumeration, cubic/full DP, and adversarial affine-fit tests."""
from collections import Counter
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

from complete import parameters,best_complete,minimum_ipl
from ordered_complete import attempt as exchange_attempt
from ramp_complete import (solve,optimize_shape,fit,potential_prefix,state_regret,
                           robust_slope)
from research import cost,cubic,knuth,label


def slot_tree(n,selected):
    """Independent structural construction, without a Cartesian depth sequence."""
    h,S,s=parameters(n);chosen=set(selected);g=0
    def build(level):
        nonlocal g
        if not level:
            here=g;g+=1
            return (None,None) if here in chosen else None
        return build(level-1),build(level-1)
    result,end=label(build(h))
    assert end==n and g==S and len(chosen)==s
    return result


def enumerate_class(n):
    _,S,s=parameters(n)
    return [(selected,slot_tree(n,selected)) for selected in itertools.combinations(range(S),s)]


def audit_potential(n,lam,mu,p,q,checks):
    h,S,s=parameters(n);ref=slot_tree(n,range(s));trees=enumerate_class(n)
    rp=[lam*i for i in range(n)];rq=[mu*i for i in range(n+1)]
    base=cost(ref,rp,rq);prefix=potential_prefix(S,lam,mu,Counter());minimum={}
    direct={selected:cost(t,p,q) for selected,t in trees}
    for selected,t in trees:
        baseline_regret=cost(t,rp,rq)-base
        assert baseline_regret==sum(prefix[g+1]-prefix[g] for g in selected)-prefix[s]
        e=0;chosen=set(selected)
        for g in range(S+1):
            a=g-e;b=s-e
            minimum[a,b]=min(minimum.get((a,b),baseline_regret),baseline_regret)
            if g<S:e+=g in chosen
        for g in range(S-1):
            if g not in chosen and g+1 in chosen:
                moved=tuple(sorted((chosen-{g+1})|{g}))
                i=g+sum(t<g for t in chosen)
                change=(1+((g+1 & -(g+1)).bit_length()-1))*(p[i]-p[i+1])+q[i]-q[i+2]
                assert direct[moved]-direct[selected]==change
                checks['direct_exchange_checks']+=1
        checks['affine_shape_cost_checks']+=1
    for (a,b),v in minimum.items():
        assert state_regret(prefix,s,a,b)==v>=(lam+2*mu)*a*b
        checks['minimum_prefix_regret_checks']+=1
    model=fit(p,q,ref,Counter());lam=model['key_slope'];mu=model['gap_slope']
    dp=[v-lam*i for i,v in enumerate(p)];dq=[v-mu*i for i,v in enumerate(q)]
    checks['negative_residual_cases']+=min(dp+dq)<0
    rp=[lam*i for i in range(n)];rq=[mu*i for i in range(n+1)]
    base=cost(ref,rp,rq);opt=min(direct.values());prefix=potential_prefix(S,lam,mu,Counter())
    for selected,t in trees:
        assert cost(t,dp,dq)>=model['profile_lower_bound']
        checks['signed_profile_checks']+=1
        if direct[selected]==opt:
            assert cost(t,rp,rq)-base<=model['gain_bound']
            e=0;chosen=set(selected)
            for g in range(S+1):
                assert state_regret(prefix,s,g-e,s-e)<=model['gain_bound']
                checks['optimal_prefix_retained_checks']+=1
                if g<S:e+=g in chosen


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--max-n',type=int,default=768)
    parser.add_argument('--scale-n',type=int,default=24576)
    args=parser.parse_args();sys.setrecursionlimit(10000)
    rng=random.Random(319077);checks=Counter();rows=[]
    def check(p,q,shape=False):
        n=len(p);value,t,stats,model=solve(p,q);ref,_,kc=knuth(p,q)
        assert value==ref==cost(t,p,q)
        if n<=12:assert value==cubic(p,q)[0];checks['cubic_checks']+=1
        checks['solves']+=1;checks['certified']+=stats['certified']
        checks['budget_rejections']+=stats['state_budget_rejected']
        checks['gate_rejections']+=stats['global_gate_rejected']
        checks['preflight_rejections']+=stats['preflight_rejected']
        if n<=12:
            old_value,_,old_stats,_=solve(p,q,preflight=False)
            assert old_value==value and old_stats['certified']==stats['certified']
            checks['unfiltered_gate_controls']+=1
        if shape:
            v,tt,sc,mm=optimize_shape(p,q)
            assert v==best_complete(p,q)[0]==cost(tt,p,q)
            checks['unrestricted_shape_dp_checks']+=1
            if n<=10:
                assert v==min(cost(z,p,q) for _,z in enumerate_class(n))
                checks['independent_shape_enumerations']+=1
        return dict(n=n,value=value,counts=dict(stats),model=model,knuth_candidates=kc)
    for n in range(5):
        for v in itertools.product((0,1),repeat=2*n+1):
            check(list(v[:n]),list(v[n:]),shape=True)
    for n in range(1,41):
        for trial in range(10):
            B=4*(n+1)**3 if trial>=4 else 0
            p=[B+rng.randrange(32) for _ in range(n)];q=[B+rng.randrange(32) for _ in range(n+1)]
            if trial%3==0:p.sort();q.sort()
            if trial%3==1:p.sort(reverse=True);q.sort(reverse=True)
            check(p,q,shape=True)
        if n<=14:
            for trial in range(3):
                p=[rng.randrange(40) for _ in range(n)];q=[rng.randrange(40) for _ in range(n+1)]
                audit_potential(n,rng.randrange(5),rng.randrange(5),p,q,checks)
        print('fuzz',n,flush=True)
    # Robust slope recovery includes concentrated endpoint and ignored-tail errors.
    for n in (32,33,48,64,127,192,256):
        for trial in range(40):
            lam,mu=rng.randrange(9),rng.randrange(9);B=4*(n+1)**3
            u=[0]*n;v=[0]*(n+1)
            if trial<6:
                array=u if trial<3 else v
                pos=(0,len(array)//2,len(array)-1)[trial%3]
                array[pos]=rng.choice((-n,n))
            else:
                for _ in range(n):
                    array=u if rng.randrange(2) else v
                    array[rng.randrange(len(array))]+=rng.choice((-1,1))
            p=[B+lam*i+x for i,x in enumerate(u)];q=[B+mu*i+x for i,x in enumerate(v)]
            assert robust_slope(p,Counter())==lam and robust_slope(q,Counter())==mu
            checks['robust_slope_recovery_pairs']+=1
            if trial<6:
                row=check([B+i+x for i,x in enumerate(u)],[B+i+x for i,x in enumerate(v)])
                assert row['counts'].get('certified')==1
                checks['concentrated_perturbation_solves']+=1
    # Explicit positive witness: the left-filled shape can cease to be optimal.
    n=24;B=4*(n+1)**3;p=[B+i+(-1)**i for i in range(n)];q=[B+i for i in range(n+1)]
    _,S,s=parameters(n);reference=slot_tree(n,range(s))
    moved=slot_tree(n,(set(range(s))-{s-2})|{s})
    rv=cost(reference,p,q);mv=cost(moved,p,q)
    assert mv==rv-1 and exchange_attempt(p,q)[0] is None
    row=check(p,q,shape=True)
    witness=dict(n=n,p=p,q=q,reference_cost=rv,two_exchange_cost=mv,optimum=row['value'])
    assert row['counts']['certified']==1 and row['value']<rv
    n=1536;B=4*(n+1)**3
    p=[B+rng.randrange(3) for _ in range(n)];q=[B+rng.randrange(3) for _ in range(n+1)]
    budget_control=check(p,q)
    assert budget_control['counts'].get('state_budget_rejected')==1
    for n in (48,96,192,384,768):
        if n>args.max_n:continue
        B=4*(n+1)**3
        random_u=[0]*n;random_v=[0]*(n+1)
        for _ in range(n):
            array=random_u if rng.randrange(2) else random_v
            array[rng.randrange(len(array))]+=rng.choice((-1,1))
        checker=[B+i+(-1)**i for i in range(n)];ramp=[B+i for i in range(n+1)]
        fixtures=[
            ('alternating_key_perturbation',checker,ramp),
            ('alternating_key_reverse',checker[::-1],ramp[::-1]),
            ('random_signed_perturbations',[B+i+x for i,x in enumerate(random_u)],
             [B+i+x for i,x in enumerate(random_v)]),
            ('bounded_both',[B+i+rng.choice((-1,0,1)) for i in range(n)],
             [B+i+rng.choice((-1,0,1)) for i in range(n+1)]),
            ('endpoint_spike',[B+i+(n if i==0 else 0) for i in range(n)],ramp),
            ('near_constant',[B+rng.randrange(3) for _ in range(n)],[B+rng.randrange(3) for _ in range(n+1)]),
            ('geometric',[1<<i for i in range(n)],[1<<i for i in range(n+1)]),
            ('random',[rng.randrange(64) for _ in range(n)],[rng.randrange(64) for _ in range(n+1)]),
        ]
        for name,p,q in fixtures:
            row=check(p,q,shape=n<=192);row['family']=name
            if name in ('alternating_key_perturbation','alternating_key_reverse','random_signed_perturbations','bounded_both','endpoint_spike'):
                assert row['counts']['certified']==1
            rows.append(row)
            print(name,n,'states',row['counts'].get('shape_states',0),'cert',row['counts'].get('certified',0),flush=True)
    scaling=[]
    for n in (1536,6144,24576,98304):
        if n>args.scale_n:continue
        for family in ('alternating_key','bounded_both'):
            B=4*(n+1)**3
            p=[B+i+(-1)**i for i in range(n)];q=[B+i for i in range(n+1)]
            if family=='bounded_both':
                p=[B+i+rng.choice((-1,0,1)) for i in range(n)]
                q=[B+i+rng.choice((-1,0,1)) for i in range(n+1)]
            value,t,stats,model=solve(p,q)
            assert stats['certified']==1 and value==cost(t,p,q)
            reference=slot_tree(n,range(parameters(n)[2]))
            reference_cost=cost(reference,p,q)
            assert value<=reference_cost
            if family=='alternating_key':assert value<reference_cost and exchange_attempt(p,q)[0] is None
            row=dict(n=n,family=family,value=value,reference_cost=reference_cost,counts=dict(stats),model=model)
            if n<=1536:
                expected,_,kc=knuth(p,q);assert value==expected
                assert value==best_complete(p,q)[0]
                row['knuth_candidates']=kc;checks['large_knuth_and_shape_controls']+=1
            scaling.append(row)
            print('scaling',n,family,'states',stats.get('shape_states',0),'gain',reference_cost-value,flush=True)
    root=Path(__file__).resolve().parents[1]
    result=dict(seed=319077,checks=dict(checks),rows=rows,constructor_scaling=scaling,
                noncanonical_witness=witness,budget_rejection_control=budget_control,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest()
                    for f in ('check_ramp_complete.py','ramp_complete.py','ordered_complete.py',
                              'ruler_barrier.py','complete.py','sparse.py','research.py')})
    (root/'results'/'ramp_complete.json').write_text(json.dumps(result,indent=2)+'\n')
    print(dict(checks),flush=True)


if __name__=='__main__':main()
