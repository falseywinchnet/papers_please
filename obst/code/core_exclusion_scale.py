#!/usr/bin/env python3
"""Full constructions with linear, rather than cubic, heavy gap weights."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import time

from core_exclusion import solve
from heavy_core import select_plan as previous_core_plan
from heavy_core_scale import uniform_cost
from mass_frontier import select_plan as frontier_plan
from research import cost, cubic


def main():
    rows = []
    for h in range(3, 17):
        n = 1 << h
        theta = 4*n
        p, q = [1]*n, [1]*(n+1)
        q[1] = q[n-1] = theta
        start = time.perf_counter()
        value, tree, counts = solve(p, q)
        seconds = time.perf_counter()-start
        exact_core = cubic([1]*4, [1, theta, 2*n-7, theta, 1])[0]
        expected = exact_core+uniform_cost(n-4)
        assert value == expected == cost(tree, p, q) == (2*h+23)*n-6*h-3
        assert counts['certified_core'] and len(counts['attempts']) == 1
        attempt = counts['attempts'][0]
        assert attempt['protected_cost'] == 5*theta
        assert attempt['light_lower_bound'] == 2*n*h-n+2
        assert attempt['witness_light_cost'] == (2*h+3)*n-6*h-3
        assert attempt['kernel_short_states'] == 10
        assert attempt['uniform_reconstructed_keys'] == n-4
        old = Counter()
        assert previous_core_plan(p, q, old) is None
        fp = Counter()
        frontier_plan(p, q, 'adaptive', fp)
        rows.append(dict(n=n, h=h, optimum=value, seconds=seconds, counts=counts,
                         previous_core_plan=dict(old), previous_frontier_plan=dict(fp),
                         previous_full_solve=False))
        print(n, 'cost', value, 'new cells', attempt['kernel_short_states'],
              'old planned cells', fp['selected_short_states'], flush=True)
    target = Path(__file__).resolve().parents[1]/'results'/'core_exclusion_scale.json'
    source = Path(__file__).with_name('core_exclusion.py')
    target.write_text(json.dumps(dict(python=platform.python_version(), platform=platform.platform(),
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), rows=rows), indent=2)+'\n')


if __name__ == '__main__':
    main()
