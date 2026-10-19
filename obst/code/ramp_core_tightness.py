#!/usr/bin/env python3
"""Independent controls for the odd-ramp core lower bound; no fitted exponent."""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
from penalty_layers import fib_limit

def nu(t):return (t & -t).bit_length()-1

def choose_score(values,m):
    dp=[0]+[-10**30]*m
    for v in values:
        for r in range(m,0,-1):dp[r]=max(dp[r],dp[r-1]+(2*r-1)*v)
    return dp[m]

def deletion_score(values,m):
    skip=len(values)-m;omitted=set()
    for i in range(len(values)-1,-1,-1):
        if skip and values[i]==0:omitted.add(i);skip-=1
    assert skip==0
    return sum((2*r-1)*v for r,v in enumerate((x for i,x in enumerate(values) if i not in omitted),1))

def layer(n,h,p,counts,all_roots=False):
    W=sum(p);H=min(n,fib_limit(W)+n.bit_length());M=(H+1)*W+1
    old=[[M*(j-i) if j>=i else 0 for j in range(n+1)] for i in range(n+1)]
    pre=[0]
    for x in p:pre.append(pre[-1]+x)
    for depth in range(1,h+1):
        cur=[[0]*(n+1) for _ in range(n+1)];rr=[[0]*(n+1) for _ in range(n+1)]
        for size in range(1,n+1):
            for i in range(n-size+1):
                j=i+size
                lo=i if all_roots or size==1 else rr[i][j-1]
                hi=j-1 if all_roots or size==1 else rr[i+1][j]
                v,r=min((old[i][r]+old[r+1][j],r) for r in range(lo,hi+1))
                cur[i][j]=pre[j]-pre[i]+v;rr[i][j]=r
                counts['layer_states']+=1;counts['root_candidates']+=hi-lo+1
        old=cur
    return old

def main():
    counts=Counter();rows=[]
    # Independent subset enumeration before the larger dynamic-programming checks.
    for h in range(2,5):
        v=[nu(t) for t in range(1,1<<h)]
        for a in range(len(v)):
            for b in range(a+1,min(len(v),a+9)+1):
                for m in range(1,min(5,b-a)+1):
                    brute=max(sum((2*r-1)*v[t] for r,t in enumerate(ts,1))
                              for ts in itertools.combinations(range(a,b),m))
                    assert brute==choose_score(v[a:b],m)
                    counts['literal_subsequence_checks']+=1
    # All-root interval recurrence versus the subsequence embedding, with no size claim.
    for n,m,h in ((16,4,3),(32,4,4),(64,8,5)):
        start=(n-m)//2;p=[0]*n;p[start:start+m]=range(1,2*m,2)
        A=layer(n,h,p,counts,True);c=(1<<h)-1
        for i in range(start+1):
            for j in range(start+m,n+1):
                if j-i>c:continue
                a=start-i;b=c-j+start+m
                value=h*sum(p)-choose_score([nu(t+1) for t in range(a,b)],m)
                assert A[i][j]==value
                counts['all_root_embedding_checks']+=1
    for t in (5,6,7,8):
        m=1<<t;n=m*m;h=2*t-1;c=(1<<h)-1;start=(n-m)//2;D=h-1
        assert m>2*(m//4+1)+D
        p=[0]*n;p[start:start+m]=range(1,2*m,2);assert sum(p)==n
        A=layer(n,h,p,counts) if t==5 else None
        cells=0;mass=0
        # For t<=6, use independent DP for every required ruler window.
        # Larger cases count the proved explicit coordinates/formula, not fresh DP.
        F={}
        if t<=6:
            v=[nu(k+1) for k in range(c)]
            for a in range(c-m):
                dp=[0]+[-10**30]*m
                for b in range(a,min(c,a+m+m//4+2)):
                    for r in range(m,0,-1):dp[r]=max(dp[r],dp[r-1]+(2*r-1)*v[b])
                    if b-a+1>=m:
                        F[a,b+1]=dp[m]
                        s=b-a+1-m
                        if m>2*s+D:
                            assert dp[m]==deletion_score(v[a:b+1],m)
                            counts['rightmost_zero_formula_checks']+=1
        for s in range(1,m//4+1):
            for a in range(1,c-m-s):
                b=a+m+s
                if b%2:continue
                predicted=2*nu(b-2*s);assert predicted>0
                if t<=6:
                    got=-(F[a-1,b]+F[a,b-1]-F[a-1,b-1]-F[a,b])
                    assert got==predicted
                    counts['subsequence_density_checks']+=1
                if A is not None:
                    i=start-a;j=c-b+start+m
                    got=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
                    assert got==predicted
                    assert A[i][j]==h*n-F[a,b]
                    counts['original_layer_density_checks']+=1
                cells+=1;mass+=predicted
        exact=n*m//16-9*n//64-m//4
        assert cells==exact and cells>=n*m//32
        row=dict(n=n,m=m,W=n,h=h,explicit_core_cells=cells,density_mass=mass,
                 independent_subsequence_dp=(t<=6),independent_original_layer=(t==5))
        rows.append(row);print(row,flush=True)
    root=Path(__file__).resolve().parents[1]
    files=['ramp_core_tightness.py','penalty_layers.py','research.py']
    report=dict(scope='Exact checks of a separately proved Omega(n^(3/2)) lower bound with W=n; larger rows evaluate the proved formula, not an independent solve',
                checks=counts,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results'/'ramp_core_tightness.json').write_text(json.dumps(report,indent=2)+'\n')
    print(dict(counts),flush=True)

if __name__=='__main__':main()
