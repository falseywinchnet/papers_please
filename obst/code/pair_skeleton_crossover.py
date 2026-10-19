#!/usr/bin/env python3
"""Matched larger nonuniform-family construction, with exact Knuth reference."""
import hashlib
import json
from pathlib import Path
import platform
import random
import statistics
import time

from pair_skeleton import solve
from pair_skeleton_family import family
from research import cost, knuth


def main():
    rng = random.Random(0x2F0E58)
    rows = []
    for n in (2048, 4096):
        trials = []
        for trial in range(4):
            p, q = family(n, 'random', rng)
            order = ('knuth', 'pair') if trial % 2 == 0 else ('pair', 'knuth')
            runs = {}
            for mode in order:
                start = time.perf_counter()
                if mode == 'knuth':
                    value, tree, scans = knuth(p, q)
                    counts = dict(short_states=n*(n+1)//2, root_candidates=scans)
                else:
                    value, tree, counts = solve(p, q)
                    assert counts['certified_core']
                elapsed = time.perf_counter()-start
                assert value == cost(tree, p, q)
                runs[mode] = dict(value=value, seconds=elapsed, counts=counts)
            assert runs['knuth']['value'] == runs['pair']['value']
            trials.append(dict(order=order, runs=runs))
            print(n, trial, {k: round(v['seconds'], 4) for k, v in runs.items()}, flush=True)
        ratio = statistics.median(t['runs']['pair']['seconds']/t['runs']['knuth']['seconds'] for t in trials)
        rows.append(dict(n=n, trials=trials, median_pair_knuth=ratio))
    sources = ('pair_skeleton_crossover.py', 'pair_skeleton_family.py', 'pair_skeleton.py',
               'research.py', 'mass_frontier.py', 'heavy_core.py', 'core_exclusion.py')
    hashes = {s: hashlib.sha256(Path(__file__).with_name(s).read_bytes()).hexdigest() for s in sources}
    target = Path(__file__).resolve().parents[1]/'results'/'pair_skeleton_crossover.json'
    target.write_text(json.dumps(dict(seed=0x2F0E58, sources=hashes,
        platform=platform.platform(), python=platform.python_version(), rows=rows), indent=2)+'\n')


if __name__ == '__main__':
    main()
