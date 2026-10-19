#!/usr/bin/env python3
"""Full positive family with distinct gaps and light endpoint keys."""
import hashlib,json
from pathlib import Path
from endpoint_prices import attempt
from shifted_alphabetic import attempt as previous,tree_cost
from research import cubic,knuth


def family(h):
    assert h>=3
    B=1<<h;n=B-1;p=[0]*n;q=[j+1 for j in range(n+1)];q[0]=B;q[-1]=B+n
    def build(lo,hi,d):
        if lo==hi:return None
        r=(lo+hi)//2;p[r]=B+(h+1-d)*B+r
        return r,build(lo,r,d+1),build(r+1,hi,d+1)
    tree=build(0,n,1);p[0]=p[-1]=1;p[2]=B
    expected=((8*h-11)*B*B+(13-7*h)*B)//2-1
    return p,q,tree,expected


def main():
    rows=[]
    for h in (3,4,5,6,7,8,9,10,12,14,16,18):
        p,q,t,expected=family(h);v,tt,s,d=attempt(p,q)
        assert v==expected==tree_cost(t,p,q)==tree_cost(tt,p,q)
        assert s['certified'] and s['oracle_calls']==1 and not s['lp_vertex_triples']
        assert len(set(p))==len(p)-1 and len(set(q))==len(q)
        old,_,os=previous(p,q);assert old is None and os['global_lower_bound']<=v-3
        if h<=9:assert v==knuth(p,q)[0]
        if h<=5:assert v==cubic(p,q)[0]
        rows.append(dict(h=h,n=len(p),cost=v,distinct_keys=len(set(p)),distinct_gaps=len(set(q)),
                         old_lower=os['global_lower_bound'],stats=dict(s)))
        print(h,len(p),v,'old deficit',v-os['global_lower_bound'],flush=True)
    result=dict(rows=rows,source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in ('endpoint_price_family.py','endpoint_prices.py','shifted_alphabetic.py','research.py')})
    (Path(__file__).resolve().parents[1]/'results'/'endpoint_price_family.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
