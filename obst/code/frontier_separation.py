#!/usr/bin/env python3
"""Count plans for the positive light-block separation; no timing claims."""
from collections import Counter
import json
from math import isqrt
from pathlib import Path
from mass_frontier import select_plan,solve
from research import cost,cubic,knuth


def instance(n):
    length=isqrt(isqrt(n**3))
    start=(n-length)//2
    a=n*n
    p=[a]*n
    q=[a]*(n+1)
    p[start:start+length]=[1]*length
    q[start:start+length+1]=[1]*(length+1)
    return p,q,length


def main():
    checked=[]
    for n in (16,81,256,625):
        p,q,length=instance(n)
        true,_,_=knuth(p,q)
        if n<=81: assert true==cubic(p,q)[0]
        for mode in ('adaptive','uniform'):
            value,tree,c=solve(p,q,mode)
            assert value==true==cost(tree,p,q)
        checked.append(n)
    rows=[]
    for n in (256,1024,4096,16384,65536):
        p,q,length=instance(n)
        modes={}
        for mode in ('adaptive','uniform'):
            c=Counter()
            d,ends=select_plan(p,q,mode,c)
            modes[mode]=dict(c)
        row=dict(n=n,light_keys=length,counts=modes)
        rows.append(row)
        print(n,length,[(m,modes[m]['selected_depth'],modes[m]['selected_work_proxy']) for m in modes],flush=True)
    out=Path(__file__).resolve().parents[1]/'results'/'frontier_separation.json'
    out.write_text(json.dumps(dict(exact_checked_sizes=checked,rows=rows),indent=2)+'\n')


if __name__=='__main__': main()
