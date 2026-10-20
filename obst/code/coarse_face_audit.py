#!/usr/bin/env python3
"""Independent all-root and all-interval controls for coarse-face refinement."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random
from coarse_face import Oracle,Prepared,solve,certificate
from slot_records_audit import check_tree


def reference(p,q):
    n=len(p);C=[[0]*(n+1) for _ in range(n+1)];roots={};counts=[[1]*(n+1) for _ in range(n+1)]
    for size in range(1,n+1):
        for i in range(n-size+1):
            j=i+size;items=[(C[i][r]+C[r+1][j],r) for r in range(i,j)]
            best=min(v for v,r in items);rs=[r for v,r in items if v==best]
            C[i][j]=best+sum(p[i:j])+sum(q[i:j+1]);roots[i,j]=rs
            counts[i][j]=sum(counts[i][r]*counts[r+1][j] for r in rs)
    return C,roots,counts[0][n]


def main():
    rng=random.Random(662019);checks=Counter();rows=[]
    fixtures=[]
    for n in range(1,5):fixtures.extend((list(x[:n]),list(x[n:])) for x in product((0,1),repeat=2*n+1))
    for n in (5,8,12):
        for _ in range(12):fixtures.append(([rng.randrange(8) for _ in range(n)],[rng.randrange(8) for _ in range(n+1)]))
    for p,q in fixtures:
        n=len(p);C,roots,ways=reference(p,q);oracle=Oracle(p,q)
        assert oracle.value==C[0][n]
        for (i,j),rs in roots.items():
            assert oracle.extremes(i,j)==(min(rs),max(rs));checks['all_interval_extremes']+=1
        # This separately validates all optimal roots, including roots whose
        # complete optimum exceeds the sufficient balanced-zero height.
        plan=oracle.partition();assert plan['unique']==(ways==1)
        for (i,j),r in plan['forced'].items():assert roots[i,j]==[r]
        checks['coarse_faces']+=1;checks['unique_faces']+=int(ways==1)
        D=16*(n+1)**4
        for trial in range(2):
            fine=[]
            for x in p+q:
                e=Fraction(rng.randrange(-2*n-1,2*n+2),3)
                if not x:e=abs(e)
                fine.append(D*x+e)
            pp,qq=fine[:n],fine[n:];cert=certificate(pp,qq,D,Counter());assert cert is not None
            counts=Counter();ans=solve(pp,qq,counts,delta=D)
            target,_,_=reference(pp,qq)
            assert ans['method']=='face' and ans['cost']==target[0][n]
            assert check_tree(ans['tree'],pp,qq,n,Counter())==ans['cost']
            # The returned full tree must also be coarse-optimal.
            assert check_tree(ans['tree'],p,q,n,Counter())==C[0][n]
            assert sum((b-a)*(b-a+1)//2 for a,b in ans['blocks'])==counts['height_fallback_states']
            checks['full_refinements']+=1
    for n in (1,2,3,7,16,31):
        D=64*(n+1)**4;p=[D*(1+rng.randrange(7))+i for i in range(n)]
        q=[D*(1+rng.randrange(7))+n+i+1 for i in range(n+1)]
        counts=Counter();ans=solve(p,q,counts);C,_,_=reference(p,q)
        assert ans['cost']==C[0][n]==check_tree(ans['tree'],p,q,n,Counter())
        assert ans['method']=='face';checks['automatic_controls']+=1
        rows.append(dict(n=n,method=ans['method'],mass=ans['coarse_mass'],blocks=ans['blocks'],counts=counts))
    for n in (2,3,8,16):
        p=[Fraction(rng.randrange(1,100),13) for _ in range(n)]
        q=[Fraction(rng.randrange(1,100),17) for _ in range(n+1)]
        counts=Counter();ans=solve(p,q,counts,delta=Fraction(1,10));C,_,_=reference(p,q)
        assert ans['cost']==C[0][n]==check_tree(ans['tree'],p,q,n,Counter())
        checks['rejection_controls']+=1
    # Zero coarse mass preserves every tree, not only those of small height.
    for n in (5,8,16):
        p=[1<<i for i in range(n)];q=[1]*(n+1);D=2*n*(sum(p)+sum(q))
        counts=Counter();ans=solve(p,q,counts,delta=D);C,_,_=reference(p,q)
        assert ans['method']=='face' and ans['coarse_mass']==0 and ans['blocks']==[(0,n)]
        assert ans['cost']==C[0][n];checks['zero_face_controls']+=1
    for n in (3,8,15,24):
        bp=[rng.randrange(8) for _ in range(n)];bq=[rng.randrange(8) for _ in range(n+1)]
        prepared=Prepared(bp,bq,Counter());D=64*(n+1)**4
        for trial in range(5):
            p=[D*x+Fraction(rng.randrange(32),7) for x in bp]
            q=[D*x+Fraction(rng.randrange(32),11) for x in bq]
            counts=Counter();ans=prepared.refine(p,q,D,counts);C,_,_=reference(p,q)
            assert ans['method']=='face' and ans['cost']==C[0][n]==check_tree(ans['tree'],p,q,n,Counter())
            assert not counts['product_calls'];checks['reused_face_controls']+=1
    root=Path(__file__).resolve().parents[1]
    files=['coarse_face_audit.py','coarse_face.py','compact_obst.py','core_monge.py','penalty_layers.py','research.py','trimmed_height.py','slot_records_audit.py']
    out=dict(scope='Exact unrestricted coarse root extremes, complete optimal-face refinement, signed rational errors, automatic scale selection and rejection controls',seed=662019,checks=checks,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/coarse_face_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(checks),flush=True)
if __name__=='__main__':main()
