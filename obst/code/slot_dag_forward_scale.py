#!/usr/bin/env python3
"""Complete scalar-carry constructions at necessary height, with exact counts."""
from pathlib import Path
from collections import Counter
import hashlib,json,random
from slot_dag_forward import solve
from slot_records_audit import check_tree
from trimmed_height import knuth_fallback


def main():
    root=Path(__file__).resolve().parents[1];rows=[];rng=random.Random(602019)
    for n in (24,32,48,64):
        a=8*(n+1)**2
        p=[rng.randrange(1,n+1)*a**(n-i) for i in range(n)]
        q=[rng.randrange(1,n+1)*a**max(0,n-i-1) for i in range(n+1)]
        for i in range(n):assert p[i]>n*(sum(p[i+1:])+sum(q[i:]))
        counts=Counter();answer=solve(p,q,n,counts)
        expected=sum((i+1)*p[i] for i in range(n))+sum(min(i+1,n)*q[i] for i in range(n+1))
        reference,_=knuth_fallback(p,q,counts)
        assert answer['cost']==expected==reference==check_tree(answer['tree'],p,q,n,counts)
        t=answer['tree']
        for i in range(n):assert t[0]==i and t[1] is None;t=t[2]
        assert t is None
        assert counts['dag_min_calls']==counts['dag_add_calls']==counts['dag_prefix_calls']==0
        rows.append(dict(n=n,height=n,p=p,q=q,stage_nodes=answer['stage_nodes'],counts=counts,
                         verification='Strict dominant-key certificate, unique chain cost, independent Knuth, full output tree'))
        print(n,answer['stage_nodes'][-1],counts['dag_all_nodes'],counts['forward_contexts'],flush=True)
    files=['slot_dag_forward_scale.py','slot_dag_forward.py','slot_dag_skyline.py','slot_dag.py',
           'slot_vector.py','slot_records.py','slot_records_audit.py','trimmed_height.py']
    result=dict(scope='Finite full mixed constructions at necessary height; counts do not prove all-stage diagram growth',seed=602019,rows=rows,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_dag_forward_scale.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
