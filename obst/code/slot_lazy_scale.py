#!/usr/bin/env python3
"""Matched complete lazy searches, including unsuccessful searches and fallback."""
from collections import Counter
from pathlib import Path
import hashlib,json,random
from slot_lazy import solve,Search,Meter,Exhausted
from slot_vector import normalize
from slot_record_barrier import family
from slot_records_audit import check_tree
from trimmed_height import height_bound,knuth_fallback


def main():
    root=Path(__file__).resolve().parents[1];rng=random.Random(653019);rows=[]
    def check(p,q,kind,limit=None):
        counts=Counter();answer=solve(p,q,counts,limit=limit)
        reference_counts=Counter();ref,_=knuth_fallback(p,q,reference_counts)
        assert answer['cost']==ref==check_tree(answer['tree'],p,q,len(p),Counter())
        rows.append(dict(kind=kind,n=len(p),p=p,q=q,height=answer['height'],method=answer['method'],limit=answer['limit'],counts=counts,reference_counts=reference_counts))
        print(kind,len(p),answer['height'],answer['method'],counts['lazy_work'],counts['lazy_expanded_states'],flush=True)
    for n in (32,64,128,256,512):
        check([1]*n,[1]*(n+1),'uniform')
        check([rng.randrange(4) for _ in range(n)],[rng.randrange(3) for _ in range(n+1)],'bounded_mixed')
        check([rng.randrange(2) for _ in range(n)],[rng.randrange(2) for _ in range(n+1)],'binary_mixed')
    for n in (6,8,10,12,14,16,18):
        p,q,w=family(n);check(p,q,'necessary_chain',limit=2000000)
    files=['slot_lazy_scale.py','slot_lazy.py','slot_vector.py','slot_punctured.py',
           'slot_record_barrier.py','slot_records.py','slot_records_audit.py','trimmed_height.py']
    result=dict(scope='Matched exact full constructions; finite counts, no search-size bound; failures of the work budget are retained',seed=653019,rows=rows,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_lazy_scale.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
