#!/usr/bin/env python3
"""Search for a height-independent local tile-mass bound (not a theorem)."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib,json,random
from aggregate_core_audit import partition


def evaluate(p,q,counts,all_roots=False):
    n=len(p);N=1<<(n-1).bit_length();L=n.bit_length();W=sum(p)+sum(q)
    pp=p+[0]*(N-n);qq=q+[0]*(N-n);M=(N+1)*W+1
    pre=[0]
    for k in range(N):pre.append(pre[-1]+pp[k]+qq[k+1])
    def mass(i,j):return pre[j]-pre[i]+qq[i]
    old=[[M*max(j-i,0) for j in range(N+1)] for i in range(N+1)]
    winner=None;best=Fraction(0);ratios=[]
    for h in range(1,L):
        cur=[[0]*(N+1) for _ in range(N+1)];roots=[[0]*(N+1) for _ in range(N+1)]
        for k in range(1,N+1):
            for i in range(N-k+1):
                j=i+k;lo=i if all_roots or k==1 else roots[i][j-1];hi=j-1 if all_roots or k==1 else roots[i+1][j]
                value,r=min((old[i][r]+old[r+1][j],r) for r in range(lo,hi+1))
                cur[i][j]=mass(i,j)+value;roots[i][j]=r
                counts['root_candidates']+=hi-lo+1;counts['dense_states']+=1
        tiles,_=partition(N,(1<<h)-1);layer_best=Fraction(0)
        for s,ts in tiles.items():
            for a,b in ts:
                density=cur[a][b+s]+cur[a+s][b]-cur[a][b]-cur[a+s][b+s]
                local=mass(a,b+s)
                assert 0<=density<=2*h*local
                counts['tiles']+=1
                ratio=Fraction(density,local) if local else Fraction(0)
                layer_best=max(layer_best,ratio)
                if ratio>best:
                    best=ratio;winner=dict(h=h,a=a,b=b,side=s,density_mass=density,interval_mass=local,
                                         ratio=[ratio.numerator,ratio.denominator])
        ratios.append([layer_best.numerator,layer_best.denominator]);old=cur
    counts['evaluations']+=1
    return best,dict(n=n,W=W,winner=winner,layer_ratios=ratios,p=p,q=q)


def main():
    counts=Counter();rng=random.Random(27019);rows=[];best=Fraction(0);winner=None
    for n in [4,7,8,15,16,31,32,63,64,127,128,255,256]:
        fixtures=[]
        for i in sorted(set([0,n//4,n//2,n//2+1,n-1])):
            p=[0]*n;p[i]=n;fixtures.append(('one_key_'+str(i),p,[0]*(n+1)))
            q=[0]*(n+1);q[i]=n;fixtures.append(('one_gap_'+str(i),[0]*n,q))
        for t in range(12):
            w=[0]*(2*n+1)
            slots=list(range(2*n+1)) if t<4 else rng.sample(range(2*n+1),min(2*n+1,1+t))
            for _ in range(n):w[rng.choice(slots)]+=1
            fixtures.append(('mixed_'+str(t),w[:n],w[n:]))
        fixtures.extend([('uniform',[1]*n,[1]*(n+1)),('odd_ramp',[2*i+1 for i in range(n)],[0]*(n+1)),
                         ('geometric',[1<<i for i in range(n)],[1<<min(i,n-i) for i in range(n+1)])])
        for name,p,q in fixtures:
            value,row=evaluate(p,q,counts);row['family']=name
            if n<=16:
                independent,control=evaluate(p,q,counts,True)
                assert control=={k:v for k,v in row.items() if k!='family'}
                counts['all_root_controls']+=1
            if value>best:best=value;winner=row
            rows.append(row)
        print(n,'best',str(best),winner['winner'],flush=True)
    # Fixed-mass hill search, objective is tile density divided by its own span mass.
    for n in [16,32,64]:
        w=[0]*(2*n+1)
        for _ in range(n):w[rng.randrange(2*n+1)]+=1
        value,current=evaluate(w[:n],w[n:],counts)
        for t in range(250):
            nxt=w[:];a=rng.choice([i for i,x in enumerate(nxt) if x]);b=rng.randrange(len(w))
            nxt[a]-=1;nxt[b]+=1
            new,row=evaluate(nxt[:n],nxt[n:],counts)
            if new>=value:w=nxt;value=new;current=row
            if new>best:best=new;winner=row
        rows.append(dict(family='local_search',**current))
        print('search',n,'best',str(best),winner['winner'],flush=True)
    root=Path(__file__).resolve().parents[1]
    sources=['dyadic_mass_probe.py','aggregate_core_audit.py']
    report=dict(seed=27019,scope='Falsification probe only; no inferred upper bound',counts=counts,
                maximum_ratio=[best.numerator,best.denominator],winner=winner,rows=rows,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in sources})
    (root/'results'/'dyadic_mass_probe.json').write_text(json.dumps(report,indent=2)+'\n')
    print(dict(counts),flush=True)
if __name__=='__main__':main()
