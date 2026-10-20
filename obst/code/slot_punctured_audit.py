#!/usr/bin/env python3
"""Harness first: literal prefixes, reset charges, conversion, and full trees."""
from pathlib import Path
from collections import Counter
from itertools import product
from fractions import Fraction
import hashlib,json,random
from slot_punctured import PuncturedDiagram,finite_min,solve,sparse_repair
from slot_dag_forward import ForwardDiagram,solve as old_solve
from slot_vector import normalize
from slot_records_audit import check_tree
from slot_records import sparse_repair as old_repair
from aggregate_core_audit import layers
from trimmed_height import knuth_fallback


def certify(manager,ref,w,g,first,stats):
    source=manager.reachable_set([ref]);before=manager.stats.copy();captured={}
    def observe(contexts,summaries,templates):captured.update(contexts=contexts,summaries=summaries,templates=templates)
    result=manager.transition(ref,w,g,first,observe)
    delta=Counter({k:manager.stats[k]-before[k] for k in manager.stats})
    contexts=captured['contexts'];edges={};seeds=set();resets={}
    def context(r,p):
        if r is None or (p is not None and p<=r[0]):return None
        return r[1],None if p is None else p-r[0]
    root=context(ref,first)
    if root is not None:seeds.add(root)
    for key in contexts:
        node,p=key;l,c,r=manager.children((0,node))
        C=finite_min(None if l is None else l[0],c)
        lc=context(l,p);rc=context(r,finite_min(p,C));inherited=[]
        if lc is not None:inherited.append(lc)
        reset=p is None or (C is not None and C<=p)
        if rc is not None:
            if reset:
                assert node not in resets or resets[node]==rc
                resets[node]=rc;seeds.add(rc);stats['punctured_reset_edges']+=1
            else:inherited.append(rc)
        assert len(inherited)<=1
        for child in (lc,rc):assert child is None or child in contexts
        edges[key]=inherited[0] if inherited else None
    covered=set();path_steps=0
    for seed in seeds:
        key=seed;previous=manager.h+1
        while key is not None:
            d=manager.nodes[key[0]][0];assert d<previous;previous=d
            covered.add(key);path_steps+=1;key=edges[key]
    assert covered==set(contexts)
    bound=manager.h+sum(manager.nodes[u][0]-1 for u in source)
    Z=len(contexts);T=len(captured['templates'])-1
    assert Z<=path_steps<=bound
    assert set(resets)<=source and T<=manager.h
    assert delta['punctured_make_calls']==Z+T
    assert delta['punctured_build_calls']==2*Z+1
    assert delta['punctured_summary_expansions']<=len(source)
    assert delta['punctured_summary_calls']<=2*len(source)+Z
    stats['punctured_update_certificates']+=1;stats['punctured_context_controls']+=Z
    return result,dict(input_nodes=len(source),output_nodes=manager.reachable([result]),contexts=Z,templates=T,
                       context_bound=bound,path_steps=path_steps,counts=delta)


