#!/usr/bin/env python3
"""Experimental exact demand-driven OBST. No subquadratic bound is claimed.

Uses the exact unordered mixed-node relaxation to exclude candidate roots.
Every unit of bound construction is counted, not only surviving DP states.
"""
from bisect import bisect_left
from collections import Counter
from functools import lru_cache
import argparse
import heapq
import json
from pathlib import Path
import platform
import random
import time

from research import check_weights, cost, cubic, knuth


class Counted:
    __slots__ = ('value', 'counter')
    def __init__(self, value, counter):
        self.value, self.counter = value, counter
    def __lt__(self, other):
        self.counter['bound_weight_comparisons'] += 1
        return self.value < other.value


class SparseSolver:
    def __init__(self, p, q):
        check_weights(p, q)
        self.p, self.q = p, q
        self.n = len(p)
        self.stats = Counter()
        self.prefix = [0]
        for a, b in zip(p, q[1:]):
            self.prefix.append(self.prefix[-1] + a + b)

    def mass(self, i, j):
        return self.prefix[j] - self.prefix[i] + self.q[i]

    @lru_cache(None)
    def lower(self, i, j):
        if i == j:
            return 0
        self.stats['bound_intervals'] += 1
        self.stats['bound_input_items'] += 2*(j-i)+1
        c = self.stats
        p = sorted(Counted(w,c) for w in self.p[i:j])
        h = [Counted(w,c) for w in self.q[i:j+1]]
        heapq.heapify(h)
        ans = 0
        for w in p:
            a,b=heapq.heappop(h),heapq.heappop(h)
            v=a.value+b.value+w.value
            ans += v
            heapq.heappush(h,Counted(v,c))
            c['bound_contractions'] += 1
        return ans

    @lru_cache(None)
    def upper(self, i, j):
        if i == j:
            return 0, None
        self.stats['upper_intervals'] += 1
        target = (self.prefix[i] + self.prefix[j] - self.q[i]) // 2
        r = max(i, min(j-1, bisect_left(self.prefix,target,i,j+1)))
        # Choose among the nearby key positions by exact balance, to account
        # for the key mass and both adjacent gaps.
        choices=range(max(i,r-1),min(j,r+2))
        r=min(choices,key=lambda k:abs(self.mass(i,k)-self.mass(k+1,j)))
        a,ta=self.upper(i,r)
        b,tb=self.upper(r+1,j)
        return self.mass(i,j)+a+b,(r,ta,tb)

    @lru_cache(None)
    def solve(self, i, j):
        if i == j:
            return 0,None
        self.stats['exact_intervals'] += 1
        best, tree = self.upper(i,j)
        floor = self.lower(i,j)
        if floor == best:
            self.stats['whole_interval_certificates'] += 1
            return best,tree
        w=self.mass(i,j)
        first=tree[0]
        order=[first]
        for distance in range(1,max(first-i,j-1-first)+1):
            if first-distance>=i: order.append(first-distance)
            if first+distance<j: order.append(first+distance)
        for r in order:
            self.stats['root_candidates'] += 1
            la,lb=self.lower(i,r),self.lower(r+1,j)
            if w+la+lb>=best:
                self.stats['root_pruned_by_two_bounds'] += 1
                continue
            a,ta=self.solve(i,r)
            if w+a+lb>=best:
                self.stats['root_pruned_after_left'] += 1
                continue
            b,tb=self.solve(r+1,j)
            if w+a+b<best:
                best,tree=w+a+b,(r,ta,tb)
                if best==floor:
                    self.stats['whole_interval_certificates'] += 1
                    break
        return best,tree

    def run(self):
        value,tree=self.solve(0,self.n)
        assert cost(tree,self.p,self.q)==value
        # Method caches otherwise retain self and its instance data forever.
        self.lower.cache_clear()
        self.upper.cache_clear()
        self.solve.cache_clear()
        return value,tree,dict(self.stats)


def weights(n,kind,rng):
    if kind=='uniform': return [10]*n,[10]*(n+1)
    if kind=='near_uniform': return [1000+rng.randrange(-1,2) for _ in range(n)],[1000+rng.randrange(-1,2) for _ in range(n+1)]
    if kind=='random': return [rng.randrange(1000) for _ in range(n)],[rng.randrange(1000) for _ in range(n+1)]
    if kind=='geometric': return [1<<i for i in range(n)],[1<<i for i in range(n+1)]
    if kind=='geometric_reverse':
        p,q=weights(n,'geometric',rng)
        return p[::-1],q[::-1]
    if kind=='geometric_folded': return [1<<min(i,n-1-i) for i in range(n)],[1<<min(i,n-i) for i in range(n+1)]
    if kind=='log_uniform': return [1<<rng.randrange(20) for _ in range(n)],[1<<rng.randrange(20) for _ in range(n+1)]
    if kind=='alternating': return [1 if i%2 else 1000 for i in range(n)],[1000 if i%2 else 1 for i in range(n+1)]
    if kind=='zero': return [0]*n,[0]*(n+1)
    if kind=='spike':
        p,q=[1]*n,[1]*(n+1)
        p[n//2]=1000000
        return p,q
    if kind=='gap_spike':
        p,q=[1]*n,[1]*(n+1)
        q[n//2]=1000000
        return p,q
    if kind=='keys_only': return [rng.randrange(1000) for _ in range(n)],[0]*(n+1)
    if kind=='gaps_only': return [0]*n,[rng.randrange(1000) for _ in range(n+1)]
    raise ValueError(kind)


FAMILIES=['uniform','near_uniform','random','geometric','geometric_reverse',
          'geometric_folded','log_uniform','alternating','zero','spike',
          'gap_spike','keys_only','gaps_only']


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-n',type=int,default=128)
    parser.add_argument('--trials',type=int,default=3)
    parser.add_argument('--output',default='obst/results/sparse.json')
    args=parser.parse_args()
    rng=random.Random(0x0B57FA22)
    # Mixed nonzero, zeros/ties, and broad dynamic range; independent oracle.
    for n in range(1,10):
        for trial in range(100):
            p=[rng.randrange(20) for _ in range(n)]
            q=[rng.randrange(20) for _ in range(n+1)]
            value,tree,stats=SparseSolver(p,q).run()
            assert value==cubic(p,q)[0], (p,q,value)
    result={'host':platform.platform(),'seed':0x0B57FA22,
            'fuzz_verified':900,'rows':[]}
    n=16
    while n<=args.max_n:
        for family in FAMILIES:
            for trial in range(args.trials):
                p,q=weights(n,family,rng)
                oracle,_,candidates=knuth(p,q)
                started=time.perf_counter()
                value,tree,stats=SparseSolver(p,q).run()
                assert value==oracle,(n,family,trial,p,q,value,oracle)
                row=dict(n=n,family=family,trial=trial,cost=value,
                    knuth_intervals=n*(n+1)//2,knuth_candidates=candidates,
                    seconds=time.perf_counter()-started,**stats)
                result['rows'].append(row)
                print(json.dumps(row),flush=True)
                out=Path(args.output)
                out.parent.mkdir(parents=True,exist_ok=True)
                out.write_text(json.dumps(result,indent=2)+'\n')
        n*=2


if __name__=='__main__': main()
