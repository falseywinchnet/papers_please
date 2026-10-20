#!/usr/bin/env python3
"""Independent domination, literal subsequences, all-root layers, and dense formulas."""
from collections import Counter
from fractions import Fraction
from itertools import product,combinations
from pathlib import Path
import hashlib,json,random
from valley_above import ValleyAbove,valley_floor,largest_end_split,dense_valley,dense_valley_density
from aggregate_core_audit import layers


def literal_valley(p):
    return any(all(p[i]>=p[i+1] for i in range(z)) and all(p[i]<=p[i+1] for i in range(z,len(p)-1)) for z in range(len(p)))


def nu(r):return (r&-r).bit_length()-1


def original(p,q,stats,dense_s=None,density_scale=1):
    n=len(p);H=n.bit_length();M=(H+1)*(sum(p)+sum(q))+1
    obj=ValleyAbove(p,q,stats)
    for h,A in enumerate(layers(p,q,H,M,stats)):
        c=(1<<h)-1
        if not h or c>n:continue
        for i in range(n):
            for j in range(i+c,n+1):
                value,blocks=obj.layer(h,i,j,M)
                assert value==A[i][j],(p,q,h,i,j,value,A[i][j])
                indices=[x for a,b in blocks for x in range(a,b)]
                assert len(indices)==c and indices==sorted(set(indices))
                reward=sum(p[x]*nu(r) for r,x in enumerate(indices,1))
                assert value==M*(j-i-c)+h*(sum(p[i:j])+sum(q[i:j+1]))-reward
                stats['original_interval_controls']+=1;stats['witness_controls']+=1
        if dense_s and c==2*dense_s-1:
            count=0
            for i in range(dense_s):
                for j in range(3*dense_s,4*dense_s):
                    d=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
                    assert d==density_scale*dense_valley_density(dense_s,i,j)
                    count+=d>0;stats['original_dense_formula_cells']+=1
            assert count==dense_s*dense_s//2
    stats['original_inputs']+=1


def main():
    root=Path(__file__).resolve().parents[1];rng=random.Random(461019)
    stats=Counter();large=[]
    for n in range(1,9):
        for p in product(range(3),repeat=n):
            valid=literal_valley(p)
            try:z=valley_floor(p)
            except ValueError:
                assert not valid;stats['nonvalleys_rejected']+=1;continue
            assert valid;stats['exhaustive_valley_words']+=1
            for c in range(1,n+1):
                t=largest_end_split(p,0,n,c,z,stats)
                chosen=tuple(range(t))+tuple(range(n-c+t,n));word=[p[x] for x in chosen]
                weights=[rng.randrange(8) for _ in range(c)]
                best=None
                for ts in combinations(range(n),c):
                    assert all(v>=p[x] for v,x in zip(word,ts))
                    score=sum(w*p[x] for w,x in zip(weights,ts))
                    best=score if best is None else max(best,score)
                    stats['literal_domination_controls']+=1
                assert sum(v*w for v,w in zip(word,weights))==best
                stats['arbitrary_reward_controls']+=1
            if n<=5:original(list(p),[rng.randrange(5) for _ in range(n+1)],stats)
        print('exhaustive',n,flush=True)
    for n in (6,7,8,12,16,24,32):
        for trial in range(12):
            z=rng.randrange(n)
            if trial==0:p=list(range(n))
            elif trial==1:p=list(range(n,0,-1))
            elif trial==2:p=[3]*n
            elif trial==3:p=[1<<abs(i-z) for i in range(n)]
            else:p=sorted((rng.randrange(12) for _ in range(z)),reverse=True)+[0]+sorted(rng.randrange(12) for _ in range(n-z-1))
            q=[rng.randrange(6) for _ in range(n+1)]
            if trial==11:p=[Fraction(x,7) for x in p];q=[Fraction(x,5) for x in q]
            original(p,q,stats)
        print('mixed',n,flush=True)
    for s in (4,8,16):
        original(dense_valley(s),[rng.randrange(4) for _ in range(4*s+1)],stats,s)
        original([Fraction(x,4*s) for x in dense_valley(s)],[0]*(4*s+1),stats,s,Fraction(1,4*s))
    # Large queries construct no dense layer. Sampled literal top-c enumeration
    # and formula controls are separate from the original recurrence above.
    for n in (64,127,256,1023,4096,16384,65536):
        for kind in ('distinct_valley','irregular_valley'):
            if kind=='distinct_valley':
                p=list(range(2*(n//2),0,-2))+list(range(1,2*(n-n//2),2))
            else:
                z=n//3;p=sorted((rng.randrange(n) for _ in range(z)),reverse=True)+[0]+sorted(rng.randrange(n) for _ in range(n-z-1))
            local=Counter();obj=ValleyAbove(p,[0]*(n+1),local)
            for _ in range(64):
                i=rng.randrange(n);j=rng.randrange(i+1,n+1)
                h=rng.randrange(1,(j-i+1).bit_length());c=(1<<h)-1
                reward,blocks=obj.score(h,i,j)
                selected=sorted(sorted(range(i,j),key=lambda x:(-p[x],x))[:c])
                expected=sum(p[x]*nu(r) for r,x in enumerate(selected,1))
                assert reward==expected
                local['large_literal_top_key_controls']+=1
                # Prefix routines checked at arbitrary lengths, not just capacities.
                length=rng.randrange(n-i+1)
                expected=sum(p[i+r-1]*nu(r) for r in range(1,length+1))
                assert obj.forward.query(i,length)==expected
                local['large_literal_prefix_controls']+=1
            if kind=='distinct_valley' and n>=16 and n&(n-1)==0:
                s=n//4;h=(2*s).bit_length()-1
                for _ in range(128):
                    i=rng.randrange(s);j=rng.randrange(3*s,4*s)
                    vals=[obj.score(h,a,b)[0] for a,b in ((i,j),(i,j+1),(i+1,j),(i+1,j+1))]
                    assert vals[0]+vals[3]-vals[1]-vals[2]==dense_valley_density(s,i,j)
                    local['large_sampled_dense_formula_cells']+=1
            large.append(dict(n=n,kind=kind,counts=dict(local),verification='implicit query construction, sampled literal top-key selections and prefix sums, and sampled formula cells; no original all-root layer at this size'))
            print('scale',n,kind,flush=True)
    files=('valley_above.py','valley_above_audit.py','unimodal_above.py','aggregate_core_audit.py')
    result=dict(scope='Exact above-capacity implicit queries for valley keys with arbitrary nonnegative gaps; explicit quadratic original interval-core family; no full-BST solver claim.',checks=dict(stats),scale_rows=large,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/valley_above_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(dict(stats),flush=True)


if __name__=='__main__':main()
