#!/usr/bin/env python3
"""Matched full constructors; all successes and fallback overhead retained."""
import gc
import hashlib
import itertools
import json
from pathlib import Path
import platform
import random
import statistics
import subprocess
import sys
import time
from shifted_alphabetic import solve,tree_cost
from threshold_complete import portfolio_solve
from check_shifted_alphabetic import family as shifted_family
from check_threshold_complete import family as previous_family
from check_profile_complete import fixture
from benchmark_ramp_complete import plain


def main():
    sys.setrecursionlimit(10000);rng=random.Random(871044);rows=[]
    solvers=dict(shifted=solve,previous=portfolio_solve,knuth=plain)
    orders=list(itertools.permutations(solvers));families=('shifted','random','uniform_key_random_gap','previous_profile','previous_multilevel','near_uniform','geometric')
    cpu=subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string'],text=True).strip()
    load_start=subprocess.check_output(['uptime'],text=True).strip()
    for h in (6,7):
        n=7*(1<<h)-1
        for name in families:
            for trial,order in enumerate(orders):
                if name=='shifted':p,q,_,_=shifted_family(h)
                elif name=='random':p=[rng.randrange(64) for _ in range(n)];q=[rng.randrange(64) for _ in range(n+1)]
                elif name=='uniform_key_random_gap':p=[7]*n;q=[rng.randrange(64) for _ in range(n+1)]
                elif name=='previous_profile':p,q=fixture(n,rng)
                elif name=='previous_multilevel':p,q,_=previous_family(h+2,1<<h)
                elif name=='near_uniform':p=[100+rng.randrange(3) for _ in range(n)];q=[100+rng.randrange(3) for _ in range(n+1)]
                else:p=[1<<i for i in range(n)];q=[1<<i for i in range(n+1)]
                row=dict(n=len(p),nominal_n=n,family=name,trial=trial,order=order,seconds={},counts={});expected=None
                for solver in order:
                    gc.collect();start=time.perf_counter();v,t,s=solvers[solver](p,q);elapsed=time.perf_counter()-start
                    assert tree_cost(t,p,q)==v
                    if expected is None:expected=v
                    else:assert v==expected
                    row['seconds'][solver]=elapsed;row['counts'][solver]=dict(s);del t
                row['cost']=expected;rows.append(row)
                print(n,name,trial,row['seconds']['shifted']/row['seconds']['knuth'],flush=True)
    summaries=[]
    for n in (447,895):
        for name in families:
            rr=[r for r in rows if r['nominal_n']==n and r['family']==name]
            summaries.append(dict(n=rr[0]['n'],family=name,trials=len(rr),
                shifted_over_knuth=statistics.median(r['seconds']['shifted']/r['seconds']['knuth'] for r in rr),
                shifted_over_previous=statistics.median(r['seconds']['shifted']/r['seconds']['previous'] for r in rr),
                median_seconds={s:statistics.median(r['seconds'][s] for r in rr) for s in solvers}))
    root=Path(__file__).resolve().parents[1]
    files=('benchmark_shifted_alphabetic.py','shifted_alphabetic.py','check_shifted_alphabetic.py','threshold_complete.py','check_threshold_complete.py','profile_complete.py','check_profile_complete.py','run_complete.py','ramp_complete.py','ordered_complete.py','ruler_barrier.py','complete.py','research.py','sparse.py','benchmark_ramp_complete.py')
    result=dict(seed=871044,cpu=cpu,platform=platform.platform(),python=platform.python_version(),load_start=load_start,
        load_end=subprocess.check_output(['uptime'],text=True).strip(),
        protocol='all six solver orders; full preprocessing, certification, reconstruction; GC and direct tree checks outside timing; same process, no isolation claim',
        rows=rows,summaries=summaries,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results'/'shifted_alphabetic_matched.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(summaries,indent=2),flush=True)


if __name__=='__main__':main()
