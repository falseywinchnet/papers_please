#!/usr/bin/env python3
"""Full large solves of the certified two-heavy-gap family.

Global exact cost is checked using an independent four-key cubic core and the
closed uniform-payload cost. The previous constructor is counted, not run.
"""
from collections import Counter
import json
from pathlib import Path
import platform
import sys
import time

from heavy_core import solve
from mass_frontier import select_plan
from research import cost,cubic


def uniform_cost(n):
    remaining=n
    level=ipl=0
    while remaining:
        nodes=min(1<<level,remaining)
        ipl+=level*nodes
        remaining-=nodes
        level+=1
    return 2*ipl+3*n


def main():
    sys.setrecursionlimit(20000)
    rows=[]
    for n in (512,2048,8192,32768,65536):
        p=[1]*n;q=[1]*(n+1)
        q[1]=q[n-1]=n**3
        start=time.perf_counter()
        value,tree,counts=solve(p,q)
        seconds=time.perf_counter()-start
        expected=cubic([1]*4,[1,n**3,2*n-7,n**3,1])[0]+uniform_cost(n-4)
        assert value==expected==cost(tree,p,q)
        old=Counter()
        depth,_=select_plan(p,q,'adaptive',old)
        assert depth==0 and old['selected_short_states']==n*(n+1)//2
        assert counts['core_keys']==4 and counts['kernel_short_states']==10
        assert counts['uniform_reconstructed_keys']==n-4
        rows.append(dict(n=n,optimum=value,seconds=seconds,counts=counts,previous_plan=dict(old),previous_full_solve=False))
        print(n,'cost',value,'seconds',round(seconds,6),'old planned cells',old['selected_short_states'],flush=True)
    out=Path(__file__).resolve().parents[1]/'results'/'heavy_core_scale.json'
    out.write_text(json.dumps(dict(python=platform.python_version(),platform=platform.platform(),rows=rows),indent=2)+'\n')


if __name__=='__main__':main()
