#!/usr/bin/env python3
"""Balanced matched full-construction timings for residual core exclusion."""
import hashlib
import json
from pathlib import Path
import platform
import random
import statistics
import sys
import time

from check_core_exclusion import fixtures, mixed_fixtures
from core_exclusion import solve
from heavy_core import solve as previous_solve
from research import cost, knuth


def main():
    sys.setrecursionlimit(20000)
    rng = random.Random(0xE7C10B)
    modes = ('knuth', 'previous', 'exclusion_frontier', 'exclusion_knuth')
    orders = []
    for k in range(4):
        order = modes[k:]+modes[:k]
        orders.extend((order, order[::-1]))
    cases = [(1024, f) for f in ('linear_two_gaps_4', 'linear_two_gaps_2',
              'linear_many_gaps', 'linear_mixed_outcomes', 'random', 'near_uniform')]
    cases.append((512, 'geometric'))
    cases.extend((1024, f) for f in ('linear_random_two_gaps', 'linear_random_many_gaps', 'linear_random_mixed'))
    rows = []
    for n, family in cases:
        trials = []
        for order in orders:
            options = mixed_fixtures(n, rng) if family.startswith('linear_random') else fixtures(n, rng)
            _, p, q = next(x for x in options if x[0] == family)
            runs = {}
            for mode in order:
                start = time.perf_counter()
                if mode == 'knuth':
                    value, tree, scans = knuth(p, q)
                    counts = dict(short_states=n*(n+1)//2, root_candidates=scans)
                elif mode == 'previous':
                    value, tree, counts = previous_solve(p, q)
                else:
                    value, tree, counts = solve(p, q, 'knuth' if mode.endswith('knuth') else 'frontier')
                seconds = time.perf_counter()-start
                assert value == cost(tree, p, q)
                runs[mode] = dict(value=value, seconds=seconds, counts=counts)
            assert len({x['value'] for x in runs.values()}) == 1
            trials.append(dict(order=order, runs=runs))
        row = dict(n=n, family=family, trials=trials)
        for mode in modes[1:]:
            row['median_'+mode+'_knuth'] = statistics.median(
                t['runs'][mode]['seconds']/t['runs']['knuth']['seconds'] for t in trials)
        row['median_exclusion_frontier_previous'] = statistics.median(
            t['runs']['exclusion_frontier']['seconds']/t['runs']['previous']['seconds'] for t in trials)
        rows.append(row)
        print(n, family, {k: round(v, 6) for k, v in row.items() if k.startswith('median')}, flush=True)
    target = Path(__file__).resolve().parents[1]/'results'/'core_exclusion_matched.json'
    source = Path(__file__).with_name('core_exclusion.py')
    target.write_text(json.dumps(dict(seed=0xE7C10B, python=platform.python_version(),
        platform=platform.platform(), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), rows=rows), indent=2)+'\n')


if __name__ == '__main__':
    main()
