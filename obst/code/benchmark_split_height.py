#!/usr/bin/env python3
"""Matched complete construction at minimum height and one extra level."""
import itertools
import json
from pathlib import Path
import platform
import random
import statistics
import sys
import time

from ordered_obstruction import witness
from research import cost,knuth
from sparse import weights
from split_height import solve


def main():
    sys.setrecursionlimit(20000)
    rng=random.Random(0x5A11B3AC)
    rows=[]
    fixtures=[(n,'near_uniform') for n in (384,768,1000,1536,3072)]
    fixtures += [(1536,'perturbation_4'),(1536,'random'),(1023,'periodic_16')]
    for n,family in fixtures:
        trials=[]
        for order in itertools.permutations(('knuth','height0','height1')):
            if family=='perturbation_4':
                p=[1000+rng.randrange(-4,5) for _ in range(n)]
                q=[1000+rng.randrange(-4,5) for _ in range(n+1)]
            elif family=='periodic_16':
                _,_,p,q=witness((n+1).bit_length()-1,16)
            else: p,q=weights(n,family,rng)
            runs={}
            for name in order:
                start=time.perf_counter()
                if name=='knuth':
                    value,tree,scans=knuth(p,q)
                    stats=dict(root_candidates=scans,states=n*(n+1)//2)
                else:
                    value,tree,stats=solve(p,q,extra_height=int(name[-1]))
                elapsed=time.perf_counter()-start
                assert cost(tree,p,q)==value
                runs[name]=dict(seconds=elapsed,value=value,counts=stats)
            assert len({r['value'] for r in runs.values()})==1
            trials.append(dict(order=order,runs=runs))
        row=dict(n=n,family=family,trials=trials)
        for name in ('height0','height1'):
            row['median_'+name+'_knuth']=statistics.median(
                t['runs'][name]['seconds']/t['runs']['knuth']['seconds'] for t in trials)
            row[name+'_certified']=sum(t['runs'][name]['counts'].get('certified',0) for t in trials)
        rows.append(row)
        print(n,family,[(name,row['median_'+name+'_knuth'],row[name+'_certified'])
                       for name in ('height0','height1')],flush=True)
    out=Path(__file__).resolve().parents[1]/'results'/'split_height_matched.json'
    out.write_text(json.dumps(dict(seed=0x5A11B3AC,python=platform.python_version(),
                                   platform=platform.platform(),rows=rows),indent=2)+'\n')


if __name__=='__main__': main()
