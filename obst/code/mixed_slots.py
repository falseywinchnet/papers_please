#!/usr/bin/env python3
"""Exact height-limited mixed OBST via ruler slots and unused-slot states."""
from collections import Counter
from research import check_weights


def valuations(c):
    return [0]+[(r & -r).bit_length()-1 for r in range(1,c+1)]


def repair(slots,h,counts):
    """Delete unwanted perfect-tree keys with threaded successors in O(2^h)."""
    c=(1<<h)-1;left=[0]*(c+1);right=[0]*(c+1);parent=[0]*(c+1)
    key=list(range(c+1));where=list(range(c+1));prev=[i-1 for i in range(c+1)];nxt=[i+1 for i in range(c+1)]
    nxt[c]=0;rank=[-1]*(c+1)
    for i,slot in enumerate(slots):rank[slot]=i
    counts['repair_array_entries']+=8*(c+1)
    def build(a,b,par):
        if a>b:return 0
        m=(a+b)//2;parent[m]=par;left[m]=build(a,m-1,m);right[m]=build(m+1,b,m)
        counts['perfect_nodes']+=1
        return m
    root=build(1,c,0)
    for label in range(1,c+1):
        if rank[label]>=0:continue
        node=where[label]
        if left[node] and right[node]:
            dead=nxt[node];moved=key[dead];key[node]=moved;where[moved]=node
            assert not left[dead]
        else:dead=node
        child=left[dead] or right[dead];par=parent[dead]
        if not par:root=child
        elif left[par]==dead:left[par]=child
        else:assert right[par]==dead;right[par]=child
        if child:parent[child]=par
        a,b=prev[dead],nxt[dead]
        if a>0:nxt[a]=b
        if b:prev[b]=a
        where[label]=0;counts['deleted_nodes']+=1
    def output(node):
        if not node:return None
        counts['output_nodes']+=1
        return rank[key[node]],output(left[node]),output(right[node])
    return output(root)


def solve(p,q,h,counts=None):
    check_weights(p,q);n=len(p);assert n>=1 and h>=1
    if counts is None:counts=Counter()
    c=(1<<h)-1;r=c-n
    if r<0:return None
    v=valuations(c);counts['valuation_entries']+=c
    old=[(p[0]+q[0])*v[1+y] for y in range(r+1)];parents=[None]
    counts['states']+=r+1
    best=[None]*h;suffix=[None]*h;best_tag=[0]*h;suffix_tag=[0]*h
    for i in range(2,n+1):
        new=[];back=[];gap=q[i-1]
        for y in range(r+1):
            d=v[i-1+y];candidate=(old[y],-y)
            if best_tag[d]!=i or candidate>best[d]:best[d]=candidate;best_tag[d]=i
            counts['exact_level_updates']+=1
            for level in range(d+1):
                if suffix_tag[level]!=i or candidate>suffix[level]:suffix[level]=candidate;suffix_tag[level]=i
                counts['suffix_updates']+=1
            z=v[i+y];winner=None
            for level in range(z):
                if best_tag[level]==i:
                    b=best[level];candidate=(b[0]+gap*level,b[1])
                    if winner is None or candidate>winner:winner=candidate
                counts['lower_level_scans']+=1
            if suffix_tag[z]==i:
                b=suffix[z];candidate=(b[0]+gap*z,b[1])
                if winner is None or candidate>winner:winner=candidate
            counts['suffix_queries']+=1
            assert winner is not None
            new.append(winner[0]+p[i-1]*z);back.append(-winner[1]);counts['states']+=1
        old=new;parents.append(back)
    score,negative_y=max((old[y]+q[n]*v[n+y],-y) for y in range(r+1))
    y=-negative_y;slots=[0]*n
    for i in range(n,0,-1):
        slots[i-1]=i+y
        if i>1:y=parents[i-1][y]
        counts['traceback_states']+=1
    tree=repair(slots,h,counts)
    return dict(cost=h*(sum(p)+sum(q))-score,tree=tree,slots=slots,h=h,slack=r)
