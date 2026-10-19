#!/usr/bin/env python3
"""Exact dominant-outcome separators with local mass-frontier terminal solves.

The interior-gap certificate retains both adjacent key weights. It forces a
class with that gap at depth two, then chooses between its two orientations.
"""
from collections import Counter
import itertools
import json
from pathlib import Path
import random
import sys

from mass_frontier import solve as frontier_solve
from research import check_weights,cost,cubic,knuth,label,shapes
from sparse import FAMILIES,weights


class RangeMaximum:
    def __init__(self,values,stats):
        self.stats=stats
        self.base=1
        while self.base<len(values): self.base*=2
        self.tree=[(-1,-1)]*(2*self.base)
        for i,v in enumerate(values): self.tree[self.base+i]=(v,-i)
        for i in range(self.base-1,0,-1):
            self.tree[i]=max(self.tree[2*i],self.tree[2*i+1])
            stats['range_build_comparisons']+=1

    def query(self,lo,hi):
        best=(-1,-1)
        lo+=self.base
        hi+=self.base
        while lo<hi:
            if lo&1:
                best=max(best,self.tree[lo]); lo+=1
                self.stats['range_query_comparisons']+=1
            if hi&1:
                hi-=1; best=max(best,self.tree[hi])
                self.stats['range_query_comparisons']+=1
            lo//=2; hi//=2
        return best[0],-best[1]


def solve(p,q,terminal='frontier'):
    check_weights(p,q)
    assert terminal in ('frontier','knuth')
    n=len(p)
    stats=Counter()
    prefix=[0]
    for a,b in zip(p,q[1:]): prefix.append(prefix[-1]+a+b)
    def mass(i,j): return q[i]+prefix[j]-prefix[i]
    key_index=gap_index=None
    stats['prefix_items']=n
    def prepare_indexes():
        nonlocal key_index,gap_index
        if key_index is not None: return
        key_index=RangeMaximum([2*w for w in p],stats)
        gap_scores=[-1]+[2*q[j]+p[j-1]+p[j]+min(p[j-1],p[j]) for j in range(1,n)]+[-1]
        gap_index=RangeMaximum(gap_scores,stats)
        stats['separator_score_items']=n+max(0,n-1)
    terminal_sizes=[]

    def shift(t,offset):
        if t is None: return None
        r,a,b=t
        stats['terminal_relabelled_keys']+=1
        return r+offset,shift(a,offset),shift(b,offset)

    def zero_tree(i,j):
        if i==j: return None
        r=(i+j)//2
        stats['zero_component_keys']+=1
        return r,zero_tree(i,r),zero_tree(r+1,j)

    def visit(i,j,depth):
        stats['component_calls']+=1
        stats['max_separator_depth']=max(stats['max_separator_depth'],depth)
        if i==j: return 0,None
        total=mass(i,j)
        if not total: return 0,zero_tree(i,j)
        # Endpoint certificates cost O(1) and can exhaust a long chain
        # without ever constructing or querying a range index.
        stats['endpoint_checks']+=1
        if 2*(q[i]+p[i])>=total:
            r=i; stats['left_endpoint_separators']+=1
        else:
            stats['endpoint_checks']+=1
            if 2*(q[j]+p[j-1])>=total:
                r=j-1; stats['right_endpoint_separators']+=1
            else:
                prepare_indexes()
                score,gap=gap_index.query(i+1,j)
                if score>=total:
                    left,lt=visit(i,gap-1,depth+1)
                    right,rt=visit(gap+1,j,depth+1)
                    wl,wr=mass(i,gap-1),mass(gap+1,j)
                    a,b=p[gap-1]+wl,p[gap]+wr
                    if b<=a:
                        tree=(gap-1,lt,(gap,None,rt))
                        stats['gap_left_root']+=1
                    else:
                        tree=(gap,(gap-1,lt,None),rt)
                        stats['gap_right_root']+=1
                    stats['gap_separators']+=1
                    return left+right+total+q[gap]+min(a,b),tree
                score,r=key_index.query(i,j)
                if score<total:
                    m=j-i
                    if terminal=='frontier':
                        value,tree,c=frontier_solve(p[i:j],q[i:j+1])
                        for name,value_count in c.items(): stats['terminal_'+name]+=value_count
                    else:
                        value,tree,scans=knuth(p[i:j],q[i:j+1])
                        stats['terminal_short_states']+=m*(m+1)//2
                        stats['terminal_short_root_candidates']+=scans
                    stats['terminal_components']+=1
                    stats['terminal_keys']+=m
                    stats['terminal_size_squares']+=m*m
                    terminal_sizes.append(m)
                    return value,shift(tree,i)
                stats['key_separators']+=1
        left,lt=visit(i,r,depth+1)
        right,rt=visit(r+1,j,depth+1)
        return total+left+right,(r,lt,rt)

    value,tree=visit(0,n,0)
    assert value==cost(tree,p,q)
    counts=dict(stats)
    counts['terminal_sizes']=terminal_sizes
    return value,tree,counts


