#!/usr/bin/env python3
"""Matched exploratory timings and full work counters; alternate run order."""
import json
import math
from pathlib import Path
import platform
import random
import statistics
import sys
import time
from research import cost,knuth
from recursive_contract import solve
from sparse import weights


def main():
    sys.setrecursionlimit(20000)
    rng=random.Random(0xB3AC4)
    rows=[]
    families=['near_uniform','random','log_uniform','geometric_folded',
              'spike','gap_spike','heavy_separators']
    for n in (512,1024):
        for family in families:
            for trial in range(5):
                if family=='heavy_separators':
                    p=[rng.randrange(1,4) for _ in range(n)]
                    q=[rng.randrange(1,4) for _ in range(n+1)]
                    for k in rng.sample(range(n),math.isqrt(n)): p[k]=1000000
                else:
                    p,q=weights(n,family,rng)
                outputs={}
                for name in (('knuth','recursive') if trial%2 else ('recursive','knuth')):
                    started=time.perf_counter()
                    result=(knuth if name=='knuth' else solve)(p,q)
                    seconds=time.perf_counter()-started
                    outputs[name]=(result,seconds)
                (ref,t,scans),base=outputs['knuth']
                (got,tree,counts),elapsed=outputs['recursive']
                assert ref==got==cost(t,p,q)==cost(tree,p,q)
                rows.append(dict(n=n,family=family,trial=trial,
                                 baseline_seconds=base,seconds=elapsed,
                                 ratio=elapsed/base,baseline_states=n*(n+1)//2,
                                 baseline_candidates=scans,**counts))
            group=rows[-5:]
            print(n,family,'ratio',round(statistics.median(r['ratio'] for r in group),3),
                  'states',statistics.median(r.get('dp_states',0) for r in group),flush=True)
    target=Path(__file__).resolve().parents[1]/'results/recursive_matched.json'
    target.write_text(json.dumps(dict(host=platform.platform(),seed=0xB3AC4,
                                     trials_per_family=5,rows=rows),indent=2)+'\n')


if __name__=='__main__':
    main()
