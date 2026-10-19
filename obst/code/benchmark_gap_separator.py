#!/usr/bin/env python3
"""Matched baseline, local-frontier separator, and separator-only comparison."""
import itertools
import json
from pathlib import Path
import platform
import random
import statistics
import sys
import time

from gap_separator import fixtures,solve
from mass_frontier import solve as frontier_solve
from research import cost,knuth
from recursive_contract import solve as recursive_solve


def main():
    sys.setrecursionlimit(20000)
    rng=random.Random(0x6A9B3AC)
    rows=[]
    cases=[(2048,f) for f in ('random','near_uniform','spike','gap_spike','random_heavy_gap','hierarchical_gaps')]
    cases.append((1024,'geometric'))
    modes=('knuth','frontier','separator','separator_knuth','recursive')
    # Five cyclic rotations, each once forward and once reversed, balance
    # positions without the 120 trials per fixture of all permutations.
    orders=[]
    for k in range(len(modes)):
        order=modes[k:]+modes[:k]
        orders.extend((order,order[::-1]))
    for n,family in cases:
        trials=[]
        for order in orders:
            _,p,q=next(x for x in fixtures(n,rng) if x[0]==family)
            runs={}
            for mode in order:
                start=time.perf_counter()
                if mode=='knuth':
                    value,tree,scans=knuth(p,q)
                    c=dict(states=n*(n+1)//2,root_candidates=scans)
                elif mode=='frontier': value,tree,c=frontier_solve(p,q)
                elif mode=='recursive': value,tree,c=recursive_solve(p,q)
                else: value,tree,c=solve(p,q,'knuth' if mode=='separator_knuth' else 'frontier')
                seconds=time.perf_counter()-start
                assert value==cost(tree,p,q)
                runs[mode]=dict(value=value,seconds=seconds,counts=c)
            assert len({v['value'] for v in runs.values()})==1
            trials.append(dict(order=order,runs=runs))
        row=dict(n=n,family=family,trials=trials)
        for mode in modes[1:]:
            row['median_'+mode+'_knuth']=statistics.median(t['runs'][mode]['seconds']/t['runs']['knuth']['seconds'] for t in trials)
        row['median_separator_frontier']=statistics.median(t['runs']['separator']['seconds']/t['runs']['frontier']['seconds'] for t in trials)
        row['median_separator_recursive']=statistics.median(t['runs']['separator']['seconds']/t['runs']['recursive']['seconds'] for t in trials)
        rows.append(row)
        print(n,family,{k:round(v,6) for k,v in row.items() if k.startswith('median')},flush=True)
    out=Path(__file__).resolve().parents[1]/'results'/'gap_separator_matched.json'
    out.write_text(json.dumps(dict(seed=0x6A9B3AC,python=platform.python_version(),platform=platform.platform(),rows=rows),indent=2)+'\n')


if __name__=='__main__': main()
