#!/usr/bin/env python3
"""Full condensed constructor validation with large integer baselines."""
from collections import Counter
import hashlib,itertools,json,random
from pathlib import Path
from centered_obst import solve
from centered_layers import height_bound,baseline
from compact_obst import solve as original
from check_core_monge import dense
from research import knuth,cubic,cost


def main():
    rng=random.Random(294381);checks=Counter();rows=[]
    def check(p,q,audit=False,control=False,fixed=False):
        n=len(p);w=sum(p)+sum(q);H=height_bound(p,q);M=(H+1)*w+1
        a=min(p) if n else 0;b=min(q);pd=[v-a for v in p];qd=[v-b for v in q];previous=None
        def observer(h,matrix,witness):
            nonlocal previous
            table=dense(matrix.top,matrix.left,matrix.entries)
            for i in range(n):
                for j in range(i+1,n+1):
                    assert 0<=table[i][j]-baseline(j-i,h,a,b,M)<=h*(sum(pd[i:j])+sum(qd[i:j+1]))
                    if h:
                        v,r=min((previous[i][r]+previous[r+1][j],r) for r in range(i,j))
                        assert table[i][j]==sum(p[i:j])+sum(q[i:j+1])+v
                        assert witness.query(i,j)==r;checks['layer_values_and_witnesses']+=1
            previous=table
        value,tree,counts,layers=solve(p,q,early_stop=not fixed,observer=observer if audit else None)
        ref,_,kc=knuth(p,q);assert value==ref==cost(tree,p,q)
        if n:assert counts['normalized_height_budget']==H
        assert counts.get('constructed_keys',0)==n
        if n<=12:assert cubic(p,q)[0]==value;checks['cubic_solves']+=1
        if control:assert original(p,q)[0]==value;checks['original_compact_controls']+=1
        checks['solves']+=1;checks['constructed_keys']+=n;checks['fixed_budget_controls']+=fixed
        return dict(n=n,mass=w,deviation=sum(pd)+sum(qd),value=value,counts=counts,layers=layers,knuth_candidates=kc)
    for n in range(5):
        for v in itertools.product((0,1),repeat=2*n+1):check(list(v[:n]),list(v[n:]))
    for n in range(1,33):
        for trial in range(8):
            a,b=rng.choice((0,1,10**6,1<<256)),rng.choice((0,1,10**6,1<<200))
            p=[a+rng.randrange(4) for _ in range(n)];q=[b+rng.randrange(4) for _ in range(n+1)]
            check(p,q,audit=n<=10 and trial==0,control=n<=12 and trial==0)
            if trial==0:check(p,q,fixed=True)
        print('random',n,flush=True)
    for n in (16,32,64):
        for name,p,q in (('geometric',[1<<i for i in range(n)],[1<<i for i in range(n+1)]),('all_zero',[0]*n,[0]*(n+1)),('one_gap',[0]*n,[0]*(n//2)+[1]+[0]*(n-n//2))):
            r=check(p,q);r['family']=name;rows.append(r)
    for n in (32,64,128,256):
        for name,a,b in (('unit',1,1),('large_both',1<<256,1<<200),('large_keys',1<<256,0),('large_gaps',0,1<<256),('zero_baseline',0,0)):
            p=[a+rng.randrange(3) for _ in range(n)];q=[b+rng.randrange(3) for _ in range(n+1)]
            r=check(p,q);r['family']=name;rows.append(r)
            print(name,n,'H',r['counts']['normalized_height_budget'],'layers',r['counts']['completed_layers'],'core',r['counts']['maximum_layer_core'],flush=True)
    root=Path(__file__).resolve().parents[1]
    files=('centered_obst.py','check_centered_obst.py','centered_layers.py','core_monge.py','research.py','penalty_layers.py')
    out=dict(seed=294381,checks=dict(checks),rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results'/'centered_obst.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(checks),flush=True)
if __name__=='__main__':main()
