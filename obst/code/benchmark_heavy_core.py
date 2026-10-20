#!/usr/bin/env python3
"""Matched complete-construction comparison for joint heavy-outcome cores."""
import json
from pathlib import Path
import platform
import random
import statistics
import sys
import time

from gap_separator import solve as separator_solve
from heavy_core import fixtures,solve
from recursive_contract import solve as recursive_solve
from research import cost,knuth


def main():
    sys.setrecursionlimit(20000)
    rng=random.Random(0xC07E83)
    modes=('knuth','separator','core_frontier','core_knuth','recursive')
    orders=[]
    for k in range(5):
        order=modes[k:]+modes[:k]
        orders.extend((order,order[::-1]))
    cases=[(2048,f) for f in ('random','near_uniform','two_heavy_gaps','two_heavy_gaps_random','many_heavy_gaps','moderate_heavy_gaps','mixed_heavy_outcomes')]
    cases.extend(((512,'random'),(1024,'geometric')))
    rows=[]
    for n,family in cases:
        trials=[]
        for order in orders:
            _,p,q=next(x for x in fixtures(n,rng) if x[0]==family)
            runs={}
            for mode in order:
                start=time.perf_counter()
                if mode=='knuth':
                    value,tree,scans=knuth(p,q)
                    c=dict(short_states=n*(n+1)//2,root_candidates=scans)
                elif mode=='separator': value,tree,c=separator_solve(p,q)
                elif mode=='recursive': value,tree,c=recursive_solve(p,q)
                else: value,tree,c=solve(p,q,'knuth' if mode=='core_knuth' else 'frontier')
                seconds=time.perf_counter()-start
                assert value==cost(tree,p,q)
                runs[mode]=dict(value=value,seconds=seconds,counts=c)
            assert len({r['value'] for r in runs.values()})==1
            trials.append(dict(order=order,runs=runs))
        row=dict(n=n,family=family,trials=trials)
        for mode in modes[1:]:
            row['median_'+mode+'_knuth']=statistics.median(t['runs'][mode]['seconds']/t['runs']['knuth']['seconds'] for t in trials)
        row['median_core_frontier_separator']=statistics.median(t['runs']['core_frontier']['seconds']/t['runs']['separator']['seconds'] for t in trials)
        row['median_core_frontier_recursive']=statistics.median(t['runs']['core_frontier']['seconds']/t['runs']['recursive']['seconds'] for t in trials)
        rows.append(row)
        print(n,family,{k:round(v,6) for k,v in row.items() if k.startswith('median')},flush=True)
    out=Path(__file__).resolve().parents[1]/'results'/'heavy_core_matched.json'
    out.write_text(json.dumps(dict(certificate='protected-height',seed=0xC07E83,python=platform.python_version(),platform=platform.platform(),rows=rows),indent=2)+'\n')


if __name__=='__main__': main()
