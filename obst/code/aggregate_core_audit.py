#!/usr/bin/env python3
"""Independent integer audit of per-outcome tiling and aggregate layer bounds.

Dense all-root recurrence is a diagnostic, not the sparse constructor.
No runtime measurements are used as complexity evidence.
"""
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path
import hashlib
import json
import random


def partition(N, c):
    assert N > 0 and N & (N-1) == 0
    tiles = defaultdict(list)
    exceptional = []
    def visit(a,b,s):
        if b+s-1 <= a:
            return
        lo, hi = b-a-s+1, b-a+s-1
        hit = lo <= 0 <= hi or lo <= c <= hi
        if not hit:
            assert a+s <= b
            tiles[s].append((a,b))
        elif s == 1:
            if a < b:
                exceptional.append((a,b))
        else:
            t=s//2
            for da,db in ((0,0),(t,0),(0,t),(t,t)):
                visit(a+da,b+db,t)
    visit(0,0,N)
    assert sum(s*s*len(ts) for s,ts in tiles.items())+len(exceptional)==N*(N-1)//2
    return tiles, exceptional


def geometry(n,h,stats):
    N=1<<(n-1).bit_length(); c=(1<<h)-1
    tiles, exceptional=partition(N,c)
    rows=[]
    for s,ts in sorted(tiles.items()):
        delta=[0]*(N+2)
        for a,b in ts:
            # Its rejected parent must intersect one of the two diagonals.
            A=a//(2*s)*(2*s); B=b//(2*s)*(2*s)
            assert any(abs(B-A-d)<2*s for d in (0,c))
            assert any(abs(b-a-d)<3*s for d in (0,c))
            delta[a]+=1; delta[b+s+1]-=1
        running=maximum=0
        for x in range(N+1):
            running+=delta[x]; maximum=max(maximum,running)
            assert running*s<=60*(s+c)
            stats['outcome_overlap_checks']+=1
        assert len(ts)*s<=24*n
        rows.append(dict(side=s,tiles=len(ts),maximum_overlap=maximum))
        stats['geometry_scales']+=1
        stats['geometry_tiles']+=len(ts)
    stats['geometry_partitions']+=1
    return dict(n=n,padded_n=N,h=h,exceptional=len(exceptional),scales=rows)


def layers(p,q,H,M,stats):
    n=len(p); old=[[M*max(j-i,0) for j in range(n+1)] for i in range(n+1)]
    yield old
    for h in range(1,H+1):
        cur=[[0]*(n+1) for _ in range(n+1)]
        for k in range(1,n+1):
            for i in range(n-k+1):
                j=i+k
                cur[i][j]=sum(p[i:j])+sum(q[i:j+1])+min(old[i][r]+old[r+1][j] for r in range(i,j))
                stats['all_root_candidates']+=k
                stats['dense_states']+=1
        yield cur
        old=cur


def instance(p,q,stats):
    n=len(p); N=1<<(n-1).bit_length(); L=n.bit_length(); W=sum(p)+sum(q)
    a,b,f=0,1,0
    while a<=W:a,b,f=b,a+b,f+1
    H=min(n,f+L); M=(H+1)*W+1
    originals=layers(p,q,H,M,stats)
    padded=layers(p+[0]*(N-n),q+[0]*(N-n),H,M,stats)
    counts=[]
    for h,(A,B) in enumerate(zip(originals,padded)):
        assert all(A[i][j]==B[i][j] for i in range(n+1) for j in range(i,n+1))
        stats['padding_layer_checks']+=1
        if h==0:
            counts.append(n); continue
        c=(1<<h)-1
        density={(i,j):B[i][j+1]+B[i+1][j]-B[i][j]-B[i+1][j+1]
                 for i in range(N) for j in range(i+1,N)}
        assert all(v>=0 for v in density.values())
        for i in range(N):
            for j in range(i+1,N+1):
                mass=sum(p[i:min(j,n)])+sum(q[i:min(j,n)+1]) if i<=n else 0
                assert 0<=B[i][j]-M*max(0,j-i-c)<=h*mass
                stats['residual_checks']+=1
        K=n+sum(v>0 for (i,j),v in density.items() if j<n)
        counts.append(K)
        if h>=L:
            assert K<=n+L*W
            stats['late_layer_checks']+=1
            continue
        tiles, exceptional=partition(N,c)
        covered=sum(density[i,j]>0 for i,j in exceptional if j<n)
        for s,ts in tiles.items():
            summed_mass=0; positive=0
            for a,b in ts:
                # The inclusive gap span [a,b+s] bounds both positive corners.
                mass=sum(p[a:min(b+s,n)])+sum(q[a:min(b+s,n)+1]) if a<=n else 0
                summed_mass+=mass
                vals=[density[i,j] for i in range(a,a+s) for j in range(b,b+s)]
                assert sum(vals)==B[a][b+s]+B[a+s][b]-B[a][b]-B[a+s][b+s]
                assert 0<=sum(vals)<=2*h*mass
                assert sum(v>0 for v in vals)<=min(s*s,2*h*mass)
                positive+=sum(v>0 for v in vals)
                covered+=sum(density[i,j]>0 for i in range(a,min(a+s,n)) for j in range(b,min(b+s,n)))
                stats['weighted_tiles']+=1
            assert s*summed_mass<=60*W*(s+c)
            assert positive<=len(ts)*s*s
            assert positive<=2*h*summed_mass
            # Rational bound stored with denominator s to avoid rounding.
            assert positive*s<=min(24*n*s*s,120*h*W*(s+c))
            stats['weighted_scales']+=1
        assert covered==K-n
        stats['early_layer_checks']+=1
    stats['instances']+=1
    return dict(n=n,W=W,H=H,core_sum=sum(counts),maximum_core=max(counts),cores=counts)


def main():
    stats=Counter(); geometry_rows=[]; instance_rows=[]; rng=random.Random(26019)
    sizes=list(range(1,130))+[255,256,257,511,512,513,1023,1024,1025,2047,2048,2049]
    for n in sizes:
        for h in range(1,n.bit_length()):geometry_rows.append(geometry(n,h,stats))
    print('geometry',dict(stats),flush=True)
    for n in range(1,4):
        for v in product((0,1),repeat=2*n+1):instance(list(v[:n]),list(v[n:]),stats)
    for n in list(range(4,18))+[23,31,32,33]:
        fixtures=[([0]*n,[0]*(n+1)),([1]*n,[1]*(n+1)),
                  ([rng.randrange(4) for _ in range(n)],[rng.randrange(4) for _ in range(n+1)]),
                  ([0]*n,[0]*n+[n]),([0]*n,[n]+[0]*n),
                  ([0]*(n//2)+[n]+[0]*(n-n//2-1),[0]*(n+1))]
        if n<=17:fixtures.append(([1<<i for i in range(n)],[1<<min(i,n-i) for i in range(n+1)]))
        for p,q in fixtures:instance_rows.append(instance(p,q,stats))
        print('weights',n,flush=True)
    root=Path(__file__).resolve().parents[1]
    out=dict(seed=26019,counts=dict(stats),geometry=geometry_rows,instances=instance_rows,
             source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
             scope='Independent dense diagnostics; the asymptotic bound follows from the proof, not these counts.')
    (root/'results'/'aggregate_core_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(dict(stats),flush=True)
if __name__=='__main__':main()
