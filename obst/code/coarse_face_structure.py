#!/usr/bin/env python3
"""Independent audit of reachable coarse-optimal intervals and rotation traps.

No new constructor is claimed. Direct all-root dynamic programming and literal
shape enumeration test the proposed representation before any implementation.
Large rows evaluate proved formulas only and are labeled as such.
"""
from collections import Counter
from pathlib import Path
import hashlib,json,random
from research import shapes,label,cost,rotations,knuth


def all_roots(p,q,stats):
    n=len(p);C={};R={}
    for i in range(n+1):C[i,i]=0
    for size in range(1,n+1):
        for i in range(n-size+1):
            j=i+size;best=None;roots=[]
            for r in range(i,j):
                v=C[i,r]+C[r+1,j];stats['reference_root_candidates']+=1
                if best is None or v<best:best=v;roots=[r]
                elif v==best:roots.append(r)
            C[i,j]=best+sum(p[i:j])+sum(q[i:j+1]);R[i,j]=roots
            stats['reference_interval_states']+=1
    return C,R


def reachable(n,roots,stats):
    seen=set();arcs=set();pending=[(0,n)]
    while pending:
        i,j=pending.pop()
        if i==j or (i,j) in seen:continue
        seen.add((i,j))
        for r in roots[i,j]:
            arcs.add((i,j,r));pending.extend(((i,r),(r+1,j)))
    stats['reachable_intervals']+=len(seen);stats['reachable_root_triples']+=len(arcs)
    return seen,arcs


def intervals(t,i,j,out):
    if t is None:assert i==j;return
    r,left,right=t;out.add((i,j));intervals(left,i,r,out);intervals(right,r+1,j,out)


def minimum_shape(B,extras):
    """A B-1-node perfect upper tree, expanded at selected bottom gaps."""
    assert B>=1 and B&(B-1)==0 and 0<=extras<=B
    def build(slots,start):
        if slots==1:return (None,None) if start<extras else None
        half=slots//2
        return build(half,start),build(half,start+half)
    return build(B,0)


def witness(B,u,v):
    # Fill the other two blocks with the remaining 2B-u-v expansions.
    remaining=2*B-u-v;x2=min(B,remaining);x3=remaining-x2
    parts=[minimum_shape(B,x) for x in (u,v,x2,x3)]
    return label(((parts[0],parts[1]),(parts[2],parts[3])))[0]


