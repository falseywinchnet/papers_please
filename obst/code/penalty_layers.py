#!/usr/bin/env python3
"""Dense reference audit for a proposed core-sparse Monge OBST reduction.

This does NOT implement the cited sparse product. Dense states and candidate
counts remain explicit. The terminal penalty, padding, core accounting, and
complete tree reconstruction are checked independently on small instances.
"""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random

from research import check_weights, cost, cubic, knuth, label, shapes


def fib_limit(w):
    a, b, h = 0, 1, 0
    while a <= w:
        a, b, h = b, a+b, h+1
    return h


def core(c):
    n = len(c)-1
    return {(i,j): c[i][j+1]+c[i+1][j]-c[i][j]-c[i+1][j+1]
            for i in range(n-1) for j in range(i+1,n)}


def tile_audit(c, h, penalty, w, stats):
    """Certify the dyadic count bound; dense diagnostic, not an extractor."""
    n=len(c)-1; cap=(1<<h)-1; N=1<<(n-1).bit_length()
    dd=core(c); result=Counter()
    def rem(i,j):
        return c[i][j]-penalty*max(0,j-i-cap)
    def visit(a,b,s):
        if a>=n or b>=n or b+s-1<a: return
        if a+s>n or b+s>n:
            assert s>1
            t=s//2
            for x,y in ((a,b),(a+t,b),(a,b+t),(a+t,b+t)):visit(x,y,t)
            return
        lo,hi=b-(a+s-1),b+s-1-a
        hits=(lo<=0<=hi) or (lo<=cap<=hi)
        if hits and s>1:
            t=s//2
            for x,y in ((a,b),(a+t,b),(a,b+t),(a+t,b+t)):visit(x,y,t)
        elif hits:
            if a<b:
                result['exceptional_core']+=int(dd[a,b]>0)
        else:
            assert a+s<=b
            total=rem(a,b+s)+rem(a+s,b)-rem(a,b)-rem(a+s,b+s)
            actual=sum(dd[i,j] for i in range(a,a+s) for j in range(b,b+s))
            count=sum(dd[i,j]>0 for i in range(a,a+s) for j in range(b,b+s))
            assert total==actual and 0<=total<=2*h*w
            assert count<=min(s*s,total)
            result['tiles']+=1
            result['tile_count_bound']+=min(s*s,total)
            result['ordinary_core']+=count
    visit(0,0,N)
    assert result['ordinary_core']+result['exceptional_core']==sum(v>0 for v in dd.values())
    stats['verified_dyadic_tiles']+=result['tiles']
    return dict(result)


