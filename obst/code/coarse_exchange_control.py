#!/usr/bin/env python3
"""Retained exact trap for descendant promotions plus one bottom-gap swap."""
from itertools import combinations
from pathlib import Path
import hashlib,json
from research import shapes,label,cost,promotions,knuth


def expanded(B,selected):
    selected=set(selected)
    def build(size,offset):
        if size==1:return (None,None) if offset in selected else None
        half=size//2
        return build(half,offset),build(half,offset+half)
    return label(build(B,0))[0]


def main():
    B=8;n=9;S=(6,7);T=expanded(B,S)
    p=[2,5,4,4,5,2,0,4,4];q=[3,4,4,6,8,7,1,1,7,2]
    basep=[1]*n;baseq=[1]*(n+1);base=cost(T,basep,baseq)
    ts=[label(s)[0] for s in shapes(n)]
    bestbase=min(cost(t,basep,baseq) for t in ts);assert base==bestbase
    family={expanded(B,s) for s in combinations(range(B),2)}
    assert family=={t for t in ts if cost(t,basep,baseq)==base}
    neighbors={expanded(B,(set(S)-{a})|{b}) for a in S for b in range(B) if b not in S}
    neighbors.update(t for t in promotions(T) if t in family)
    actual=cost(T,p,q);best=min(cost(t,p,q) for t in family)
    costs=sorted(cost(t,p,q) for t in neighbors)
    assert actual==219 and best==212 and len(neighbors)==14 and min(costs)>actual
    delta=(n-1)*(sum(p)+sum(q))+1
    fp=[delta+a for a in p];fq=[delta+a for a in q]
    value,tree,scans=knuth(fp,fq)
    assert value==delta*base+best==min(cost(t,fp,fq) for t in ts)
    assert all(cost(t,fp,fq)>cost(T,fp,fq) for t in promotions(T))
    assert all(cost(t,fp,fq)>cost(T,fp,fq) for t in neighbors)
    root=Path(__file__).resolve().parents[1]
    out=dict(scope='One exact strict local trap; no general algorithmic lower bound',
             B=B,n=n,expanded_slots=S,p=p,q=q,base_cost=base,
             candidate_tree=T,candidate_error_cost=actual,optimum_error_cost=best,
             neighbors=sorted(neighbors,key=repr),neighbor_error_costs=costs,
             original_delta=delta,original_candidate=cost(T,fp,fq),original_optimum=value,
             literal_shapes=len(ts),coarse_optima=len(family),knuth_candidates=scans,
             source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest()
                            for f in ('coarse_exchange_control.py','research.py')})
    (root/'results/coarse_exchange_control.json').write_text(json.dumps(out,indent=2)+'\n')
    print({k:v for k,v in out.items() if k not in ('neighbors','candidate_tree','source_sha256')})


if __name__=='__main__':main()
