#!/usr/bin/env python3
"""Literal majorization, all-root mixed controls, and large sparse constructors."""
from collections import Counter
from fractions import Fraction
from itertools import product,combinations
from pathlib import Path
from math import comb
import hashlib,json,random
from unimodal_above import UnimodalAbove,WindowEnvelope,unimodal_peak,dominating_window
from aggregate_core_audit import layers


def is_unimodal(p):
    return any(all(p[i]<=p[i+1] for i in range(k)) and all(p[i]>=p[i+1] for i in range(k,len(p)-1)) for k in range(len(p)))


def direct_score(p,weights):
    return max(sum(p[x]*v for x,v in zip(ts,weights)) for ts in combinations(range(len(p)),len(weights)))


def check_original(p,q,stats):
    n=len(p);H=n.bit_length();M=(H+1)*(sum(p)+sum(q))+1
    obj=UnimodalAbove(p,q,stats)
    for h,A in enumerate(layers(p,q,H,M,stats)):
        if h not in obj.windows:continue
        c=(1<<h)-1;want={}
        for i in range(n):
            for j in range(i+c,n+1):
                value,start=obj.layer(h,i,j,M)
                assert value==A[i][j]
                reward=sum(p[start+r-1]*((r&-r).bit_length()-1) for r in range(1,c+1))
                assert value==M*(j-i-c)+h*(sum(p[i:j])+sum(q[i:j+1]))-reward
                stats['original_unimodal_interval_controls']+=1
                stats['contiguous_witness_controls']+=1
                if j<n and j-i>c:
                    d=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
                    if d:want[i,j]=d
                    stats['original_unimodal_density_controls']+=1
        assert obj.cores[h]==want;stats['original_unimodal_support_sets']+=1
        for side in range(1,n//2+1):
            # Exhaust every above-capacity square on these small original layers.
            for a in range(n-side+1):
                for b in range(a+side+c,n-side+1):
                    count=sum(a<=i<a+side and b<=j<b+side for i,j in want)
                    assert count<=2*side-1;stats['original_unimodal_square_controls']+=1
    stats['original_unimodal_inputs']+=1


def check_envelope(p,q,stats,witnesses):
    n=len(p);H=n.bit_length();M=(H+1)*(sum(p)+sum(q))+1
    env=WindowEnvelope(p,q,stats)
    for i in range(n):
        for j in range(i+1,n+1):
            assert env.span.query(i,j)==is_unimodal(p[i:j])
            stats['independent_span_controls']+=1
    for h,A in enumerate(layers(p,q,H,M,stats)):
        if h not in env.windows:continue
        c=(1<<h)-1;hat={}
        for i in range(n):
            for j in range(i+c,n+1):
                value,start=env.upper_layer(h,i,j,M);hat[i,j]=value
                assert value>=A[i][j];stats['envelope_upper_cost_controls']+=1
                if env.span.query(i,j):
                    assert env.layer(h,i,j,M)[0]==A[i][j]
                    stats['certified_exact_interval_controls']+=1
        certified={}
        for i in range(n):
            for j in range(i+c+1,n):
                D=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
                Dh=hat[i,j+1]+hat[i+1,j]-hat[i,j]-hat[i+1,j+1]
                assert env.cores[h].get((i,j),0)==Dh
                stats['envelope_density_controls']+=1
                if env.span.query(i,j+1):
                    assert D==Dh
                    if D:certified[i,j]=D
                    stats['certified_exact_density_controls']+=1
                correction=Dh-D
                key='negative_correction_density' if correction<0 else 'positive_correction_density' if correction>0 else None
                if key and key not in witnesses:
                    corners=((i,j),(i,j+1),(i+1,j),(i+1,j+1))
                    Es=[hat[a,b]-A[a][b] for a,b in corners]
                    witnesses[key]=dict(p=p,q=q,h=h,i=i,j=j,original_density=D,envelope_density=Dh,correction_density=correction,correction_corners=Es)
        assert env.certified_cores[h]==certified
        stats['certified_support_set_controls']+=1
    stats['arbitrary_key_inputs']+=1


def main():
    root=Path(__file__).resolve().parents[1];rng=random.Random(451019);stats=Counter();scale=[]
    # The subsequence lemma is tested without ruler rewards, through every subset.
    for n in range(1,9):
        for p in product((0,1,2),repeat=n):
            valid=is_unimodal(p)
            try:peak=unimodal_peak(p)
            except ValueError:
                assert not valid;stats['rejected_nonunimodal_inputs']+=1;continue
            assert valid;stats['exhaustive_unimodal_inputs']+=1
            for k in range(1,n+1):
                for ts in combinations(range(n),k):
                    a=dominating_window(p,ts,peak)
                    assert all(p[a+r]>=p[x] for r,x in enumerate(ts))
                    stats['literal_dominating_subsequences']+=1
            if n<=6:
                for k in range(1,n+1):
                    weights=[rng.randrange(7) for _ in range(k)]
                    best=direct_score(p,weights)
                    assert best==max(sum(p[a+r]*v for r,v in enumerate(weights)) for a in range(n-k+1))
                    stats['arbitrary_template_controls']+=1;stats['arbitrary_template_subsequences']+=comb(n,k)
            if n<=5:
                q=[rng.randrange(4) for _ in range(n+1)]
                check_original(list(p),q,stats)
        print('exhaustive',n,flush=True)
    for n in (6,7,8,12,16,24,32):
        for trial in range(10):
            peak=rng.randrange(n)
            if trial==0:p=list(range(n))
            elif trial==1:p=list(range(n,0,-1))
            elif trial==2:p=[7]*n
            elif trial==3:p=[0]*n;p[peak]=n
            elif trial==4:p=[1<<min(i,n-1-i) for i in range(n)]
            else:
                p=sorted(rng.randrange(12) for _ in range(peak))+[12]+sorted((rng.randrange(12) for _ in range(n-peak-1)),reverse=True)
                if trial==9:p=[Fraction(x,7) for x in p]
            q=[rng.randrange(8) for _ in range(n+1)]
            if trial==9:q=[Fraction(x,5) for x in q]
            check_original(p,q,stats)
        print('mixed',n,flush=True)
    general=Counter();witnesses={}
    for n in (9,10):
        for p in product((0,1),repeat=n):
            check_envelope(list(p),[rng.randrange(3) for _ in range(n+1)],general,witnesses)
    for n in (10,12,16,24,32):
        for _ in range(20):
            check_envelope([rng.randrange(8) for _ in range(n)],[rng.randrange(4) for _ in range(n+1)],general,witnesses)
        print('arbitrary',n,flush=True)
    for key,w in witnesses.items():
        p=w['p'];i=w['i'];j=w['j'];c=(1<<w['h'])-1
        if len(p)<=12:
            errors=[]
            for a,b in ((i,j),(i,j+1),(i+1,j),(i+1,j+1)):
                v=[(r&-r).bit_length()-1 for r in range(1,c+1)]
                true=direct_score(p[a:b],v)
                window=max(sum(p[x+r]*v[r] for r in range(c)) for x in range(a,b-c+1))
                errors.append(true-window)
                general['literal_correction_subsequences']+=comb(b-a,c)
                general['literal_correction_scores']+=1
            assert errors==w['correction_corners']
            assert errors[1]+errors[2]-errors[0]-errors[3]==w['correction_density']
    print('correction witnesses',witnesses,flush=True)
    # Larger constructions: sampled literal windows; no original all-root control.
    for n in (64,127,256,1023,4096,16384,65536):
        for kind in ('single_peak','irregular_mountain'):
            if kind=='single_peak':p=[0]*n;p[n//2+1]=1
            else:
                left=[];v=0
                for i in range(n//2):v+=rng.randrange(4);left.append(v)
                right=[];v=0
                for i in range(n-n//2):v+=rng.randrange(4);right.append(v)
                p=[Fraction(x,3) for x in left]+[Fraction(x,3) for x in reversed(right)]
                # Both halves are monotone and share a single maximum at the join.
            local=Counter();obj=UnimodalAbove(p,[0]*(n+1),local)
            for h,values in obj.windows.items():
                c=(1<<h)-1
                for _ in range(8):
                    a=rng.randrange(len(values))
                    actual=sum(p[a+r-1]*((r&-r).bit_length()-1) for r in range(1,c+1))
                    assert values[a]==actual;local['large_literal_window_controls']+=1
                for side in (16,32,64,128,256):
                    if 2*side+c>n:continue
                    for _ in range(5):
                        a=rng.randrange(n-2*side-c+1);b=rng.randrange(a+side+c,n-side+1)
                        count=sum(a<=i<a+side and b<=j<b+side for i,j in obj.cores[h])
                        assert count<=2*side-1;local['large_constructed_square_controls']+=1
            if kind=='single_peak':
                # The already proved one-key family supplies a sharp leading coefficient.
                if n&(n-1)==0 and n>=64:
                    # Here n=2C and the spike is at C+1, so K=C-2h.
                    C=n//2;h=C.bit_length()-1
                    assert len(obj.cores[h])==C-2*h
                    local['sharp_one_key_core_controls']+=1
            scale.append(dict(n=n,kind=kind,core_sum=sum(map(len,obj.cores.values())),maximum_core=max(map(len,obj.cores.values()),default=0),counts=dict(local),verification='sparse constructor, sampled literal ruler windows, local support counts, and sharp single-key formula; no original all-root layer at this size'))
            print('scale',n,kind,scale[-1]['core_sum'],flush=True)
    files=('unimodal_above.py','unimodal_above_audit.py','plateau_core.py','aggregate_core_audit.py')
    result=dict(scope='All above-capacity layers for unimodal key weights and arbitrary nonnegative gaps; below-capacity mixed layers are outside this construction.',checks=dict(stats),arbitrary_input_checks=dict(general),correction_witnesses=witnesses,scale_rows=scale,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/unimodal_above_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
