#!/usr/bin/env python3
"""Certified joint heavy-outcome core for full mixed-weight OBST.

Selected keys and neighbors of selected gaps form an ancestor-closed core.
A dominance certificate justifies solving intervening intervals independently.
"""
from collections import Counter
import itertools
import json
from pathlib import Path
import random
import sys

from gap_separator import solve as separator_solve
from mass_frontier import solve as frontier_solve
from research import check_weights, cost, cubic, knuth, label, shapes
from sparse import FAMILIES, weights


def tri(n): return n*(n+1)//2


class Counted:
    def __init__(self,value,stats): self.value,self.stats=value,stats
    def __lt__(self,other):
        self.stats['selection_sort_comparisons']+=1
        return self.value<other.value


def anchors_at(p,q,threshold):
    return [i for i in range(len(p)) if max(p[i],q[i],q[i+1])>=threshold]


def intervals(n,anchors):
    previous=-1
    for a in anchors+[n]:
        yield previous+1,a
        previous=a


def protected_height(m,total,minimum):
    """Largest feasible key length from F_length*minimum <= total."""
    if not m: return 0
    f,g=1,1
    best=1
    for length in range(2,m+1):
        f,g=g,f+g
        if f*minimum>total: break
        best=length
    return best


def select_plan(p,q,stats,height_bound=True):
    n=len(p)
    if not n: return None
    outcomes=[x.value for x in sorted(Counted(w,stats) for w in p+q)]
    activation=[x.value for x in sorted(Counted((max(p[i],q[i],q[i+1]),i),stats) for i in range(n))]
    parent=[-1]*n
    size=[0]*n
    active=block_states=light=cursor=0
    best=tri(n)
    chosen=None
    total=sum(outcomes)
    fib=[0,1]
    for _ in range(2,n+1):
        fib.append(fib[-1]+fib[-2])
        stats['selection_fibonacci_additions']+=1
    height_index=n

    def find(i):
        while parent[i]!=i:
            stats['selection_find_steps']+=1
            parent[i]=parent[parent[i]]
            i=parent[i]
        return i

    def union(a,b):
        nonlocal block_states
        a,b=find(a),find(b)
        if a==b: return
        if size[a]<size[b]: a,b=b,a
        block_states+=size[a]*size[b]
        parent[b]=a
        size[a]+=size[b]
        stats['selection_unions']+=1

    for threshold,group in itertools.groupby(outcomes):
        while cursor<n and activation[cursor][0]<threshold:
            _,i=activation[cursor]
            parent[i]=i;size[i]=1
            active+=1;block_states+=1;cursor+=1
            stats['selection_activations']+=1
            if i and parent[i-1]>=0: union(i,i-1)
            if i+1<n and parent[i+1]>=0: union(i,i+1)
        m=n-active
        stats['selection_thresholds']+=1
        if threshold>0:
            while height_index>1:
                stats['selection_height_checks']+=1
                if fib[height_index]*threshold<=total-light: break
                height_index-=1
        h=min(m,height_index) if height_bound else m
        bound=(h+n.bit_length())*light
        proxy=tri(m)+block_states
        if threshold>0 and threshold>=bound and proxy<best:
            best=proxy
            chosen=dict(threshold=threshold,core_keys=m,core_height_bound=h,light_mass=light,
                        certificate_bound=bound,knuth_proxy=proxy)
        light+=sum(group)
    stats['selection_items']=3*n+1
    return chosen


def uniform_tree(p,q,stats):
    n=len(p)
    if n:
        for values in (p,q):
            for w in values:
                stats['uniform_checks']+=1
                if w!=values[0]: return None
    def build(i,j):
        if i==j: return None
        r=(i+j)//2
        stats['uniform_reconstructed_keys']+=1
        return r,build(i,r),build(r+1,j)
    tree=build(0,n)
    return cost(tree,p,q),tree


