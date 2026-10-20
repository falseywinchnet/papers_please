#!/usr/bin/env python3
"""Independent controls written before the coarse-regret screening solver."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib,json,math,random
from coarse_face_structure import all_roots
from research import cost,knuth,label,shapes
from trimmed_height import height_bound


def reference_tree(p,q,stats):
    C,R=all_roots(p,q,stats);n=len(p);heights={(i,i):0 for i in range(n+1)};trees={}
    for m in range(1,n+1):
        for i in range(n-m+1):
            j=i+m;r=min(R[i,j],key=lambda r:max(heights[i,r],heights[r+1,j]))
            heights[i,j]=1+max(heights[i,r],heights[r+1,j])
            trees[i,j]=(r,trees.get((i,r)),trees.get((r+1,j)))
    return C,R,trees.get((0,n)),heights


def rational_knuth(p,q):
    d=math.lcm(*(Fraction(x).denominator for x in (*p,*q)))
    v,t,k=knuth([int(d*x) for x in p],[int(d*x) for x in q])
    return Fraction(v,d),t,k


def check_inclusion(tree,p,q,ap,aq,delta,C,hc,hf,stats):
    stack=[(tree,0,len(p))]
    while stack:
        t,i,j=stack.pop()
        if t is None:continue
        r,left,right=t;m=j-i
        errors=[x-delta*a for x,a in zip(p[i:j],ap[i:j])]
        errors += [x-delta*a for x,a in zip(q[i:j+1],aq[i:j+1])]
        positive=sum(max(0,e) for e in errors);negative=sum(max(0,-e) for e in errors)
        allowance=(min(m,hc)-1)*positive+(min(m,hf)-1)*negative
        coarse_actual=cost(t,ap,aq,i,j,0)
        assert delta*(coarse_actual-C[i,j])<=allowance
        root_regret=C[i,r]+C[r+1,j]+sum(ap[i:j])+sum(aq[i:j+1])-C[i,j]
        assert delta*root_regret<=allowance
        stats['optimal_subtree_inclusion_checks']+=1
        stack.extend(((left,i,r),(right,r+1,j)))


def main():
    rng=random.Random(692019);checks=Counter();reference=Counter();rows=[]
    fixtures=[]
    # Verify the proposed signed-error height bound using independent trees.
    for n in range(1,10):
        for trial in range(12):
            ap=[rng.randrange(5) for _ in range(n)]
            aq=[rng.randrange(5) for _ in range(n+1)]
            p=[Fraction(rng.randrange(21),3) for _ in range(n)]
            q=[Fraction(rng.randrange(21),3) for _ in range(n+1)]
            if trial==0:p=[0]*n;q=[0]*(n+1)
            if trial==1:ap=[0]*n;aq=[0]*(n+1)
            delta=Fraction(rng.randrange(1,7),2)
            C,R,_,heights=reference_tree(ap,aq,reference)
            fine,_,t,fh=reference_tree(p,q,reference)
            hc=max(heights.values());hf=height_bound(p,q)['height']
            assert fh[0,n]<=hf
            check_inclusion(t,p,q,ap,aq,delta,C,hc,hf,checks)
            fixtures.append((p,q,ap,aq,delta,C,fine[0,n]))
    from root_ranges import RootRanges
    from core_monge import Monge
    # General finite Monge matrices, independent of OBST padding or weights.
    for n in range(1,16):
        for trial in range(4):
            stats=Counter();top=[0]+[rng.randrange(-30,31) for _ in range(n)]
            left=[0]+[rng.randrange(-30,31) for _ in range(n)]
            entries=[(a,b,rng.randrange(1,8)) for a in range(n) for b in range(n) if rng.randrange(4)==0]
            matrix=Monge(top,left,entries,stats)
            dense=[[matrix.value_reference(i,j) for j in range(n+1)] for i in range(n+1)]
            ranges=RootRanges(matrix);frozen=dict(stats);query=Counter()
            for node in ranges.nodes:
                for i in range(n+1):
                    for j in range(n+1):
                        expected=min(dense[i][r]+dense[r+1][j] for r in range(node.lo,node.hi))
                        assert ranges.value(node,i,j,query)==expected
                        checks['range_product_entry_checks']+=1
            for i in range(n+1):
                for j in range(n+1):
                    values=[dense[i][r]+dense[r+1][j] for r in range(n)]
                    for threshold in (min(values)-1,min(values),max(values)):
                        lo=rng.randrange(n);hi=rng.randrange(lo+1,n+1)
                        before=query['range_enumeration_nodes']
                        got=list(ranges.below(i,j,threshold,query,valid=(lo,hi)))
                        expected=[r for r in range(lo,hi) if values[r]<=threshold]
                        assert got==expected
                        visits=query['range_enumeration_nodes']-before
                        assert visits<=4*(len(got)+2)*(n.bit_length()+1)
                        checks['threshold_enumeration_checks']+=1
            assert dict(stats)==frozen
            assert len(ranges.nodes)==2*n-1
            assert all(v<=2*matrix.k for v in ranges.core_by_depth.values())
            assert sum(node.product_core for node in ranges.nodes)<=sum(ranges.core_by_depth.values())
            assert stats['range_index_nodes']<=(matrix.k+stats['range_product_core_entries'])*(n.bit_length()+1)
            assert stats['range_inner_slots']<=n*(n.bit_length()+1)
            checks['range_partition_charge_checks']+=1
    from coarse_screen import Prepared,solve
    aggregate=Counter()
    for p,q,ap,aq,delta,C,optimum in fixtures:
        n=len(p);pre=Counter();prepared=Prepared(ap,aq,pre);frozen=dict(pre)
        query=Counter();hf=height_bound(p,q)['height'];observed=[]
        def observe(i,j,roots,threshold):
            errors=[x-delta*a for x,a in zip(p[i:j],ap[i:j])]
            errors += [x-delta*a for x,a in zip(q[i:j+1],aq[i:j+1])]
            positive=sum(max(0,e) for e in errors);negative=sum(max(0,-e) for e in errors)
            eta=(min(j-i,prepared.coarse_height)-1)*positive+(min(j-i,hf)-1)*negative
            assert threshold==C[i,j]-sum(ap[i:j])-sum(aq[i:j+1])+eta/delta
            checks['threshold_formula_checks']+=1
            expected=[r for r in range(i,j) if C[i,r]+C[r+1,j]<=threshold]
            assert roots==expected;observed.append((i,j))
            checks['screened_root_set_checks']+=1
        result=prepared.refine(p,q,delta,query,budget=None,observer=observe)
        assert result['cost']==optimum==cost(result['tree'],p,q)
        assert result['method']=='screen' and len(observed)==result['states']
        assert dict(pre)==frozen
        checks['complete_screen_controls']+=1
        E=sum(abs(x-delta*a) for x,a in zip((*p,*q),(*ap,*aq)))
        if (n-1)*E>=delta:checks['old_certificate_failed_but_exact']+=1
        stopped=prepared.refine(p,q,delta,query,budget=0)
        assert stopped['method']=='knuth' and stopped['cost']==optimum
        checks['zero_budget_controls']+=1
        if n<=6:
            ts=[label(s)[0] for s in shapes(n)]
            assert min(cost(t,p,q) for t in ts)==optimum
            checks['literal_full_controls']+=1;checks['literal_tree_costs']+=len(ts)
        aggregate.update(pre);aggregate.update(query)
    # Full automatic construction and matched references at larger sizes.
    for n in (16,32,64,128,256):
        for family in ('random_mixed','near_uniform','geometric'):
            if family=='random_mixed':
                p=[rng.randrange(1,1001) for _ in range(n)]
                q=[rng.randrange(1,1001) for _ in range(n+1)]
            elif family=='near_uniform':
                p=[10**8+rng.randrange(101) for _ in range(n)]
                q=[10**8+rng.randrange(101) for _ in range(n+1)]
            else:p=[1<<i for i in range(n)];q=[1]*(n+1)
            stats=Counter();result=solve(p,q,stats)
            expected,t,scans=knuth(p,q)
            assert result['cost']==expected==cost(result['tree'],p,q)
            checks['automatic_scale_knuth_controls']+=1
            assert stats['range_product_nodes']==2*n-1
            assert stats['range_factor_core_entries']<=2*result['coarse_core']*n.bit_length()
            assert result['coarse_core']<=n+n.bit_length()*result['coarse_mass']
            rows.append(dict(n=n,family=family,p=p,q=q,method=result['method'],
                             cost=str(result['cost']),states=result.get('states'),arcs=result.get('arcs'),
                             coarse_mass=result.get('coarse_mass'),precision=result.get('precision'),
                             coarse_core=result['coarse_core'],coarse_height=result['coarse_height'],
                             fine_height=result['fine_height'],preparation=result['preparation_counts'],
                             query=result['query_counts'],
                             counters=dict(stats),reference_knuth_candidates=scans))
            print(family,n,result['method'],result.get('states'),result.get('arcs'),flush=True)
    for n in (23,47,95,191):
        p=[10**8+rng.randrange(101) for _ in range(n)]
        q=[10**8+rng.randrange(101) for _ in range(n+1)]
        stats=Counter();result=solve(p,q,stats);expected,t,scans=knuth(p,q)
        assert result['cost']==expected==cost(result['tree'],p,q)
        if n>=95:assert result['method']=='knuth'
        checks['dense_uniform_face_controls']+=1
        rows.append(dict(n=n,family='dense_uniform_face',p=p,q=q,method=result['method'],
                         cost=str(result['cost']),states=result.get('states'),arcs=result.get('arcs'),
                         preparation=result['preparation_counts'],query=result['query_counts'],
                         reference_knuth_candidates=scans))
        print('dense_uniform_face',n,result['method'],flush=True)
    for n in (1,3,8,17,31):
        p=[Fraction(rng.randrange(100),rng.randrange(2,8)) for _ in range(n)]
        q=[Fraction(rng.randrange(100),rng.randrange(2,8)) for _ in range(n+1)]
        result=solve(p,q);expected,t,scans=rational_knuth(p,q)
        assert result['cost']==expected==cost(result['tree'],p,q)
        checks['automatic_rational_controls']+=1
    # Reuse a nonuniform base for unrelated fine inputs with large signed errors.
    n=47;ap=[rng.randrange(9) for _ in range(n)];aq=[rng.randrange(9) for _ in range(n+1)]
    pre=Counter();prepared=Prepared(ap,aq,pre);frozen=dict(pre)
    for trial in range(3):
        p=[Fraction(rng.randrange(100),7) for _ in range(n)]
        q=[Fraction(rng.randrange(100),7) for _ in range(n+1)]
        query=Counter();result=prepared.refine(p,q,Fraction(3,2),query)
        expected,t,scans=rational_knuth(p,q)
        assert result['cost']==expected==cost(result['tree'],p,q) and dict(pre)==frozen
        checks['unrelated_reuse_controls']+=1
    for n in (0,1,2,7,16):
        for a,b in ((0,0),(0,7),(3,0),(5,11)):
            result=solve([a]*n,[b]*(n+1),Counter())
            expected=0 if n==0 else reference_tree([a]*n,[b]*(n+1),reference)[0][0,n]
            assert result['cost']==expected==cost(result['tree'],[a]*n,[b]*(n+1))
            checks['uniform_and_empty_controls']+=1
    root=Path(__file__).resolve().parents[1]
    files=('root_ranges.py','coarse_screen.py','coarse_screen_audit.py','core_monge.py',
           'compact_obst.py','coarse_face_structure.py','trimmed_height.py','research.py','coarse_face.py')
    out=dict(seed=692019,scope='Exact range-root products and full arbitrary-weight coarse-regret screening; no universal sparse-screen claim',
             checks=dict(checks),reference=dict(reference),small_counts=dict(aggregate),rows=rows,
             source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/coarse_screen_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(dict(checks),flush=True)


if __name__=='__main__':main()
