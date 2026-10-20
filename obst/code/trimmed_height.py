#!/usr/bin/env python3
"""Sufficient full mixed-OBST height from disjoint heavy-outcome charges.

All arithmetic is exact for integer/Fraction inputs. No posterior success
test is used: both the selected vector kernel and Knuth return full optima.
"""
from collections import Counter
from slot_vector import normalize, operations, solve as vector_solve


class CountedWeight:
    def __init__(self, value, stats):
        self.value, self.stats = value, stats

    def __lt__(self, other):
        self.stats['height_sort_comparisons'] += 1
        return self.value < other.value


def height_bound(p, q, stats=None, observer=None):
    """Bound some optimum's height; every positive subtree obeys the head bound."""
    if stats is None: stats = Counter()
    n = len(p)
    assert len(q) == n+1 and all(x >= 0 for x in (*p, *q))
    W = sum(p)+sum(q)
    zero_run = run = 0
    mu = None
    for i in range(n):
        mass = p[i]+q[i]+q[i+1]
        stats['height_singleton_scans'] += 1
        if mass:
            mu = mass if mu is None else min(mu, mass)
            run = 0
        else:
            run += 1
            zero_run = max(zero_run, run)
    if not n or mu is None:
        return dict(height=n.bit_length(), marked=0, light_mass=W, mu=mu,
                    zero_run=zero_run, zero_height=zero_run.bit_length(),
                    positive_height=0, untrimmed_height=n.bit_length(), t=0)
    zero_height = zero_run.bit_length()
    # fib[j] = mu F_(j+1). Stop at the first value above W or at n.
    # Thus the table has O(n) entries and no huge irrelevant Fibonacci tail.
    fib = [mu]
    if n: fib.append(mu)
    while len(fib)-1 < n and fib[-1] <= W:
        fib.append(fib[-1]+fib[-2])
        stats['height_fibonacci_additions'] += 1
    weights = [x.value for x in sorted(
        (CountedWeight(x, stats) for x in (*p, *q) if x), reverse=True)]
    stats['height_sorted_outcomes'] += len(weights)
    t, light = len(fib)-1, W
    best = None
    for k in range(len(weights)+1):
        if k: light -= weights[k-1]
        while t and fib[t-1] > light:
            t -= 1
            stats['height_index_decrements'] += 1
        stats['height_candidate_scans'] += 1
        positive = t if k == 0 else t+k+1
        h = min(n, positive+zero_height)
        if k == 0: untrimmed = h
        if observer is not None: observer(k, light, t, h)
        if best is None or h < best['height']:
            best = dict(height=h, marked=k, light_mass=light, mu=mu,
                        zero_run=zero_run, zero_height=zero_height,
                        positive_height=positive, untrimmed_height=untrimmed, t=t)
    assert best['height'] >= n.bit_length()
    return best


def balanced(lo, hi):
    if lo == hi: return None
    r = (lo+hi)//2
    return r, balanced(lo, r), balanced(r+1, hi)


def knuth_fallback(p, q, stats):
    """Ordinary Knuth recurrence, allowing exact rational nonnegative weights."""
    n = len(p)
    pref = [0]
    for a, b in zip(p, q[1:]): pref.append(pref[-1]+a+b)
    C = [[0]*(n+1) for _ in range(n+1)]
    roots = [[0]*(n+1) for _ in range(n+1)]
    for length in range(1, n+1):
        for i in range(n-length+1):
            j = i+length
            low = i if length == 1 else roots[i][j-1]
            high = j-1 if length == 1 else roots[i+1][j]
            best = None
            for r in range(low, high+1):
                value = C[i][r]+C[r+1][j]
                stats['height_fallback_candidates'] += 1
                if best is None or value < best:
                    best, roots[i][j] = value, r
            C[i][j] = best+pref[j]-pref[i]+q[i]
            stats['height_fallback_states'] += 1
    # An unrestricted optimum may be a chain; reconstruct without a
    # Python recursion-depth assumption.
    stack, built = [(0, n, False)], {}
    while stack:
        i, j, ready = stack.pop()
        if i == j: continue
        r = roots[i][j]
        if ready:
            built[i, j] = (r, built.pop((i, r), None),
                          built.pop((r+1, j), None))
            stats['height_fallback_output_nodes'] += 1
        else:
            stack.extend(((i, j, True), (r+1, j, False), (i, r, False)))
    return C[0][n], built.get((0, n))


def solve(p, q, stats=None, force_vector=False):
    """Globally exact constructor; force_vector is an audit override only."""
    if stats is None: stats = Counter()
    n = len(p)
    assert len(q) == n+1 and all(x >= 0 for x in (*p, *q))
    if not n:
        return dict(cost=0, tree=None, method='empty', plan=dict(height=0))
    w, g, constant = normalize(p, q)
    plan = height_bound(w, g, stats)
    h = plan['height']
    if not sum(w)+sum(g):
        return dict(cost=constant, tree=balanced(0, n), method='zero', plan=plan)
    ops = operations(w, g)
    long_runs = sum(m >= 2 for k, m, wt, gap in ops)
    singles = len(ops)-long_runs
    # A capacity above n^2 cannot win the proxy comparison. Avoid creating
    # an exponentially large integer just to reject an oversized plan.
    c = 2**h-1 if force_vector or h <= 2*n.bit_length() else None
    proxy = c*(1+h*long_runs+singles) if c is not None else None
    plan.update(long_runs=long_runs, singletons=singles, capacity=c,
                vector_work_proxy=proxy, fallback_work_proxy=n*n)
    if force_vector or proxy is not None and proxy <= n*n:
        result = vector_solve(p, q, h, stats)
        assert result is not None
        result.update(method='vector', plan=plan)
        stats['height_vector_calls'] += 1
        return result
    value, tree = knuth_fallback(p, q, stats)
    stats['height_knuth_calls'] += 1
    return dict(cost=value, tree=tree, method='knuth', plan=plan)
