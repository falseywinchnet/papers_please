#!/usr/bin/env python3
"""Independent controls for ordered-shape root-range oracles, before implementation."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib,json,random
from final_core_probe import table,profile
from research import cost,cubic,knuth,label,shapes
from ruler_barrier import construct


def gate(p,q):
    n=len(p);a=min(p);b=min(q);E=sum(x-a for x in p)+sum(x-b for x in q)
    dominant=(a+b>(n-1)*E) or E==0
    h=(n+1).bit_length()-1
    ordered=all(max(p[i]-p[i+1],h*(p[i]-p[i+1]))<=q[i+2]-q[i] for i in range(n-1))
    return dominant and ordered


def direct_shape_formula(p,q,i,j):
    m=j-i
    if not m:return 0
    h=(m+1).bit_length()-1;c=(1<<h)-1;s=m-c
    reward=0
    for t in range(1,c+1):
        r=i+t-1+min(s,t)
        reward+=(1+((t&-t).bit_length()-1))*p[r]
    return (h+1)*sum(p[i:j])-reward+h*sum(q[i:j+1])+sum(q[i:i+2*s])


def main():
    rng=random.Random(702020);checks=Counter();reference=Counter();fixtures=[]
    # Establish the shape, root-cost unimodality and closed density expression
    # directly from full all-root tables, before importing any optimized oracle.
    for n in range(1,17):
        for trial in range(9):
            if trial==0:e=list(range(n));f=[0]*(n+1)
            elif trial==1:e=[0]*n;f=[0]*(n+1)
            elif trial==2:e=sorted(rng.randrange(8) for _ in range(n));f=[0]*(n+1)
            else:
                e=[rng.randrange(8) for _ in range(n)]
                step=(n+1).bit_length()*8
                f=[step*i+rng.randrange(step//2+1) for i in range(n+1)]
            E=sum(e)+sum(f);D=n*E+1;p=[D+x for x in e];q=[D+x for x in f]
            assert gate(p,q)
            C,R=table(p,q,reference,True)
            for m in range(1,n+1):
                for i in range(n-m+1):
                    j=i+m;h=(m+1).bit_length()-1;c=(1<<h)-1;s=m-c
                    peak=i+(1<<(h-1))-1+min(s,1<<(h-1))
                    values=[C[i][r]+C[r+1][j] for r in range(i,j)]
                    assert all(values[r-i]>=values[r+1-i] for r in range(i,peak))
                    assert all(values[r-i]<=values[r+1-i] for r in range(peak,j-1))
                    assert direct_shape_formula(p,q,i,j)==C[i][j]
                    checks['unimodal_root_sequences']+=1;checks['literal_shape_formula_checks']+=1
                    if n<=7:
                        t=construct(i,j,Counter())
                        assert cost(t,p,q,i,j,0)==C[i][j]
                        checks['direct_interval_tree_checks']+=1
            if trial==0:
                for i in range(n):
                    for j in range(i+1,n):
                        m=j-i;h=(m+1).bit_length()-1;c=(1<<h)-1;s=m-c
                        expected=2*D+i-c+h if s==0 else 1+((s&-s).bit_length()-1)
                        delta=C[i][j+1]+C[i+1][j]-C[i][j]-C[i+1][j+1]
                        assert delta==expected and delta>0
                        checks['strict_ramp_density_checks']+=1
            fixtures.append((p,q,C))
    print('independent claims',dict(checks),flush=True)
    # Optimized index and complete fine construction are imported only here.
    from ordered_ranges import OrderedRanges
    from ordered_screen import Prepared
    for k,(p,q,C) in enumerate(fixtures):
        n=len(p)
        for mirror in (False,True):
            ap=p[::-1] if mirror else p;aq=q[::-1] if mirror else q
            oracle=OrderedRanges(ap,aq);frozen=dict(oracle.stats);query=Counter()
            def val(i,j):return C[n-j][n-i] if mirror else C[i][j]
            for i in range(n+1):
                for j in range(i,n+1):
                    assert oracle.query(i,j,query)==val(i,j);checks['indexed_interval_values']+=1
                    if i==j:continue
                    values=[val(i,r)+val(r+1,j) for r in range(i,j)]
                    for trial in range(3):
                        lo=rng.randrange(i,j);hi=rng.randrange(lo+1,j+1)
                        got=oracle.minimum(i,j,lo,hi,query)
                        assert got==min(values[lo-i:hi-i]);checks['indexed_root_range_minima']+=1
                        threshold=sorted(values)[rng.randrange(len(values))]+rng.choice((-1,0,1))
                        expected=[r for r in range(lo,hi) if values[r-i]<=threshold]
                        calls=query['ordered_root_cost_calls']
                        assert list(oracle.below(i,j,threshold,query,valid=(lo,hi)))==expected
                        assert query['ordered_root_cost_calls']-calls<=2*n.bit_length()+1
                        checks['indexed_threshold_sets']+=1
            assert dict(oracle.stats)==frozen
        if k%3:continue
        prep=Counter();prepared=Prepared(p,q,prep)
        for kind in ('small','unrelated','rational'):
            if kind=='small':fp=[x+rng.randrange(3) for x in p];fq=[x+rng.randrange(3) for x in q]
            elif kind=='unrelated':fp=[rng.randrange(10) for _ in p];fq=[rng.randrange(10) for _ in q]
            else:fp=[Fraction(rng.randrange(20),3) for _ in p];fq=[Fraction(rng.randrange(20),3) for _ in q]
            query=Counter();delta=Fraction(1,2) if kind=='rational' else 1
            # Direct recurrence supports rationals; the original cubic oracle is integer only.
            ref,_=table(fp,fq,reference,True)
            result=prepared.refine(fp,fq,delta,query,budget=None)
            assert result['cost']==ref[0][n]==cost(result['tree'],fp,fq)
            checks['full_fine_queries']+=1
            if n<=6:
                assert min(cost(label(s)[0],fp,fq) for s in shapes(n))==ref[0][n]
                checks['literal_full_queries']+=1
            stopped=prepared.refine(fp,fq,delta,Counter(),budget=0)
            assert stopped['cost']==ref[0][n] and stopped['method']=='knuth';checks['zero_budget_controls']+=1
    for p,q in (([1,5,1],[1]*4),([100,101,100],[100]*4)):
        try:OrderedRanges(p,q)
        except ValueError:checks['certificate_rejections']+=1
        else:raise AssertionError('invalid coarse input accepted')
    for n in (3,5,9):
        D=n**3+1;p=[Fraction(D+i,7) for i in range(n)][::-1];q=[Fraction(D,7)]*(n+1)
        prepared=Prepared(p,q);fp=[Fraction(rng.randrange(30),5) for _ in p];fq=[Fraction(rng.randrange(30),5) for _ in q]
        ref,_=table(fp,fq,reference,True);result=prepared.refine(fp,fq,Fraction(7,3),Counter(),budget=None)
        assert result['cost']==ref[0][n]==cost(result['tree'],fp,fq)
        checks['rational_coarse_mirrored_controls']+=1
    rows=[]
    for n in (23,47,95,191,383,767):
        D=n*n*n+1;ap=[D+i for i in range(n)];aq=[D]*(n+1)
        pre=Counter();prepared=Prepared(ap,aq,pre)
        for kind in ('base','perturbed','sparse_bumps','unrelated'):
            if kind=='base':p=ap;q=aq
            elif kind=='perturbed':p=[x+rng.randrange(-2,3) for x in ap];q=[x+rng.randrange(-2,3) for x in aq]
            elif kind=='sparse_bumps':
                p=ap[:];q=aq[:]
                for k in (n//3,2*n//3):p[k]+=5
                q[n//2]-=1
                assert not gate(p,q) and not gate(p[::-1],q[::-1])
                checks['fine_outside_ordered_class']+=1
            else:p=[rng.randrange(1,1001) for _ in ap];q=[rng.randrange(1,1001) for _ in aq]
            query=Counter();result=prepared.refine(p,q,1,query)
            v,t,scans=knuth(p,q);assert result['cost']==v==cost(result['tree'],p,q)
            checks['scale_knuth_controls']+=1
            rows.append(dict(n=n,kind=kind,p=p,q=q,coarse_p=ap,coarse_q=aq,method=result['method'],cost=str(v),
                             states=result.get('states'),arcs=result.get('arcs'),preparation=dict(pre),query=dict(query),reference_knuth_candidates=scans))
            print(n,kind,result['method'],result.get('states'),result.get('arcs'),flush=True)
    root=Path(__file__).resolve().parents[1];files=['ordered_range_audit.py','ordered_ranges.py','ordered_screen.py','coarse_screen.py','final_core_probe.py','research.py','ruler_barrier.py','trimmed_height.py','coarse_face.py']
    result=dict(seed=702020,scope='Full interval and root-range oracles under explicit ordered-shape certificates; arbitrary fine inputs with exact fallback',checks=dict(checks),reference=dict(reference),rows=rows,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/ordered_range_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(dict(checks),flush=True)

if __name__=='__main__':main()
