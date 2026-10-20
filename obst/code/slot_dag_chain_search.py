#!/usr/bin/env python3
"""Search implicit diagram size on mixed inputs with necessary height n."""
from collections import Counter
from pathlib import Path
import hashlib,json,random
from slot_dag_size_search import evaluate
from slot_dag_skyline import solve
from slot_records_audit import check_tree


def main():
    root=Path(__file__).resolve().parents[1];rng=random.Random(593019);stats=Counter();rows=[]
    for n in (6,8,10,12,14,16):
        a=8*(n+1)**2;best=None;attempts=[]
        for trial in range(8):
            p=[rng.randrange(1,n+1)*a**(n-i) for i in range(n)]
            q=[rng.randrange(1,n+1)*a**max(0,n-i-1) for i in range(n+1)]
            if trial%2 and best is not None:
                p=best['p'][:];q=best['q'][:]
                j=rng.randrange(n+1);q[j]=rng.randrange(1,n+1)*a**max(0,n-j-1)
            # This directly certifies the strict first-key root at every suffix.
            for i in range(n):
                assert p[i]>n*(sum(p[i+1:])+sum(q[i:]))
            sizes=evaluate(p,q,n,stats);score=max(map(sum,sizes));final=sum(sizes[-1])
            attempts.append(dict(trial=trial,largest_nodes=score,final_nodes=final))
            if best is None or (score,final)>(best['largest_nodes'],best['final_nodes']):
                best=dict(p=p,q=q,largest_nodes=score,final_nodes=final,by_stage_level=sizes,trial=trial)
        p,q=best['p'],best['q'];control=Counter();answer=solve(p,q,n,control)
        expected=sum((i+1)*p[i] for i in range(n))+sum(min(i+1,n)*q[i] for i in range(n+1))
        assert answer['cost']==expected==check_tree(answer['tree'],p,q,n,control)
        t=answer['tree']
        for i in range(n):assert t[0]==i and t[1] is None;t=t[2]
        assert t is None
        assert answer['stage_nodes']==list(map(sum,best['by_stage_level']))
        rows.append(dict(n=n,height=n,base=a,trials=8,winner=best,attempts=attempts,control_counts=control,
                         height_certificate='p[i] > n*(sum(p[i+1:])+sum(q[i:])) at every suffix; unique right chain'))
        print(n,best['largest_nodes'],best['final_nodes'],flush=True)
    files=['slot_dag_chain_search.py','slot_dag_size_search.py','slot_dag_skyline.py','slot_dag.py',
           'slot_vector.py','slot_records.py','slot_records_audit.py','trimmed_height.py']
    result=dict(scope='Finite local search on positive mixed inputs with unique height-n optimum; no diagram-size asymptotic claim',
                seed=593019,rows=rows,search_counts=stats,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_dag_chain_search.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
