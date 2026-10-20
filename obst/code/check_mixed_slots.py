#!/usr/bin/env python3
"""Independent all-root and literal controls for the mixed slot representation."""
from collections import Counter
from itertools import product,combinations
from pathlib import Path
import hashlib,json,random
from mixed_slots import solve,repair,valuations
from aggregate_core_audit import layers
from research import cost,shapes,label,cubic


def profile(tree,n):
    keys=[0]*n;gaps=[0]*(n+1)
    def walk(t,a,b,d):
        if t is None:assert a==b;gaps[a]=d;return
        r,l,rr=t;keys[r]=d+1;walk(l,a,r,d+1);walk(rr,r+1,b,d+1)
    walk(tree,0,n,0)
    return keys,gaps


def reference(p,q,h,counts):
    n=len(p);old=[[0 if i==j else None for j in range(n+1)] for i in range(n+1)]
    for depth in range(1,h+1):
        cur=[[0 if i==j else None for j in range(n+1)] for i in range(n+1)]
        for k in range(1,n+1):
            for i in range(n-k+1):
                j=i+k;options=[]
                for r in range(i,j):
                    if old[i][r] is not None and old[r+1][j] is not None:options.append(old[i][r]+old[r+1][j])
                    counts['reference_root_candidates']+=1
                if options:cur[i][j]=sum(p[i:j])+sum(q[i:j+1])+min(options)
                counts['reference_states']+=1
        old=cur
    return old[0][n]


def proxy(slots,p,q,h):
    length=[h-((t & -t).bit_length()-1) for t in slots]
    gaps=[length[0]]+[max(a,b) for a,b in zip(length,length[1:])]+[length[-1]]
    return sum(a*b for a,b in zip(p,length))+sum(a*b for a,b in zip(q,gaps))


def check(p,q,h,counts,ops,literal=False):
    got=solve(p,q,h,ops);expected=reference(p,q,h,counts)
    assert (None if got is None else got['cost'])==expected
    if got is None:return
    n=len(p);keys,gaps=profile(got['tree'],n)
    assert max(keys)<=h and cost(got['tree'],p,q)==expected
    assert proxy(got['slots'],p,q,h)==expected
    # Repair decreases every coordinate, and the external-depth identity is exact.
    lengths=[h-((t & -t).bit_length()-1) for t in got['slots']]
    assert all(a<=b for a,b in zip(keys,lengths))
    assert gaps==[keys[0]]+[max(a,b) for a,b in zip(keys,keys[1:])]+[keys[-1]]
    if literal:
        assert min(proxy(ts,p,q,h) for ts in combinations(range(1,1<<h),n))==expected
        counts['literal_slot_minima']+=1
        trees=[label(s)[0] for s in shapes(n)]
        assert min(cost(t,p,q) for t in trees if max(profile(t,n)[0])<=h)==expected
        counts['literal_tree_minima']+=1
    counts['full_constructions']+=1
    return got


