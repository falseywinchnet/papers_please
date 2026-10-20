#!/usr/bin/env python3
"""Independent direct predecessors and complete mixed skyline constructors."""
from collections import Counter
from itertools import product
from pathlib import Path
from fractions import Fraction
import hashlib,json,random
from slot_dag_skyline import solve
from slot_dag import solve as previous
from slot_vector import normalize
from slot_records_audit import check_tree
from aggregate_core_audit import layers
from trimmed_height import knuth_fallback


def main():
    root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(592019)
    def check(p,q,h):
        w,g,c=normalize(p,q);v=[0]+[(b&-b).bit_length()-1 for b in range(1,2**h)]
        old=[None]*2**h;old[0]=0
        def observe(k,manager,ref):
            nonlocal old
            values=[None]*2**h
            for b in range(k,2**h):
                values[b]=min(old[a]-w[k-1]*v[b]-g[k-1]*min(v[a],v[b])
                              for a in range(b) if old[a] is not None)
            for b in range(2**h):
                assert manager.value(ref,b)==values[b]
                stats['skyline_direct_prefix_controls']+=1
            # Every prefix query, including absent prefixes and all gap prices.
            for gap in (0,1,7,Fraction(5,3)):
                for b in range(1,2**h+1):
                    e=(b&-b).bit_length()-1
                    candidates=[(values[a]-gap*min(v[a],e),a) for a in range(b) if values[a] is not None]
                    got=manager.predecessor(ref,b,gap)
                    assert (got is None)==(not candidates)
                    if candidates:
                        assert got[0]==min(candidates)[0]
                        assert got in candidates
                    stats['skyline_direct_query_controls']+=1
            # Check the full partial-order property independently, not just queries.
            for a in range(1,2**h):
                if values[a] is None:continue
                for b in range(a,2**h):
                    if v[b]>=v[a]:
                        assert values[b]<=values[a]
                        stats['skyline_dominance_controls']+=1
            old=values
        out=solve(p,q,h,stats,observe)
        expected=list(layers(p,q,h,(h+1)*(sum(p)+sum(q))+1,stats))[-1][0][len(p)]
        assert out['cost']==expected==check_tree(out['tree'],p,q,h,stats)
        stats['skyline_full_small_trees']+=1
    for n in range(1,5):
        for vals in product((0,1),repeat=2*n+1):
            check(list(vals[:n]),list(vals[n:]),n.bit_length()+1)
    for n in (5,8,12):
        for _ in range(8):
            check([Fraction(rng.randrange(9),3) for i in range(n)],
                  [Fraction(rng.randrange(9),2) for i in range(n+1)],n.bit_length()+1)
    print('small',dict(stats),flush=True)
    # Search winners exercise real mixed inputs selected for large diagrams.
    search=json.loads((root/'results/slot_dag_size_search.json').read_text());large=[]
    for row in search['rows']:
        n=row['n'];p=row['winner']['p'];q=row['winner']['q'];counts=Counter()
        out=solve(p,q,n,counts);expected,_=knuth_fallback(p,q,counts)
        assert out['cost']==expected==check_tree(out['tree'],p,q,n,counts)
        assert out['stage_nodes']==list(map(sum,row['winner']['by_stage_level']))
        assert counts['skyline_path_steps']==n*n
        assert counts['skyline_trace_new_nodes']==0
        large.append(dict(n=n,height=n,stage_nodes=out['stage_nodes'],counts=counts))
        print('winner',n,counts['skyline_path_steps'],counts['dag_all_nodes'],flush=True)
    files=['slot_dag_skyline.py','slot_dag_skyline_audit.py','slot_dag.py','slot_vector.py',
           'slot_records.py','slot_records_audit.py','aggregate_core_audit.py','trimmed_height.py']
    result=dict(scope='Exact endpoint dominance, skyline query, and full mixed construction controls; no general diagram-size bound',
                seed=592019,counts=stats,large=large,
                search_sha256=hashlib.sha256((root/'results/slot_dag_size_search.json').read_bytes()).hexdigest(),
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_dag_skyline_audit.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
