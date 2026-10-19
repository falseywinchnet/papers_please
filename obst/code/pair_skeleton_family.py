#!/usr/bin/env python3
"""Nonuniform-key family, scaling, and balanced full-construction benchmarks."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import random
import statistics
import sys
import time

from core_exclusion import solve as previous
from pair_skeleton import closed_candidate, excluded_bound, forest_bound, solve
from research import cost, cubic, knuth


def family(n, placement, rng):
    p, q = [1]*n, [1]*(n+1)
    s = n//16-1
    if placement == 'spread':
        positions = [2+16*k for k in range(s)]
    elif placement == 'left':
        positions = list(range(2, 2+s))
    elif placement == 'middle':
        positions = list(range(n//2-s//2, n//2-s//2+s))
    else:
        positions = rng.sample(range(2, n-2), s)
    for i in positions:
        p[i] = 2
    q[1] = q[-2] = 3*n
    return p, q


def main():
    sys.setrecursionlimit(30000)
    rng = random.Random(0x2F0E57)
    checks, rows, timed = Counter(), [], []
    for h in range(5, 15):
        n, r = 2**h, 2**(h-4)
        s = r-1
        placements = ('spread', 'left', 'middle', 'random') if h <= 11 else ('random',)
        for placement in placements:
            p, q = family(n, placement, rng)
            start = time.perf_counter()
            value, tree, counts = solve(p, q)
            seconds = time.perf_counter()-start
            assert value == cost(tree, p, q)
            assert counts['certified_core'] and not counts['refinement_rescued']
            baseline = (2*h+3)*n-6*h-3
            witness_upper = 15*n+baseline+(h+2)*s
            first_lower = 18*n+(2*h+1)*n-6*h+5 + 2*s-1+(h-6)*r+2
            tail_lower = 21*n+2*n*h-n+2+(h-5)*r+1
            assert counts['witness_cost'] <= witness_upper
            assert counts['first_level_lower_bound'] >= first_lower
            assert counts['tail_lower_bound'] == tail_lower
            assert first_lower-witness_upper == 5*n//8+h+9
            assert tail_lower-witness_upper == 25*n//16+7*h+8
            if h >= 6:
                assert value > counts['basic_lower_bound']
                assert value-counts['basic_lower_bound'] >= n-6*h-5
            if n <= 2048:
                exact, _, _ = knuth(p, q)
                assert value == exact
                checks['knuth_family'] += 1
            if n <= 64:
                exact, _ = cubic(p, q)
                assert value == exact
                checks['cubic_family'] += 1
            checks['family_formula'] += 1
            rows.append(dict(n=n, placement=placement, value=value,
                             seconds=seconds, counts=counts))
            print('family', n, placement, value, round(seconds, 4), flush=True)
    # Exact uniform-background formulas, including the fixed four-key core.
    for h in range(3, 17):
        n = 2**h
        p, q = [1]*n, [1]*(n+1)
        q[1] = q[-2] = 2*n
        value, tree, counts = solve(p, q)
        assert value == cost(tree, p, q) == (2*h+13)*n-6*h-3
        assert counts['first_level_lower_bound'] == value+8
        assert counts['certified_core']
        assert forest_bound([1]*(n-5), [1]*(n-3), Counter()) == (2*h-3)*n-6*h+5
        checks['unit_formula'] += 1
        rows.append(dict(n=n, placement='unit_2n', value=value, counts=counts))
    modes = ('knuth', 'previous', 'pair_frontier', 'pair_knuth')
    orders = []
    for k in range(4):
        order = modes[k:]+modes[:k]
        orders.extend((order, order[::-1]))
    for name in ('nonuniform_spread', 'nonuniform_random', 'unit_2n',
                 'varying_2n', 'random', 'near_uniform', 'geometric'):
        n = 512
        trials = []
        for order in orders:
            if name.startswith('nonuniform'):
                p, q = family(n, name.split('_')[1], rng)
            elif name == 'unit_2n':
                p, q = [1]*n, [1]*(n+1)
                q[1] = q[-2] = 2*n
            elif name == 'varying_2n':
                p = [rng.randrange(1, 1001) for _ in range(n)]
                q = [rng.randrange(1, 1001) for _ in range(n+1)]
                q[1] = q[-2] = 1000*n
            elif name == 'geometric':
                p = [2**i for i in range(n)]
                q = [2**i for i in range(n+1)]
            else:
                lo, hi = (1, 1001) if name == 'random' else (990, 1011)
                p = [rng.randrange(lo, hi) for _ in range(n)]
                q = [rng.randrange(lo, hi) for _ in range(n+1)]
            runs = {}
            for mode in order:
                start = time.perf_counter()
                if mode == 'knuth':
                    value, tree, scans = knuth(p, q)
                    counts = dict(short_states=n*(n+1)//2, root_candidates=scans)
                elif mode == 'previous':
                    value, tree, counts = previous(p, q)
                else:
                    value, tree, counts = solve(p, q, 'knuth' if mode.endswith('knuth') else 'frontier')
                seconds = time.perf_counter()-start
                assert value == cost(tree, p, q)
                runs[mode] = dict(value=value, seconds=seconds, counts=counts)
            assert len({v['value'] for v in runs.values()}) == 1
            trials.append(dict(order=order, runs=runs))
        row = dict(n=n, family=name, trials=trials)
        for mode in modes[1:]:
            row['median_'+mode+'_knuth'] = statistics.median(
                t['runs'][mode]['seconds']/t['runs']['knuth']['seconds'] for t in trials)
        row['median_pair_frontier_previous'] = statistics.median(
            t['runs']['pair_frontier']['seconds']/t['runs']['previous']['seconds'] for t in trials)
        timed.append(row)
        print('timed', name, {k: round(v, 4) for k, v in row.items() if k.startswith('median')}, flush=True)
    target = Path(__file__).resolve().parents[1]/'results'/'pair_skeleton_family.json'
    sources = ('pair_skeleton.py', 'pair_skeleton_family.py', 'mass_frontier.py',
               'core_exclusion.py', 'heavy_core.py', 'research.py')
    hashes = {s: hashlib.sha256(Path(__file__).with_name(s).read_bytes()).hexdigest() for s in sources}
    target.write_text(json.dumps(dict(seed=0x2F0E57, python=platform.python_version(),
        platform=platform.platform(), sources=hashes, checks=checks, rows=rows,
        timed=timed), indent=2)+'\n')


if __name__ == '__main__':
    main()
