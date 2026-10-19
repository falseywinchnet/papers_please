#!/usr/bin/env python3
"""Exact-arithmetic research harness for mixed key/gap optimal BSTs.

All keys are zero-based. A tree is None or (key_index, left, right).
Cost charges each key depth+1 and each gap its number of internal ancestors.
Only Python's standard library is needed.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import heapq
import itertools
import json
from pathlib import Path
import platform
import random
import time


def check_weights(p, q):
    assert len(q) == len(p) + 1
    assert all(isinstance(w, int) and w >= 0 for w in (*p, *q))


def cost(tree, p, q, lo=0, hi=None, depth=0):
    if hi is None:
        hi = len(p)
    if tree is None:
        assert lo == hi
        return q[lo] * depth
    r, left, right = tree
    assert lo <= r < hi
    return (p[r] * (depth + 1)
            + cost(left, p, q, lo, r, depth + 1)
            + cost(right, p, q, r + 1, hi, depth + 1))


def cubic(p, q):
    """Independent recurrence: direct interval sums, every root, exact ints."""
    check_weights(p, q)
    n = len(p)
    c = [[0] * (n + 1) for _ in range(n + 1)]
    roots = {}
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length
            v, r = min((c[i][r] + c[r + 1][j], r) for r in range(i, j))
            c[i][j] = v + sum(p[i:j]) + sum(q[i:j + 1])
            roots[i, j] = r

    def tree(i, j):
        if i == j:
            return None
        r = roots[i, j]
        return r, tree(i, r), tree(r + 1, j)
    return c[0][n], tree(0, n)


def knuth(p, q):
    check_weights(p, q)
    n = len(p)
    prefix = [0]
    for a, b in zip(p, q[1:]):
        prefix.append(prefix[-1] + a + b)
    c = [[0] * (n + 1) for _ in range(n + 1)]
    roots = [[0] * (n + 1) for _ in range(n + 1)]
    candidates = 0
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length
            low = i if length == 1 else roots[i][j - 1]
            high = j - 1 if length == 1 else roots[i + 1][j]
            best = None
            for r in range(low, high + 1):
                candidates += 1
                value = c[i][r] + c[r + 1][j]
                if best is None or value < best:
                    best, roots[i][j] = value, r
            c[i][j] = best + prefix[j] - prefix[i] + q[i]

    def tree(i, j):
        if i == j:
            return None
        r = roots[i][j]
        return r, tree(i, r), tree(r + 1, j)
    return c[0][n], tree(0, n), candidates


@lru_cache(None)
def shapes(n):
    if n == 0:
        return (None,)
    return tuple((a, b) for left in range(n)
                 for a in shapes(left) for b in shapes(n - 1 - left))


def label(shape, start=0):
    if shape is None:
        return None, start
    left, r = label(shape[0], start)
    right, end = label(shape[1], r + 1)
    return (r, left, right), end


def depth_profile(shape, depth=0):
    if shape is None:
        return (), (depth,)
    pl, ql = depth_profile(shape[0], depth + 1)
    pr, qr = depth_profile(shape[1], depth + 1)
    return (depth + 1,) + pl + pr, ql + qr


@lru_cache(None)
def profiles(n):
    return tuple(set((tuple(sorted(a)), tuple(sorted(b)))
                     for s in shapes(n) for a, b in (depth_profile(s),)))


def unordered_oracle(p, q):
    """Exhaust all shapes; rearrangement inequality optimizes labels per type."""
    ps, qs = sorted(p, reverse=True), sorted(q, reverse=True)
    return min(sum(a*b for a, b in zip(ps, dp))
               + sum(a*b for a, b in zip(qs, dq)) for dp, dq in profiles(len(p)))


def unordered_huffman(p, q, return_shape=False):
    """Relax key and gap order, retain node types and every weight.

    Contract the two least-weight current leaves beneath the least-weight
    remaining internal node. Each contraction adds its total mass to cost.
    Shape payload can be relabeled in-order to give a feasible BST upper bound.
    """
    check_weights(p, q)
    h = [(w, i, None) for i, w in enumerate(q)]
    heapq.heapify(h)
    answer = 0
    serial = len(q)
    for v in sorted(p):
        a, _, left = heapq.heappop(h)
        b, _, right = heapq.heappop(h)
        w = a + b + v
        answer += w
        heapq.heappush(h, (w, serial, (left, right) if return_shape else None))
        serial += 1
    return (answer, h[0][2]) if return_shape else answer


def rotations(t):
    if t is None:
        return
    r, a, b = t
    if a is not None:
        x, aa, ab = a
        yield x, aa, (r, ab, b)
    if b is not None:
        x, ba, bb = b
        yield x, (r, a, ba), bb
    for aa in rotations(a):
        yield r, aa, b
    for bb in rotations(b):
        yield r, a, bb


def promote(t, target):
    r, a, b = t
    if r == target:
        return t
    if target < r:
        x, aa, ab = promote(a, target)
        return x, aa, (r, ab, b)
    x, ba, bb = promote(b, target)
    return x, (r, a, ba), bb


def promotions(t):
    """Promote any descendant to the root of any existing subtree."""
    if t is None:
        return
    r, a, b = t
    def keys(t):
        if t is not None:
            yield t[0]
            yield from keys(t[1])
            yield from keys(t[2])
    for k in keys(t):
        if k != r:
            yield promote(t, k)
    for aa in promotions(a):
        yield r, aa, b
    for bb in promotions(b):
        yield r, a, bb


def verify():
    rng = random.Random(0x0B570018)
    counts = Counter()
    for n in range(0, 5):
        for w in itertools.product(range(3), repeat=2*n+1):
            p, q = w[:n], w[n:]
            ref, t = cubic(p, q)
            got, kt, _ = knuth(p, q)
            lb = unordered_huffman(p, q)
            oracle = unordered_oracle(p, q)
            assert ref == got == cost(t, p, q) == cost(kt, p, q)
            assert lb == oracle <= ref, (p, q, lb, oracle, ref)
            if n <= 3:
                brute = min(cost(label(s)[0], p, q) for s in shapes(n))
                assert brute == ref
            counts['exhaustive_weight_instances'] += 1
    for n in range(1, 10):
        for _ in range(300):
            p = [rng.randrange(1000) for _ in range(n)]
            q = [rng.randrange(1000) for _ in range(n+1)]
            ref, t = cubic(p, q)
            got, kt, _ = knuth(p, q)
            lb, shape = unordered_huffman(p, q, True)
            assert got == ref == cost(t, p, q) == cost(kt, p, q)
            assert lb == unordered_oracle(p, q) <= ref <= cost(label(shape)[0], p, q)
            counts['random_instances'] += 1
    return dict(counts)


def find_traps(max_n=7, trials=1000):
    rng = random.Random(0x7A9)
    found = {}
    for n in range(3, max_n+1):
        trees = [label(s)[0] for s in shapes(n)]
        for trial in range(trials):
            p = [rng.randrange(1, 20) for _ in range(n)]
            q = [rng.randrange(1, 20) for _ in range(n+1)]
            costs = {t: cost(t, p, q) for t in trees}
            opt = min(costs.values())
            for t, c in costs.items():
                if c == opt:
                    continue
                for name, moves in [('rotation', rotations), ('promotion', promotions)]:
                    if name in found:
                        continue
                    neighbors = list(moves(t))
                    if all(costs[u] > c for u in neighbors):
                        found[name] = dict(n=n, trial=trial, p=p, q=q,
                            tree=t, cost=c, optimal_cost=opt,
                            optimum=min(costs, key=costs.get),
                            best_neighbor_cost=min(costs[u] for u in neighbors),
                            neighbor_count=len(neighbors))
            if len(found) == 2:
                return found
    return found


def bound_survey():
    rng = random.Random(0xB0A0D)
    rows = []
    for n in [16, 32, 64, 128, 256]:
        for kind in ['uniform', 'near_uniform', 'random', 'log_uniform', 'spike', 'keys_only', 'gaps_only']:
            ratios = []
            exact = 0
            for trial in range(20):
                def gen(m):
                    if kind == 'uniform': return [10]*m
                    if kind == 'near_uniform': return [rng.randrange(9,12) for _ in range(m)]
                    if kind == 'log_uniform': return [1 << rng.randrange(20) for _ in range(m)]
                    if kind == 'spike': return [1000000 if rng.random()<0.03 else 1 for _ in range(m)]
                    return [rng.randrange(1,1001) for _ in range(m)]
                p,q=gen(n),gen(n+1)
                if kind == 'keys_only': q=[0]*(n+1)
                if kind == 'gaps_only': p=[0]*n
                opt,_,_=knuth(p,q)
                lb=unordered_huffman(p,q)
                assert lb <= opt
                exact += lb == opt
                ratios.append((opt-lb)/(sum(p)+sum(q)))
            rows.append(dict(n=n, family=kind, trials=20, exact=exact,
                mean_additive_normalized_gap=sum(ratios)/len(ratios),
                max_additive_normalized_gap=max(ratios)))
    return rows


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode',choices=['verify','traps','bounds','all'],default='all')
    parser.add_argument('--output',default='obst/results/initial.json')
    args=parser.parse_args()
    result={'host':platform.platform(),'python':platform.python_version(),
            'started_unix':time.time(), 'mode':args.mode}
    for name,fun in [('verify',verify),('traps',find_traps),('bounds',bound_survey)]:
        if args.mode in [name,'all']:
            then=time.perf_counter()
            result[name]=fun()
            result[name+'_seconds']=time.perf_counter()-then
            print(name, json.dumps(result[name]),flush=True)
            out=Path(args.output)
            out.parent.mkdir(parents=True,exist_ok=True)
            out.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    main()
