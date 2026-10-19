#!/usr/bin/env python3
"""All-root audit of gap-only core mass, binary upper bound, explicit lower family."""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib,json,random


def layers(q,H,M,stats):
    n=len(q)-1; pre=[0]
    for x in q:pre.append(pre[-1]+x)
    old=[[M*max(j-i,0) for j in range(n+1)] for i in range(n+1)]
    yield old
    for h in range(1,H+1):
        a=[[0]*(n+1) for _ in range(n+1)]
        for k in range(1,n+1):
            for i in range(n-k+1):
                j=i+k
                a[i][j]=pre[j+1]-pre[i]+min(old[i][r]+old[r+1][j] for r in range(i,j))
                stats['all_root_candidates']+=k;stats['dense_states']+=1
        yield a;old=a


def audit(q,stats,explicit=False):
    n=len(q)-1;W=sum(q);H=n.bit_length()+1;M=(H+1)*W+1;cores=[]
    for h,A in enumerate(layers(q,H,M,stats)):
        if h==0:cores.append(n);continue
        c=2**h-1;below=excess=support=0
        for i in range(n):
            for j in range(i+1,n):
                d=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
                assert d>=0;stats['density_checks']+=1;support+=d>0
                if j-i<c:below+=d;excess+=max(0,d-1)
                elif j-i>c:assert d==0;stats['above_capacity_zero_checks']+=1
                else:
                    Q=max(q[t] for t in range(i+1,i+c+1,2))
                    assert d==M-Q>0;stats['capacity_formula_checks']+=1
        core=n+support;cores.append(core)
        if c<=n:
            maxima=sum(max(q[t] for t in range(i+1,i+c+1,2)) for i in range(n-c))
            mass=(h-2)*W+q[0]+q[-1]+maxima
            assert below==mass
            assert core==2*n-c+mass-excess
            stats['mass_identity_checks']+=1
            for i in range(n-c+2):
                j=i+c-1
                Q=max(q[t] for t in range(i,j+1,2))
                assert A[i][j]==h*sum(q[i:j+1])-Q
                stats['one_missing_slot_checks']+=1
        else:
            assert below==A[0][n]-sum(q[i]+q[i+1] for i in range(n))
            stats['whole_triangle_identity_checks']+=1
        if n>=16 and n&(n-1)==0 and W==n//2 and max(q)<=1:
            s=n.bit_length()-1
            assert core<=(s+1)*n//2+4;stats['binary_bound_checks']+=1
        if explicit and h==n.bit_length():
            s=n.bit_length()-1;count=0
            for i in range(n):
                for j in range(i+1,n-1):
                    k=j-i
                    d=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
                    want=int(i%2==0 and ((k+1)&k)==0)
                    assert d==want;stats['explicit_density_checks']+=1;count+=want
            assert count==(s-2)*n//2+1
            assert core>=s*n//2+1
    stats['inputs']+=1
    return dict(n=n,mass=W,cores=cores,maximum_completed_core=max(cores))


def main():
    root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(29119)
    for n in range(1,9):
        for q in product((0,1),repeat=n+1):audit(q,stats)
    for n in range(1,6):
        for q in product((0,1,3),repeat=n+1):audit(q,stats)
    for n in (7,15,16,17,31,32):
        for _ in range(12):audit([rng.randrange(8) for _ in range(n+1)],stats)
    search=json.loads((root/'results/binary_core_search.json').read_text())
    winners=[]
    for n in (16,32,64,128):
        r=max((r for r in search['rows'] if r['n']==n and r['mode']=='gaps'),key=lambda r:r['maximum_completed_core'])
        a=audit(r['weights'][n:],stats)
        assert a['maximum_completed_core']==r['maximum_completed_core'];winners.append(a)
    family=[]
    for s in range(4,8):
        n=2**s;q=[int(i%2==0) for i in range(n)]+[0]
        family.append(audit(q,stats,explicit=True))
    files=['code/gap_core_identity.py','results/binary_core_search.json']
    result=dict(scope='Exact all-root controls; asymptotic claims are proved separately.',checks=stats,
                search_winner_controls=winners,explicit_family_controls=family,
                source_sha256={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in files})
    (root/'results/gap_core_identity.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
