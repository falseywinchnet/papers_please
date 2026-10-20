#!/usr/bin/env python3
"""Dense falsification harness for baseline-centered Monge core bounds.

Not a fast constructor. Counts every dense state and candidate, and verifies
baseline formulas, refined height bounds, local residuals, and tile accounting.
"""
from collections import Counter,defaultdict
import hashlib,itertools,json,random
from pathlib import Path
from research import cubic,knuth,check_weights,cost,label,shapes
from penalty_layers import fib_limit


def height_bound(p,q):
    n=len(p)
    if not n:return 0
    w=sum(p)+sum(q)
    if not w:return n.bit_length()
    singles=[p[i]+q[i]+q[i+1] for i in range(n)]
    s=min(v for v in singles if v)
    return min(n,fib_limit(w//s)+(n.bit_length() if 0 in singles else 0))


def internal_path(k):
    if not k:return 0
    h=k.bit_length()-1
    return h*k-(1<<(h+1))+h+2


def baseline(k,h,a,b,M):
    cap=(1<<h)-1
    if k<=cap:return (a+b)*internal_path(k)+(a+2*b)*k
    return M*(k-cap)+(a+b)*h*(k+1)-a*cap


def tile_audit(c,h,a,b,M,pdelta,qdelta,stats):
    n=len(c)-1;R=sum(pdelta)+sum(qdelta);N=1<<(n-1).bit_length()
    lines=[(1<<t)-1 for t in range(1,n.bit_length()+1) if (1<<t)-1<n]
    prefix=[0]
    for x,y in zip(pdelta,qdelta[1:]):prefix.append(prefix[-1]+x+y)
    mass=lambda lo,hi:prefix[hi]-prefix[lo]+qdelta[lo]
    residual=lambda i,j:c[i][j]-baseline(j-i,h,a,b,M)
    dd={(i,j):c[i][j+1]+c[i+1][j]-c[i][j]-c[i+1][j+1] for i in range(n-1) for j in range(i+1,n)}
    byscale=defaultdict(Counter);exceptional=0;covered=0
    def visit(x,y,s):
        nonlocal exceptional,covered
        if x>=n or y>=n or y+s-1<x:return
        inside=x+s<=n and y+s<=n
        lo,hi=y-(x+s-1),y+s-1-x
        hit=lo<=0<=hi or any(lo<=d<=hi for d in lines)
        if (not inside or hit) and s>1:
            t=s//2
            for i,j in ((x,y),(x+t,y),(x,y+t),(x+t,y+t)):visit(i,j,t)
            return
        if not inside:return
        if hit:
            if x<y:exceptional+=int(dd[x,y]>0);covered+=1
            return
        assert x+s<=y
        v=residual(x,y+s)+residual(x+s,y)-residual(x,y)-residual(x+s,y+s)
        actual=sum(dd[i,j] for i in range(x,x+s) for j in range(y,y+s))
        count=sum(dd[i,j]>0 for i in range(x,x+s) for j in range(y,y+s))
        assert 0<=v==actual<=2*h*mass(x,y+s)
        assert count<=min(s*s,v)
        z=byscale[s];z['tiles']+=1;z['interval_mass_sum']+=mass(x,y+s);z['core']+=count;z['density_sum']+=v
        covered+=s*s;stats['tiles']+=1
    visit(0,0,N)
    assert covered==n*(n-1)//2
    assert exceptional+sum(z['core'] for z in byscale.values())==sum(v>0 for v in dd.values())
    for s,z in byscale.items():
        # Explicit generous constants audit the geometric packing proof.
        assert z['tiles']*s<=64*n*(1+(n//s).bit_length())
        assert z['interval_mass_sum']*s<=64*n*R
        stats['scale_checks']+=1
    return dict(exceptional=exceptional,scales={str(s):dict(z) for s,z in sorted(byscale.items())})


def check(p,q,stats,deep=False,tiles=False):
    check_weights(p,q);n=len(p)
    if not n:
        assert cubic(p,q)[0]==0;stats['solves']+=1;return dict(n=0)
    w=sum(p)+sum(q);H=height_bound(p,q);M=(H+1)*w+1;a=min(p);b=min(q)
    pd=[x-a for x in p];qd=[x-b for x in q];R=sum(pd)+sum(qd)
    prefix=[0];rp=[0]
    for x,y,u,v in zip(p,q[1:],pd,qd[1:]):prefix.append(prefix[-1]+x+y);rp.append(rp[-1]+u+v)
    mass=lambda i,j:prefix[j]-prefix[i]+q[i]
    remmass=lambda i,j:rp[j]-rp[i]+qd[i]
    old=[[M*(j-i) for j in range(n+1)] for i in range(n+1)]
    roots=[];rows=[]
    for h in range(1,H+1):
        cur=[[0]*(n+1) for _ in range(n+1)];rr=[[0]*(n+1) for _ in range(n+1)]
        for length in range(1,n+1):
            for i in range(n-length+1):
                j=i+length;lo=i if length==1 else rr[i][j-1];hi=j-1 if length==1 else rr[i+1][j]
                v,r=min((old[i][r]+old[r+1][j],r) for r in range(lo,hi+1));stats['root_candidates']+=hi-lo+1
                cur[i][j]=mass(i,j)+v;rr[i][j]=r;stats['dense_states']+=1
                assert 0<=cur[i][j]-baseline(length,h,a,b,M)<=h*remmass(i,j)
                if deep:
                    assert (v,r)==min((old[i][r]+old[r+1][j],r) for r in range(i,j));stats['all_root_cells']+=1
        if deep:
            def trunc(t,i,j,budget,aa,bb):
                if i==j:return 0
                if not budget:return M*(j-i)
                r,l,z=t
                return aa*(j-i)+bb*(j-i+1)+trunc(l,i,r,budget-1,aa,bb)+trunc(z,r+1,j,budget-1,aa,bb)
            for k in range(1,n+1):
                assert baseline(k,h,a,b,M)==min(trunc(label(s)[0],0,k,h,a,b) for s in shapes(k));stats['baseline_shape_checks']+=1
        K=0;off=0;support=[]
        for length in range(1,n):
            v=baseline(length+1,h,a,b,M)+baseline(length-1,h,a,b,M)-2*baseline(length,h,a,b,M)
            target=(M-b if length==(1<<h)-1 else a+b if length<(1<<h)-1 and ((length+1)&length)==0 else 0)
            assert v==target;stats['baseline_density_checks']+=1
            if v:support.append(length)
        for i in range(n-1):
            for j in range(i+1,n):
                v=cur[i][j+1]+cur[i+1][j]-cur[i][j]-cur[i+1][j+1]
                assert v>=0
                K+=v>0;off+=v>0 and j-i not in support
        row=dict(h=h,core=K,off_baseline_core=off,full_value=cur[0][n])
        if tiles:row['tiling']=tile_audit(cur,h,a,b,M,pd,qd,stats)
        rows.append(row);roots.append(rr);old=cur
    ref,_,_=knuth(p,q)
    assert old[0][n]==ref
    def tree(i,j,h):
        if i==j:return None
        assert h>0
        r=roots[h-1][i][j];return r,tree(i,r,h-1),tree(r+1,j,h-1)
    assert cost(tree(0,n,H),p,q)==ref
    if n<=12:assert cubic(p,q)[0]==ref;stats['cubic_solves']+=1
    stats['solves']+=1;stats['constructed_keys']+=n
    return dict(n=n,a=a,b=b,mass=w,deviation=R,height=H,old_height=min(n,fib_limit(w)+(n.bit_length() if not all(p) else 0)),cost=ref,layers=rows)


def main():
    rng=random.Random(890231);stats=Counter();rows=[]
    for n in range(5):
        for v in itertools.product((0,1),repeat=2*n+1):check(list(v[:n]),list(v[n:]),stats,deep=n<=3)
        print('exhaustive',n,flush=True)
    for n in range(1,33):
        for trial in range(12):
            a,b=rng.choice((0,1,10**6,1<<256)),rng.choice((0,1,10**6,1<<200))
            p=[a+rng.randrange(5) for _ in range(n)];q=[b+rng.randrange(5) for _ in range(n+1)]
            check(p,q,stats,deep=n<=7 and trial<2,tiles=trial==0)
        print('random',n,flush=True)
    for n in (16,32,64,128,256):
        for name,a,b in (('unit',1,1),('large_both',1<<256,1<<200),('large_keys',1<<256,0),('large_gaps',0,1<<256),('zero_baseline',0,0)):
            p=[a+rng.randrange(3) for _ in range(n)];q=[b+rng.randrange(3) for _ in range(n+1)]
            row=check(p,q,stats,tiles=True);row['family']=name;rows.append(row)
            print(name,n,'H',row['height'],'old H',row['old_height'],'core',max(z['core'] for z in row['layers']),flush=True)
        if n<=64:
            for name,p,q in (('geometric',[1<<i for i in range(n)],[1<<i for i in range(n+1)]),('all_zero',[0]*n,[0]*(n+1)),('one_gap',[0]*n,[0]*(n//2)+[1]+[0]*(n-n//2))):
                row=check(p,q,stats,tiles=True);row['family']=name;rows.append(row)
    root=Path(__file__).resolve().parents[1]
    result=dict(seed=890231,checks=dict(stats),rows=rows,implementation='dense diagnostic; baseline-centered bound and normalized height',source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in ('centered_layers.py','research.py','penalty_layers.py')})
    (root/'results'/'centered_layers.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
