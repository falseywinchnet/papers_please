#!/usr/bin/env python3
"""Harness-first controls for adaptive reachable coarse-optimal grammars.

Independent all-root and literal-tree controls precede importing the new
constructor. Counts refer to exact arithmetic and explicit traversal events.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib,json,math,random
from coarse_face_structure import all_roots,reachable
from research import shapes,label,cost,knuth


def two_roots(m):
    n=3*m-1;p=[1]*n;q=[1]*(n+1)
    p[m-1]=p[2*m-1]=2
    return p,q


def perfect(i,j):
    if i==j:return None
    assert (j-i+1)&(j-i)==0
    r=(i+j)//2
    return r,perfect(i,r),perfect(r+1,j)


def two_trees(m):
    n=3*m-1;a=m-1;c=2*m-1
    return ((a,perfect(0,a),perfect(a+1,n)),
            (c,perfect(0,c),perfect(c+1,n)))


def literal_rules(t,n):
    out=set();stack=[(t,0,n)]
    while stack:
        node,i,j=stack.pop()
        if node is None:assert i==j;continue
        r,left,right=node;out.add((i,j,r))
        stack.extend(((left,i,r),(right,r+1,j)))
    return out


def perturb(p,q,rng):
    n=len(p);errors=list(range(1,2*n+2));rng.shuffle(errors)
    errors=[Fraction(e if rng.randrange(2) else -e,7) for e in errors]
    # Nonnegative fine inputs even at zero coarse coordinates.
    errors=[abs(e) if a==0 else e for a,e in zip((*p,*q),errors)]
    delta=(n+1)*sum(map(abs,errors))+1
    x=[delta*a+e for a,e in zip((*p,*q),errors)]
    return x[:n],x[n:],delta


def rational_knuth(p,q):
    denominator=math.lcm(*(Fraction(x).denominator for x in (*p,*q)))
    value,tree,scans=knuth([int(x*denominator) for x in p],
                          [int(x*denominator) for x in q])
    return Fraction(value,denominator),tree,scans


def main():
    rng=random.Random(682019);reference=Counter();checks=Counter();rows=[]
    # Establish the proposed family without invoking any optimized code.
    for m in (2,4,8,16,32):
        p,q=two_roots(m);n=len(p);C,R=all_roots(p,q,reference)
        seen,arcs=reachable(n,R,reference);ts=two_trees(m)
        expected=literal_rules(ts[0],n)|literal_rules(ts[1],n)
        assert arcs==expected and R[0,n]==[m-1,2*m-1]
        assert all(len(R[ij])==1 for ij in seen if ij!=(0,n))
        assert all(cost(t,p,q)==C[0,n] for t in ts)
        assert len(seen)<=2*n and len(arcs)<=2*n
        checks['two_tree_dense_family_controls']+=1
        if n<=11:
            opt=[label(s)[0] for s in shapes(n) if cost(label(s)[0],p,q)==C[0,n]]
            assert set(opt)==set(ts);checks['two_tree_literal_family_controls']+=1
    from coarse_grammar import Prepared,solve,two_tree_refine,EntryIndex
    from core_monge import Monge
    # Entry index is checked separately on arbitrary nonnegative densities.
    for n in range(1,20):
        stats=Counter();entries=[(i,j,rng.randrange(1,8)) for i in range(n) for j in range(n) if rng.randrange(3)==0]
        matrix=Monge([0]*(n+1),[0]*(n+1),entries,stats);index=EntryIndex(matrix)
        for i in range(n+1):
            for j in range(n+1):
                assert index.query(i,j)==matrix.value_reference(i,j)
                checks['entry_index_controls']+=1
    aggregate=Counter()
    for n in range(1,13):
        for trial in range(8):
            p=[0]*n if trial==0 else [rng.randrange(5) for _ in range(n)]
            q=[0]*(n+1) if trial==0 else [rng.randrange(5) for _ in range(n+1)]
            C,R=all_roots(p,q,reference);seen,arcs=reachable(n,R,reference)
            stats=Counter();prepared=Prepared(p,q,stats,budget=None)
            assert prepared.available and prepared.value==C[0,n]
            actual={(i,j,r) for (i,j),roots in prepared.rules.items() for r in roots}
            assert set(prepared.rules)==seen and actual==arcs
            checks['exact_grammar_controls']+=1
            if n<=7:
                literal=set()
                for s in shapes(n):
                    t=label(s)[0];checks['literal_tree_costs']+=1
                    if cost(t,p,q)==C[0,n]:literal.update(literal_rules(t,n))
                assert actual==literal;checks['literal_grammar_controls']+=1
            for repeat in range(3):
                fp,fq,d=perturb(p,q,rng);fine,_=all_roots(fp,fq,reference)
                result=prepared.refine(fp,fq,d,stats)
                assert result['method']=='grammar' and result['cost']==fine[0,n]
                assert cost(result['tree'],fp,fq)==fine[0,n]
                assert cost(result['tree'],p,q)==C[0,n]
                checks['reused_exact_fine_controls']+=1
            # Rejected perturbations and prematurely exhausted plans remain exact.
            fp=list(range(1,n+1));fq=list(range(n+1))
            result=prepared.refine(fp,fq,Fraction(1,1000),stats)
            fine,_=all_roots(fp,fq,reference)
            assert result['cost']==fine[0,n]
            if n>1:assert result['method']=='knuth'
            stopped=Prepared(p,q,stats,budget=0)
            assert not stopped.available and stopped.rules=={}
            result=stopped.refine(p,q,1,stats)
            assert result['cost']==C[0,n] and result['method']=='knuth'
            checks['budget_fallback_controls']+=1
            aggregate.update(stats)
    # Hole and unrestricted zero-weight grammar controls.
    prepared=Prepared([4,1,4],[1]*4,budget=None)
    assert prepared.rules[0,3]==[0,2];checks['root_hole_controls']+=1
    for n in (0,1,2,5,11,20):
        p=[rng.randrange(20) for _ in range(n)];q=[rng.randrange(20) for _ in range(n+1)]
        stats=Counter();result=solve(p,q,stats)
        expected=0 if n==0 else all_roots(p,q,reference)[0][0,n]
        assert result['cost']==expected==cost(result['tree'],p,q)
        checks['automatic_full_controls']+=1;aggregate.update(stats)
    # Both branches of the two-tree optimum are exposed in certified queries.
    for m in (2,4,8,16,32,64,128):
        p,q=two_roots(m);n=len(p);pre=Counter()
        prepared=Prepared(p,q,pre);assert prepared.available
        assert prepared.rules[0,n]==[m-1,2*m-1]
        assert prepared.states<=2*n and prepared.arcs<=2*n
        assert pre['grammar_candidate_roots']<=3*n
        query_rows=[]
        for trial in range(3):
            fp,fq,d=perturb(p,q,rng);counts=Counter()
            result=prepared.refine(fp,fq,d,counts)
            candidates=[cost(t,fp,fq) for t in two_trees(m)]
            assert result['cost']==min(candidates)==cost(result['tree'],fp,fq)
            direct_counts=Counter();direct=two_tree_refine(fp,fq,d,direct_counts)
            assert direct['method']=='two_tree' and direct['cost']==result['cost']
            assert direct['difference']==candidates[0]-candidates[1]
            assert cost(direct['tree'],fp,fq)==result['cost']
            checks['direct_linear_full_controls']+=1
            assert cost(result['tree'],p,q)==prepared.value
            if n<=191:
                value,tree,scans=rational_knuth(fp,fq)
                assert result['cost']==value;checks['scale_full_knuth_controls']+=1
            query_rows.append(dict(p=list(map(str,fp)),q=list(map(str,fq)),delta=str(d),
                                   cost=str(result['cost']),root=result['tree'][0],
                                   counts=dict(counts),direct_counts=dict(direct_counts)))
        # Deterministically expose each endpoint using a tiny positive root bump.
        exposed=[]
        for root in (m-1,2*m-1):
            fp=[(n+1)*a for a in p];fq=[(n+1)*a for a in q];fp[root]+=1
            result=prepared.refine(fp,fq,n+1)
            assert result['tree'][0]==root;exposed.append(root)
            assert two_tree_refine(fp,fq,n+1)['tree'][0]==root
        fp=list(range(n));fq=list(range(n+1))
        rejected=two_tree_refine(fp,fq,1)
        assert rejected['method']=='knuth'
        assert rejected['cost']==knuth(fp,fq)[0]
        checks['direct_rejection_controls']+=1
        assert prepared.states==n+1 and prepared.arcs==n+2
        assert pre['grammar_candidate_roots']==4*m
        rows.append(dict(family='two_optima',n=n,m=m,mass=sum(p)+sum(q),
                         states=prepared.states,arcs=prepared.arcs,
                         candidates=pre['grammar_candidate_roots'],preparation=dict(pre),
                         queries=query_rows,exposed_roots=exposed,
                         reference='Full independent Knuth and explicit two-tree theorem' if n<=191 else 'Explicit two-tree theorem and complete original-cost check'))
        print('two_optima',n,prepared.states,prepared.arcs,flush=True)
    for n in (32,64,128):
        p=[rng.randrange(1,9) for _ in range(n)]
        q=[rng.randrange(1,9) for _ in range(n+1)]
        pre=Counter();prepared=Prepared(p,q,pre);query_rows=[]
        for trial in range(2):
            fp,fq,d=perturb(p,q,rng);counts=Counter()
            result=prepared.refine(fp,fq,d,counts);value,tree,scans=rational_knuth(fp,fq)
            assert result['cost']==value==cost(result['tree'],fp,fq)
            query_rows.append(dict(p=list(map(str,fp)),q=list(map(str,fq)),
                                   delta=str(d),cost=str(value),method=result['method'],
                                   counts=dict(counts)))
            checks['unstructured_scale_knuth_controls']+=1
        rows.append(dict(family='unstructured_lattice',n=n,p=p,q=q,
                         states=prepared.states,arcs=prepared.arcs,available=prepared.available,
                         preparation=dict(pre),queries=query_rows,reference='Full independent Knuth'))
    # Automatic scale selection includes its own preparation and full output.
    for m in (2,4,8,16):
        p,q=two_roots(m);n=len(p);delta=100*n**4
        fp=[delta*a+i+1 for i,a in enumerate(p)]
        fq=[delta*a+n+j+1 for j,a in enumerate(q)]
        counts=Counter();result=solve(fp,fq,counts);value,tree,scans=knuth(fp,fq)
        assert result['method']=='grammar' and result['cost']==value==cost(result['tree'],fp,fq)
        checks['automatic_accepted_controls']+=1
        rows.append(dict(family='automatic_two_optima',n=n,counts=dict(counts),
                         cost=value,scale=str(result['delta']),error=str(result['error']),
                         reference='Full independent Knuth'))
    # Keep the known dense grammar family, including partial preparation work.
    for B in (2,4,8,16):
        n=6*B-1;p=[1]*n;q=[1]*(n+1);pre=Counter()
        prepared=Prepared(p,q,pre);fp,fq,d=perturb(p,q,rng);counts=Counter()
        result=prepared.refine(fp,fq,d,counts);value,tree,scans=rational_knuth(fp,fq)
        assert result['cost']==value==cost(result['tree'],fp,fq)
        if B>=8:assert not prepared.available and result['method']=='knuth'
        rows.append(dict(family='uniform_dense_control',n=n,available=prepared.available,
                         budget=prepared.budget,preparation=dict(pre),query=dict(counts),
                         reference='Full independent Knuth'))
    root=Path(__file__).resolve().parents[1]
    files=('coarse_grammar.py','coarse_grammar_audit.py','coarse_face.py',
           'coarse_face_structure.py','core_monge.py','compact_obst.py','trimmed_height.py','research.py')
    output=dict(seed=682019,scope='Adaptive exact coarse-optimal grammar construction and full arbitrary rational refinement; no universal sparse-grammar claim',
                checks=dict(checks),reference=dict(reference),small_construction_counts=dict(aggregate),
                rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/coarse_grammar_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(dict(checks),flush=True)


if __name__=='__main__':main()