def main():
    root=Path(__file__).resolve().parents[1];rng=random.Random(621019);stats=Counter();generic=[];large=[];sharp=[]
    # Every small slot subset must produce the same repaired tree as the
    # independently retained sorting-based constructor, with a linear walk.
    for h in range(1,5):
        for mask in range(1,1<<((1<<h)-1)):
            slots=[b for b in range(1,1<<h) if mask>>(b-1)&1]
            counts=Counter();tree=sparse_repair(slots,h,counts)
            assert tree==old_repair(slots,h,Counter())
            assert counts['punctured_ancestor_walk_visits']==2*counts['record_ancestor_nodes']
            stats['punctured_repair_subsets']+=1
    # Independent conversion and exact value controls, including infeasible entries.
    for h in range(1,9):
        for trial in range(12):
            vals=[None if rng.randrange(4)==0 else Fraction(rng.randrange(-50,51),3) for _ in range(2**h)]
            old=ForwardDiagram(h);new=PuncturedDiagram(h)
            def build(a,d):
                if d==0:return None if vals[a] is None else (vals[a],0)
                return old.make(d,build(a,d-1),build(a+2**(d-1),d-1))
            oldref=build(0,h);ref=new.from_standard(old,oldref)
            assert ref==new.from_values(vals)
            assert new.reachable([ref])<=old.reachable([oldref])
            for b in range(1,2**h):assert new.value(ref,b)==vals[b];stats['punctured_conversion_values']+=1
            _,row=certify(new,ref,2,3,vals[0],stats);generic.append(dict(height=h,trial=trial,**row))
    def check(p,q,h):
        w,g,_=normalize(p,q);v=[0]+[(b&-b).bit_length()-1 for b in range(1,2**h)]
        old=[None]*2**h;old[0]=0;manager=PuncturedDiagram(h);ref=None
        for k in range(len(p)):
            values=[None]*2**h
            for b in range(k+1,2**h):
                values[b]=min(old[a]-w[k]*v[b]-g[k]*min(v[a],v[b]) for a in range(b) if old[a] is not None)
            ref,row=certify(manager,ref,w[k],g[k],0 if k==0 else None,stats)
            assert ref==manager.from_values(values)
            for b in range(2**h):assert manager.value(ref,b)==values[b];stats['punctured_prefix_controls']+=1
            for stop in range(k+2,2**h+1):
                for price in (0,Fraction(5,3)):
                    e=(stop&-stop).bit_length()-1
                    choices=[(values[a]-price*min(v[a],e),a) for a in range(stop) if values[a] is not None]
                    actual=manager.predecessor(ref,stop,price)
                    assert actual is not None and actual[0]==min(choices)[0] and actual in choices
                    stats['punctured_query_controls']+=1
            old=values
        answer=solve(p,q,h,stats)
        expected=list(layers(p,q,h,(h+1)*(sum(p)+sum(q))+1,stats))[-1][0][len(p)]
        assert answer['cost']==expected==check_tree(answer['tree'],p,q,h,stats)
        stats['punctured_full_small_trees']+=1
    for n in range(1,5):
        for vals in product((0,1),repeat=2*n+1):
            for h in (n.bit_length(),n.bit_length()+1):check(list(vals[:n]),list(vals[n:]),h)
    for n in (5,8,12):
        for _ in range(8):check([Fraction(rng.randrange(11),3) for i in range(n)],[Fraction(rng.randrange(11),2) for i in range(n+1)],n.bit_length()+1)
    print('small',dict(stats),flush=True)
    for name in ('slot_dag_size_search','slot_dag_chain_search'):
        source=json.loads((root/'results'/f'{name}.json').read_text())
        for row in source['rows']:
            p=row['winner']['p'];q=row['winner']['q'];h=row['height'];counts=Counter();manager=PuncturedDiagram(h);ref=None;w,g,_=normalize(p,q);stages=[]
            def observe(k,old,oldref):
                nonlocal ref
                ref,cert=certify(manager,ref,w[k-1],g[k-1],0 if k==1 else None,stats)
                assert ref==manager.from_standard(old,oldref)
                assert manager.reachable([ref])<=old.reachable([oldref])
                stages.append(cert)
            previous=Counter();oldanswer=old_solve(p,q,h,previous,observe)
            answer=solve(p,q,h,counts);expected,_=knuth_fallback(p,q,counts)
            assert answer['cost']==oldanswer['cost']==expected==check_tree(answer['tree'],p,q,h,counts)
            assert answer['stage_nodes']==[s['output_nodes'] for s in stages]
            large.append(dict(source=name,n=len(p),height=h,stage_nodes=answer['stage_nodes'],stages=stages,counts=counts,previous_counts=previous))
            print(name,len(p),counts['punctured_all_nodes'],previous['dag_all_nodes'],flush=True)
    for m in list(range(1,17))+[24,32,48,64]:
        h=2*m;N=2**m;old=ForwardDiagram(h);ref=(0,0)
        cs=[-2**j for j in range(m)]+[-Fraction(2**(j+1)-1,m+1) for j in range(m)]
        for d,c in enumerate(cs,1):ref=old.make(d,ref,old.offset(ref,c))
        manager=PuncturedDiagram(h);ref=manager.from_standard(old,ref)
        assert manager.reachable([ref])==2*m
        _,row=certify(manager,ref,1,1,0,stats)
        assert row['contexts']==3*m*(m+1)//2
        assert row['counts']['punctured_make_calls']==3*m*(m+1)//2+m-1
        assert manager.value(ref,N)>manager.value(ref,N-1)
        sharp.append(dict(m=m,height=h,**row))
    files=['slot_punctured.py','slot_punctured_audit.py','slot_dag_forward.py','slot_dag_skyline.py','slot_dag.py','slot_vector.py','slot_records.py','slot_records_audit.py','aggregate_core_audit.py','trimmed_height.py']
    result=dict(scope='Full mixed construction using first-entry-separated diagrams; O(h(D+1)) per update, no bound on all-stage sizes',seed=621019,counts=stats,generic=generic,large=large,sharp=sharp,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files},
                input_sha256={name:hashlib.sha256((root/'results'/f'{name}.json').read_bytes()).hexdigest() for name in ('slot_dag_size_search','slot_dag_chain_search')})
    (root/'results/slot_punctured_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print('complete',dict(stats),flush=True)

if __name__=='__main__':main()
