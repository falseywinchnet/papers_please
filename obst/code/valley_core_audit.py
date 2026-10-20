#!/usr/bin/env python3
"""Literal top-c support, original mixed cores, local mass charges, and construction."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random
from valley_core import ValleyCores
from valley_above import valley_floor,dense_valley,dense_valley_density
from aggregate_core_audit import layers


def top_score(p,i,j,c):return sum(sorted(p[i:j],reverse=True)[:c])


def check(p,q,stats,all_roots=False):
    n=len(p);obj=ValleyCores(p,q,stats);obj.construct();P=sum(p)
    for h,core in obj.cores.items():
        c=(1<<h)-1;expected={};candidate={};row_mass=Counter();column_mass=Counter()
        actual={(i,j):d for i,j,d in obj.top_candidates(c)}
        for i in range(n):
            for j in range(i+c+1,n):
                coords=((i,j),(i,j+1),(i+1,j),(i+1,j+1))
                tops=[top_score(p,a,b,c) for a,b in coords]
                T=tops[0]+tops[3]-tops[1]-tops[2]
                values=[obj.score(h,a,b)[0] for a,b in coords]
                D=values[0]+values[3]-values[1]-values[2]
                assert 0<=D<=(h-1)*T
                if T:candidate[i,j]=T
                if D:expected[i,j]=D
                row_mass[i]+=T;column_mass[j]+=T
                stats['literal_top_density_controls']+=1
                if c>=2:
                    middle=sorted(p[i+1:j],reverse=True);z=middle[c-1];w=middle[c-2]
                    assert T==max(0,min(p[i],p[j],w)-z)
                    stats['two_threshold_formula_controls']+=1
        assert actual==candidate;assert core==expected
        assert all(v<=p[i] for i,v in row_mass.items())
        assert all(v<=p[j] for j,v in column_mass.items())
        stats['top_support_set_controls']+=1;stats['ruler_support_set_controls']+=1
        integer=all(x==int(x) for x in p)
        if integer:assert len(core)<=len(candidate)<=P
        for s in range(1,n//2+1):
            for a in range(n-s+1):
                for b in range(a+s+c,n-s+1):
                    mass=sum(d for (i,j),d in candidate.items() if a<=i<a+s and b<=j<b+s)
                    bound=min(sum(p[a:a+s]),sum(p[b:b+s]))
                    assert mass<=bound
                    if integer:assert sum(a<=i<a+s and b<=j<b+s for i,j in core)<=bound
                    stats['local_boundary_mass_controls']+=1
    if all_roots:
        H=n.bit_length();M=(H+1)*(P+sum(q))+1
        for h,A in enumerate(layers(p,q,H,M,stats)):
            if h not in obj.cores:continue
            c=(1<<h)-1;expected={}
            for i in range(n):
                for j in range(i+c+1,n):
                    d=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
                    if d:expected[i,j]=d
                    stats['original_density_controls']+=1
            assert obj.cores[h]==expected;stats['original_support_set_controls']+=1
        stats['original_inputs']+=1
    stats['small_inputs']+=1


def main():
    root=Path(__file__).resolve().parents[1];rng=random.Random(471019);stats=Counter();scales=[]
    for n in range(1,10):
        for p in product(range(3),repeat=n):
            try:valley_floor(p)
            except ValueError:continue
            check(list(p),[rng.randrange(4) for _ in range(n+1)],stats,all_roots=n<=8)
        print('exhaustive',n,flush=True)
    for n in (12,16,24,32):
        for trial in range(12):
            z=rng.randrange(n)
            if trial==0:p=[7]*n
            elif trial==1:p=list(range(n))
            elif trial==2:p=[1<<abs(i-z) for i in range(n)]
            else:p=sorted((rng.randrange(12) for _ in range(z)),reverse=True)+[0]+sorted(rng.randrange(12) for _ in range(n-z-1))
            q=[rng.randrange(5) for _ in range(n+1)]
            if trial==11:p=[Fraction(x,7) for x in p];q=[Fraction(x,3) for x in q]
            check(p,q,stats,True)
        print('mixed',n,flush=True)
    for s in (4,8):
        check(dense_valley(s),[0]*(4*s+1),stats,True)
        check([Fraction(x,4*s) for x in dense_valley(s)],[0]*(4*s+1),stats,True)
    # Complete sparse constructions, with sampled literal density controls.
    for n in (64,127,256,1023,4096,16384):
        for kind in ('binary_ends','bounded_valley'):
            z=n//2
            if kind=='binary_ends':p=[1]*(n//4)+[0]*(n-2*(n//4))+[1]*(n//4)
            else:p=sorted((rng.randrange(5) for _ in range(z)),reverse=True)+sorted(rng.randrange(5) for _ in range(n-z))
            local=Counter();obj=ValleyCores(p,stats=local);obj.construct();P=sum(p)
            for h,core in obj.cores.items():
                c=(1<<h)-1
                assert len(core)<=obj.candidate_counts[h]<=P
                if c+2>n:continue
                for _ in range(32):
                    i=rng.randrange(n-c-1);j=rng.randrange(i+c+1,n)
                    coords=((i,j),(i,j+1),(i+1,j),(i+1,j+1))
                    values=[]
                    for a,b in coords:
                        ts=sorted(sorted(range(a,b),key=lambda x:(-p[x],x))[:c])
                        values.append(sum(p[x]*((r&-r).bit_length()-1) for r,x in enumerate(ts,1)))
                    D=values[0]+values[3]-values[1]-values[2]
                    assert core.get((i,j),0)==D;local['large_literal_density_controls']+=1
            scales.append(dict(n=n,kind=kind,key_mass=P,core_sum=sum(map(len,obj.cores.values())),candidate_sum=sum(obj.candidate_counts.values()),counts=dict(local),verification='complete sparse all-layer construction with sampled literal largest-key density controls; no large original all-root reference'))
            print('scale',n,kind,scales[-1]['core_sum'],flush=True)
    for s in (4,8,16,32,64):
        p=dense_valley(s);local=Counter();obj=ValleyCores(p,stats=local);obj.construct();h=(2*s).bit_length()-1
        assert sum(0<=i<s and 3*s<=j<4*s for i,j in obj.cores[h])==s*s//2
        for i in range(s):
            for j in range(3*s,4*s):
                assert obj.cores[h].get((i,j),0)==dense_valley_density(s,i,j)
                stats['constructed_dense_formula_cells']+=1
    # The support inclusion has an explicit nonvalley failure.
    p=[0,0,0,1,0,0,0,1,0];q=[0]*10;h=3;c=7;M=9;control=Counter()
    A=list(layers(p,q,h,M,control))[-1]
    corners=((0,8),(0,9),(1,8),(1,9))
    S=[M*(b-a-c)+h*sum(p[a:b])-A[a][b] for a,b in corners]
    T=[top_score(p,a,b,c) for a,b in corners]
    assert S==[2,3,0,2] and T==[2,2,2,2]
    witness=dict(p=p,h=h,cell=[0,8],ruler_scores=S,top_scores=T,original_density=1,top_density=0,original_counts=dict(control))
    files=('valley_core.py','valley_core_audit.py','valley_above.py','unimodal_above.py','aggregate_core_audit.py')
    record=dict(scope='All above-capacity valley cores, top-c support inclusion, and integer boundary-mass charges; no below-capacity or full-BST construction claim.',checks=dict(stats),scale_rows=scales,nonvalley_witness=witness,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/valley_core_audit.json').write_text(json.dumps(record,indent=2)+'\n');print(dict(stats),flush=True)


if __name__=='__main__':main()
