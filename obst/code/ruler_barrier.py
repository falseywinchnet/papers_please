#!/usr/bin/env python3
"""Dense-core/fourth-difference barrier with an exact succinct cost oracle.

Positive mixed family p[r]=q[r]=B+r, B=4(n+1)^3. The constructor and formula
are specialized to this certified family. Dense tables below are independent
validation work, explicitly counted, not part of the specialized constructor.
"""
from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path

from research import cost, cubic, label, shapes


def v2(t):
    return (t & -t).bit_length()-1


def formula(i,j,B,stats):
    """Exact interval value using O(log(j-i+1)) integer arithmetic steps."""
    k=j-i
    stats['formula_queries']+=1
    if not k:return 0
    h=(k+1).bit_length()-1;c=(1<<h)-1;s=k-c
    ipl=(h-2)*(1<<h)+2+h*s
    d=2*ipl+3*k
    J=T=0
    for ell in range(1,h):
        power=1<<ell;m=c//power;u=min(m,s//power)
        J+=power*m*(m+1)//2-m
        T+=power*u*(u+1)//2+(m-u)*s
        stats['dyadic_sum_terms']+=1
    e=h*c*c-J+s*(2*h*c+h+1)+(h+3)*s*(s-1)-T
    return (B+i)*d+e


def construct(i,j,stats):
    if i==j:return None
    k=j-i;h=(k+1).bit_length()-1;slots=1<<h;s=k-(slots-1)
    r=i+slots//2-1+min(s,slots//2)
    stats['constructed_keys']+=1
    return r,construct(i,r,stats),construct(r+1,j,stats)


def dense(p,q,stats):
    n=len(p);a=[[0]*(n+1) for _ in range(n+1)];roots=[[0]*(n+1) for _ in range(n+1)]
    ps=[0];qs=[0]
    for x in p:ps.append(ps[-1]+x)
    for x in q:qs.append(qs[-1]+x)
    for k in range(1,n+1):
        for i in range(n-k+1):
            j=i+k;lo=i if k==1 else roots[i][j-1];hi=j-1 if k==1 else roots[i+1][j]
            best=None
            for r in range(lo,hi+1):
                z=a[i][r]+a[r+1][j]
                stats['dense_candidates']+=1
                if best is None or z<best:best=z;roots[i][j]=r
            a[i][j]=best+ps[j]-ps[i]+qs[j+1]-qs[i]
            stats['dense_states']+=1
    return a


def check(n,stats,enumerate_shapes=False):
    B=4*(n+1)**3;p=[B+i for i in range(n)];q=[B+i for i in range(n+1)]
    a=dense(p,q,stats)
    for i in range(n+1):
        for j in range(i,n+1):
            assert a[i][j]==formula(i,j,B,stats),(n,i,j)
            stats['interval_value_checks']+=1
    tree=construct(0,n,stats)
    assert cost(tree,p,q)==a[0][n]
    if n<=12:
        assert cubic(p,q)[0]==a[0][n];stats['cubic_checks']+=1
    if enumerate_shapes:
        for k in range(1,n+1):
            pp=p[:k];qq=q[:k+1]
            values=[]
            for shape in shapes(k):
                values.append(cost(label(shape)[0],pp,qq));stats['shape_checks']+=1
            assert min(values)==a[0][k]
            stats['enumerated_optima']+=1
    dd={}
    ruler_cells=fourth_ruler=0
    for i in range(n-1):
        for j in range(i+1,n):
            k=j-i;h=(k+1).bit_length()-1;c=(1<<h)-1;s=k-c
            z=a[i][j+1]+a[i+1][j]-a[i][j]-a[i+1][j+1]
            assert z>=0
            dd[i,j]=z
            if 1<=s<1<<h:
                assert z==3+v2(s),(n,i,j,z,s)
                ruler_cells+=1;stats['ruler_density_checks']+=1
    fourth=0;fourth_cells=0
    for (i,j),z in dd.items():
        if (i+1,j) not in dd or (i,j+1) not in dd or (i+1,j+1) not in dd:continue
        y=dd[i,j+1]+dd[i+1,j]-z-dd[i+1,j+1]
        fourth+=y!=0;fourth_cells+=1
        k=j-i;h=(k+1).bit_length()-1;s=k-((1<<h)-1)
        if 2<=s<=(1<<h)-2:
            assert y==v2(s+1)+v2(s-1)-2*v2(s) and y!=0
            fourth_ruler+=1;stats['fourth_ruler_checks']+=1
    lower=(n//4-3)*(n//2+2) if n>=32 and n&(n-1)==0 else None
    if lower is not None:assert fourth_ruler>=lower
    stats['solves']+=1
    return dict(n=n,baseline=B,cost=a[0][n],core=sum(x>0 for x in dd.values()),
                core_cells=len(dd),ruler_density_cells=ruler_cells,
                fourth_nonzero=fourth,fourth_cells=fourth_cells,
                fourth_ruler_cells=fourth_ruler,proved_quadratic_lower_bound=lower)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--max-n',type=int,default=512)
    args=parser.parse_args();stats=Counter();rows=[]
    for n in range(65):
        check(n,stats,enumerate_shapes=n<=8)
    n=128
    while n<=args.max_n:
        row=check(n,stats);rows.append(row);print(row,flush=True);n*=2
    # Query and construction counts are separated from all dense oracle work.
    scaling=[]
    for n in (1024,4096,16384,65536):
        fast=Counter();B=4*(n+1)**3
        value=formula(0,n,B,fast);t=construct(0,n,fast)
        p=[B+i for i in range(n)];q=[B+i for i in range(n+1)]
        assert cost(t,p,q)==value
        scaling.append(dict(n=n,cost=value,operations=dict(fast)))
        print('formula/constructor',scaling[-1],flush=True)
    root=Path(__file__).resolve().parents[1]
    result=dict(checks=dict(stats),rows=rows,constructor_scaling=scaling,
                implementation='specialized exact formula and constructor; separately counted dense audit',
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest()
                               for f in ('ruler_barrier.py','research.py')})
    (root/'results'/'ruler_barrier.json').write_text(json.dumps(result,indent=2)+'\n')
    print(dict(stats),flush=True)


if __name__=='__main__':main()
