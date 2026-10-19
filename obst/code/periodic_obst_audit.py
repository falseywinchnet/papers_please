"""Independent all-root, shape, exact-period, and full reconstruction checks."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random
from periodic_obst import PeriodicOBST,joint_period,solve
from research import shapes,label,cost,knuth
from aggregate_core_audit import layers


def all_root(p,q,stats):
    n=len(p);C=[[0]*(n+1) for _ in range(n+1)];R={}
    for k in range(1,n+1):
        for i in range(n-k+1):
            j=i+k;v,r=min((C[i][r]+C[r+1][j],r) for r in range(i,j))
            C[i][j]=v+sum(p[i:j])+sum(q[i:j+1]);R[i,j]=r
            stats['independent_all_root_candidates']+=k;stats['independent_states']+=1
    return C,R


def tree_check(t,p,q,stats):
    n=len(p);seen=set();total=0;todo=[(t['root'],0,n,0)]
    while todo:
        r,i,j,d=todo.pop()
        if i==j:
            assert r==-1 and t['gap_depth'][i]==d
            total+=q[i]*d;stats['independent_gap_visits']+=1;continue
        assert i<=r<j and r not in seen and t['key_depth'][r]==d+1
        seen.add(r);total+=p[r]*(d+1);stats['independent_key_visits']+=1
        todo.append((t['left'][r],i,r,d+1));todo.append((t['right'][r],r+1,j,d+1))
    assert len(seen)==n
    return total


def main():
    stats=Counter();rng=random.Random(481901);rows=[]
    def check(p,q,enumerate_shapes=False):
        v,t,s=solve(p,q,stats);n=len(p)
        expected_b=next(b for b in range(1,n+2) if
            all(p[i]==p[i-b] for i in range(b,n)) and
            all(q[i]==q[i-b] for i in range(b,n+1)))
        assert s.b==expected_b;stats['literal_minimum_period_controls']+=1
        C,R=all_root(p,q,stats)
        assert v==C[0][n]==tree_check(t,p,q,stats)
        for i in range(n+1):
            for j in range(i,n+1):
                assert s.value(i,j)==C[i][j];stats['original_interval_values']+=1
                if i<j:
                    assert i+s.roots[j-i][i%s.b]==R[i,j];stats['leftmost_root_controls']+=1
        # Independent references also cover artificial phase intervals crossing
        # the input endpoint; the cyclic telescoping uses every phase.
        ep=[s.p[i%s.b] for i in range(n+s.b-1)]
        eq=[s.q[i%s.b] for i in range(n+s.b)]
        E,ER=all_root(ep,eq,stats)
        for a in range(s.b):
            for k in range(1,n+1):
                assert s.costs[k][a]==E[a][a+k]
                assert a+s.roots[k][a]==ER[a,a+k]
                stats['extended_phase_controls']+=1
        if enumerate_shapes:
            literal=min(cost(label(sh)[0],p,q) for sh in shapes(n))
            assert literal==v;stats['exhaustive_shapes']+=len(shapes(n))
        stats['small_inputs']+=1
    for n in range(0,5):
        for w in product((0,1),repeat=2*n+1):check(list(w[:n]),list(w[n:]),True)
    for b in range(1,4):
        for w in product((0,1),repeat=2*b):
            for n in (b,2*b+1,3*b+2):
                check([w[i%b] for i in range(n)],[w[b+i%b] for i in range(n+1)])
    for n in (7,12,17,24,33,48):
        for trial in range(18):
            b=rng.randrange(1,min(n,9)+1)
            pp=[rng.randrange(12) for _ in range(b)];qq=[rng.randrange(12) for _ in range(b)]
            if trial%6==0:pp=[0]*b
            if trial%6==1:qq=[0]*b
            if trial%6==2:pp=[2**j for j in range(b)]
            p=[pp[i%b] for i in range(n)];q=[qq[i%b] for i in range(n+1)]
            if trial%6==3:q[-1]+=1
            if trial%6==4:
                p=[Fraction(x,7) for x in p];q=[Fraction(x,11) for x in q]
            check(p,q)
    print('small',dict(stats),flush=True)
    for n in (63,128,257,512):
        for b in (1,2,3,5,11):
            pp=[rng.randrange(1000) for _ in range(b)];qq=[rng.randrange(1000) for _ in range(b)]
            p=[pp[i%b] for i in range(n)];q=[qq[i%b] for i in range(n+1)]
            counts=Counter();v,t,s=solve(p,q,counts);reference,_,scans=knuth(p,q)
            assert v==reference==tree_check(t,p,q,counts)
            stats['matched_knuth_controls']+=1;stats['matched_knuth_candidates']+=scans
            rows.append(dict(n=n,requested_period=b,detected_period=s.b,value=v,counts=counts,verification='full independent ordinary Knuth recurrence and tree traversal'))
    for n in (4095,16384,65537,262144):
        for pp,qq in (([0,0,1],[1,4,2]),([3,0,11,2,7],[0,13,1,8,5]),([1],[1]),([0],[0])):
            b=len(pp);p=[pp[i%b] for i in range(n)];q=[qq[i%b] for i in range(n+1)]
            counts=Counter();v,t,s=solve(p,q,counts)
            assert v==tree_check(t,p,q,counts)
            assert counts['periodic_root_candidates']==s.b*(2*n-1)
            if not any(pp+qq):assert v==0
            # A large run verifies construction and its exact operation count;
            # no quadratic independent optimality oracle is claimed here.
            rows.append(dict(n=n,key_period=pp,gap_period=qq,detected_period=s.b,value=v,counts=counts,verification='complete phase-DP construction and independent tree traversal; no large independent optimality reference'))
            print('large',n,s.b,v,counts['periodic_root_candidates'],flush=True)
    witness=[1, 2, 0, 2, 3, 0, 0, 0, 4, 0, 2, 0, 0, 3, 0, 0, 1, 0, 0, 3, 0, 0, 3, 0, 3, 0, 2, 1, 0, 3, 0, 0, 0, 0, 1, 3, 0, 0, 3, 1, 0, 2, 0, 0, 2, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 3, 0, 0, 3, 0, 2, 1, 0, 1, 1, 0, 0, 0, 3, 0, 0, 3, 0, 0, 1, 2, 1, 0, 0, 1, 0, 2, 0, 0, 2, 0, 4, 1, 0, 1, 2, 2, 0, 1, 4, 0, 3, 1, 4, 0, 2, 0, 4, 0, 3, 0, 0, 0, 0, 2, 0, 1, 1, 0, 1, 1, 0, 2, 0, 3, 1, 3, 0, 0, 2, 0, 3, 2]
    density_counts=Counter();h=5;n=len(witness)
    A=list(layers(witness,[0]*(n+1),h,(n+1)*sum(witness)+1,density_counts))[-1]
    c=(1<<h)-1
    core=sum(A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]>0
             for i in range(n) for j in range(i+c+1,n))
    assert core==270 and core>n+sum(witness)
    obstruction=dict(keys=witness,n=n,mass=sum(witness),h=h,above_core=core,checks=density_counts,
                     scope='Finite counterexample to coefficient one in K_above<=n+P; no asymptotic lower bound.')
    root=Path(__file__).resolve().parents[1]
    files=('periodic_obst.py','periodic_obst_audit.py','research.py','aggregate_core_audit.py')
    out=dict(scope='Exact unrestricted-height mixed OBST for jointly periodic inputs; O(nb), quadratic when b is linear in n. Large checks do not replace the proof.',seed=481901,checks=stats,rows=rows,above_counterexample=obstruction,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/periodic_obst_audit.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
