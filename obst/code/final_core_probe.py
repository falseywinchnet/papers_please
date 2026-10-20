#!/usr/bin/env python3
"""Exact diagnostic of final unrestricted cores under certified shallow optima.

Dense reference work is counted. This is a falsification/direction harness,
not a sparse constructor or an empirical complexity proof.
"""
from collections import Counter
from pathlib import Path
import hashlib,json,random
from research import cubic,cost


def table(p,q,stats,all_roots=False):
    n=len(p);C=[[0]*(n+1) for _ in range(n+1)];R=[[0]*(n+1) for _ in range(n+1)]
    pref=[0]
    for a,b in zip(p,q[1:]):pref.append(pref[-1]+a+b)
    for m in range(1,n+1):
        for i in range(n-m+1):
            j=i+m
            lo=i if all_roots or m==1 else R[i][j-1]
            hi=j-1 if all_roots or m==1 else R[i+1][j]
            best=None
            for r in range(lo,hi+1):
                v=C[i][r]+C[r+1][j];stats['reference_root_candidates']+=1
                if best is None or v<best:best=v;R[i][j]=r
            C[i][j]=best+pref[j]-pref[i]+q[i];stats['reference_interval_states']+=1
    return C,R


def profile(C,stats):
    n=len(C)-1;bylength=Counter();rows=[]
    for i in range(n):
        row=[]
        for j in range(i+1,n):
            d=C[i][j+1]+C[i+1][j]-C[i][j]-C[i+1][j+1]
            assert d>=0;stats['reference_density_checks']+=1
            if d:row.append(j);bylength[j-i]+=1
        rows.append(row)
    return dict(interior_core=sum(map(len,rows)),completed_core=n+sum(map(len,rows)),
                by_length=dict(sorted(bylength.items())),support_rows=rows)


def main():
    rng=random.Random(702019);stats=Counter();rows=[]
    for n in (1,2,3,5,8,11,16,23,32,47,64,95,128,191,256,383,512):
        for family in ('uniform','ramp','valley','alternating','random_keys','random_mixed','wide_mixed','ruler'):
            e=[0]*n;f=[0]*(n+1)
            if family=='ramp':e=list(range(n))
            elif family=='valley':e=[abs(2*i-n+1) for i in range(n)]
            elif family=='alternating':e=[i%2 for i in range(n)]
            elif family=='random_keys':e=[rng.randrange(n+1) for _ in range(n)]
            elif family=='random_mixed':e=[rng.randrange(n+1) for _ in range(n)];f=[rng.randrange(n+1) for _ in range(n+1)]
            elif family=='wide_mixed':e=[rng.getrandbits(64) for _ in range(n)];f=[rng.getrandbits(64) for _ in range(n+1)]
            elif family=='ruler':e=[((i+1)&-(i+1)).bit_length()-1 for i in range(n)]
            E=sum(e)+sum(f);D=n*E+1;p=[D+x for x in e];q=[D+x for x in f]
            assert (n-1)*E<D
            C,R=table(p,q,stats)
            if n<=16:
                slow,_=table(p,q,stats,True);assert C==slow;stats['all_root_table_controls']+=1
                value,t=cubic(p,q);assert value==C[0][n]==cost(t,p,q);stats['independent_cubic_controls']+=1
            counts=profile(C,stats);L=n.bit_length()
            if n>16:counts.pop('support_rows')
            # Every interval optimum is minimum IPL by the integer-gap certificate.
            h=[[0]*(n+1) for _ in range(n+1)]
            for m in range(1,n+1):
                for i in range(n-m+1):
                    j=i+m;r=R[i][j];h[i][j]=1+max(h[i][r],h[r+1][j]);assert h[i][j]==m.bit_length()
                    stats['attaining_interval_height_checks']+=1
            rows.append(dict(n=n,family=family,p_residual=e,q_residual=f,baseline=D,height=L,
                             cost=C[0][n],**counts))
            print(n,family,counts['completed_core'], 'nL',n*L,flush=True)
    root=Path(__file__).resolve().parents[1];files=['final_core_probe.py','research.py']
    result=dict(seed=702019,scope='Certified minimum-IPL optima on every interval; final unrestricted cost cores only; dense diagnostic, not a constructor',counts=dict(stats),rows=rows,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/final_core_probe.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
