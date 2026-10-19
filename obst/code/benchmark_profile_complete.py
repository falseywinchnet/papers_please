#!/usr/bin/env python3
"""Matched complete constructors, including profile rejection and old fast routes."""
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
from check_profile_complete import fixture
from profile_complete import solve,portfolio_solve
from run_complete import portfolio_solve as previous,make_fixture
from research import cost


def main():
    sys.setrecursionlimit(10000);rng=random.Random(871042);rows=[]
    solvers=dict(portfolio=portfolio_solve,standalone=solve,previous=previous,full_shape=full_shape,knuth=plain)
    names=tuple(solvers);orders=[names[j:]+names[:j] for j in range(5)]
    families=('witness_pattern','alternating','unattained','large_baseline','ordinary_random','geometric','four_blocks','affine')
    for n in (768,1536):
        for family in families:
            for trial,order in enumerate(orders):
                if family in ('witness_pattern','alternating','unattained','large_baseline'):
                    p,q=fixture(n,rng,baseline=family in ('large_baseline','unattained'),alternating=family=='alternating')
                    if family=='unattained':p.sort()
                elif family=='ordinary_random':
                    p=[rng.randrange(64) for _ in range(n)];q=[rng.randrange(64) for _ in range(n+1)]
                elif family=='geometric':p=[1<<i for i in range(n)];q=[1<<i for i in range(n+1)]
                elif family=='four_blocks':p,q=make_fixture(n,4,rng)
                else:
                    B=4*(n+1)**3;p=[B+i+(-1)**i for i in range(n)];q=[B+i for i in range(n+1)]
                row=dict(n=n,family=family,trial=trial,order=order,seconds={},counts={});expected=None
                for name in order:
                    gc.collect();start=time.perf_counter()
                    value,tree,counts=solvers[name](p,q);elapsed=time.perf_counter()-start
                    assert value==cost(tree,p,q)
                    if expected is None:expected=value
                    else:assert value==expected
                    row['seconds'][name]=elapsed;row['counts'][name]=dict(counts);del tree
                row['value']=expected;rows.append(row)
                print(n,family,trial,row['seconds']['portfolio']/row['seconds']['knuth'],flush=True)
    summaries=[]
    for n in (768,1536):
        for family in families:
            rr=[r for r in rows if r['n']==n and r['family']==family]
            summary=dict(n=n,family=family,trials=len(rr),median_seconds={name:statistics.median(r['seconds'][name] for r in rr) for name in names})
            for numerator in ('portfolio','standalone'):
                for denominator in ('knuth','previous','full_shape'):
                    summary[numerator+'_over_'+denominator]=statistics.median(r['seconds'][numerator]/r['seconds'][denominator] for r in rr)
            summaries.append(summary)
    root=Path(__file__).resolve().parents[1]
    files=('benchmark_profile_complete.py','profile_complete.py','check_profile_complete.py','run_complete.py','ramp_complete.py','ordered_complete.py','ruler_barrier.py','complete.py','research.py','sparse.py','benchmark_ramp_complete.py')
    result=dict(seed=871042,platform=platform.platform(),python=platform.python_version(),
                protocol='five cyclic orders; full preprocessing, certification, reconstruction; external direct-cost checks and GC outside timing',
                arithmetic='exact Python integers',rows=rows,summaries=summaries,
                source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results'/'profile_complete_matched.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(summaries,indent=2),flush=True)


if __name__=='__main__':main()
