#!/usr/bin/env python3
"""Matched Python timings for the complete-shape certificate hybrid.

All three solvers see identical inputs; all six run orders are used.
Correctness and direct cost checks are outside the timed region.
These are exploratory single-host measurements, not production benchmarks.
"""
import itertools
import json
import math
from pathlib import Path
import platform
import random
import statistics
import subprocess
import sys
import time

from complete import hybrid_solve
from recursive_contract import solve as recursive_solve
from research import cost, knuth
from sparse import weights


def main():
    sys.setrecursionlimit(20000)
    rng = random.Random(0xC0A9B3AC)
    solvers = dict(knuth=knuth, recursive=recursive_solve, hybrid=hybrid_solve)
    orders = list(itertools.permutations(solvers))
    rows = []
    fixtures = [(n, f) for n in (512, 1024)
                for f in ('near_uniform', 'random', 'log_uniform',
                          'gap_spike', 'heavy_separators')]
    fixtures += [(n, 'near_uniform') for n in (768, 1000, 1023)]
    for n, family in fixtures:
        for trial in range(6):
            if family == 'heavy_separators':
                p = [rng.randrange(1, 4) for _ in range(n)]
                q = [rng.randrange(1, 4) for _ in range(n+1)]
                for k in rng.sample(range(n), math.isqrt(n)):
                    p[k] = 1000000
            else:
                p, q = weights(n, family, rng)
            outputs, elapsed = {}, {}
            for name in orders[trial]:
                start = time.perf_counter()
                outputs[name] = solvers[name](p, q)
                elapsed[name] = time.perf_counter()-start
            expected = outputs['knuth'][0]
            for value, tree, _ in outputs.values():
                assert value == expected == cost(tree, p, q)
            rows.append(dict(n=n, family=family, trial=trial,
                             order=orders[trial], seconds=elapsed,
                             hybrid_vs_knuth=elapsed['hybrid']/elapsed['knuth'],
                             hybrid_vs_recursive=elapsed['hybrid']/elapsed['recursive'],
                             knuth_dp_states=n*(n+1)//2,
                             knuth_root_candidates=outputs['knuth'][2],
                             hybrid_counts=outputs['hybrid'][2],
                             recursive_counts=outputs['recursive'][2]))
        group = rows[-6:]
        print(n, family,
              'hybrid/Knuth', round(statistics.median(x['hybrid_vs_knuth'] for x in group), 4),
              'hybrid/recursive', round(statistics.median(x['hybrid_vs_recursive'] for x in group), 4),
              'certificates', sum(x['hybrid_counts'].get('certified', 0) for x in group),
              flush=True)
    try:
        cpu = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string'],
                                      text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        cpu = platform.processor()
    target = Path(__file__).resolve().parents[1]/'results'/'complete_matched.json'
    target.write_text(json.dumps(dict(host=platform.platform(), cpu=cpu,
                                     python=platform.python_version(), seed=0xC0A9B3AC,
                                     trials_per_fixture=6, rows=rows), indent=2)+'\n')


if __name__ == '__main__':
    main()
