#!/usr/bin/env python3
"""Positive two-heavy-gap obstruction to the current separator/frontier plan.

This is a lower bound only for the implemented architecture, not for OBST.
Large sizes count plans; only small sizes run full exact constructors.
"""
from collections import Counter
import json
from pathlib import Path
import sys

from gap_separator import solve
from mass_frontier import contour, mass_function, select_plan
from research import cost, cubic, knuth


def inspect(n,full=False):
    p=[1]*n
    q=[1]*(n+1)
    q[1]=q[n-1]=n**3
    total=sum(p)+sum(q)
    assert total==2*n**3+2*n-1
    assert 2*(p[0]+q[0])<total and 2*(p[-1]+q[-1])<total
    assert max(2*x for x in p)<total
    assert max(2*q[j]+p[j-1]+p[j]+min(p[j-1],p[j]) for j in range(1,n))<total
    stats=Counter()
    d,ends=select_plan(p,q,'adaptive',stats)
    assert d==0 and stats['selected_short_states']==n*(n+1)//2
    # Independent contours at every depth with a possibly competitive top term.
    mass=mass_function(p,q)
    f,g=1,1
    levels=[]
    for depth in range(1,n.bit_length()):
        f,g=g,f+g
        e=contour(n,mass,total,f,Counter())
        cells=sum(j-i for i,j in enumerate(e))
        middle=(n-4)*(n-3)//2
        expected=n*(n+1)//2 if depth==1 else middle+4*((n-1)//2) if depth==2 else middle
        assert cells==expected,(n,depth,cells,expected)
        assert cells+n*(1<<depth)>n*(n+1)//2
        levels.append(dict(depth=depth,cells=cells,proxy=cells+n*(1<<depth)))
    row=dict(n=n,mass=total,selected=dict(stats),levels=levels,full_solve=full)
    if full:
        value,tree,c=solve(p,q)
        assert value==cost(tree,p,q)==knuth(p,q)[0]
        if n<=32: assert value==cubic(p,q)[0]
        assert c.get('gap_separators',0)==c.get('key_separators',0)==0
        assert c['terminal_sizes']==[n]
        assert c['terminal_short_states']==n*(n+1)//2
        row.update(optimum=value,counts=c)
    return row


def main():
    sys.setrecursionlimit(20000)
    rows=[inspect(n,True) for n in (5,6,8,16,32,64,128,256)]
    rows.extend(inspect(n) for n in (1024,4096,16384,65536))
    out=Path(__file__).resolve().parents[1]/'results'/'separator_obstruction.json'
    out.write_text(json.dumps(dict(rows=rows),indent=2)+'\n')
    for r in rows: print(r['n'],'full' if r['full_solve'] else 'plan only',r['selected']['selected_work_proxy'],flush=True)


if __name__=='__main__': main()
