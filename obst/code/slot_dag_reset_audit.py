#!/usr/bin/env python3
"""Reset-path certificates for the unchanged scalar-carry constructor.

Checks arbitrary finite/infinite diagram inputs and actual mixed OBST prefixes.
All work bounds are proved separately; no timing or measured exponent is used.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
from itertools import product
import hashlib,json,random
from slot_dag_forward import ForwardDiagram,finite_min,solve
from slot_vector import normalize
from slot_records_audit import check_tree
from aggregate_core_audit import layers
from trimmed_height import knuth_fallback


def certify(manager,ref,w,g,stats):
    D=manager.reachable([ref]);captured={};before=manager.stats.copy()
    def observe(contexts,summaries):captured.update(contexts=contexts,summaries=summaries)
    result=manager.transition(ref,w,g,observe)
    delta=Counter({k:manager.stats[k]-before[k] for k in manager.stats})
    contexts=captured['contexts'];edges={};seeds=set();parents={}
    def context(r,p):
        if r is None or manager.nodes[r[1]][0]==0:return None
        if p is not None and p<=r[0]:return None
        return r[1],None if p is None else p-r[0]
    root=context(ref,manager.first(ref))
    if root is not None:seeds.add(root)
    for key in contexts:
        node,p=key;d=manager.nodes[node][0]
        left,right=manager.children((0,node))
        c=finite_min(None if left is None else left[0],manager.first(right))
        rightp=finite_min(p,c)
        lc=context(left,p);rc=context(right,rightp)
        inherited=[]
        if lc is not None:inherited.append(lc)
        # Infinity is the greatest value. Ties are classified as resets.
        reset=(p is None or (c is not None and c<=p))
        if rc is not None:
            if reset:
                assert node not in parents or parents[node]==rc
                parents[node]=rc;seeds.add(rc)
                stats['reset_edges']+=1
            else:inherited.append(rc)
        assert len(inherited)<=1,(key,lc,rc,c)
        for child in ([lc] if lc is not None else [])+([rc] if rc is not None else []):
            assert child in contexts
        edges[key]=inherited[0] if inherited else None
        stats['reset_context_controls']+=1
    covered=set();path_steps=0;depth_charge=0
    for seed in seeds:
        state=seed;previous=manager.h+1;length=0
        while state is not None:
            assert state in contexts
            d=manager.nodes[state[0]][0];assert d<previous
            previous=d;length+=1;path_steps+=1;depth_charge+=d
            covered.add(state);state=edges[state]
        assert length<=manager.nodes[seed[0]][0]
    assert covered==set(contexts)
    source_nodes=set();pending=[] if ref is None else [ref[1]]
    while pending:
        node=pending.pop()
        if node in source_nodes:continue
        source_nodes.add(node);_,l,r=manager.nodes[node]
        pending.extend(x[1] for x in (l,r) if x is not None)
    assert set(parents)<=source_nodes
    h=manager.h
    context_bound=h+sum(max(manager.nodes[node][0]-1,0) for node in source_nodes)
    make_bound=h*(h+1)+sum(manager.nodes[node][0]*(manager.nodes[node][0]-1)//2 for node in source_nodes)
    assert len(contexts)<=path_steps<=context_bound
    assert sum(manager.nodes[key[0]][0] for key in contexts)<=depth_charge
    assert delta['forward_contexts']==len(contexts)
    assert delta['forward_calls']==2*len(contexts)+1
    assert delta['dag_make_calls']==delta['forward_replace_visits']
    assert delta['dag_make_calls']<=sum(manager.nodes[key[0]][0] for key in contexts)+h*(h+1)//2
    assert delta['dag_make_calls']<=make_bound
    assert delta['forward_summary_expansions']<=D
    assert delta['forward_summary_calls']<=2*D+len(contexts)
    assert delta['dag_min_calls']==delta['dag_add_calls']==delta['dag_prefix_calls']==0
    stats['reset_updates']+=1
    multiplicity=Counter(key[0] for key in contexts)
    proper=sum(p is not None and (manager.first_values[node] is None or p<manager.first_values[node]) for node,p in contexts)
    return result,dict(input_nodes=D,output_nodes=manager.reachable([result]),contexts=len(contexts),
                       seeds=len(seeds),reset_parent_nodes=len(parents),path_steps=path_steps,
                       max_carries_per_node=max(multiplicity.values(),default=0),proper_carry_contexts=proper,
                       context_bound=context_bound,make_bound=make_bound,counts=delta)


def main():
    root=Path(__file__).resolve().parents[1];rng=random.Random(611019);stats=Counter();generic=[];small=[];large=[]
    # The carry-state count is valid for arbitrary inputs; only correctness
    # as an OBST transition requires actual-prefix endpoint dominance.
    for h in range(1,10):
        for trial in range(16):
            manager=ForwardDiagram(h)
            if trial<8:
                ref=(0,0)
                for d in range(1,h+1):
                    coefficient=Fraction(rng.randrange(-100,101),rng.randrange(1,5))
                    ref=manager.make(d,ref,manager.offset(ref,coefficient))
            else:
                values=[None if rng.randrange(4)==0 else Fraction(rng.randrange(-100,101),3) for _ in range(2**h)]
                def build(a,d):
                    if d==0:return None if values[a] is None else (values[a],0)
                    return manager.make(d,build(a,d-1),build(a+2**(d-1),d-1))
                ref=build(0,h)
            _,row=certify(manager,ref,Fraction(5,3),Fraction(7,2),stats)
            generic.append(dict(height=h,trial=trial,**row))
    # Very high address capacities with compact arbitrary input diagrams.
    for h in (16,32,64,128):
        manager=ForwardDiagram(h);ref=(0,0)
        for d in range(1,h+1):ref=manager.make(d,ref,manager.offset(ref,(-1 if d%3==0 else 1)*(2**d+1)))
        _,row=certify(manager,ref,3,5,stats);generic.append(dict(height=h,trial='compact_signed',**row))
    print('generic',len(generic),flush=True)
    def check(p,q,h,reference=True):
        w,g,c=normalize(p,q);manager=ForwardDiagram(h);ref=manager.point(h,0);stages=[]
        for k in range(len(p)):
            ref,row=certify(manager,ref,w[k],g[k],stats);stages.append(row)
        counts=Counter();answer=solve(p,q,h,counts)
        assert answer['stage_nodes']==[r['output_nodes'] for r in stages]
        assert check_tree(answer['tree'],p,q,h,stats)==answer['cost']
        if reference:
            expected=list(layers(p,q,h,(h+1)*(sum(p)+sum(q))+1,stats))[-1][0][len(p)]
            assert answer['cost']==expected
        else:
            expected,_=knuth_fallback(p,q,stats);assert answer['cost']==expected
        stats['reset_full_trees']+=1
        return dict(n=len(p),height=h,stages=stages,counts=counts)
    for n in range(1,4):
        for values in product((0,1),repeat=2*n+1):
            for h in (n.bit_length(),n.bit_length()+1):
                row=check(list(values[:n]),list(values[n:]),h)
                # Aggregate binary runs without retaining hundreds of repeated rows.
                small.append(dict(n=n,height=h,contexts=sum(r['contexts'] for r in row['stages']),
                                  context_bound=sum(r['context_bound'] for r in row['stages'])))
    for n in (4,8,16):
        for trial in range(8):
            p=[Fraction(rng.randrange(13),3) for _ in range(n)];q=[Fraction(rng.randrange(13),2) for _ in range(n+1)]
            row=check(p,q,n.bit_length()+1);large.append(dict(kind='rational',trial=trial,**row))
    for name in ('slot_dag_size_search','slot_dag_chain_search'):
        source=json.loads((root/'results'/f'{name}.json').read_text())
        for row in source['rows']:
            result=check(row['winner']['p'],row['winner']['q'],row['height'],False)
            assert [s['output_nodes'] for s in result['stages']]==list(map(sum,row['winner']['by_stage_level']))
            large.append(dict(kind=name,**result))
    print('actual',dict(stats),flush=True)
    files=['slot_dag_reset_audit.py','slot_dag_forward.py','slot_dag_skyline.py','slot_dag.py',
           'slot_vector.py','slot_records.py','slot_records_audit.py','aggregate_core_audit.py','trimmed_height.py']
    result=dict(scope='Exact reset-path cover and operation bounds for the unchanged forward constructor; arbitrary diagrams are context-count controls only',
                seed=611019,counts=stats,generic=generic,binary=small,large=large,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files},
                input_sha256={name:hashlib.sha256((root/'results'/f'{name}.json').read_bytes()).hexdigest() for name in ('slot_dag_size_search','slot_dag_chain_search')})
    (root/'results/slot_dag_reset_audit.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