def exhaustive_certificates():
    tests=gap_checks=endpoint_checks=key_checks=0
    for n in range(1,5):
        trees=[label(s)[0] for s in shapes(n)]
        gap_depths=[]
        for t in trees:
            gap_depths.append([cost(t,[0]*n,[int(k==g) for k in range(n+1)]) for g in range(n+1)])
        for v in itertools.product(range(3),repeat=2*n+1):
            p=list(v[:n]); q=list(v[n:]); total=sum(v)
            costs=[cost(t,p,q) for t in trees]
            optimum=min(costs)
            for g in range(1,n):
                outside=total-p[g-1]-p[g]-q[g]
                if q[g]+min(p[g-1],p[g])>=outside:
                    restricted=min(c for c,d in zip(costs,gap_depths) if d[g]==2)
                    assert restricted==optimum,(p,q,g,optimum,restricted)
                    left=cubic(p[:g-1],q[:g])[0]
                    right=cubic(p[g+1:],q[g+1:])[0]
                    wl=sum(p[:g-1])+sum(q[:g])
                    wr=sum(p[g+1:])+sum(q[g+1:])
                    formula=left+right+total+q[g]+min(p[g-1]+wl,p[g]+wr)
                    assert formula==restricted
                    gap_checks+=1
            for r in range(n):
                if 2*p[r]>=total:
                    assert min(c for c,t in zip(costs,trees) if t[0]==r)==optimum
                    key_checks+=1
            for g,r in ((0,0),(n,n-1)):
                if 2*(q[g]+p[r])>=total:
                    assert min(c for c,t in zip(costs,trees) if t[0]==r)==optimum
                    endpoint_checks+=1
            tests+=1
    return dict(exhaustive_inputs=tests,gap_certificate_checks=gap_checks,
                endpoint_certificate_checks=endpoint_checks,key_certificate_checks=key_checks)


def fixtures(n,rng):
    result=[(f,*weights(n,f,rng)) for f in ('random','near_uniform','geometric','log_uniform','spike','gap_spike')]
    # Random background weights make the remaining subproblems genuinely
    # mixed; large gaps force several levels of the decomposition.
    p=[rng.randrange(1,1001) for _ in range(n)]
    q=[rng.randrange(1,1001) for _ in range(n+1)]
    q[n//2]=100*sum(p+q)
    result.append(('random_heavy_gap',p,q))
    p=[rng.randrange(1,1001) for _ in range(n)]
    q=[rng.randrange(1,1001) for _ in range(n+1)]
    def plant(i,j):
        if j-i<32: return
        g=(i+j)//2
        plant(i,g-1); plant(g+1,j)
        q[g]=4*(sum(p[i:j])+sum(q[i:j+1]))
    plant(0,n)
    result.append(('hierarchical_gaps',p,q))
    return result


def main():
    sys.setrecursionlimit(20000)
    checks=exhaustive_certificates()
    # Replacing the smaller neighboring key by the larger one is unsafe.
    cp,cq=[100,1,50],[1,1,1,1]
    restricted=min(cost(label(t)[0],cp,cq) for t in shapes(3)
                   if cost(label(t)[0],[0]*3,[0,1,0,0])==2)
    assert cubic(cp,cq)[0]==212 and restricted==261
    checks['max_neighbor_counterexample']=dict(p=cp,q=cq,optimum=212,restricted=261)
    print('Exhaustive:',checks,flush=True)
    rng=random.Random(0x6A9CE27)
    full_checks=0
    for n in range(41):
        for trial in range(40):
            if n and trial<13: p,q=weights(n,FAMILIES[trial],rng)
            else:
                p=[rng.randrange(30) if trial%2 else 1<<rng.randrange(14) for _ in range(n)]
                q=[rng.randrange(30) if trial%3 else 1<<rng.randrange(14) for _ in range(n+1)]
            expected=cubic(p,q)[0]
            for terminal in ('frontier','knuth'):
                value,tree,c=solve(p,q,terminal)
                assert value==expected==cost(tree,p,q),(p,q,terminal,value,expected)
                assert c.get('terminal_keys',0)<=n
                full_checks+=1
    checks['full_solve_checks']=full_checks
    print('Full solve checks:',full_checks,flush=True)
    rows=[]
    for n in (128,256,512,1024,2048):
        for family,p,q in fixtures(n,rng):
            expected,_,scans=knuth(p,q)
            runs={}
            for terminal in ('frontier','knuth'):
                value,tree,c=solve(p,q,terminal)
                assert value==expected==cost(tree,p,q)
                runs[terminal]=c
            direct,_,base=frontier_solve(p,q)
            assert direct==expected
            rows.append(dict(n=n,family=family,optimum=expected,counts=runs,
                             direct_frontier=base,knuth_states=n*(n+1)//2,
                             knuth_root_candidates=scans))
            print(n,family,'gaps',runs['frontier'].get('gap_separators',0),
                  'terminal states',runs['frontier'].get('terminal_short_states',0),
                  'direct states',base['short_states'],flush=True)
    out=Path(__file__).resolve().parents[1]/'results'/'gap_separator.json'
    out.write_text(json.dumps(dict(**checks,rows=rows),indent=2)+'\n')


if __name__=='__main__': main()