def main():
    stats=Counter();rows=[];rng=random.Random(672019)
    # Every small literal optimum contributes exactly the DP-reachable intervals.
    for n in range(1,9):
        ts=[label(s)[0] for s in shapes(n)]
        for trial in range(5):
            p=[1]*n if trial==0 else [rng.randrange(4) for _ in range(n)]
            q=[1]*(n+1) if trial==0 else [rng.randrange(4) for _ in range(n+1)]
            C,R=all_roots(p,q,stats);seen,arcs=reachable(n,R,stats)
            literal=set();literal_arcs=set();best=None;opts=[]
            for t in ts:
                z=cost(t,p,q);stats['literal_tree_costs']+=1
                if best is None or z<best:best=z;opts=[t]
                elif z==best:opts.append(t)
            assert best==C[0,n]
            for t in opts:
                st=[(t,0,n)]
                while st:
                    node,i,j=st.pop()
                    if node is None:continue
                    r,a,b=node;literal.add((i,j));literal_arcs.add((i,j,r))
                    st.extend(((a,i,r),(b,r+1,j)))
            assert literal==seen and literal_arcs==arcs
            stats['literal_reachable_family_checks']+=1
            if trial==0:
                for t in opts:
                    B=n*n+1;ep=[0]*n;st=[(t,0)]
                    while st:
                        node,d=st.pop()
                        if node is None:continue
                        r,a,b=node;ep[r]=B**(n-1-d);st.extend(((a,d+1),(b,d+1)))
                    eq=[0]*(n+1);target=cost(t,ep,eq)
                    assert all(u==t or cost(u,ep,eq)>target for u in ts)
                    D=n*sum(ep)+1;fp=[D+x for x in ep];fq=[D]*(n+1)
                    fine=cost(t,fp,fq)
                    assert (n-1)*sum(ep)<D
                    assert all(u==t or cost(u,fp,fq)>fine for u in ts)
                    stats['unique_exposing_perturbations']+=1
    # Root extremes alone do not imply that intervening roots are optimal.
    p=[4,1,4];q=[1]*4;C,R=all_roots(p,q,stats)
    assert R[0,3]==[0,2] and C[0,3]==24
    hole_costs=[C[0,r]+C[r+1,3]+sum(p)+sum(q) for r in range(3)]
    assert hole_costs==[24,25,24]
    # Exact five-key components and a strict single-rotation local minimum.
    n=5;ts=[label(s)[0] for s in shapes(n)];basep=[1]*n;baseq=[1]*(n+1)
    optimum=min(cost(t,basep,baseq) for t in ts)
    opts={t for t in ts if cost(t,basep,baseq)==optimum};todo=set(opts);components=[]
    while todo:
        stack=[todo.pop()];part=[]
        while stack:
            t=stack.pop();part.append(t)
            for u in rotations(t):
                if u in todo:todo.remove(u);stack.append(u)
        components.append(part)
    assert optimum==27 and sorted(map(len,components))==[2,4]
    t=(1,(0,None,None),(3,(2,None,None),(4,None,None)))
    traps=[]
    for D in (9,16,256,65536):
        p=[D,D+1,D+1,D,D];q=[D]*6
        actual=cost(t,p,q);neighbors=sorted(cost(u,p,q) for u in rotations(t))
        target=min(cost(u,p,q) for u in ts);kvalue,ktree,scans=knuth(p,q)
        assert 4*2<D and target==27*D+3==kvalue==cost(ktree,p,q)
        assert actual==27*D+4 and neighbors==[27*D+5,29*D+3,29*D+5,33*D+6]
        assert all(x>actual for x in neighbors)
        stats['strict_rotation_traps']+=1
        traps.append(dict(delta=D,p=p,q=q,candidate=actual,optimum=target,neighbor_costs=neighbors,tree=t))
    for B in (2,4,8,16,32):
        n=6*B-1;p=[1]*n;q=[1]*(n+1);C,R=all_roots(p,q,stats);seen,arcs=reachable(n,R,stats)
        selected=set();selected_arcs=set()
        for u in range(B+1):
            for v in range(B+1):
                i=B+u;j=2*B-1+u+v
                selected.add((i,j));assert (i,j) in seen
                lo=i+B//2-1+max(0,v-B//2);hi=i+B//2-1+min(v,B//2)
                assert R[i,j]==list(range(lo,hi+1))
                for r in range(lo,hi+1):selected_arcs.add((i,j,r));assert (i,j,r) in arcs
                t=witness(B,u,v);literal=set();intervals(t,0,n,literal)
                assert (i,j) in literal and cost(t,p,q)==C[0,n]
                stats['explicit_witness_trees']+=1
        assert len(selected)==(B+1)**2
        assert len(selected_arcs)==(B+1)*(B//2+1)**2
        # Distinct, unstructured original weights still satisfy the certificate.
        errors=list(range(1,2*n+2));rng.shuffle(errors);D=2*n*sum(errors)
        fp=[D+x for x in errors[:n]];fq=[D+x for x in errors[n:]]
        value,t,scans=knuth(fp,fq)
        assert len(set(fp+fq))==2*n+1 and (n-1)*sum(errors)<D
        assert cost(t,fp,fq)==value and cost(t,p,q)==C[0,n]
        stats['distinct_fine_full_controls']+=1
        rows.append(dict(B=B,n=n,scope='all-root graph and explicit full-tree witnesses',selected_intervals=len(selected),selected_root_triples=len(selected_arcs),all_reachable_intervals=len(seen),all_reachable_root_triples=len(arcs),delta=D,fine_p=fp,fine_q=fq,fine_optimum=value,fine_knuth_candidates=scans))
    formulas=[dict(B=2**k,n=6*2**k-1,selected_intervals=(2**k+1)**2,selected_root_triples=(2**k+1)*(2**(k-1)+1)**2,scope='proved formula only; no graph enumeration') for k in (8,10,12,16,20)]
    root=Path(__file__).resolve().parents[1];files=['coarse_face_structure.py','research.py']
    out=dict(scope='Reachable optimal-interval grammar barriers; no general OBST lower bound',seed=672019,checks=stats,root_hole=dict(p=[4,1,4],q=[1]*4,root_costs=hole_costs),rotation_component_sizes=sorted(map(len,components)),rotation_traps=traps,rows=rows,formula_rows=formulas,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/coarse_face_structure.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