def core_solve(p,q,threshold,kernel,stats):
    n=len(p)
    anchors=anchors_at(p,q,threshold)
    blocks=list(intervals(n,anchors))
    stats['core_keys']=len(anchors)
    stats['block_sizes']=[j-i for i,j in blocks]
    payload=[]
    cq=[]
    offset=0

    def kernel_solve(a,b):
        shortcut=uniform_tree(a,b,stats)
        if shortcut is not None: return shortcut
        if kernel=='knuth':
            value,tree,scans=knuth(a,b)
            stats['kernel_short_states']+=tri(len(a))
            stats['kernel_short_root_candidates']+=scans
        else:
            value,tree,c=frontier_solve(a,b)
            for k,v in c.items(): stats['kernel_'+k]+=v
        return value,tree

    def shift(t,offset):
        if t is None: return None
        r,a,b=t
        stats['block_relabelled_keys']+=1
        return r+offset,shift(a,offset),shift(b,offset)

    for i,j in blocks:
        value,tree=kernel_solve(p[i:j],q[i:j+1])
        offset+=value
        cq.append(sum(p[i:j])+sum(q[i:j+1]))
        payload.append(shift(tree,i))
    value,tree=kernel_solve([p[i] for i in anchors],cq)

    def expand(t,lo=0):
        if t is None: return payload[lo]
        r,a,b=t
        stats['core_reconstructed_keys']+=1
        return anchors[r],expand(a,lo),expand(b,r+1)
    return offset+value,expand(tree)


def solve(p,q,kernel='frontier',height_bound=True):
    check_weights(p,q)
    assert kernel in ('frontier','knuth')
    stats=Counter()
    direct=uniform_tree(p,q,stats)
    if direct is not None:
        value,tree=direct
        stats['global_uniform']=1
    else:
        plan=select_plan(p,q,stats,height_bound)
        if plan is None:
            value,tree,c=separator_solve(p,q,terminal=kernel)
            for k,v in c.items(): stats['fallback_'+k]=v
            stats['no_core_certificate']=1
        else:
            stats.update({'plan_'+k:v for k,v in plan.items()})
            value,tree=core_solve(p,q,plan['threshold'],kernel,stats)
            stats['certified_core']=1
    assert value==cost(tree,p,q)
    return value,tree,dict(stats)


def fits(tree,anchors,below=False):
    if tree is None: return True
    r,a,b=tree
    if below and r in anchors: return False
    under=below or r not in anchors
    return fits(a,anchors,under) and fits(b,anchors,under)


def projection_checks():
    checked=0
    for n in range(1,5):
        trees=[label(t)[0] for t in shapes(n)]
        depths=[[cost(t,[int(i==k) for i in range(n)],[0]*(n+1)) for k in range(n)]+
                [cost(t,[0]*n,[int(i==k) for i in range(n+1)]) for k in range(n+1)] for t in trees]
        for bits in range(1,1<<(2*n+1)):
            selected=[i for i in range(2*n+1) if bits>>i&1]
            p=[int(i in selected) for i in range(n)]
            q=[int(n+i in selected) for i in range(n+1)]
            anchors=set(anchors_at(p,q,1))
            good=[d for t,d in zip(trees,depths) if fits(t,anchors)]
            for t,d in zip(trees,depths):
                if fits(t,anchors): continue
                assert any(all(e[i]<=d[i] for i in selected) and any(e[i]<d[i] for i in selected) for e in good),(n,bits,t)
                checked+=1
    return checked


def exhaustive_checks():
    inputs=certificates=0
    for n in range(1,5):
        trees=[label(t)[0] for t in shapes(n)]
        for v in itertools.product((0,1,100),repeat=2*n+1):
            p,q=list(v[:n]),list(v[n:])
            costs=[cost(t,p,q) for t in trees]
            for threshold in set(v)-{0}:
                anchors=anchors_at(p,q,threshold)
                light=sum(w for w in v if w<threshold)
                h=protected_height(len(anchors),sum(v)-light,threshold)
                if len(anchors)==n or threshold<(h+n.bit_length())*light: continue
                restricted=min(c for t,c in zip(trees,costs) if fits(t,set(anchors)))
                assert restricted==min(costs),(p,q,threshold)
                value,tree=core_solve(p,q,threshold,'knuth',Counter())
                assert value==restricted==cost(tree,p,q)
                certificates+=1
            inputs+=1
    return inputs,certificates


