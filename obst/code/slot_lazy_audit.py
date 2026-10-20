#!/usr/bin/env python3
"""Harness first: rearrangement bounds before lazy full construction."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random
from aggregate_core_audit import layers
from slot_vector import normalize,gap_pass
from slot_records_audit import check_tree
from trimmed_height import knuth_fallback
from slot_lazy import Search,Meter,solve


def main():
    root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(652019)
    fixtures=[]
    for n in range(1,5):
        fixtures.extend((list(x[:n]),list(x[n:])) for x in product((0,1),repeat=2*n+1))
    for n in (5,8,12):
        for _ in range(16):fixtures.append(([Fraction(rng.randrange(13),3) for _ in range(n)],[Fraction(rng.randrange(9),2) for _ in range(n+1)]))
    for p,q in fixtures:
        n=len(p)
        for h in (n.bit_length(),n.bit_length()+1):
            w,g,c=normalize(p,q);counts=Counter();search=Search(w,g,h,Meter(counts))
            vals=[0]+[(b&-b).bit_length()-1 for b in range(1,1<<h)]
            old=[None]*(1<<h);old[0]=0
            for k in range(1,n+1):
                old,_=gap_pass(old,k-1,w[k-1],g[k-1],vals,h,Counter())
                for b in range(k,1<<h):
                    bound=search.lower2(k,b)
                    assert bound<=2*old[b]
                    coeff=sorted(search.coefficients[:k-1],reverse=True)
                    rewards=sorted(vals[1:b],reverse=True)[:k-1]
                    expected=-sum(x*y for x,y in zip(coeff,rewards))-(2*w[k-1]+g[k-1])*vals[b]
                    assert bound==expected
                    stats['bound_entries']+=1
            value,slots=search.run()
            assert value==min(x for x in old if x is not None)
            assert len(slots)==n and all(a<b for a,b in zip(slots,slots[1:]))
            for (k,b),(v,pred) in search.exact.items():
                if k<=n:
                    # Check each evaluated state against a fresh independent
                    # all-predecessor recurrence at this exact ending slot.
                    prev={0:0}
                    for t in range(k):
                        cur={}
                        for end in range(t+1,b+1):
                            cur[end]=min(z-g[t]*min(vals[a],vals[end]) for a,z in prev.items() if a<end)-w[t]*vals[end]
                        prev=cur
                    assert v==prev[b]
                    stats['literal_visited_states']+=1
            M=(h+1)*(sum(p)+sum(q))+1
            assert h*(sum(w)+sum(g))+value+c==list(layers(p,q,h,M,Counter()))[h][0][n]
            stats['height_optimum_controls']+=1
        ref,_=knuth_fallback(p,q,Counter())
        for limit in (0,17,None):
            counts=Counter();ans=solve(p,q,counts,limit=limit)
            assert ans['cost']==ref==check_tree(ans['tree'],p,q,n,Counter())
            if ans['method']=='knuth':assert counts['lazy_work']==ans['limit']+1
            stats['full_tree_controls']+=1;stats['full_'+ans['method']]+=1
    files=['slot_lazy_audit.py','slot_lazy.py','slot_vector.py','slot_punctured.py',
           'slot_records.py','slot_records_audit.py','aggregate_core_audit.py','trimmed_height.py']
    result=dict(scope='Exact relaxation, literal queried-state, prescribed-height optimum, budget fallback and complete original-weight controls',seed=652019,checks=stats,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_lazy_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(stats),flush=True)


if __name__=='__main__':main()
