#!/usr/bin/env python3
"""Matched exact-solver timings for the optional baseline-price search."""
import itertools
import json
from pathlib import Path
import platform
import random
import statistics
import subprocess
import sys
import time

from complete import hybrid_solve
from research import cost, knuth
from sparse import weights


def main():
    sys.setrecursionlimit(20000)
    rng = random.Random(0xBA5EB3AC)
    solvers = dict(knuth=knuth, unpriced=hybrid_solve,
                   priced=lambda p,q: hybrid_solve(p,q,optimize_baseline=True))
    orders = list(itertools.permutations(solvers))
    rows = []
    fixtures = [(1024,'perturbation_1'), (1024,'perturbation_2'),
                (2048,'perturbation_1'), (2048,'perturbation_2'),
                (1024,'random'), (1024,'gap_spike'), (768,'near_uniform')]
    for n, family in fixtures:
        for trial in range(6):
            if family.startswith('perturbation_'):
                epsilon = int(family.split('_')[-1])
                p = [1000+rng.randrange(-epsilon,epsilon+1) for _ in range(n)]
                q = [1000+rng.randrange(-epsilon,epsilon+1) for _ in range(n+1)]
            else:
                p,q = weights(n,family,rng)
            outputs, elapsed = {}, {}
            for name in orders[trial]:
                start = time.perf_counter()
                outputs[name] = solvers[name](p,q)
                elapsed[name] = time.perf_counter()-start
            expected = outputs['knuth'][0]
            for value, tree, _ in outputs.values():
                assert value == expected == cost(tree,p,q)
            rows.append(dict(n=n,family=family,trial=trial,order=orders[trial],
                             seconds=elapsed,priced_vs_knuth=elapsed['priced']/elapsed['knuth'],
                             priced_vs_unpriced=elapsed['priced']/elapsed['unpriced'],
                             knuth_dp_states=n*(n+1)//2,
                             knuth_root_candidates=outputs['knuth'][2],
                             unpriced_counts=outputs['unpriced'][2],
                             priced_counts=outputs['priced'][2]))
        group = rows[-6:]
        print(n,family,'priced/Knuth',round(statistics.median(x['priced_vs_knuth'] for x in group),4),
              'priced/unpriced',round(statistics.median(x['priced_vs_unpriced'] for x in group),4),
              'rescues',sum(x['priced_counts'].get('price_rescued',0) for x in group),flush=True)
    cpu = subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string'],text=True).strip()
    target = Path(__file__).resolve().parents[1]/'results'/'baseline_matched.json'
    target.write_text(json.dumps(dict(host=platform.platform(),cpu=cpu,
                                     python=platform.python_version(),seed=0xBA5EB3AC,
                                     trials_per_fixture=6,rows=rows),indent=2)+'\n')


if __name__ == '__main__':
    main()
