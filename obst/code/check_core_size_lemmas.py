#!/usr/bin/env python3
"""Direct rotation-cost identities and integer-cell dyadic boundary lemma."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
from research import cost, label, shapes

def main():
    rng=random.Random(251020);checks=Counter()
    for n in range(3,9):
        for shape in shapes(n):
            tree=label(shape)[0]
            p=[rng.randrange(9) for _ in range(n)];q=[rng.randrange(9) for _ in range(n+1)]
            def mass(t,lo,hi):return sum(p[lo:hi])+sum(q[lo:hi+1])
            def walk(t,lo,hi):
                if t is None:return
                v,y,D=t
                if y is not None:
                    ky,A,X=y
                    if A is not None:
                        new=(ky,A,(v,X,D))
                        expected=p[v]+mass(D,v+1,hi)-p[ky]-mass(A,lo,ky)
                        assert cost(new,p,q)-cost(t,p,q)==expected if lo==0 and hi==n else True
                        # Evaluate local trees using original labels via direct depths.
                        assert local(new,lo,hi,p,q)-local(t,lo,hi,p,q)==expected
                        checks['straight_identities']+=1
                    if X is not None:
                        kx,B,C=X;new=(kx,(ky,A,B),(v,C,D))
                        expected=p[v]+mass(D,v+1,hi)-p[kx]-mass(X,ky+1,v)
                        assert local(new,lo,hi,p,q)-local(t,lo,hi,p,q)==expected
                        checks['bent_identities']+=1
                walk(y,lo,v);walk(D,v+1,hi)
            walk(tree,0,n)
    for n in range(1,130):
        N=1<<(n-1).bit_length()
        for d in sorted({1,n//2,n-1,*[(1<<h)-1 for h in range(1,n.bit_length())]}):
            if d<=0:continue
            per=Counter();covered=0
            def visit(a,b,s):
                nonlocal covered
                if a>=n or b>=n or b+s-1<=a:return
                lo=b-a-s+1;hi=b+s-1-a
                allowed=a+s<=n and b+s<=n and lo>0 and not(lo<=d<=hi)
                if allowed:
                    per[s]+=1;covered+=s*s
                elif s>1:
                    t=s//2
                    for x,y in ((a,b),(a+t,b),(a,b+t),(a+t,b+t)):visit(x,y,t)
            visit(0,0,N)
            assert covered==n*(n-1)//2-max(0,n-d)
            assert all(k*s<=24*n for s,k in per.items())
            checks['partitions']+=1;checks['scale_bounds']+=len(per)
    root=Path(__file__).resolve().parents[1]
    files=['check_core_size_lemmas.py','research.py']
    (root/'results'/'core_size_lemmas.json').write_text(json.dumps(dict(checks=checks,
      source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files}),indent=2)+'\n')
    print(dict(checks),flush=True)

def local(t,lo,hi,p,q,depth=0):
    if t is None:return q[lo]*depth
    r,a,b=t
    return p[r]*(depth+1)+local(a,lo,r,p,q,depth+1)+local(b,r+1,hi,p,q,depth+1)

if __name__=='__main__':main()
