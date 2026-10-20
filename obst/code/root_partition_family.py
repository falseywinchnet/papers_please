#!/usr/bin/env python3
"""Positive, mostly distinct family beyond all separable additive transfers."""
import hashlib
import json
from pathlib import Path
from root_partition import solve
from endpoint_prices import attempt as priced
from research import cubic,knuth
from shifted_alphabetic import tree_cost


def family(h):
    assert h>=3
    N=1<<h;n=N-1;r=N//4-1;C=4*h*N;w=h*N*N//2
    lengths=[h-((i+1)&-(i+1)).bit_length()+1 for i in range(n)]
    p=[1+(h-d)*N+i+1 for i,d in enumerate(lengths)]
    p[0]=p[-1]=p[2]=1;p[r]=w+1
    q=[C+j-1 for j in range(N)]
    return p,q


def perfect(lo,hi):
    if lo==hi:return None
    r=(lo+hi)//2
    return r,perfect(lo,r),perfect(r+1,hi)


def formulas(h):
    N=1<<h
    full=((8*h*h+6*h-7)*N*N+(12-5*h)*N)//2+1-3*h
    deficit=(h*N*N-(2*h-1)*N)//2
    return full,full-deficit,deficit


def main():
    rows=[]
    for h in (3,4,5,6,7,8,9,10,12,14,16,18):
        p,q=family(h);n=len(p)
        value,tree,stats=solve(p,q);expected,separable,deficit=formulas(h)
        assert value==expected==tree_cost(tree,p,q)==tree_cost(perfect(0,n),p,q)
        assert stats['certified'] and stats['alphabetic_calls']==3
        assert stats['separable_lower_bound']==separable
        assert len(set(p))==n-2 and len(set(q))==n+1
        assert min(p+q)>0 and stats['largest_residual']-stats['second_residual']==deficit
        assert stats['nonroot_lower_bound']==value<=stats['fixed_root_lower_bound']
        if h<=9:assert knuth(p,q)[0]==value
        if h<=5:assert cubic(p,q)[0]==value
        if h<=8:
            old,_,oldstats,meta=priced(p,q,budget=100,stop_on_certificate=False)
            assert old is None and meta['max_complete'] and meta['lower']==separable
        row=dict(h=h,n=n,cost=value,separable_maximum=separable,deficit=deficit,
                 distinct_keys=len(set(p)),distinct_gaps=len(set(q)),stats=dict(stats))
        rows.append(row);print(h,n,value,'deficit',deficit,'calls',stats['alphabetic_calls'],flush=True)
    result=dict(rows=rows,source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest()
       for f in ('root_partition_family.py','root_partition.py','shifted_alphabetic.py','endpoint_prices.py','research.py')})
    (Path(__file__).resolve().parents[1]/'results'/'root_partition_family.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
