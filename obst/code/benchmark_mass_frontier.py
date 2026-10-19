#!/usr/bin/env python3
"""Matched Knuth, fixed-width, and variable-contour full OBST construction."""
import itertools
import json
from math import isqrt
from pathlib import Path
import platform
import random
import statistics
import sys
import time

from mass_frontier import solve
from research import cost,knuth
from sparse import weights


def fixture(n,family,rng):
    if family=='light_window':
        p=[1000+rng.randrange(-10,11) for _ in range(n)]
        q=[1000+rng.randrange(-10,11) for _ in range(n+1)]
        length=isqrt(isqrt(n**3))
        start=rng.randrange(n-length+1)
        p[start:start+length]=[1]*length
        q[start:start+length+1]=[1]*(length+1)
        return p,q
    return weights(n,family,rng)


def main():
    sys.setrecursionlimit(20000)
    rng=random.Random(0xF1B0B3AC)
    rows=[]
    fixtures=[(n,'random') for n in (512,1024,2048)]
    fixtures += [(2048,'light_window'),(2048,'near_uniform'),
                 (1024,'log_uniform'),(512,'geometric'),(2048,'spike')]
    for n,family in fixtures:
        trials=[]
        for order in itertools.permutations(('knuth','uniform','adaptive')):
            p,q=fixture(n,family,rng)
            runs={}
            for mode in order:
                start=time.perf_counter()
                if mode=='knuth':
                    value,tree,scans=knuth(p,q)
                    stats=dict(states=n*(n+1)//2,root_candidates=scans)
                else: value,tree,stats=solve(p,q,mode)
                elapsed=time.perf_counter()-start
                assert cost(tree,p,q)==value
                runs[mode]=dict(value=value,seconds=elapsed,counts=stats)
            assert len({x['value'] for x in runs.values()})==1
            trials.append(dict(order=order,runs=runs))
        row=dict(n=n,family=family,trials=trials)
        for mode in ('uniform','adaptive'):
            row['median_'+mode+'_knuth']=statistics.median(
                t['runs'][mode]['seconds']/t['runs']['knuth']['seconds'] for t in trials)
        row['median_adaptive_uniform']=statistics.median(
            t['runs']['adaptive']['seconds']/t['runs']['uniform']['seconds'] for t in trials)
        rows.append(row)
        print(n,family,{k:round(v,6) for k,v in row.items() if k.startswith('median')},flush=True)
    out=Path(__file__).resolve().parents[1]/'results'/'mass_frontier_matched.json'
    out.write_text(json.dumps(dict(seed=0xF1B0B3AC,python=platform.python_version(),
                                   platform=platform.platform(),rows=rows),indent=2)+'\n')


if __name__=='__main__': main()
