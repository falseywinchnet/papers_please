#!/usr/bin/env python3
"""Matched full constructions and certified-height arbitrary mixed controls."""
from pathlib import Path
from collections import Counter
import hashlib,json,random
from slot_punctured import solve
from slot_records_audit import check_tree
from trimmed_height import knuth_fallback,height_bound


def main():
    root=Path(__file__).resolve().parents[1];source=root/'results/slot_dag_forward_scale.json'
    previous=json.loads(source.read_text());rng=random.Random(622019);rows=[]
    def check(p,q,h,kind,old=None,certificate=None):
        counts=Counter();answer=solve(p,q,h,counts);reference,_=knuth_fallback(p,q,counts)
        assert answer['cost']==reference==check_tree(answer['tree'],p,q,h,counts)
        if kind=='necessary_chain':
            n=len(p)
            for i in range(n):assert p[i]>n*(sum(p[i+1:])+sum(q[i:]))
            expected=sum((i+1)*p[i] for i in range(n))+sum(min(i+1,n)*q[i] for i in range(n+1))
            assert answer['cost']==expected
            tree=answer['tree']
            for i in range(n):assert tree[0]==i and tree[1] is None;tree=tree[2]
            assert tree is None
        row=dict(kind=kind,n=len(p),height=h,p=p,q=q,stage_nodes=answer['stage_nodes'],counts=counts,
                 height_certificate=certificate,previous_counts=None if old is None else old['counts'],
                 previous_stage_nodes=None if old is None else old['stage_nodes'])
        rows.append(row)
        print(kind,len(p),h,answer['stage_nodes'][-1],counts['punctured_all_nodes'],counts['punctured_make_calls'],flush=True)
    for row in previous['rows']:check(row['p'],row['q'],row['height'],'necessary_chain',row)
    for n in (32,64,128,256):
        p=[rng.randrange(4) for _ in range(n)];q=[rng.randrange(3) for _ in range(n+1)]
        cert=height_bound(p,q);check(p,q,cert['height'],'bounded_integer',certificate=cert)
    files=['slot_punctured_scale.py','slot_punctured.py','slot_vector.py','slot_records.py','slot_records_audit.py','trimmed_height.py']
    result=dict(scope='Full exact construction on matched necessary-height chains and arbitrary mixed integer inputs at proved sufficient height; no size-growth claim',seed=622019,rows=rows,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files},
                input_sha256={'slot_dag_forward_scale':hashlib.sha256(source.read_bytes()).hexdigest()})
    (root/'results/slot_punctured_scale.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
