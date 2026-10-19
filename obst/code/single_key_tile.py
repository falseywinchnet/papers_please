#!/usr/bin/env python3
"""Exact one-key core formula and obstruction to constant local tile charging."""
from collections import Counter
from pathlib import Path
import hashlib,json
from aggregate_core_audit import partition
from ramp_core_tightness import layer
from penalty_layers import fib_limit


def vmax(lo,hi,h):
    assert 1<=lo<=hi<(1<<h)
    return max(d for d in range(h) if (lo+(1<<d)-1)//(1<<d)<=hi//(1<<d))


def value(i,j,x,h,M):
    c=(1<<h)-1;k=j-i
    penalty=M*max(0,k-c)
    if not i<=x<j:return penalty
    u=x-i+1;l=c+x+1-j
    lo=max(1,min(u,l));hi=min(c,max(u,l))
    return penalty+h-vmax(lo,hi,h)


def supports(h):
    n=1<<(h+1);c=(1<<h)-1;x=(1<<h)+1
    below=set();above=set()
    for d in range(1,h):
        step=1<<d
        for k in range(1<<(h-d)):
            a=k*step;b=a+step
            i=x-a;j=c+x+1-b
            assert 0<=i<j<n and j-i<c
            assert (i,j) not in below
            below.add((i,j))
            if 0<a<b<c+1:
                i=x+1-b;j=c+x-a
                assert 0<=i<j<n and j-i>c
                assert (i,j) not in above
                above.add((i,j))
    assert len(below)==(1<<h)-2
    assert len(above)==(1<<h)-2*h
    return below,above


def main():
    counts=Counter();rows=[]
    for h in range(3,10):
        n=1<<(h+1);c=(1<<h)-1;x=(1<<h)+1;s=1<<(h-2)
        p=[0]*n;p[x]=1;H=min(n,fib_limit(1)+n.bit_length());M=H+2
        A=layer(n,h,p,counts,all_roots=h<=5)
        below,above=supports(h);ordinary=below|above;observed=set()
        for i in range(n):
            for j in range(i+1,n+1):
                assert A[i][j]==value(i,j,x,h,M)
                counts['interval_formula_checks']+=1
                if j==n:continue
                density=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
                if j-i==c:
                    assert density>0;counts['penalty_line_checks']+=1
                else:
                    assert density==int((i,j) in ordinary),(h,i,j,density)
                    if density:observed.add((i,j))
                counts['density_formula_checks']+=1
        assert observed==ordinary
        completed=n+(n-c)+len(ordinary)
        assert completed==2*n+(1<<h)-2*h-1
        tiles,_=partition(n,c)
        assert (2*s,7*s) in tiles[s]
        tile_cells={(3*s+2-(1<<d),7*s) for d in range(2,h-1)}
        actual={(i,j) for i,j in ordinary if 2*s<=i<3*s and 7*s<=j<8*s}
        assert actual==tile_cells and len(actual)==h-3
        density=A[2*s][8*s]+A[3*s][7*s]-A[2*s][7*s]-A[3*s][8*s]
        assert density==h-3
        row=dict(h=h,n=n,W=1,key_position=x,completed_core=completed,
                 below_capacity_core=len(below),above_capacity_core=len(above),
                 tile_side=s,tile_core=h-3,tile_density_mass=density,
                 verification='all-root recurrence' if h<=5 else 'monotone-root recurrence')
        rows.append(row);print(row,flush=True)
    # The general linear-core corollary: every possible key position, two masses.
    for n in range(1,17):
        for x in range(n):
            for weight in (1,17):
                p=[0]*n;p[x]=weight
                for h in range(1,min(n,n.bit_length()+1)+1):
                    A=layer(n,h,p,counts,all_roots=True)
                    c=(1<<h)-1
                    expected=set()
                    for d in range(1,h):
                        step=1<<d
                        for k in range(1<<(h-d)):
                            a=k*step;b=a+step
                            i=x-a;j=c+x+1-b
                            if 0<=i<j<n:expected.add((i,j))
                            if 0<a<b<c+1:
                                i=x+1-b;j=c+x-a
                                if 0<=i<j<n:expected.add((i,j))
                    observed=set()
                    for i in range(n):
                        for j in range(i+1,n):
                            density=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
                            if j-i==c:assert density>0
                            else:
                                assert density==weight*int((i,j) in expected)
                                if density:observed.add((i,j))
                            counts['general_density_checks']+=1
                    assert observed==expected
                    assert n+max(0,n-c)+len(expected)<=3*n
                    counts['general_single_key_cases']+=1
    print('general one-key controls complete',flush=True)
    # Large rows evaluate only the proved formulas, not dense interval tables.
    for h in [10,12,16,20,24,30]:
        n=1<<(h+1);s=1<<(h-2);x=(1<<h)+1;M=h+10
        corners=[value(i,j,x,h,M) for i,j in [(2*s,8*s),(3*s,7*s),(2*s,7*s),(3*s,8*s)]]
        assert corners[0]+corners[1]-corners[2]-corners[3]==h-3
        rows.append(dict(h=h,n=n,W=1,key_position=x,completed_core=2*n+(1<<h)-2*h-1,
                         tile_side=s,tile_core=h-3,verification='closed-form evaluation only'))
    root=Path(__file__).resolve().parents[1]
    sources=['single_key_tile.py','aggregate_core_audit.py','ramp_core_tightness.py','penalty_layers.py','research.py']
    result=dict(scope='Independent recurrence controls for a proved local charging obstruction and exact linear core family',
                counts=counts,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in sources})
    (root/'results'/'single_key_tile.json').write_text(json.dumps(result,indent=2)+'\n')
    print(dict(counts),flush=True)
if __name__=='__main__':main()
