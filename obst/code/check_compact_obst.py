#!/usr/bin/env python3
"""Fuzz and operation-count audit of the complete condensed constructor."""
from collections import Counter
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import time
from compact_obst import solve
from check_core_monge import dense
from research import cost,cubic,knuth


def fixture(n,name,rng):
    if name=='uniform':return [1]*n,[1]*(n+1)
    if name=='binary':return [1+rng.randrange(2) for _ in range(n)],[1+rng.randrange(2) for _ in range(n+1)]
    if name=='near_uniform':return [100+rng.randrange(3) for _ in range(n)],[100+rng.randrange(3) for _ in range(n+1)]
    if name=='random_16':return [1+rng.randrange(16) for _ in range(n)],[1+rng.randrange(16) for _ in range(n+1)]
    if name=='sparse':return [int(rng.randrange(8)==0) for _ in range(n)],[int(rng.randrange(8)==0) for _ in range(n+1)]
    if name=='alternating':return [1+i%2 for i in range(n)],[2-i%2 for i in range(n+1)]
    if name=='geometric':return [1<<i for i in range(n)],[1<<i for i in range(n+1)]
    if name=='folded':return [1<<min(i,n-1-i) for i in range(n)],[1<<min(i,n-i) for i in range(n+1)]
    raise ValueError(name)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--max-n',type=int,default=512);args=ap.parse_args()
    rng=random.Random(709513);checks=Counter();rows=[]
    def check(p,q,early=True,audit=False):
        previous=None
        def observer(h,matrix,witness):
            nonlocal previous
            table=dense(matrix.top,matrix.left,matrix.entries)
            if h:
                for i in range(len(p)):
                    for j in range(i+1,len(p)+1):
                        val,r=min((previous[i][r]+previous[r+1][j],r) for r in range(i,j))
                        assert table[i][j]==sum(p[i:j])+sum(q[i:j+1])+val
                        assert witness.query(i,j)==r
                        checks['layer_value_and_witness_cells']+=1
                checks['audited_layers']+=1
            previous=table
        value,tree,stats,layers=solve(p,q,early_stop=early,observer=observer if audit else None)
        ref,_,candidates=knuth(p,q)
        assert value==ref==cost(tree,p,q)
        assert stats.get('constructed_keys',0)==len(p)
        if len(p)<=12:
            assert cubic(p,q)[0]==value;checks['cubic_solves']+=1
        checks['complete_solves']+=1;checks['constructed_keys']+=len(p)
        return dict(value=value,counts=stats,layers=layers,knuth_candidates=candidates)
    for n in range(0,5):
        for v in itertools.product((0,1),repeat=2*n+1):
            check(list(v[:n]),list(v[n:]))
            checks['exhaustive_binary_inputs']+=1
        print('exhaustive',n,flush=True)
    for n in range(1,33):
        for t in range(12):
            p=[rng.randrange(30) for _ in range(n)];q=[rng.randrange(30) for _ in range(n+1)]
            row=check(p,q)
            if t==0:
                fixed=check(p,q,False,audit=n<=12)
                assert fixed['value']==row['value'];checks['fixed_budget_controls']+=1
        print('random',n,flush=True)
    for n in (16,32,64):
        for name in ('geometric','folded'):
            if n>args.max_n:continue
            p,q=fixture(n,name,rng);row=check(p,q);row.update(n=n,family=name);rows.append(row)
            print(name,n,row['counts']['completed_layers'],flush=True)
    n=32
    while n<=args.max_n:
        for name in ('uniform','binary','near_uniform','random_16','sparse','alternating'):
            p,q=fixture(n,name,rng)
            started=time.perf_counter();row=check(p,q);elapsed=time.perf_counter()-started
            row.update(n=n,family=name,mass=sum(p)+sum(q));rows.append(row)
            print(name,n,'layers',row['counts']['completed_layers'],'core',row['counts']['maximum_layer_core'],
                  'core visits',row['counts']['core_visits'],'audit seconds',round(elapsed,3),flush=True)
        n*=2
    root=Path(__file__).resolve().parents[1]
    names=('core_monge.py','compact_obst.py','check_compact_obst.py','penalty_layers.py')
    data=dict(seed=709513,checks=checks,rows=rows,max_n=args.max_n,
              source_sha256={name:hashlib.sha256((root/'code'/name).read_bytes()).hexdigest() for name in names})
    (root/'results'/'compact_obst.json').write_text(json.dumps(data,indent=2)+'\n')
    print(dict(checks),flush=True)

if __name__=='__main__':main()
