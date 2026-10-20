#!/usr/bin/env python3
"""Adversarial actual-OBST DAG size search; exact values, no timings."""
from collections import Counter
from pathlib import Path
import hashlib,json,random
from slot_vector import normalize,gap_pass
from slot_dag import Diagram,solve
from slot_records_audit import check_tree
from trimmed_height import knuth_fallback


def sizes(values,h,stats):
    # Independently normalize every complete block, bottom up. Infinity is None.
    refs=[None if x is None else (x,0) for x in values]
    counts=[int(any(x is not None for x in refs))]
    for d in range(1,h+1):
        unique={};nextrefs=[]
        for i in range(0,len(refs),2):
            l,r=refs[i:i+2];stats['size_block_visits']+=1
            if l is None and r is None:nextrefs.append(None);continue
            a=min(x[0] for x in (l,r) if x is not None)
            key=tuple(None if x is None else (x[0]-a,x[1]) for x in (l,r))
            if key not in unique:unique[key]=len(unique)
            nextrefs.append((a,unique[key]))
        counts.append(len(unique));refs=nextrefs
    return counts


def evaluate(p,q,h,stats,verify=False):
    w,g,c=normalize(p,q);n=len(w)
    v=[0]+[(b&-b).bit_length()-1 for b in range(1,2**h)]
    old=[None]*2**h;old[0]=0;rows=[];vectors=[]
    for k in range(n):
        old,_=gap_pass(old,k,w[k],g[k],v,h,stats)
        rows.append(sizes(old,h,stats))
        if verify:vectors.append(old)
    optimum=h*(sum(w)+sum(g))+min(x for x in old if x is not None)+c
    reference,_=knuth_fallback(p,q,stats)
    assert optimum==reference  # h=n throughout, hence unrestricted.
    if verify:
        def observe(k,m,ref):
            assert m.reachable([ref])==sum(rows[k-1])
            for b,x in enumerate(vectors[k-1]):
                assert m.value(ref,b)==x
                stats['searched_prefix_controls']+=1
        answer=solve(p,q,h,stats,observe)
        assert answer['cost']==optimum==check_tree(answer['tree'],p,q,h,stats)
    return rows


def main():
    root=Path(__file__).resolve().parents[1];rng=random.Random(591019)
    counts=Counter();out=[]
    for n,trials in ((6,48),(8,48),(10,48),(12,32),(14,20),(16,8)):
        base=8*(n+1)**2;best=None;attempts=[]
        for trial in range(trials):
            if trial<6 or trial%8==0:
                order=list(range(1,n+1));rng.shuffle(order)
                if trial==0:order=list(range(n,0,-1))
                if trial==1:order=list(range(1,n+1))
                p=[base**e-1 for e in order]
                q=[1]*(n+1)
                if trial>=2:q=[base**rng.randrange(n+1) for _ in range(n+1)]
            else:
                p,q=best['p'][:],best['q'][:]
                target=p if rng.randrange(2)==0 else q
                a,b=rng.sample(range(len(target)),2)
                if rng.randrange(3):target[a],target[b]=target[b],target[a]
                else:target[a]=base**rng.randrange(n+1)
            rows=evaluate(p,q,n,counts)
            score=max(map(sum,rows));final=sum(rows[-1])
            attempts.append(dict(trial=trial,largest_nodes=score,final_nodes=final))
            if best is None or (score,final)>(best['largest_nodes'],best['final_nodes']):
                best=dict(p=p,q=q,largest_nodes=score,final_nodes=final,by_stage_level=rows,trial=trial)
        control=Counter();assert evaluate(best['p'],best['q'],n,control,True)==best['by_stage_level']
        out.append(dict(n=n,height=n,base=base,trials=trials,winner=best,attempts=attempts,control_counts=control))
        print(n,best['largest_nodes'],best['final_nodes'],flush=True)
    files=['slot_dag_size_search.py','slot_dag.py','slot_vector.py','slot_records.py',
           'slot_records_audit.py','trimmed_height.py']
    result=dict(scope='Finite local search over actual mixed OBST prefix functions at h=n; no asymptotic size bound inferred',seed=591019,rows=out,search_counts=counts,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_dag_size_search.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