def fixtures(n,rng):
    result=[(f,*weights(n,f,rng)) for f in ('random','near_uniform','geometric','spike','gap_spike')]
    for family,count,uniform in [('two_heavy_gaps',2,True),('two_heavy_gaps_random',2,False),('many_heavy_gaps',max(2,int(n**0.5)),False),('moderate_heavy_gaps',max(2,int(n**0.5)),False),('mixed_heavy_outcomes',max(2,int(n**0.5)),False)]:
        p=[1 if uniform else rng.randrange(1,1001) for _ in range(n)]
        q=[1 if uniform else rng.randrange(1,1001) for _ in range(n+1)]
        gaps=[1,n-1] if count==2 else [max(1,min(n-1,(k+1)*n//(count+1))) for k in range(count)]
        for k,g in enumerate(gaps):
            if family=='mixed_heavy_outcomes' and k%2: p[g]=1000*n**3
            else: q[g]=(1 if uniform else 1000)*n**3
        if family=='moderate_heavy_gaps':
            light=sum(p)+sum(q)-sum(q[g] for g in gaps)
            m=len({i for g in gaps for i in (g-1,g)})
            h=protected_height(m,len(gaps),1)
            for g in gaps: q[g]=(h+n.bit_length())*light
        result.append((family,p,q))
    return result


def main():
    sys.setrecursionlimit(20000)
    proj=projection_checks();print('projection',proj,flush=True)
    exhaustive,certificates=exhaustive_checks();print('exhaustive',exhaustive,certificates,flush=True)
    rng=random.Random(0xC07E59)
    full=selections=0
    for n in range(33):
        for trial in range(40):
            if n and trial<13: p,q=weights(n,FAMILIES[trial],rng)
            else:
                p=[rng.randrange(6) if trial%3 else 1<<rng.randrange(18) for _ in range(n)]
                q=[rng.randrange(6) if trial%2 else 1<<rng.randrange(18) for _ in range(n+1)]
            expected=cubic(p,q)[0]
            for kernel in ('frontier','knuth'):
                value,tree,c=solve(p,q,kernel)
                assert value==expected==cost(tree,p,q),(p,q,kernel,value,expected)
                full+=1
            if n<=12:
                plan=select_plan(p,q,Counter())
                reference=tri(n)
                for threshold in set(p+q)-{0}:
                    anchors=anchors_at(p,q,threshold)
                    light=sum(w for w in p+q if w<threshold)
                    h=protected_height(len(anchors),sum(p)+sum(q)-light,threshold)
                    if threshold>=(h+n.bit_length())*light:
                        reference=min(reference,tri(len(anchors))+sum(tri(j-i) for i,j in intervals(n,anchors)))
                assert (plan['knuth_proxy'] if plan else tri(n))==reference
                selections+=1
    print('full',full,'selection',selections,flush=True)
    rows=[]
    for n in (128,512,2048):
        for family,p,q in fixtures(n,rng):
            expected,_,scans=knuth(p,q)
            runs={}
            for kernel in ('frontier','knuth'):
                value,tree,c=solve(p,q,kernel)
                assert value==expected==cost(tree,p,q)
                runs[kernel]=c
            old,_,baseline=separator_solve(p,q)
            assert old==expected
            rows.append(dict(n=n,family=family,optimum=expected,counts=runs,separator=baseline,knuth_states=tri(n),knuth_root_candidates=scans))
            print(n,family,'core',runs['frontier'].get('core_keys'), 'states',runs['frontier'].get('kernel_short_states',0),flush=True)
    out=Path(__file__).resolve().parents[1]/'results'/'heavy_core.json'
    out.write_text(json.dumps(dict(projection_checks=proj,exhaustive_inputs=exhaustive,exhaustive_certificates=certificates,full_solves=full,selection_checks=selections,rows=rows),indent=2)+'\n')


if __name__=='__main__': main()
