#!/usr/bin/env python3
"""Five-order complete-constructor comparison, including adverse controls."""
import gc
import hashlib
import json
from pathlib import Path
import platform
import random
import statistics
import sys
import time

from benchmark_ramp_complete import full_shape,plain
from ramp_complete import solve as affine
from run_complete import solve,portfolio_solve,make_fixture
from research import cost


def main():
    sys.setrecursionlimit(10000);rng=random.Random(480327);rows=[]
    solvers=dict(portfolio=portfolio_solve,runs=solve,affine=lambda p,q:affine(p,q)[:3],full_shape=full_shape,knuth=plain)
    names=tuple(solvers);orders=[names[j:]+names[:j] for j in range(5)]
    families=('four_blocks','sixteen_blocks','irregular','random','geometric','affine')
    for n in (768,1536):
        for family in families:
            for trial,order in enumerate(orders):
                if family in ('four_blocks','sixteen_blocks','irregular'):
                    k={'four_blocks':4,'sixteen_blocks':16,'irregular':n}[family]
                    p,q=make_fixture(n,k,rng,baseline=True)
                elif family=='random':
                    p=[rng.randrange(64) for _ in range(n)];q=[rng.randrange(64) for _ in range(n+1)]
                elif family=='geometric':
                    p=[1<<i for i in range(n)];q=[1<<i for i in range(n+1)]
                else:
                    B=4*(n+1)**3
                    p=[B+i+(-1)**i for i in range(n)];q=[B+i for i in range(n+1)]
                row=dict(n=n,family=family,trial=trial,order=order,seconds={},counts={})
                expected=None
                for name in order:
                    gc.collect();start=time.perf_counter()
                    value,tree,counts=solvers[name](p,q);elapsed=time.perf_counter()-start
                    assert value==cost(tree,p,q)
                    if expected is None:expected=value
                    else:assert expected==value
                    row['seconds'][name]=elapsed;row['counts'][name]=dict(counts)
                    del tree
                row['value']=expected
                for other in ('knuth','affine','full_shape'):
                    row['runs_over_'+other]=row['seconds']['runs']/row['seconds'][other]
                for other in ('knuth','affine','full_shape','runs'):
                    row['portfolio_over_'+other]=row['seconds']['portfolio']/row['seconds'][other]
                rows.append(row);print(n,family,trial,'portfolio',row['portfolio_over_knuth'],'kernel',row['runs_over_knuth'],flush=True)
    summaries=[]
    for n in (768,1536):
        for family in families:
            rr=[r for r in rows if r['n']==n and r['family']==family]
            summary=dict(n=n,family=family,trials=len(rr),
                         median_seconds={name:statistics.median(r['seconds'][name] for r in rr) for name in names})
            for other in ('knuth','affine','full_shape'):
                summary['median_paired_over_'+other]=statistics.median(r['runs_over_'+other] for r in rr)
            for other in ('knuth','affine','full_shape','runs'):
                summary['portfolio_median_paired_over_'+other]=statistics.median(r['portfolio_over_'+other] for r in rr)
            summaries.append(summary);print(summary,flush=True)
    root=Path(__file__).resolve().parents[1]
    names=('benchmark_run_complete.py','run_complete.py','benchmark_ramp_complete.py','ramp_complete.py',
           'ordered_complete.py','ruler_barrier.py','complete.py','sparse.py','research.py')
    result=dict(seed=480327,platform=platform.platform(),python=platform.python_version(),
                arithmetic='exact Python integers for every solver',
                protocol='5 cyclic orders; full preprocessing and reconstruction; direct oracle cost checks and GC outside timing',
                rows=rows,summaries=summaries,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in names})
    (root/'results'/'run_complete_matched.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
