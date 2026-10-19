#!/usr/bin/env python3
"""Independent explicit-product tests for the condensed Monge backend."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
from core_monge import Monge,multiply


def dense(top,left,entries):
    p,q=len(left),len(top)
    d=[[0]*(q+1) for _ in range(p+1)]
    for i,j,v in entries:d[i+1][j+1]+=v
    for i in range(1,p+1):
        for j in range(1,q+1):d[i][j]+=d[i-1][j]+d[i][j-1]-d[i-1][j-1]
    return [[left[i]+top[j]-top[0]-d[i][j] for j in range(q)] for i in range(p)]


def random_matrix(p,q,rng,stats,density):
    top=[rng.randrange(-30,31) for _ in range(q)]
    left=[top[0]]+[rng.randrange(-30,31) for _ in range(p-1)]
    entries=[(i,j,rng.randrange(1,11)) for i in range(p-1) for j in range(q-1) if rng.random()<density]
    return Monge(top,left,entries,stats),dense(top,left,entries)


def main():
    rng=random.Random(941723);stats=Counter();tests=Counter()
    for t in range(1600):
        p,q,r=[rng.randrange(1,25) for _ in range(3)]
        density=(0,.02,.1,.5,1)[t%5]
        a,ad=random_matrix(p,q,rng,stats,density)
        b,bd=random_matrix(q,r,rng,stats,density)
        c,w=multiply(a,b)
        cd=dense(c.top,c.left,c.entries)
        for i in range(p):
            for j in range(r):
                value,k=min((ad[i][k]+bd[k][j],k) for k in range(q))
                assert cd[i][j]==value,(t,p,q,r,i,j,cd[i][j],value)
                assert w.query(i,j)==k,(t,p,q,r,i,j,'witness',w.query(i,j),k)
                tests['product_cells']+=1
        rr=sorted(rng.sample(range(p),rng.randrange(1,p+1)))
        cc=sorted(rng.sample(range(q),rng.randrange(1,q+1)))
        sub=a.select(rr,cc);sd=dense(sub.top,sub.left,sub.entries)
        assert sd==[[ad[i][j] for j in cc] for i in rr]
        tests['arbitrary_submatrices']+=1;tests['products']+=1
        if t%200==0:print('passed products',t,flush=True)
    # Large dimensions with tiny cores: production never expands the grid.
    large=[]
    for n in (128,512,2048):
        st=Counter();en=[(i*n//9,i*n//9,2*(1+i)) for i in range(1,8)]
        boundary=[sum(v//2 for a,_,v in en if a<j) for j in range(n)]
        a=Monge(boundary,boundary,en,st)
        b=Monge(boundary,boundary,list(reversed(en)),st)
        c,w=multiply(a,b)
        assert c.entries==a.entries and c.top==a.top and c.left==a.left
        for _ in range(20):
            i,j=rng.randrange(n),rng.randrange(n)
            value,k=min((a.value_reference(i,k)+b.value_reference(k,j),k) for k in range(n))
            assert c.value_reference(i,j)==value and w.query(i,j)==k
        large.append(dict(n=n,input_cores=[a.k,b.k],output_core=c.k,counts=st))
    root=Path(__file__).resolve().parents[1]
    data=dict(seed=941723,tests=tests,counts=stats,large_sparse=large,
              source_sha256={name:hashlib.sha256((root/'code'/name).read_bytes()).hexdigest()
                             for name in ('core_monge.py','check_core_monge.py')})
    (root/'results'/'core_monge.json').write_text(json.dumps(data,indent=2)+'\n')
    print(dict(tests),flush=True);print(dict(stats),flush=True)

if __name__=='__main__':main()
