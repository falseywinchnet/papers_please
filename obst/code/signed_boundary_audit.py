"""Independent exact audit of legal-response collision and signed recovery."""
from collections import Counter,defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random
from boundary_response import profiles
from research import cubic,shapes,label,cost
from signed_boundary import chain_costs,LineOracle,recover_gaps


def signed_cubic(p,q,stats):
    n=len(p);C=[[0]*(n+1) for _ in range(n+1)]
    for length in range(1,n+1):
        for i in range(n-length+1):
            j=i+length;C[i][j]=min(C[i][r]+C[r+1][j] for r in range(i,j))+sum(p[i:j])+sum(q[i:j+1])
            stats['signed_reference_candidates']+=length
    return C[0][n]


def main():
    rng=random.Random(511020);counts=Counter();rows=[]
    def verify(p,q,literal=False):
        n=len(p);stats=Counter();fast=LineOracle(p,q,stats);W=sum(p)+sum(q)
        def independent(x,y):
            qq=list(q);qq[0]+=x;qq[-1]+=y
            observed=signed_cubic(p,qq,counts);assert fast(x,y)==observed
            counts['independent_signed_queries']+=1
            if literal:
                assert min(cost(label(sh)[0],p,qq) for sh in shapes(n))==observed
                counts['signed_shape_evaluations']+=len(shapes(n))
            return observed
        recovered=recover_gaps(p,W,q[0],independent,stats);assert recovered==q
        assert stats['signed_recovery_queries']<=n
        if n>=2:
            assert stats['signed_largest_denominator']<=n*n-1
        if literal:
            bypair=defaultdict(list)
            for tree,kd,gd in profiles(n):
                bypair[gd[0],gd[-1]].append(sum(x*y for x,y in zip(p,kd))+sum(x*y for x,y in zip(q,gd)))
                assert gd[0]+gd[-1]<=n+1;counts['boundary_union_controls']+=1
            for r,c in enumerate(chain_costs(p,q)):
                assert bypair[r+1,n-r]==[c];counts['unique_chain_controls']+=1
        counts.update(stats);counts['small_inputs']+=1
    for n in range(1,5):
        for w in product((0,1),repeat=2*n+1):verify(list(w[:n]),list(w[n:]),True)
    for n in (5,7,10,16,24):
        for trial in range(24):
            p=[rng.randrange(30) for _ in range(n)];q=[rng.randrange(30) for _ in range(n+1)]
            if trial%6==0:p=[2**i for i in range(n)];q=[1]*(n+1)
            if trial%6==1:p=[1]*n;q=[1]*(n+1)
            if trial%6==2:p=[0]*n
            if trial%6==3:q=[0]*(n+1)
            verify(p,q,n<=7)
    # Complete profile certificate on the whole nonnegative endpoint domain.
    p=[2,1,2,4];qa=[0,4,2,1,0];qb=[0,4,1,2,0]
    retained={(1,2):45,(1,3):42,(2,1):43,(2,2):36,(3,1):39}
    tables=[]
    for q in (qa,qb):
        table={}
        for tree,kd,gd in profiles(4):
            key=gd[0],gd[-1];v=sum(x*y for x,y in zip(p,kd))+sum(x*y for x,y in zip(q,gd))
            table[key]=min(table.get(key,v),v)
        assert all(table[k]==v for k,v in retained.items())
        for (a,b),c in table.items():
            assert any(x<=a and y<=b and v<=c for (x,y),v in retained.items())
            counts['whole_quadrant_domination_controls']+=1
        tables.append([[a,b,c] for (a,b),c in sorted(table.items())])
    outerp=[1,6]+p+[4,3];outerqa=[1,1,1,4,2,1,1,1,1];outerqb=[1,1,1,4,1,2,1,1,1]
    values=[];rootcosts=[]
    for qq in (outerqa,outerqb):
        value,_=cubic(outerp,qq);literal=[cost(label(sh)[0],outerp,qq) for sh in shapes(8)]
        assert value==min(literal);counts['context_shape_evaluations']+=len(literal);values.append(value)
        rootcosts.append([sum(outerp)+sum(qq)+cubic(outerp[:r],qq[:r+1])[0]+cubic(outerp[r+1:],qq[r+1:])[0] for r in range(8)])
    assert values==[101,100]
    signed_values=[]
    for q in (qa,qb):
        qq=list(q);qq[-1]=-1;signed_values.append(signed_cubic(p,qq,counts))
    assert signed_values==[33,34]
    collision=dict(keys=p,interior_gaps_A=qa[1:-1],interior_gaps_B=qb[1:-1],actual_endpoint_gaps=[1,1],actual_mass=18,profile_tables=tables,retained_planes=[[a,b,c] for (a,b),c in retained.items()],context_keys=outerp,context_gaps_A=outerqa,context_gaps_B=outerqb,context_costs=values,context_root_costs=rootcosts,signed_absolute_endpoint_probe=[0,-1],signed_values=signed_values)
    print('small',dict(counts),flush=True)
    for n in (1024,4096,16384,65536):
        for kind in ('random','uniform','zeros'):
            p=[rng.randrange(100) for _ in range(n)];q=[rng.randrange(100) for _ in range(n+1)]
            if kind=='uniform':p=[1]*n;q=[1]*(n+1)
            if kind=='zeros':p=[0]*n;q=[0]*(n+1)
            stats=Counter();oracle=LineOracle(p,q,stats);answer=recover_gaps(p,sum(p)+sum(q),q[0],oracle,stats)
            assert answer==q and stats['signed_recovery_queries']<=n
            rows.append(dict(n=n,kind=kind,counts=stats,verification='exact linear chain representation and complete recovery; no large independent signed-DP oracle'))
            print('large',n,kind,stats['signed_recovery_queries'],flush=True)
    root=Path(__file__).resolve().parents[1];files=('signed_boundary.py','signed_boundary_audit.py','boundary_response.py','research.py','pair_skeleton.py')
    out=dict(scope='Information sufficiency of signed endpoint response with known key weights, total mass, and left endpoint gap; not a general subquadratic constructor.',seed=511020,counts=counts,collision=collision,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/signed_boundary_audit.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
