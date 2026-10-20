#!/usr/bin/env python3
"""Prefix-operation bounds and full mixed input probes; no timing claims."""
from collections import Counter
from pathlib import Path
import hashlib, json, random
from slot_dag import Diagram, solve
from slot_vector import normalize
from slot_records_audit import check_tree
from trimmed_height import height_bound, knuth_fallback


def main():
    root = Path(__file__).resolve().parents[1]
    rng = random.Random(581020); prefix_rows = []; rows = []; minimum_rows = []
    # Arbitrary signs and infeasibility patterns exercise the prefix lemma.
    for h in range(1, 10):
        for trial in range(12):
            stats = Counter(); manager = Diagram(h, stats)
            if trial < 4:
                coefficients = [rng.randrange(-99,100) for _ in range(h)]
                ref = (0,0)
                for d in range(1,h+1):
                    ref = manager.make(d, ref, manager.offset(ref, coefficients[d-1]))
                values = [sum(coefficients[d] for d in range(h) if b >> d & 1) for b in range(2**h)]
            else:
                values = [None if rng.randrange(5)==0 else rng.randrange(-99,100) for _ in range(2**h)]
                def build(a,d):
                    if d==0: return None if values[a] is None else (values[a],0)
                    return manager.make(d,build(a,d-1),build(a+2**(d-1),d-1))
                ref=build(0,h)
            size=manager.reachable([ref]); before=stats.copy()
            result=manager.prefix(ref,h); best=None
            for b,value in enumerate(values):
                assert manager.value(result,b)==best
                if value is not None and (best is None or value<best):best=value
            counts={k:stats[k]-before[k] for k in stats}
            assert counts.get('dag_prefix_expansions',0)<=size
            assert counts.get('dag_min_calls',0)<=4*(h+1)*max(1,size)
            assert counts.get('dag_created_nodes',0)<=4*(h+1)*max(1,size)
            prefix_rows.append(dict(h=h,trial=trial,input_nodes=size,output_nodes=manager.reachable([result]),counts=counts))
    print('prefix',len(prefix_rows),flush=True)
    # A formal lower-bound family for generic pointwise minima, not OBST.
    for m in range(1,13):
        h=2*m;N=2**m;stats=Counter();manager=Diagram(h,stats)
        def linear(coefficients):
            ref=(0,0)
            for d,coefficient in enumerate(coefficients,1):
                ref=manager.make(d,ref,manager.offset(ref,coefficient))
            return ref
        f=linear([-2*2**d+(2**(d-m) if d>=m else 0) for d in range(h)])
        g=linear([-2*2**d+(2**d if d<m else 0) for d in range(h)])
        assert manager.reachable([f])==h+1==manager.reachable([g])
        result=manager.minimum(f,g,h);middle=set();checks=0
        for x in range(N):
            ref=result
            for bit in range(h-1,m-1,-1):
                left,right=manager.children(ref)
                ref=right if x >> (bit-m) & 1 else left
            middle.add(ref[1])
            ys=range(N) if m<=6 else sorted({0,max(0,x-1),x,min(N-1,x+1),N-1})
            for y in ys:
                b=x*N+y
                assert manager.value(f,b)==-2*b+x
                assert manager.value(g,b)==-2*b+y
                assert manager.value(result,b)==-2*b+min(x,y)
                checks+=1
        assert len(middle)==N
        assert manager.reachable([result])==3*N-2
        minimum_rows.append(dict(m=m,height=h,input_nodes_each=h+1,distinct_middle_nodes=len(middle),
                                 output_nodes=manager.reachable([result]),value_controls=checks,counts=stats))
    print('minimum barrier',[(r['m'],r['output_nodes']) for r in minimum_rows],flush=True)
    for kind in ('random_mixed','near_uniform','nonaffine_geometric'):
        sizes=(8,12,16) if kind=='nonaffine_geometric' else (16,32,64)
        for n in sizes:
            if kind=='random_mixed':
                p=[rng.randrange(1,10) for _ in range(n)];q=[rng.randrange(1,10) for _ in range(n+1)]
            elif kind=='near_uniform':
                p=[3+rng.randrange(2) for _ in range(n)];q=[2+rng.randrange(2) for _ in range(n+1)]
            else:
                a=8*(n+1)**2;p=[a**(n-i)-1 for i in range(n)]
                q=[rng.randrange(1,4) for _ in range(n+1)]
                q[0:3]=[1,3,2]
            w,g,_=normalize(p,q);h=height_bound(w,g)['height']
            counts=Counter();reference_counts=Counter()
            result=solve(p,q,h,counts)
            expected,_=knuth_fallback(p,q,reference_counts)
            assert result['cost']==expected==check_tree(result['tree'],p,q,h,counts)
            rows.append(dict(kind=kind,n=n,height=h,p=p,q=q,stage_nodes=result['stage_nodes'],
                             counts=counts,reference_counts=reference_counts,
                             verification='Full mixed DAG construction at certified sufficient height, independent Knuth optimum, complete output tree'))
            print('mixed full',kind,n,h,counts['dag_all_nodes'],flush=True)
    files=['slot_dag_probe.py','slot_dag.py','slot_vector.py','slot_records.py',
           'slot_records_audit.py','trimmed_height.py']
    out=dict(scope='Finite prefix-operation and unrestricted mixed full-tree controls; no diagram-size upper bound inferred',
             seed=581020,prefix_rows=prefix_rows,minimum_rows=minimum_rows,full_rows=rows,
             source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_dag_probe.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':main()
