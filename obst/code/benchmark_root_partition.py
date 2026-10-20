#!/usr/bin/env python3
"""Matched full root-partition construction, including rejection and fallback."""
import gc,hashlib,json,platform,random,statistics,subprocess,sys,time
from pathlib import Path
from root_partition import solve
from endpoint_prices import solve as priced_solve
from root_partition_family import family as coupled_family
from endpoint_price_family import family
from shifted_alphabetic import solve as shifted,tree_cost
from check_shifted_alphabetic import family as old_shifted
from threshold_complete import portfolio_solve
from check_threshold_complete import family as multilevel
from check_profile_complete import fixture
from run_complete import make_fixture
from benchmark_ramp_complete import plain


def priced(p,q):
    v,t,s,d=priced_solve(p,q);return v,t,s


def main():
    sys.setrecursionlimit(10000);rng=random.Random(871046);rows=[]
    solvers=dict(coupled=solve,priced=priced,previous=portfolio_solve,knuth=plain)
    names=tuple(solvers);orders=[names[i:]+names[:i] for i in range(4)]
    kinds=('coupled','endpoint','random','near_uniform','geometric','uniform_interior','old_profile','old_multilevel','old_shifted','four_signatures','affine')
    cpu=subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string'],text=True).strip()
    load_start=subprocess.check_output(['uptime'],text=True).strip()
    for h in (8,9):
        n=(1<<h)-1
        for kind in kinds:
            for trial,order in enumerate(orders):
                if kind=='coupled':p,q=coupled_family(h)
                elif kind=='endpoint':p,q,_,_=family(h)
                elif kind=='random':p=[rng.randrange(1,65) for _ in range(n)];q=[rng.randrange(1,65) for _ in range(n+1)]
                elif kind=='near_uniform':p=[100+rng.randrange(3) for _ in range(n)];q=[100+rng.randrange(3) for _ in range(n+1)]
                elif kind=='geometric':p=[1<<i for i in range(n)];q=[1<<i for i in range(n+1)]
                elif kind=='uniform_interior':p=[17]*n;p[0]=p[-1]=1;q=[rng.randrange(1,65) for _ in range(n+1)]
                elif kind=='old_profile':p,q=fixture(n,rng)
                elif kind=='old_multilevel':p,q,_=multilevel(h-1,1<<(h-3))
                elif kind=='old_shifted':p,q,_,_=old_shifted(h-3)
                elif kind=='four_signatures':p,q=make_fixture(n,4,rng)
                else:B=4*(n+1)**3;p=[B+i+(-1)**i for i in range(n)];q=[B+i for i in range(n+1)]
                row=dict(n=len(p),nominal_n=n,family=kind,trial=trial,order=order,seconds={},counts={});expected=None
                for name in order:
                    gc.collect();start=time.perf_counter();v,t,s=solvers[name](p,q);elapsed=time.perf_counter()-start
                    assert v==tree_cost(t,p,q)
                    if expected is None:expected=v
                    else:assert v==expected
                    row['seconds'][name]=elapsed;row['counts'][name]=dict(s);del t
                row['cost']=expected;rows.append(row)
                print(n,kind,trial,row['seconds']['coupled']/row['seconds']['knuth'],flush=True)
    summaries=[]
    for n in (255,511):
        for kind in kinds:
            rr=[r for r in rows if r['nominal_n']==n and r['family']==kind]
            summaries.append(dict(n=rr[0]['n'],family=kind,trials=len(rr),
                median_seconds={s:statistics.median(r['seconds'][s] for r in rr) for s in names},
                **{'coupled_over_'+s:statistics.median(r['seconds']['coupled']/r['seconds'][s] for r in rr) for s in names if s!='coupled'}))
    root=Path(__file__).resolve().parents[1]
    files=('benchmark_root_partition.py','root_partition.py','root_partition_family.py','endpoint_prices.py','endpoint_price_family.py','shifted_alphabetic.py','check_shifted_alphabetic.py','threshold_complete.py','check_threshold_complete.py','profile_complete.py','check_profile_complete.py','run_complete.py','ramp_complete.py','ordered_complete.py','ruler_barrier.py','complete.py','research.py','sparse.py','benchmark_ramp_complete.py')
    result=dict(seed=871046,cpu=cpu,platform=platform.platform(),python=platform.python_version(),load_start=load_start,
        load_end=subprocess.check_output(['uptime'],text=True).strip(),protocol='four cyclic solver orders; full preprocessing, root partition, certification, fallback and reconstruction; GC and tree-cost checks outside timing; same-process non-isolated measurements',
        rows=rows,summaries=summaries,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results'/'root_partition_matched.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(summaries,indent=2),flush=True)


if __name__=='__main__':main()
