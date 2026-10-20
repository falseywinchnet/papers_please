#!/usr/bin/env python3
"""Independent shape-stability harness, authored before the range constructor."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random,sys
from research import shapes,label,cost,cubic,knuth
from complete import minimum_ipl


def depths(t,n):
    p=[0]*n;q=[0]*(n+1)
    def visit(t,i,j,d):
        if t is None:q[i]=d;return
        r,l,rr=t;p[r]=d+1;visit(l,i,r,d+1);visit(rr,r+1,j,d+1)
    visit(t,0,n,0)
    return p,q


def perfect(lo,hi):
    if lo==hi:return None
    mid=(lo+hi)//2
    return mid,perfect(lo,mid),perfect(mid+1,hi)


def shifted_perfect(h):
    # Delete the greatest leaf key, then insert a new least key.
    n=(1<<h)-1;t=perfect(0,n)
    def remove(t):
        r,l,rr=t
        if rr is None:assert l is None;return None
        return r,l,remove(rr)
    def insert(t):
        if t is None:return (0,None,None)
        r,l,rr=t
        def shift(t):return None if t is None else(t[0]+1,shift(t[1]),shift(t[2]))
        return r+1,insert(l),shift(rr)
    return insert(remove(t))


def main():
    sys.setrecursionlimit(10000);rng=random.Random(710022);checks=Counter();rows=[];boundary_cases=[]
    for n in range(1,10):
        L=n.bit_length();K=(1<<L)-L-1;G=0 if L<=1 else 1<<(L-1)
        for shape in shapes(n):
            t=label(shape)[0];p,q=depths(t,n)
            assert sum(max(L-x,0) for x in p)<=K
            assert sum(max(L-x,0) for x in q)<=G
            checks['literal_capacity_bounds']+=1
            if n+1==1<<L:
                d=sum(p)-n-minimum_ipl(n)
                assert sum(max(L-x,0) for x in q)<=d
                assert sum(max(L-x,0) for x in p)<=K
                checks['literal_perfect_gap_charge']+=1
    # Every extremal assignment in small boxes, including equality and mixed gaps.
    for n in (3,7):
        h=(n+1).bit_length()-1;K=n-h;t=perfect(0,n)
        # Exhaust every joint key/gap box vertex at both perfect sizes.
        for P,Q,mode in [(1,0,'keys'),(0,1,'gaps'),(1,1,'joint')]:
            dim=n if mode=='keys' else n+1 if mode=='gaps' else 2*n+1
            threshold=P*K+Q;a=threshold//2;b=threshold-a
            for bits in product((0,1),repeat=dim):
                pp=bits[:n] if mode!='gaps' else [0]*n
                qq=bits[n:] if mode=='joint' else bits if mode=='gaps' else [0]*(n+1)
                p=[a+P*x for x in pp];q=[b+Q*x for x in qq]
                ref,_=cubic(p,q)
                assert cost(t,p,q)==ref
                checks['perfect_box_vertices']+=1
    for h in range(2,17):
        n=(1<<h)-1;t=shifted_perfect(h);ls,gs=depths(t,n)
        expected=[h+1]+[h-((i & -i).bit_length()-1) for i in range(1,n)]
        assert ls==expected and gs==[h+1,h+1]+[h]*(n-2)+[h-1]
        assert sum(ls)-n-minimum_ipl(n)==1
        assert sum(max(h-x,0) for x in ls)==n-h
        for P,Q in ((1,0),(0,1),(2,3)):
            threshold=(n-h)*P+Q
            for margin in (-1,0,1):
                a=max(0,threshold+margin);b=0
                p=[a+P*(i>=2 and i%2==0) for i in range(n)]
                q=[b+Q*(i==n) for i in range(n+1)]
                delta=cost(t,p,q)-cost(perfect(0,n),p,q)
                assert delta==a+b-threshold
                checks['explicit_threshold_identity']+=1
                if n<=127:
                    ref,_,_=knuth(p,q)
                    if margin>=0:assert cost(perfect(0,n),p,q)==ref
                    else:assert ref<cost(perfect(0,n),p,q)
                    checks['sharp_boundary_knuth_controls']+=1
                    boundary_cases.append((p,q,ref,margin))
        rows.append(dict(family='sharp_box',n=n,h=h,key_coefficient=n-h,gap_coefficient=1))
    print('independent range and sharpness claims',dict(checks),flush=True)
    from range_exchange import solve,shape_certificate
    for p,q,ref,margin in boundary_cases:
        answer=solve(p,q,Counter());assert answer['cost']==ref
        assert (answer['method']=='range_direct')==(margin>=0)
        checks['sharp_boundary_solver_controls']+=1
    for n in range(1,33):
        for trial in range(18):
            kind=trial%6
            base=(0,1,n,8*n,4*n*n,0)[kind]
            p=[base+rng.randrange(5) for _ in range(n)]
            q=[base+rng.randrange(5) for _ in range(n+1)]
            if kind==5:p=[1<<rng.randrange(10) for _ in range(n)]
            if trial%7==0:p=[Fraction(x,3) for x in p];q=[Fraction(x,3) for x in q]
            stats=Counter();answer=solve(p,q,stats)
            if trial%7==0:
                ref,_=cubic([int(x*3) for x in p],[int(x*3) for x in q]);ref=Fraction(ref,3)
                checks['rational_full_controls']+=1
            else:ref,_=cubic(p,q)
            assert answer['cost']==ref==cost(answer['tree'],p,q)
            checks['full_cubic_controls']+=1
            if n<=8:
                assert ref==min(cost(label(t)[0],p,q) for t in shapes(n))
                checks['literal_full_controls']+=1
            if answer['method']=='knuth':checks['fallback_controls']+=1
            else:checks['accepted_controls']+=1
            if kind==3:
                plan=shape_certificate(p,q,Counter());assert plan['accepted'];checks['general_range_guarantees']+=1
    for n in (23,47,95,191,383,767,1535):
        for family in ('curved','reflected','ordinary','geometric'):
            f=[i+i*i//n for i in range(n)];B=n*(f[-1]+4)+2
            p=[B+x+(-1 if i%3==0 else 1) for i,x in enumerate(f)]
            q=[B+(-1 if i%2 else 1) for i in range(n+1)]
            if family=='reflected':p.reverse();q.reverse()
            elif family=='ordinary':p=[rng.randrange(1,1000) for _ in range(n)];q=[rng.randrange(1,1000) for _ in range(n+1)]
            elif family=='geometric':p=[1<<i for i in range(n)];q=[1]*(n+1)
            stats=Counter();answer=solve(p,q,stats);ref,_,scans=knuth(p,q)
            assert answer['cost']==ref==cost(answer['tree'],p,q);checks['scale_knuth_controls']+=1
            old_a=min(p);old_b=min(q);oldE=sum(x-old_a for x in p)+sum(x-old_b for x in q)
            old_accept=min(p)+min(q)>(n-1)*oldE
            if family in ('curved','reflected'):
                assert answer['method']=='range_corridor' and not old_accept
                checks['old_gate_rejections_recovered']+=1
            rows.append(dict(n=n,family=family,p=p,q=q,cost=str(ref),method=answer['method'],certificate=answer['certificate'],model=answer.get('model'),old_gate_accepts=old_accept,counts=dict(stats),reference_candidates=scans))
            print(n,family,answer['method'],stats.get('exchange_shape_states',0),flush=True)
    for n in (6143,24575,98303):
        f=[i+i*i//n for i in range(n)];B=n*(f[-1]+4)+2
        p=[B+x+(-1 if i%3==0 else 1) for i,x in enumerate(f)];q=[B+(-1 if i%2 else 1) for i in range(n+1)]
        stats=Counter();answer=solve(p,q,stats)
        assert answer['method']=='range_corridor' and answer['cost']==cost(answer['tree'],p,q)
        old_a=min(p);old_b=min(q);oldE=sum(x-old_a for x in p)+sum(x-old_b for x in q);assert min(p)+min(q)<=(n-1)*oldE
        checks['large_certificate_controls']+=1
        rows.append(dict(n=n,family='large_curved',input_formula='f_i=i+floor(i^2/n); B=n*(f_(n-1)+4)+2; p_i=B+f_i+(-1 if i mod 3=0 else 1); q_i=B+(-1 if i odd else 1)',reference_scope='range certificate and full original-cost traversal, no large Knuth reference',cost=str(answer['cost']),method=answer['method'],certificate=answer['certificate'],model=answer['model'],counts=dict(stats)))
        print(n,'large_curved',stats['exchange_shape_states'],flush=True)
    root=Path(__file__).resolve().parents[1];files=['shape_range_audit.py','range_exchange.py','exchange_corridor.py','complete.py','research.py','trimmed_height.py','coarse_face.py','sparse.py']
    result=dict(seed=710022,scope='Sharp perfect-size box stability, general range certificate and complete mixed nonlinear-corridor construction; no timing claims',checks=dict(checks),rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/shape_range_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(checks),flush=True)

if __name__=='__main__':main()
