#!/usr/bin/env python3
"""Matched complete-construction controls; counters are separate from timings."""
import gc
import hashlib
import json
from pathlib import Path
import platform
import random
import statistics
import sys
import time

from complete import attempt as full_shape_attempt
from ramp_complete import solve as corridor
from research import cost,knuth


def plain(p,q):
    value,t,scans=knuth(p,q)
    return value,t,dict(dense_states=len(p)*(len(p)+1)//2,root_candidates=scans)


def full_shape(p,q):
    value,t,stats=full_shape_attempt(p,q,unrestricted=True)
    if value is None:
        value,t,scans=knuth(p,q)
        stats['fallback_dense_states']=len(p)*(len(p)+1)//2
        stats['fallback_root_candidates']=scans
    return value,t,dict(stats)


def main():
    sys.setrecursionlimit(10000);rng=random.Random(103599);rows=[]
    solvers=dict(corridor=lambda p,q:corridor(p,q)[:3],
                 unfiltered=lambda p,q:corridor(p,q,preflight=False)[:3],
                 full_shape=full_shape,knuth=plain)
    names=tuple(solvers)
    orders=[names[i:]+names[:i] for i in range(len(names))]
    for n in (768,1536):
        for family in ('alternating_key','random_signed','bounded_both','random','geometric'):
            for trial,order in enumerate(orders):
                B=4*(n+1)**3
                if family=='alternating_key':
                    p=[B+i+(-1)**i for i in range(n)];q=[B+i for i in range(n+1)]
                elif family=='random_signed':
                    u=[0]*n;v=[0]*(n+1)
                    for _ in range(n):
                        array=u if rng.randrange(2) else v
                        array[rng.randrange(len(array))]+=rng.choice((-1,1))
                    p=[B+i+x for i,x in enumerate(u)];q=[B+i+x for i,x in enumerate(v)]
                elif family=='bounded_both':
                    p=[B+i+rng.choice((-1,0,1)) for i in range(n)]
                    q=[B+i+rng.choice((-1,0,1)) for i in range(n+1)]
                elif family=='random':
                    p=[rng.randrange(64) for _ in range(n)];q=[rng.randrange(64) for _ in range(n+1)]
                else:
                    p=[1<<i for i in range(n)];q=[1<<i for i in range(n+1)]
                record=dict(n=n,family=family,trial=trial,order=order,seconds={},counts={})
                expected=None
                for name in order:
                    gc.collect()
                    start=time.perf_counter();result=solvers[name](p,q);elapsed=time.perf_counter()-start
                    value,t,counts=result
                    assert value==cost(t,p,q)
                    if expected is None:expected=value
                    else:assert value==expected
                    record['seconds'][name]=elapsed;record['counts'][name]=dict(counts)
                    del result,t
                record['value']=expected
                record['corridor_over_knuth']=record['seconds']['corridor']/record['seconds']['knuth']
                record['corridor_over_full_shape']=record['seconds']['corridor']/record['seconds']['full_shape']
                record['corridor_over_unfiltered']=record['seconds']['corridor']/record['seconds']['unfiltered']
                rows.append(record)
                print(n,family,trial,'ratio',record['corridor_over_knuth'],flush=True)
    summaries=[]
    for n in (768,1536):
        for family in ('alternating_key','random_signed','bounded_both','random','geometric'):
            selected=[r for r in rows if r['n']==n and r['family']==family]
            summary=dict(n=n,family=family,trials=len(selected),
                         median_seconds={name:statistics.median(r['seconds'][name] for r in selected) for name in solvers},
                         median_paired_over_knuth=statistics.median(r['corridor_over_knuth'] for r in selected),
                         median_paired_over_full_shape=statistics.median(r['corridor_over_full_shape'] for r in selected),
                         median_paired_over_unfiltered=statistics.median(r['corridor_over_unfiltered'] for r in selected))
            summaries.append(summary);print(summary,flush=True)
    root=Path(__file__).resolve().parents[1]
    data=dict(seed=103599,platform=platform.platform(),python=platform.python_version(),
              arithmetic='exact Python integers for every solver',
              protocol='4 cyclic orders; full preprocessing and tree construction; oracle cost checks and GC outside timings',
              rows=rows,summaries=summaries,
              source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest()
                for f in ('benchmark_ramp_complete.py','ramp_complete.py','ordered_complete.py',
                          'ruler_barrier.py','complete.py','sparse.py','research.py')})
    (root/'results'/'ramp_complete_matched.json').write_text(json.dumps(data,indent=2)+'\n')


if __name__=='__main__':main()
