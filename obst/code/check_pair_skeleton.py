#!/usr/bin/env python3
"""Independent forest and excluded-class checks for two-gap skeleton bounds."""
from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

from heavy_core import fits
from pair_skeleton import (closed_candidate, excluded_bound, forest_bound,
                           pair_data, solve)
from research import cost, cubic, knuth, label, shapes
from sparse import FAMILIES, weights


@lru_cache(None)
def forest_profiles(n, roots):
    if roots == 0:
        return (((), ()),) if n == 0 else ()
    result = set()
    for left in range(n+1):
        for shape in shapes(left):
            t = label(shape)[0]
            kl = tuple(cost(t, [int(i == k) for i in range(left)], [0]*(left+1))
                       for k in range(left))
            gd = tuple(cost(t, [0]*left, [int(i == g) for i in range(left+1)])
                       for g in range(left+1))
            for a, b in forest_profiles(n-left, roots-1):
                result.add((tuple(sorted(kl+a)), tuple(sorted(gd+b))))
    return tuple(result)


def forest_checks():
    checked = 0
    rng = random.Random(0xB21D6E)
    for n in range(7):
        for roots in (1, 2, 3, 4):
            profiles = forest_profiles(n, roots)
            inputs = itertools.product((0, 1, 3), repeat=2*n+roots) if n <= 2 else (
                [rng.randrange(20) for _ in range(2*n+roots)] for _ in range(60))
            for v in inputs:
                p, q = list(v[:n]), list(v[n:])
                ps, qs = sorted(p, reverse=True), sorted(q, reverse=True)
                expected = min(sum(a*b for a, b in zip(ps, kl))+
                               sum(a*b for a, b in zip(qs, gd)) for kl, gd in profiles)
                assert forest_bound(p, q, Counter()) == expected, (p, q, roots)
                checked += 1
    return checked


def exhaustive():
    counts = Counter()
    example = None
    for n in range(1, 6):
        trees = [label(s)[0] for s in shapes(n)]
        kl = [[cost(t, [int(i == k) for i in range(n)], [0]*(n+1)) for k in range(n)] for t in trees]
        gd = [[cost(t, [0]*n, [int(i == g) for i in range(n+1)]) for g in range(n+1)] for t in trees]
        geometry = []
        for gaps in itertools.combinations(range(1, n), 2):
            _, anchors, _, _ = pair_data(n, gaps)
            if len(anchors) == n:
                continue
            inside = [fits(t, set(anchors)) for t in trees]
            levels = [d[gaps[0]]+d[gaps[1]] for d in gd]
            geometry.append((gaps, len(anchors), inside, levels))
        for v in itertools.product((0, 1, 4) if n <= 4 else (0, 1), repeat=2*n+1):
            p, q = list(v[:n]), list(v[n:])
            full = [sum(a*b for a, b in zip(p, arow))+sum(a*b for a, b in zip(q, brow))
                    for arow, brow in zip(kl, gd)]
            counts['exhaustive_inputs'] += 1
            for gaps, m, inside, levels in geometry:
                c = Counter()
                bound = excluded_bound(p, q, gaps, c)
                outside = [v for v, yes in zip(full, inside) if not yes]
                assert bound <= min(outside), (p, q, gaps, bound, outside)
                for name, test in [('first_level_lower_bound', lambda d: d == m+2),
                                   ('tail_lower_bound', lambda d: d >= m+3)]:
                    values = [v for v, yes, d in zip(full, inside, levels) if not yes and test(d)]
                    if values:
                        assert c[name] <= min(values), (p, q, gaps, name, c[name], values)
                        counts[name+'_checks'] += 1
                assert all(yes or d >= m+2 for yes, d in zip(inside, levels))
                value, tree = closed_candidate(p, q, gaps, Counter(), 'knuth')
                assert value == min(v for v, yes in zip(full, inside) if yes) == cost(tree, p, q)
                witness, _ = closed_candidate(p, q, gaps, Counter(), balanced=True)
                if witness <= bound:
                    assert value == min(full)
                    counts['witness_certificates'] += 1
                if value <= bound:
                    assert value == min(full)
                    counts['refined_certificates'] += 1
                    if value > c['basic_lower_bound']:
                        counts['coupling_rescues'] += 1
                        if example is None:
                            example = dict(p=p, q=q, gaps=gaps, optimum=value, counts=dict(c))
                counts['pair_exclusion_checks'] += 1
    return dict(counts), example


def fixtures(n, rng):
    result = [(f, *weights(n, f, rng)) for f in ('random', 'near_uniform', 'geometric', 'spike', 'gap_spike')]
    for family in ('unit_pair_1n', 'unit_pair_2n', 'varying_pair_1n', 'varying_pair_2n',
                   'interior_varying_pair', 'adjacent_varying_pair', 'key_perturbed_pair'):
        if family.startswith('unit') or family == 'key_perturbed_pair':
            p, q = [1]*n, [1]*(n+1)
            scale = 1
        else:
            p = [rng.randrange(1, 1001) for _ in range(n)]
            q = [rng.randrange(1, 1001) for _ in range(n+1)]
            scale = 1000
        if family == 'key_perturbed_pair':
            p = [1+(i % 7 == 3) for i in range(n)]
        gaps = (n//3, 2*n//3) if family == 'interior_varying_pair' else (
            (n//2, n//2+1) if family == 'adjacent_varying_pair' else (1, n-1))
        factor = 1 if family.endswith('1n') else 2
        for g in gaps:
            q[g] = factor*scale*n
        result.append((family, p, q))
    return result


def main():
    sys.setrecursionlimit(20000)
    forest = forest_checks()
    print('forest checks', forest, flush=True)
    checks, rescue = exhaustive()
    checks['forest_checks'] = forest
    print('exhaustive', checks, flush=True)
    rng = random.Random(0xB21D6F)
    full = 0
    for n in range(41):
        for trial in range(40):
            if n and trial < len(FAMILIES):
                p, q = weights(n, FAMILIES[trial], rng)
            else:
                p = [rng.randrange(20) if trial % 2 else 1 << rng.randrange(12) for _ in range(n)]
                q = [rng.randrange(20) if trial % 3 else 1 << rng.randrange(12) for _ in range(n+1)]
            expected = cubic(p, q)[0]
            for kernel in ('frontier', 'knuth'):
                for refine in (False, True):
                    value, tree, _ = solve(p, q, kernel, refine)
                    assert value == expected == cost(tree, p, q)
                    full += 1
    checks['full_solves'] = full
    print('full solves', full, flush=True)
    from core_exclusion import solve as old_solve
    rows = []
    for n in (128, 512, 2048):
        for family, p, q in fixtures(n, rng):
            expected, _, scans = knuth(p, q)
            old, _, previous = old_solve(p, q)
            assert old == expected
            runs = {}
            for kernel in ('frontier', 'knuth'):
                value, tree, stats = solve(p, q, kernel)
                assert value == expected == cost(tree, p, q)
                runs[kernel] = stats
            rows.append(dict(n=n, family=family, optimum=expected, previous=previous,
                             counts=runs, knuth_root_candidates=scans))
            print(n, family, 'certified', runs['frontier'].get('certified_core', 0), flush=True)
    source = Path(__file__).with_name('pair_skeleton.py')
    target = Path(__file__).resolve().parents[1]/'results'/'pair_skeleton.json'
    target.write_text(json.dumps(dict(checks=checks, first_coupling_rescue=rescue,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), rows=rows), indent=2)+'\n')


if __name__ == '__main__':
    main()
