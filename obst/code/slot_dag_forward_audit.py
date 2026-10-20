#!/usr/bin/env python3
"""Direct mixed prefixes, original-tree optima, and carry-context injection."""
from collections import Counter
from itertools import product
from fractions import Fraction
from pathlib import Path
import hashlib,json,random
from slot_dag_forward import ForwardDiagram,solve
from slot_vector import normalize
from slot_records_audit import check_tree
from aggregate_core_audit import layers
from trimmed_height import knuth_fallback


def inclusive(manager,ref,d,cache):
    if ref is None:return None
    if d==0:return ref
    if ref[1] not in cache:
        left,right=manager.children((0,ref[1]))
        l=inclusive(manager,left,d-1,cache);r=inclusive(manager,right,d-1,cache)
        if left is not None:r=manager.minimum(r,manager.constant(d-1,left[0]),d-1)
        cache[ref[1]]=manager.make(d,l,r)
    return manager.offset(cache[ref[1]],ref[0])


def main():
    root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(601019)
    def check(p,q,h):
        w,g,c=normalize(p,q);v=[0]+[(b&-b).bit_length()-1 for b in range(1,2**h)]
        old=[None]*2**h;old[0]=0;manager=ForwardDiagram(h);oldref=manager.point(h,0)
        for k in range(len(p)):
            new=[None]*2**h
            for b in range(k+1,2**h):
                new[b]=min(old[a]-w[k]*v[b]-g[k]*min(v[a],v[b]) for a in range(b) if old[a] is not None)
                stats['forward_direct_states']+=1
            captured={}
            def observe(contexts,summaries):captured.update(contexts=contexts,summaries=summaries)
            newref=manager.transition(oldref,w[k],g[k],observe)
            for b,value in enumerate(new):
                assert manager.value(newref,b)==value,(p,q,h,k,b,value,manager.value(newref,b))
                stats['forward_prefix_controls']+=1
            # Independently construct inclusive prefix and map every actual
            # non-pruned block context to a pair of normalized nodes.
            qref=inclusive(manager,oldref,h,{})
            pairs={};seencontexts=set()
            def visit(r,s,d):
                if d==0 or r is None:return
                first=manager.first(s)
                if first is not None and first<=r[0]:return
                relative=None if first is None else first-r[0]
                key=r[1],relative;pair=r[1],s[1]
                assert s[0]==r[0]
                assert manager.first_values[s[1]]==relative
                assert pair not in pairs or pairs[pair]==key
                pairs[pair]=key;seencontexts.add(key)
                l,rr=manager.children(r);ql,qr=manager.children(s)
                visit(l,ql,d-1);visit(rr,qr,d-1)
            visit(oldref,qref,h)
            assert set(captured['contexts'])==seencontexts
            D=manager.reachable([oldref]);Q=manager.reachable([qref])
            assert len(seencontexts)<=D*Q
            assert len(captured['summaries'])<=D
            stats['forward_injection_controls']+=len(seencontexts)
            old=new;oldref=newref
        result=solve(p,q,h,stats)
        expected=list(layers(p,q,h,(h+1)*(sum(p)+sum(q))+1,stats))[-1][0][len(p)]
        assert result['cost']==expected==check_tree(result['tree'],p,q,h,stats)
        stats['forward_full_small_trees']+=1
    for n in range(1,5):
        for values in product((0,1),repeat=2*n+1):
            for h in (n.bit_length(),n.bit_length()+1):
                check(list(values[:n]),list(values[n:]),h)
    for n in (5,8,12):
        for _ in range(8):check([Fraction(rng.randrange(11),3) for i in range(n)],[Fraction(rng.randrange(11),2) for i in range(n+1)],n.bit_length()+1)
    print('small',dict(stats),flush=True)
    rows=[]
    for name in ('slot_dag_size_search','slot_dag_chain_search'):
        source=json.loads((root/'results'/f'{name}.json').read_text())
        for row in source['rows']:
            p=row['winner']['p'];q=row['winner']['q'];h=row['height'];counts=Counter()
            answer=solve(p,q,h,counts);expected,_=knuth_fallback(p,q,counts)
            assert answer['cost']==expected==check_tree(answer['tree'],p,q,h,counts)
            assert answer['stage_nodes']==list(map(sum,row['winner']['by_stage_level']))
            assert counts['dag_min_calls']==counts['dag_add_calls']==counts['dag_prefix_calls']==0
            rows.append(dict(source=name,n=len(p),h=h,stage_nodes=answer['stage_nodes'],counts=counts,
                             previous_all_nodes=row['control_counts']['dag_all_nodes']))
            print(name,len(p),counts['dag_all_nodes'],counts['forward_contexts'],flush=True)
    files=['slot_dag_forward.py','slot_dag_forward_audit.py','slot_dag_skyline.py','slot_dag.py','slot_vector.py',
           'slot_records.py','slot_records_audit.py','aggregate_core_audit.py','trimmed_height.py']
    result=dict(scope='Exact scalar-carry mixed forward construction; polynomial per-update context bound, no bound on all-stage diagram growth',
                seed=601019,counts=stats,large=rows,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files},
                input_sha256={name:hashlib.sha256((root/'results'/f'{name}.json').read_bytes()).hexdigest() for name in ('slot_dag_size_search','slot_dag_chain_search')})
    (root/'results/slot_dag_forward_audit.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
