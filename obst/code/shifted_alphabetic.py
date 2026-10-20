#!/usr/bin/env python3
"""Exact full mixed certificate using a shifted Hu--Tucker gap optimum.

Hu--Tucker is established prior work. The certificate may reject an optimal
candidate; solve then uses exact Knuth. Counters count logical work only.
"""
from collections import Counter
import heapq
from research import knuth


class HeapNode:
    __slots__=('item','left','right','rank')
    def __init__(self,item):
        self.item=item;self.left=None;self.right=None;self.rank=1


def alphabetic(q,stats=None):
    """Hu--Tucker compatible merging with meldable heaps and lazy candidates."""
    if stats is None:stats=Counter()
    N=len(q)
    if N<1 or any(x<0 for x in q):raise ValueError('nonnegative nonempty gap vector required')
    stats['alphabetic_validation_items']+=N
    mass=list(q);last=list(range(N));children=[None]*N
    stats['alphabetic_input_items']+=N
    def less(a,b):
        stats['heap_item_comparisons']+=1
        return (mass[a],last[a])<(mass[b],last[b])
    def meld(a,b):
        stats['meld_calls']+=1
        if a is None:return b
        if b is None:return a
        if less(b.item,a.item):a,b=b,a
        a.right=meld(a.right,b)
        if a.left is None or (a.right is not None and a.left.rank<a.right.rank):a.left,a.right=a.right,a.left
        a.rank=1+(a.right.rank if a.right else 0)
        return a
    # A live group is the internal-item heap between two consecutive original
    # leaves. Removing a leaf melds its two incident groups. Sentinels have -1.
    groups=[];left_group=[0]*N;right_group=[0]*N;queue=[]
    class Event:
        __slots__=('value',)
        def __init__(self,value):self.value=value
        def __lt__(self,other):
            stats['priority_comparisons']+=1
            return self.value<other.value
    def make_group(left,right,heap):
        g=len(groups);groups.append([left,right,heap,True,0])
        if left>=0:right_group[left]=g
        if right>=0:left_group[right]=g
        stats['groups_created']+=1
        return g
    def pair(g):
        left,right,h,alive,version=groups[g];items=[]
        if left>=0:items.append(left)
        if right>=0:items.append(right)
        if h:
            items.append(h.item)
            h2=h.left
            if h2 is None or (h.right is not None and less(h.right.item,h2.item)):h2=h.right
            if h2:items.append(h2.item)
        # At most four items; explicit insertion comparisons are counted.
        for i in range(1,len(items)):
            j=i
            while j and less(items[j],items[j-1]):items[j],items[j-1]=items[j-1],items[j];j-=1
        if len(items)<2:return None
        a,b=items[:2];stats['compatible_pair_candidates']+=1
        # Active clusters partition the original leaves. Their distinct largest
        # leaf indices implement the order of sums of symbolic weights 2^i.
        return (mass[a]+mass[b],max(last[a],last[b]),min(last[a],last[b]),a,b)
    def publish(g):
        groups[g][4]+=1;choice=pair(g)
        if choice is not None:
            heapq.heappush(queue,Event(choice[:3]+(g,groups[g][4],choice[3],choice[4])))
            stats['priority_pushes']+=1
    for i in range(N+1):
        g=make_group(i-1 if i else -1,i if i<N else -1,None);publish(g)
    charges=0
    for _ in range(N-1):
        while True:
            value,_,_,g,version,a,b=heapq.heappop(queue).value;stats['priority_pops']+=1
            if groups[g][3] and groups[g][4]==version:break
            stats['stale_priority_pops']+=1
        for item in (a,b):
            if item>=N:
                h=groups[g][2];assert h.item==item
                groups[g][2]=meld(h.left,h.right)
        for item in (a,b):
            if item<N:
                x,y=left_group[item],right_group[item]
                assert groups[x][3] and groups[y][3] and x!=y
                l,r=groups[x][0],groups[y][1]
                heap=meld(groups[x][2],groups[y][2])
                groups[x][3]=groups[y][3]=False
                g=make_group(l,r,heap);stats['original_leaves_removed']+=1
        node=len(mass);mass.append(value);last.append(max(last[a],last[b]));children.append((a,b))
        groups[g][2]=meld(groups[g][2],HeapNode(node));publish(g)
        charges+=value;stats['compatible_merges']+=1
    depths=[0]*N;todo=[(len(mass)-1,0)]
    while todo:
        node,d=todo.pop();stats['merge_tree_visits']+=1
        if node<N:depths[node]=d
        else:
            a,b=children[node];todo.extend(((a,d+1),(b,d+1)))
    # Canonical alphabetic reconstruction from the ordered leaf depths.
    stack=[]
    for i,d in enumerate(depths):
        stats['reconstruction_leaf_visits']+=1
        stack.append((d,None,i))
        while len(stack)>1 and stack[-1][0]==stack[-2][0]:
            d,right,split=stack.pop();_,left,first=stack.pop()
            stack.append((d-1,(split-1,left,right),first));stats['constructed_keys']+=1
    assert len(stack)==1 and stack[0][0]==0
    assert sum(x*d for x,d in zip(q,depths))==charges
    return charges,stack[0][1],stats


def tree_cost(tree,p,q,stats=None):
    if stats is None:stats=Counter()
    result=0;todo=[(tree,0,len(p),0)]
    while todo:
        t,lo,hi,d=todo.pop()
        if t is None:
            assert lo==hi;result+=q[lo]*d;stats['cost_gap_visits']+=1
        else:
            r,left,right=t;assert lo<=r<hi
            result+=p[r]*(d+1);stats['cost_key_visits']+=1
            todo.extend(((left,lo,r,d+1),(right,r+1,hi,d+1)))
    return result


def attempt(p,q):
    n=len(p);stats=Counter()
    if len(q)!=n+1 or any(x<0 for x in p) or any(x<0 for x in q):raise ValueError('nonnegative full vectors required')
    stats['input_validation_items']+=2*n+1
    stats['key_min_items']+=n;stats['gap_shift_items']+=n+1
    m=min(p) if p else 0;shifted=[x+m for x in q]
    gap,tree,stats=alphabetic(shifted,stats)
    # Count sorting comparisons separately from fixed scans and heap work.
    class Weight:
        __slots__=('value',)
        def __init__(self,value):self.value=value
        def __lt__(self,other):
            stats['key_sort_comparisons']+=1
            return self.value>other.value
    ranked=sorted(Weight(x-m) for x in p)
    stats['key_residual_items']+=n;stats['key_rank_sum_items']+=n
    key=sum(x.value*(i+1).bit_length() for i,x in enumerate(ranked))
    lower=gap+key-m*n;value=tree_cost(tree,p,q,stats)
    stats.update(dict(input_keys=n,shift=m,shifted_gap_optimum=gap,key_residual_lower=key,
                      global_lower_bound=lower,candidate_cost=value,certified=int(value==lower)))
    assert value>=lower
    return (value,tree,stats) if value==lower else (None,None,stats)


def solve(p,q):
    value,tree,stats=attempt(p,q)
    if value is None:
        value,tree,scans=knuth(p,q)
        stats['fallback_dense_states']=len(p)*(len(p)+1)//2
        stats['fallback_root_candidates']=scans
        stats['fallback_constructed_keys']=len(p)
    return value,tree,stats