def main():
    counts=Counter();ops=Counter();rng=random.Random(28019);rows=[]
    # Test repair on every nonempty subset of every perfect tree through height 4.
    repair_ops=Counter()
    for h in range(1,5):
        c=(1<<h)-1
        for mask in range(1,1<<c):
            slots=[i+1 for i in range(c) if mask>>i&1]
            t=repair(slots,h,repair_ops);keys,gaps=profile(t,len(slots))
            lengths=[h-((r & -r).bit_length()-1) for r in slots]
            assert all(a<=b for a,b in zip(keys,lengths))
            assert gaps==[keys[0]]+[max(a,b) for a,b in zip(keys,keys[1:])]+[keys[-1]]
            counts['arbitrary_subset_repairs']+=1
    for n in range(1,4):
        for w in product((0,1),repeat=2*n+1):
            for h in range(n.bit_length(),min(n+1,4)+1):check(list(w[:n]),list(w[n:]),h,counts,ops,True)
    p=[100,1,1,1];q=[1]*5
    example=check(p,q,3,counts,ops,True)
    assert example['cost']==cubic(p,q)[0]==121
    candidates=[label(s)[0] for s in shapes(4)]
    minimum_ipl=min(sum(profile(t,4)[0])-4 for t in candidates)
    minimum_ipl_cost=min(cost(t,p,q) for t in candidates if sum(profile(t,4)[0])-4==minimum_ipl)
    assert minimum_ipl_cost==218
    separation=dict(p=p,q=q,h=3,cost=121,unrestricted_cost=121,minimum_ipl_cost=218)
    for n in range(4,25):
        h0=n.bit_length()
        for t in range(12):
            p=[rng.randrange(20) for _ in range(n)];q=[rng.randrange(20) for _ in range(n+1)]
            if t%4==0:p=[0]*n
            if t%4==1:q=[0]*(n+1)
            check(p,q,h0+t%2,counts,ops,literal=n<=7 and t<2)
    # Above capacity: all gaps reach level h; only key weights affect choices.
    for n in range(2,25):
        for h in range(1,n.bit_length()):
            c=(1<<h)-1
            for trial in range(4):
                p=[rng.randrange(9) for _ in range(n)];q=[rng.randrange(9) for _ in range(n+1)]
                M=(h+1)*(sum(p)+sum(q))+1
                A=list(layers(p,q,h,M,counts))[-1]
                Z=list(layers(p,[0]*(n+1),h,M,counts))[-1]
                v=valuations(c)
                for i in range(n):
                    for j in range(i+c,n+1):
                        if j<=i:continue
                        dp=[0]+[None]*c
                        for weight in p[i:j]:
                            for k in range(c,0,-1):
                                if dp[k-1] is not None:
                                    candidate=dp[k-1]+weight*v[k]
                                    if dp[k] is None or candidate>dp[k]:dp[k]=candidate
                        predicted=M*(j-i-c)+h*(sum(p[i:j])+sum(q[i:j+1]))-dp[c]
                        assert A[i][j]==predicted
                        assert A[i][j]-Z[i][j]==h*sum(q[i:j+1])
                        counts['above_capacity_interval_checks']+=1
                        if j<n and j-i>c:
                            da=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
                            dz=Z[i][j+1]+Z[i+1][j]-Z[i][j]-Z[i+1][j+1]
                            assert da==dz
                            counts['gap_independent_density_checks']+=1
    print('above-capacity checks complete',flush=True)
    for h in range(4,13):
        for r in sorted(set([0,1,2,4,8,16])):
            n=(1<<h)-1-r
            if n<1:continue
            p=[(1<<60)+rng.randrange(1000) for _ in range(n)]
            q=[(1<<61)+rng.randrange(1000) for _ in range(n+1)]
            local=Counter();got=solve(p,q,h,local)
            keys,gaps=profile(got['tree'],n)
            assert max(keys)<=h and cost(got['tree'],p,q)==got['cost']
            assert proxy(got['slots'],p,q,h)==got['cost']
            if n<=128:assert reference(p,q,h,counts)==got['cost']
            assert local['states']==n*(r+1)
            # Each position is visited at most min(n,r+1) times, and sum nu_2<C.
            assert local['suffix_updates']+local['lower_level_scans']<=5*n*(r+1)
            rows.append(dict(n=n,h=h,slack=r,cost=got['cost'],counts=local,independent_reference=n<=128))
        print('scale',h,flush=True)
    root=Path(__file__).resolve().parents[1];sources=['mixed_slots.py','check_mixed_slots.py','research.py','aggregate_core_audit.py']
    out=dict(seed=28019,scope='Exact height-limited mixed-weight constructor; unrestricted optimality is not inferred from a height restriction',
             checks=counts,separation_example=separation,small_constructor_operations=ops,repair_operations=repair_ops,scale_rows=rows,
             source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in sources})
    (root/'results'/'mixed_slots.json').write_text(json.dumps(out,indent=2)+'\n')
    print(dict(counts),flush=True)
if __name__=='__main__':main()
