#!/usr/bin/env python3
"""Explicit unprunable Boolean-subset witnesses for lazy skyline search."""
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib,json
from slot_lazy import Search,Meter
from slot_record_barrier import family
from slot_punctured_barrier import greedy


def main():
    root=Path(__file__).resolve().parents[1];rows=[]
    for n in (6,8,10,12):
        p,q,w=family(n);counts=Counter();search=Search(w,[0]*(n+1),n,Meter(counts))
        value,slots=search.run();expected=-sum(w[i]*(n-1-i) for i in range(n))
        assert value==expected
        j=(n-2)//2;states=set();edges=set();central=set()
        for subset in (subset for size in range(1,n-2) for subset in combinations(range(n-2),size)):
            x=0;k=n+1;b=1<<n
            for d in reversed(subset):
                child=b-(1<<d);m=k-1
                assert child>3*(1<<(n-2)) and m>=4
                # This leading-bit prefix of b-1 is an actual skyline edge.
                assert ((b-1)>>d)<<d==child and (b-1)>>d&1
                shift=0 if k==n+1 else -w[k-1]*((b&-b).bit_length()-1)
                bound=search.lower2(m,child)+2*shift
                actual=expected if k==n+1 else -sum(a*v for a,v in zip(w,greedy(k,b)))
                assert bound<2*actual
                assert (m,child) in search.exact
                edges.add((k,b,m,child));x+=1<<d;k=m;b=child
            assert b==(1<<n)-x and k==n-len(subset)+1
            states.add((k,b))
            if len(subset)==j:central.add((k,b))
        assert len(states)==(1<<(n-2))-2
        assert len(central)==comb(n-2,j)
        rows.append(dict(n=n,height=n,central_depth=j,central_states=len(central),forced_states=len(states),forced_edges=len(edges),exact_states=len(search.exact),expanded_states=counts['lazy_expanded_states'],counts=counts))
        print(n,len(states),len(search.exact),len(edges),flush=True)
    formulas=[dict(n=n,central_depth=(n-2)//2,central_states=comb(n-2,(n-2)//2),forced_states=(1<<(n-2))-2,scope='formula only') for n in (16,24,32,64,128,256)]
    files=['slot_lazy_barrier.py','slot_lazy.py','slot_record_barrier.py','slot_punctured_barrier.py',
           'slot_vector.py','slot_punctured.py','slot_records.py','trimmed_height.py']
    result=dict(scope='Unbudgeted mechanical search has an exponential family of reachable states whose relaxation bounds are strictly below true parent optima; budgeted full solver retains quadratic fallback',rows=rows,formula_only_rows=formulas,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_lazy_barrier.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