def solve(p,q,stats,deep=False,tiles=False):
    check_weights(p,q); n=len(p); w=sum(p)+sum(q)
    # Zero-mass terminal subtrees may be balanced after the positive-mass part.
    extra=0 if all(x>0 for x in p) else n.bit_length()
    H=min(n,fib_limit(w)+extra)
    M=(H+1)*w+1
    padding=4*n*M+4*w+1
    prefix=[0]
    for a,b in zip(p,q[1:]):prefix.append(prefix[-1]+a+b)
    def mass(i,j):return prefix[j]-prefix[i]+q[i]
    old=[[M*(j-i) if j>=i else 0 for j in range(n+1)] for i in range(n+1)]
    roots=[]; rows=[]
    expected,_,_=knuth(p,q)
    first_equal=None
    for h in range(1,H+1):
        current=[[0]*(n+1) for _ in range(n+1)]
        rr=[[0]*(n+1) for _ in range(n+1)]
        for length in range(1,n+1):
            for i in range(n-length+1):
                j=i+length
                lo=i if length==1 else rr[i][j-1]
                hi=j-1 if length==1 else rr[i+1][j]
                value,r=min((old[i][r]+old[r+1][j],r) for r in range(lo,hi+1))
                stats['dense_root_candidates']+=hi-lo+1
                stats['dense_states']+=1
                current[i][j]=mass(i,j)+value;rr[i][j]=r
                assert current[i][j]<=old[i][j]
                cap=(1<<h)-1
                rem=current[i][j]-M*max(0,j-i-cap)
                assert 0<=rem<=h*mass(i,j)
                if deep:
                    brute=min((old[i][r]+old[r+1][j],r) for r in range(i,j))
                    assert brute==(value,r)
                    stats['all_root_cell_checks']+=1
        dd=core(current)
        assert all(v>=0 for v in dd.values())
        density=sum(dd.values())
        assert density==current[0][n]-sum(current[i][i+1] for i in range(n))
        if deep:
            def ext(i,j):return old[i][j] if i<=j else padding*(i-j)
            full=[[ext(i,j) for j in range(n+1)] for i in range(n+1)]
            assert all(full[i][j+1]+full[i+1][j]-full[i][j]-full[i+1][j+1]>=0
                       for i in range(n) for j in range(n))
            product=[[min(ext(i,r)+ext(r+1,j) for r in range(n))
                      for j in range(n+1)] for i in range(n+1)]
            assert all(product[i][j]+mass(i,j)==current[i][j]
                       for i in range(n) for j in range(i+1,n+1))
            stats['padded_products_checked']+=1
            def truncated(t,i,j,budget):
                if i==j:return 0
                if budget==0:return M*(j-i)
                r,left,right=t
                return mass(i,j)+truncated(left,i,r,budget-1)+truncated(right,r+1,j,budget-1)
            assert min(truncated(label(s)[0],0,n,h) for s in shapes(n))==current[0][n]
            stats['all_shape_layer_checks']+=1
        row=dict(h=h,nonzero_core=sum(v>0 for v in dd.values()),
                 density_mass=density,full_value=current[0][n])
        if (1<<h)-1>=n:
            assert current[0][n]<=n.bit_length()*w
            assert row['nonzero_core']<=n.bit_length()*w
        if tiles:row['tiling']=tile_audit(current,h,M,w,stats)
        if current[0][n]==expected and first_equal is None:first_equal=h
        roots.append(rr);rows.append(row);old=current
    assert old[0][n]==expected
    def tree(i,j,h):
        if i==j:return None
        assert h>0,('unresolved terminal',p,q,i,j)
        r=roots[h-1][i][j]
        stats['constructed_keys']+=1
        return r,tree(i,r,h-1),tree(r+1,j,h-1)
    result=tree(0,n,H)
    assert cost(result,p,q)==expected
    if n<=9:
        assert cubic(p,q)[0]==expected
        for i in range(n):
            for j in range(i+1,n+1):
                assert old[i][j]==cubic(p[i:j],q[i:j+1])[0]
                stats['cubic_interval_checks']+=1
    stats['complete_solves']+=1
    return dict(n=n,mass=w,height_budget=H,penalty=M,
                first_global_exact_layer=first_equal,cost=expected,layers=rows)


def main():
    rng=random.Random(380713);stats=Counter();rows=[]
    # Exhaustive mixed nonnegative inputs, including all-zero and one-sided cases.
    for n in range(1,5):
        for v in itertools.product((0,1),repeat=2*n+1):
            solve(list(v[:n]),list(v[n:]),stats,deep=n<=3)
        print('binary exhaustive',n,flush=True)
    for n in range(1,33):
        for t in range(12):
            p=[rng.randrange(20) for _ in range(n)]
            q=[rng.randrange(20) for _ in range(n+1)]
            solve(p,q,stats,deep=n<=7,tiles=t==0)
        print('random',n,flush=True)
    for n in (32,64,128,256):
        fixtures={
          'uniform':([1]*n,[1]*(n+1)),
          'mixed_binary':([1+rng.randrange(2) for _ in range(n)],[1+rng.randrange(2) for _ in range(n+1)]),
          'near_uniform':([100+rng.randrange(3) for _ in range(n)],[100+rng.randrange(3) for _ in range(n+1)]),
          'random_16':([1+rng.randrange(16) for _ in range(n)],[1+rng.randrange(16) for _ in range(n+1)]),
          'alternating':([1+(i%2) for i in range(n)],[2-(i%2) for i in range(n+1)]),
          'sparse_positive':([int(rng.randrange(8)==0) for _ in range(n)],[int(rng.randrange(8)==0) for _ in range(n+1)]),
        }
        if n<=64:
            fixtures['geometric']=([1<<i for i in range(n)],[1<<i for i in range(n+1)])
            fixtures['folded']=([1<<min(i,n-1-i) for i in range(n)],[1<<min(i,n-i) for i in range(n+1)])
        for name,(p,q) in fixtures.items():
            row=solve(p,q,stats,tiles=True);row['family']=name
            rows.append(row)
            print(name,n,'H',row['height_budget'],'exact',row['first_global_exact_layer'],
                  'max core',max(x['nonzero_core'] for x in row['layers']),flush=True)
    target=Path(__file__).resolve().parents[1]/'results'/'penalty_layers.json'
    target.write_text(json.dumps(dict(seed=380713,counts=stats,rows=rows,
      implementation='dense diagnostic; sparse multiplication not implemented',
      source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')
    print(dict(stats),flush=True)

if __name__=='__main__':main()
