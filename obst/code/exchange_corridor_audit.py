#!/usr/bin/env python3
"""Literal exchange-regret controls written before the nonlinear corridor solver."""
from collections import Counter
from fractions import Fraction
from final_core_probe import table
from itertools import combinations,product
from pathlib import Path
import hashlib,json,random,sys
from research import cost,knuth,cubic,label,shapes
from complete import parameters,minimum_ipl


def literal_shape(bits):
    def build(lo,hi):
        if hi-lo==1:return (None,None) if bits[lo] else None
        mid=(lo+hi)//2
        return build(lo,mid),build(mid,hi)
    return label(build(0,len(bits)))[0]


def inversions(bits):
    zeros=0;result=0
    for x in bits:
        if x:result+=zeros
        else:zeros+=1
    return result


def main():
    sys.setrecursionlimit(10000)
    rng=random.Random(702021);checks=Counter();rows=[]
    for n in range(1,15):
        h,S,s=parameters(n);refbits=[1]*s+[0]*(S-s);ref=literal_shape(refbits)
        for trial in range(6):
            p=[];v=0
            for _ in range(n):v+=rng.randrange(1,10);p.append(v)
            q=[rng.randrange(5)]*(n+1)
            fp=[max(0,x+rng.randrange(-5,6)) for x in p];fq=[max(0,x+rng.randrange(-5,6)) for x in q]
            Ep=sum(abs(x-y) for x,y in zip(fp,p));Eq=sum(abs(x-y) for x,y in zip(fq,q));V=h*Ep+Eq
            base=cost(ref,p,q);fine=cost(ref,fp,fq);opts=[];best=None
            for selected in combinations(range(S),s):
                bits=[0]*S
                for k in selected:bits[k]=1
                t=literal_shape(bits);inv=inversions(bits);value=cost(t,fp,fq)
                assert cost(t,p,q)-base>=inv
                assert fine-value<=V
                checks['literal_exchange_regret_checks']+=1
                if best is None or value<best:best=value;opts=[bits]
                elif value==best:opts.append(bits)
            for bits in opts:
                assert inversions(bits)<=V
                used=0
                for g,x in enumerate(bits,1):
                    used+=x;assert (g-used)*(s-used)<=V
                    checks['optimal_prefix_inclusion_checks']+=1
    print('independent claims',dict(checks),flush=True)
    from exchange_corridor import solve,model,optimize
    # The shape optimizer is independently checked even without a global gate.
    for n in range(1,17):
        h,S,s=parameters(n)
        for trial in range(8):
            p=[rng.randrange(30) for _ in range(n)];q=[rng.randrange(30) for _ in range(n+1)]
            stats=Counter();fit=model(p,q,stats);v,t=optimize(p,q,fit,stats)
            expected=min(cost(literal_shape([int(k in selected) for k in range(S)]),p,q) for selected in combinations(range(S),s))
            assert v==expected==cost(t,p,q);checks['literal_class_optima']+=1
            assert stats['exchange_shape_states']<=fit['state_bound'];checks['state_bound_checks']+=1
    for n in range(0,9):
        for trial in range(12):
            p=[rng.randrange(8) for _ in range(n)];q=[rng.randrange(8) for _ in range(n+1)]
            if trial<6:
                D=10*(n+1)**4;p=[D+i+(i*i//max(1,n))+rng.randrange(-2,3) for i in range(n)];q=[D+rng.randrange(-2,3) for _ in range(n+1)]
            stats=Counter();answer=solve(p,q,stats)
            expected,t=cubic(p,q);assert answer['cost']==expected==cost(answer['tree'],p,q)
            checks['full_cubic_controls']+=1
            if n<=6:
                assert min(cost(label(s)[0],p,q) for s in shapes(n))==expected;checks['literal_full_controls']+=1
    for n in (23,47,95,191,383,767,1535):
        for family in ('curved_unit','curved_two','irregular','decreasing','ordinary','geometric'):
            U=2 if family=='curved_two' else 1
            f=[i+i*i//n for i in range(n)]
            if family=='irregular':
                v=0;f=[]
                for _ in range(n):v+=rng.randrange(1,6);f.append(v)
            D=2*n*sum(f)+20*(n+1)**2
            p=[D+x+rng.randrange(-U,U+1) for x in f];q=[D+rng.randrange(-U,U+1) for _ in range(n+1)]
            if family=='decreasing':p.reverse();q.reverse()
            if family=='ordinary':p=[rng.randrange(1001) for _ in range(n)];q=[rng.randrange(1001) for _ in range(n+1)]
            if family=='geometric':p=[1<<i for i in range(n)];q=[1]*(n+1)
            stats=Counter();answer=solve(p,q,stats);expected,t,scans=knuth(p,q)
            assert answer['cost']==expected==cost(answer['tree'],p,q);checks['scale_knuth_controls']+=1
            if family not in ('ordinary','geometric'):
                assert answer['method']=='exchange_corridor'
                assert answer['model']['key_error']<=2*U*n and answer['model']['gap_error']<=2*U*(n+1)
                checks['nonlinear_family_guarantees']+=1
            rows.append(dict(n=n,family=family,p=p,q=q,cost=str(expected),method=answer['method'],model=answer.get('model'),counts=dict(stats),reference_knuth_candidates=scans))
            print(n,family,answer['method'],stats['exchange_shape_states'],flush=True)
    for n in (1,2,5,23,128):
        for a,b in ((0,0),(1,0),(0,2),(3,5)):
            counts=Counter();answer=solve([a]*n,[b]*(n+1),counts)
            assert answer['method']=='uniform' and answer['cost']==(a+b)*minimum_ipl(n)+(a+2*b)*n
            checks['uniform_linear_controls']+=1
    for n in range(1,10):
        for large in (False,True):
            D=100*n**4 if large else 0
            p=[Fraction(3*D+3*i+rng.randrange(6),3) for i in range(n)]
            q=[Fraction(3*D+rng.randrange(6),3) for _ in range(n+1)]
            stats=Counter();answer=solve(p,q,stats);ref,_=table(p,q,Counter(),True)
            assert answer['cost']==ref[0][n]==cost(answer['tree'],p,q)
            checks['rational_full_controls']+=1
    # Large rows have direct traversal and the proved certificate, not large Knuth controls.
    for n in (6143,24575,98303):
        f=[i+i*i//n for i in range(n)];D=2*n*sum(f)+20*(n+1)**2
        p=[D+x+(-1 if i%3==0 else 1) for i,x in enumerate(f)]
        q=[D+(-1 if i%2 else 1) for i in range(n+1)]
        stats=Counter();answer=solve(p,q,stats)
        assert answer['method']=='exchange_corridor' and answer['cost']==cost(answer['tree'],p,q)
        assert answer['model']['key_error']<=2*n and answer['model']['gap_error']<=2*(n+1)
        checks['large_certificate_controls']+=1
        from ramp_complete import fit as affine_fit
        from ruler_barrier import construct
        old_counts=Counter();old_model=affine_fit(p,q,construct(0,n,Counter()),old_counts)
        rows.append(dict(n=n,family='large_curved_unit',input_formula='f_i=i+floor(i^2/n); D=2n sum(f)+20(n+1)^2; p_i=D+f_i+(-1 if i mod 3=0 else 1); q_i=D+(-1 if i odd else 1)',reference_scope='proved global certificate and complete original-cost traversal; no large Knuth reference',old_affine_preflight_bound=old_model,old_affine_fit_counts=dict(old_counts),cost=str(answer['cost']),method=answer['method'],model=answer['model'],counts=dict(stats)))
        print(n,'large_curved_unit',stats['exchange_shape_states'],flush=True)
    root=Path(__file__).resolve().parents[1];files=['exchange_corridor_audit.py','exchange_corridor.py','complete.py','research.py','ruler_barrier.py','trimmed_height.py','coarse_face.py','final_core_probe.py','ramp_complete.py','ordered_complete.py','sparse.py']
    result=dict(seed=702021,scope='Nonlinear ordered-reference inversion corridor; full mixed-weight construction, independent literal and Knuth controls, separately labeled large certificate rows',checks=dict(checks),rows=rows,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/exchange_corridor_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(checks),flush=True)

if __name__=='__main__':main()
