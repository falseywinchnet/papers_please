#!/usr/bin/env python3
"""Six matched orders of Knuth, prior hybrid, and excess-2 constructor."""
import itertools
import json
from pathlib import Path
import platform
import random
import statistics
import time

from complete import hybrid_solve
from excess import solve
from ordered_obstruction import witness
from research import cost, knuth
from sparse import weights


def main():
    rng=random.Random(0xEACEB3AC)
    rows=[]
    for n,family in ((1023,'perturbation_4'),(1024,'perturbation_4'),
                     (1023,'periodic_16'),(768,'near_uniform'),
                     (1023,'random'),(2047,'periodic_16'),
                     (2047,'perturbation_16')):
        trials=[]
        for order in itertools.permutations(('knuth','prior','excess2')):
            if family.startswith('perturbation_'):
                epsilon=int(family.split('_')[-1])
                p=[1000+rng.randrange(-epsilon,epsilon+1) for _ in range(n)]
                q=[1000+rng.randrange(-epsilon,epsilon+1) for _ in range(n+1)]
            elif family.startswith('periodic_'):
                _,_,p,q=witness((n+1).bit_length()-1,int(family.split('_')[-1]))
            else:
                p,q=weights(n,family,rng)
            runs={}
            for name in order:
                start=time.perf_counter()
                if name=='knuth':
                    value,tree,scans=knuth(p,q)
                    counts=dict(root_candidates=scans,states=n*(n+1)//2)
                elif name=='prior':
                    value,tree,counts=hybrid_solve(p,q,optimize_baseline=True)
                else:
                    value,tree,counts=solve(p,q,budget=2)
                elapsed=time.perf_counter()-start
                assert cost(tree,p,q)==value
                runs[name]=dict(seconds=elapsed,value=value,counts=counts)
            assert len({v['value'] for v in runs.values()})==1
            trials.append(dict(order=order,runs=runs))
        row=dict(n=n,family=family,trials=trials,
                 median_excess_knuth=statistics.median(t['runs']['excess2']['seconds']/
                                      t['runs']['knuth']['seconds'] for t in trials),
                 median_excess_prior=statistics.median(t['runs']['excess2']['seconds']/
                                      t['runs']['prior']['seconds'] for t in trials),
                 certified=sum(t['runs']['excess2']['counts'].get('certified',0)
                               for t in trials))
        rows.append(row)
        print(n,family,row['median_excess_knuth'],row['certified'],flush=True)
    output=Path(__file__).resolve().parents[1]/'results'/'excess_matched.json'
    output.write_text(json.dumps(dict(seed=0xEACEB3AC,python=platform.python_version(),
                        platform=platform.platform(),rows=rows),indent=2)+'\n')


if __name__=='__main__': main()
