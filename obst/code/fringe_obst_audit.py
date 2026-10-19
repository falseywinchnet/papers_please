"""Independent LWS, column, period-recognition, and full mixed-tree audit."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random
from concave_lws import concave_lws
from fringe_obst import extend_column,longest_middle,FringeOBST,solve
from periodic_obst_audit import all_root,tree_check
from research import knuth,shapes,label,cost


def main():
    rng=random.Random(491019);checks=Counter();rows=[]
    # Fresh dense LWS recurrence precedes any OBST use of the primitive.
    for n in range(1,65):
        for trial in range(12):
            alpha=rng.randrange(4);row=[rng.randrange(-20,21) for _ in range(n)]
            col=[rng.randrange(-20,21) for _ in range(n+1)]
            w=lambda i,j:alpha*(j-i)**2+row[i]+col[j]
            stats=Counter();F,P=concave_lws(n,w,stats);D=[0];pred=[-1]
            for j in range(1,n+1):
                value,r=min((D[i]+w(i,j),i) for i in range(j));D.append(value);pred.append(r)
                checks['literal_lws_candidates']+=j
            assert F==D and P==pred
            checks['generic_lws_instances']+=1
            checks.update(stats)
    def verify(p,q,explicit=None,enumerate_shapes=False):
        n=len(p);C,R=all_root(p,q,checks);stats=Counter()
        if explicit is None:v,t,s=solve(p,q,stats)
        else:
            s=FringeOBST(p,q,*explicit,stats);v=s.value();t=s.reconstruct()
        assert v==C[0][n]==tree_check(t,p,q,checks)
        for i in range(n+1):
            for j in range(i,n+1):
                assert s.value(i,j)==C[i][j];checks['full_interval_values']+=1
                if i<j and isinstance(s,FringeOBST):
                    r=s.root(i,j);assert C[i][r]+C[r+1][j]+sum(p[i:j])+sum(q[i:j+1])==C[i][j]
                    checks['full_root_witnesses']+=1
        # Test boundary-column reduction on an arbitrary nonperiodic old table.
        vals,roots=extend_column(n,lambda i,r:C[i][r],lambda i:sum(p[i:])+sum(q[i:]),Counter())
        assert vals==[C[i][n] for i in range(n+1)]
        for i in range(n):
            rightmost=max(r for r in range(i,n) if C[i][r]+C[r+1][n]+sum(p[i:])+sum(q[i:])==C[i][n])
            assert roots[i]==rightmost;checks['column_rightmost_controls']+=1
        for b in range(1,min(n,6)):
            observed=longest_middle(p,q,b,Counter());best=0
            for i in range(n):
                for j in range(i+b+1,n+1):
                    if all(p[k]==p[k-b] for k in range(i+b,j)) and all(q[k]==q[k-b] for k in range(i+b,j+1)):best=max(best,j-i)
                    checks['literal_middle_candidates']+=1
            assert (0 if observed is None else observed[1]-observed[0])==best
            checks['middle_length_controls']+=1
        if enumerate_shapes:
            assert min(cost(label(sh)[0],p,q) for sh in shapes(n))==v
            checks['literal_shapes']+=len(shapes(n))
        checks['small_full_inputs']+=1;checks.update(stats)
    for n in range(1,5):
        for w in product((0,1),repeat=2*n+1):verify(list(w[:n]),list(w[n:]),enumerate_shapes=True)
    for n in (6,9,13,19,27):
        for trial in range(30):
            b=rng.randrange(1,4);l=rng.randrange(0,min(3,n-b));r=n-rng.randrange(0,min(3,n-l-b))
            pp=[rng.randrange(9) for _ in range(b)];qq=[rng.randrange(9) for _ in range(b)]
            p=[rng.randrange(30) for _ in range(n)];q=[rng.randrange(30) for _ in range(n+1)]
            for i in range(l,r):p[i]=pp[(i-l)%b]
            for i in range(l,r+1):q[i]=qq[(i-l)%b]
            if trial%5==0:p=[Fraction(x,7) for x in p];q=[Fraction(x,11) for x in q]
            if trial%5==1:
                p[0]=10**30;q[-1]=10**40
                if l==0:l=1
                if r==n:r=n-1
                pp=p[l:l+b];qq=q[l:l+b]
                # Revised span remains periodic as a restriction of the old middle.
            verify(p,q,explicit=(l,r,b));verify(p,q)
    print('small',dict(checks),flush=True)
    for n in (63,128,257,512):
        for b,l,dright in ((1,0,1),(3,1,0),(5,3,4),(2,4,3)):
            r=n-dright;pp=[rng.randrange(12) for _ in range(b)];qq=[rng.randrange(12) for _ in range(b)]
            p=[pp[(i-l)%b] for i in range(n)];q=[qq[(i-l)%b] for i in range(n+1)]
            for i in list(range(l))+list(range(r,n)):p[i]=rng.randrange(1000)
            for i in list(range(l))+list(range(r+1,n+1)):q[i]=rng.randrange(1000)
            if dright:q[-1]=10**30
            counts=Counter();v,t,s=solve(p,q,counts);expected,_,scans=knuth(p,q)
            assert v==expected==tree_check(t,p,q,counts)
            rows.append(dict(n=n,b=b,left=l,right=dright,value=v,counts=counts,reference_candidates=scans,verification='independent full ordinary Knuth recurrence and tree traversal'))
    for n in (4095,16384,65537):
        for b,l,dright in ((1,0,1),(3,1,0),(5,3,4),(2,4,3)):
            r=n-dright;pp=list(range(1,b+1));qq=list(range(b,0,-1))
            p=[pp[(i-l)%b] for i in range(n)];q=[qq[(i-l)%b] for i in range(n+1)]
            for i in range(l):p[i]=10**20+i;q[i]=10**21+i
            for i in range(r,n):p[i]=10**22+i;q[i+1]=10**23+i
            counts=Counter();v,t,s=solve(p,q,counts);assert isinstance(s,FringeOBST)
            assert v==tree_check(t,p,q,counts)
            rows.append(dict(n=n,b=b,left=l,right=dright,value=v,counts=counts,verification='complete automatic construction and independent tree traversal; no large independent optimality oracle'))
            print('large',n,b,l,dright,counts['fringe_transition_queries'],flush=True)
    root=Path(__file__).resolve().parents[1]
    files=('concave_lws.py','fringe_obst.py','fringe_obst_audit.py','periodic_obst.py','periodic_obst_audit.py','research.py')
    out=dict(scope='Full mixed OBST with arbitrary fringes around a periodic middle; linear concave LWS is Wilber prior work. General nonperiodic worst case remains quadratic.',seed=491019,checks=checks,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/fringe_obst_audit.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
