#!/usr/bin/env python3
"""Exact full mixed OBST certificate using a root/nonroot partition.

At most three alphabetic constructions, one key sort, and linear scans.
Rejection uses Knuth. The unrestricted worst case remains quadratic.
"""
from collections import Counter
from research import knuth
from shifted_alphabetic import alphabetic, tree_cost


def normalize(p,q,stats):
    n=len(p)
    a=min(p[1:-1])
    x=max(0,p[0]-a);y=max(0,p[-1]-a)
    pp=[x]+[v-a for v in p[1:-1]]+[y]
    qq=[p[0]+q[0]-x]+[v+a for v in q[1:-1]]+[p[-1]+q[-1]-y]
    stats['interior_min_items']+=n-2
    stats['transformed_outcomes']+=2*n+1
    return pp,qq,a*n


def offset_tree(tree,offset,stats):
    if tree is None:return None
    stack=[(tree,False)];built={}
    while stack:
        t,done=stack.pop()
        if t is None:continue
        r,left,right=t
        if done:
            built[r]=(r+offset,built[left[0]] if left is not None else None,
                      built[right[0]] if right is not None else None)
            stats['offset_constructed_keys']+=1
        else:
            stack.extend(((t,True),(right,False),(left,False)))
    return built[tree[0]]


def attempt(p,q):
    n=len(p);stats=Counter(input_keys=n)
    if len(q)!=n+1 or any(type(v) is not int or v<0 for v in p+q):
        raise ValueError('nonnegative integer weights required')
    stats['input_validation_outcomes']+=2*n+1
    if n<3:
        v,t,scans=knuth(p,q)
        stats.update(tiny_root_candidates=scans,certified=1,global_lower_bound=v)
        return v,t,stats
    pp,qq,constant=normalize(p,q,stats)
    class Ranked:
        __slots__=('i',)
        def __init__(self,i):self.i=i
        def __lt__(self,other):
            stats['key_sort_comparisons']+=1
            return (-pp[self.i],self.i)<(-pp[other.i],other.i)
    order=sorted(Ranked(i) for i in range(n))
    stats['rank_wrapper_items']+=n;stats['key_rank_sum_items']+=n
    key=sum(pp[item.i]*(j+1).bit_length() for j,item in enumerate(order))
    r=order[0].i;w=pp[r];v=pp[order[1].i]
    gap,base,stats=alphabetic(qq,stats)
    stats['alphabetic_calls']+=1
    lower=key+gap-constant
    best=tree_cost(base,p,q,stats);tree=base
    stats.update(separable_lower_bound=lower,marked_key=r,largest_residual=w,
                 second_residual=v,transfer_constant=constant)
    if best==lower:
        stats.update(certified=1,global_lower_bound=lower,candidate_cost=best,
                     partition_evaluated=0)
        return best,tree,stats
    nonroot=key+w-v+gap
    left_count=right_count=0;left_key=right_key=0
    for item in order:
        stats['conditional_rank_items']+=1
        if item.i<r:
            left_count+=1;left_key+=pp[item.i]*left_count.bit_length()
        elif item.i>r:
            right_count+=1;right_key+=pp[item.i]*right_count.bit_length()
    left_gap,left_tree,stats=alphabetic(qq[:r+1],stats)
    right_gap,right_tree,stats=alphabetic(qq[r+1:],stats)
    stats['alphabetic_calls']+=2
    stats['alphabetic_slice_items']+=n+1
    stats['mass_sum_outcomes']+=2*n+1
    fixed=sum(pp)+sum(qq)+left_key+right_key+left_gap+right_gap
    forced=(r,left_tree,offset_tree(right_tree,r+1,stats))
    stats['joined_roots']+=1
    value=tree_cost(forced,p,q,stats)
    if value<best:best=value;tree=forced
    lower=min(nonroot,fixed)-constant
    assert lower>=stats['separable_lower_bound'] and lower<=best
    stats.update(nonroot_lower_bound=nonroot-constant,fixed_root_lower_bound=fixed-constant,
                 global_lower_bound=lower,candidate_cost=best,certified=int(best==lower),
                 partition_evaluated=1)
    return (best,tree,stats) if best==lower else (None,None,stats)


def solve(p,q):
    v,t,stats=attempt(p,q)
    if v is None:
        v,t,scans=knuth(p,q)
        stats['fallback_dense_states']=len(p)*(len(p)+1)//2
        stats['fallback_root_candidates']=scans
        stats['fallback_constructed_keys']=len(p)
    return v,t,stats
