"""Independent harness for affine translation of full mixed OBST costs."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random
from periodic_obst_audit import all_root,tree_check
from research import shapes,label,cost,knuth
from affine_period_obst import AffinePeriodOBST,recognize,solve


def instance(n,b,scale,offset,pp,qq):
    p=list(pp);q=list(qq)
    for i in range(b,n):p.append(scale*p[i-b]+offset)
    for i in range(b,n+1):q.append(scale*q[i-b]-offset)
    return p[:n],q[:n+1]


def literal_affine(p,q,b):
    n=len(p)
    equations=[(p[i],1,p[i+b]) for i in range(n-b)]
    equations += [(q[i],-1,q[i+b]) for i in range(n-b+1)]
    x,y,z=equations[0];lam=1;alpha=Fraction(z-x,y)
    for u,v,w in equations[1:]:
        det=x*v-y*u
        if det:
            lam=Fraction(z*v-y*w,det);alpha=Fraction(x*w-z*u,det);break
    return lam>0 and all(lam*u+alpha*v==w for u,v,w in equations)


def main():
    rng=random.Random(501019);checks=Counter();rows=[]
    # Test the cost identity by literal shapes before testing the quotient.
    for n in range(1,8):
        for trial in range(10):
            p=[rng.randrange(4,12) for _ in range(n)];q=[rng.randrange(4,12) for _ in range(n+1)]
            lam=rng.choice((Fraction(1,2),1,2,3));alpha=rng.randrange(-2,3)
            pp=[lam*x+alpha for x in p];qq=[lam*x-alpha for x in q]
            assert min(pp+qq)>=0
            for sh in shapes(n):
                t=label(sh)[0];assert cost(t,pp,qq)==lam*cost(t,p,q)-alpha*n
                checks['literal_shape_transformations']+=1
    def verify(p,q,witness=None,enumerate_shapes=False):
        n=len(p);C,R=all_root(p,q,checks);stats=Counter()
        feasible=[]
        for b in range(1,n+1):
            yes=literal_affine(p,q,b);observed=recognize(p,q,b,Counter())
            assert yes==(observed is not None)
            if yes:feasible.append(b)
            checks['independent_affine_feasibility']+=1
        if witness is None:
            v,t,s=solve(p,q,stats)
            if n:assert s.b==min(feasible);checks['minimum_affine_periods']+=1
        else:
            s=AffinePeriodOBST(p,q,*witness,stats);v=s.value();t=s.reconstruct()
        assert v==C[0][n]==tree_check(t,p,q,checks)
        for i in range(n+1):
            for j in range(i,n+1):
                assert s.value(i,j)==C[i][j];checks['interval_values']+=1
                if i<j:assert s.root(i,j)==R[i,j];checks['leftmost_roots']+=1
        for length in range(1,s.m+1):
            for a in range(s.b):
                assert s.costs[length][a]==C[a][a+length]
                assert s.roots[length][a]+a==R[a,a+length]
                checks['phase_states']+=1
        if n:
            assert stats['affine_phase_candidates']==s.b*(2*s.m-1)
            assert stats['affine_tail_states']==s.b*(s.b-1)//2
            assert stats['affine_tail_candidates']<=(s.b-1)*n+(s.b-1)*(s.b-2)//2
        if enumerate_shapes:
            assert min(cost(label(sh)[0],p,q) for sh in shapes(n))==v
            checks['optimal_shape_controls']+=len(shapes(n))
        checks.update(stats);checks['small_inputs']+=1
    for n in range(0,5):
        for w in product((0,1),repeat=2*n+1):verify(list(w[:n]),list(w[n:]),enumerate_shapes=True)
    for n in (6,9,13,21,32):
        for trial in range(36):
            b=rng.randrange(1,n+1);lam=rng.choice((Fraction(1,2),1,2,3));alpha=rng.randrange(-3,4)
            # Start large enough to keep every actual weight nonnegative.
            base=10*2**(n+2)
            p,q=instance(n,b,lam,alpha,[base+rng.randrange(20) for _ in range(b)],
                         [base+rng.randrange(20) for _ in range(b)])
            verify(p,q,(b,lam,alpha));verify(p,q)
            for k in range(1,n+1):
                w=recognize(p,q,k,Counter())
                if w is not None:
                    ll,aa=w
                    assert ll>0 and all(p[i+k]==ll*p[i]+aa for i in range(n-k))
                    assert all(q[i+k]==ll*q[i]-aa for i in range(n-k+1))
                checks['recognition_witness_controls']+=1
    # Finite-domain cases whose next translated weights would be negative.
    for n in (7,13,24):
        for b in range(1,min(7,n)+1):
            p,q=instance(n,b,1,1,list(range(1,b+1)),[(n-j)//b for j in range(b)])
            assert min(p+q)>=0
            verify(p,q,(b,1,1));checks['negative_extension_controls']+=1
    print('small',dict(checks),flush=True)
    for n in (63,128,257,512):
        for b,lam,alpha in ((1,1,1),(3,2,0),(5,1,-2),(7,2,1)):
            base=3*n+7;p,q=instance(n,b,lam,alpha,[base+i for i in range(b)],[base+2*i for i in range(b)])
            counts=Counter();v,t,s=solve(p,q,counts);ref,_,scans=knuth(p,q)
            assert v==ref==tree_check(t,p,q,counts)
            rows.append(dict(n=n,b=s.b,scale=str(s.scale),offset=str(s.offset),counts=counts,value=str(v),reference_candidates=scans,verification='independent ordinary Knuth and full tree traversal'))
    for n in (4095,16384,65537):
        for b,lam,alpha in ((1,1,1),(3,1,-2),(5,1,2)):
            base=3*n+7;p,q=instance(n,b,lam,alpha,[base+i for i in range(b)],[base+2*i for i in range(b)])
            counts=Counter();v,t,s=solve(p,q,counts);assert s.b<=b
            assert v==tree_check(t,p,q,counts)
            rows.append(dict(n=n,b=s.b,scale=str(s.scale),offset=str(s.offset),counts=counts,value=str(v),verification='complete construction and independent traversal; no quadratic optimality reference'))
            print('large',n,s.b,counts['affine_phase_candidates'],counts['affine_tail_candidates'],flush=True)
    # Exact geometric rows stay smaller because bit lengths grow with n.
    for n in (1023,4095):
        p,q=instance(n,3,2,1,[9,11,7],[13,8,10]);counts=Counter();v,t,s=solve(p,q,counts)
        assert v==tree_check(t,p,q,counts)
        rows.append(dict(n=n,b=s.b,scale=str(s.scale),offset=str(s.offset),counts=counts,value=str(v),verification='exact growing-integer construction and traversal; arithmetic counts, not bit complexity'))
    root=Path(__file__).resolve().parents[1];files=('affine_period_obst.py','affine_period_audit.py','periodic_obst_audit.py','research.py')
    out=dict(scope='Exact full mixed OBST under positive affine translation of key/gap weights. General arbitrary-input fallback remains quadratic.',checks=checks,rows=rows,seed=501019,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/affine_period_audit.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
