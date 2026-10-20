#!/usr/bin/env python3
"""Independent exact and adversarial checks for residual core exclusion."""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

from core_exclusion import attempt, choose_plans, solve
from heavy_core import (anchors_at, fits, fixtures as old_fixtures, intervals,
                        protected_height, solve as old_solve, tri)
from research import cost, cubic, knuth, label, shapes, unordered_huffman
from sparse import FAMILIES, weights


def exhaustive():
    counts = Counter()
    rescue = None
    for n in range(1, 5):
        trees = [label(t)[0] for t in shapes(n)]
        for v in itertools.product((0, 1, 4), repeat=2*n+1):
            p, q = list(v[:n]), list(v[n:])
            full = [cost(t, p, q) for t in trees]
            counts['exhaustive_inputs'] += 1
            for theta in set(v)-{0}:
                anchors = set(anchors_at(p, q, theta))
                if len(anchors) == n:
                    continue
                hp = [w if w >= theta else 0 for w in p]
                hq = [w if w >= theta else 0 for w in q]
                lp = [w if w < theta else 0 for w in p]
                lq = [w if w < theta else 0 for w in q]
                protected = min(cost(t, hp, hq) for t in trees)
                lb = unordered_huffman(lp, lq)
                assert lb <= min(cost(t, lp, lq) for t in trees)
                inside = [c for t, c in zip(trees, full) if fits(t, anchors)]
                outside = [c for t, c in zip(trees, full) if not fits(t, anchors)]
                ceiling = protected+theta+lb
                assert min(outside) >= ceiling, (p, q, theta, ceiling, outside)
                counts['excluded_class_checks'] += 1
                for refine in (False, True):
                    stats = Counter()
                    result = attempt(p, q, stats, 'knuth', refine, theta)
                    assert stats['protected_cost'] == protected
                    assert stats['light_lower_bound'] == lb
                    if refine:
                        assert (result is not None) == (min(inside) <= ceiling)
                    if result is not None:
                        value, tree = result
                        assert value == min(full) == min(inside) == cost(tree, p, q)
                        counts['refined_certificates' if refine else 'witness_certificates'] += 1
                        counts['refinement_rescues'] += stats['refinement_rescued']
                        if stats['refinement_rescued'] and rescue is None:
                            rescue = dict(p=p, q=q, threshold=theta, counts=dict(stats))
    return dict(counts), rescue


def arbitrary_selected():
    checks = 0
    for n in range(1, 4):
        trees = [label(t)[0] for t in shapes(n)]
        for v in itertools.product((1, 3), repeat=2*n+1):
            p, q = list(v[:n]), list(v[n:])
            full = [cost(t, p, q) for t in trees]
            for mask in range(1, 1 << (2*n+1)):
                selected = [bool(mask >> i & 1) for i in range(2*n+1)]
                anchors = set(anchors_at([int(x) for x in selected[:n]],
                                         [int(x) for x in selected[n:]], 1))
                if len(anchors) == n:
                    continue
                hv = [w if chosen else 0 for w, chosen in zip(v, selected)]
                lv = [w if not chosen else 0 for w, chosen in zip(v, selected)]
                protected = min(cost(t, hv[:n], hv[n:]) for t in trees)
                light = min(cost(t, lv[:n], lv[n:]) for t in trees)
                theta = min(w for w, chosen in zip(v, selected) if chosen)
                for t, value in zip(trees, full):
                    if not fits(t, anchors):
                        assert value >= protected+theta+light, (n, v, mask, t)
                        checks += 1
    return checks


def fixtures(n, rng):
    result = old_fixtures(n, rng)
    for factor in (1, 2, 4, 8):
        p, q = [1]*n, [1]*(n+1)
        q[1] = q[n-1] = factor*n
        result.append(('linear_two_gaps_'+str(factor), p, q))
    for family in ('linear_many_gaps', 'linear_mixed_outcomes'):
        p, q = [1]*n, [1]*(n+1)
        count = max(2, int(n**0.5))
        for k in range(count):
            g = max(1, min(n-1, (k+1)*n//(count+1)))
            if family == 'linear_mixed_outcomes' and k % 2:
                p[g] = 4*n
            else:
                q[g] = 4*n
        result.append((family, p, q))
    return result


def mixed_fixtures(n, rng):
    result = []
    for family in ('linear_random_two_gaps', 'linear_random_many_gaps', 'linear_random_mixed'):
        p = [rng.randrange(1, 1001) for _ in range(n)]
        q = [rng.randrange(1, 1001) for _ in range(n+1)]
        count = 2 if family == 'linear_random_two_gaps' else max(2, int(n**0.5))
        gaps = [1, n-1] if count == 2 else [(k+1)*n//(count+1) for k in range(count)]
        for k, g in enumerate(gaps):
            if family == 'linear_random_mixed' and k % 2:
                p[g] = 4000*n
            else:
                q[g] = 4000*n
        result.append((family, p, q))
    return result


def check_mixed():
    rng = random.Random(0xE7C10D)
    rows = []
    for n in (128, 512, 2048):
        for family, p, q in mixed_fixtures(n, rng):
            expected, _, scans = knuth(p, q)
            previous, _, old_counts = old_solve(p, q)
            assert previous == expected
            runs = {}
            for kernel in ('frontier', 'knuth'):
                value, tree, counts = solve(p, q, kernel)
                assert value == expected == cost(tree, p, q)
                runs[kernel] = counts
            rows.append(dict(n=n, family=family, optimum=expected, previous=old_counts,
                             counts=runs, knuth_root_candidates=scans))
            print(n, family, 'certified', runs['frontier'].get('certified_core', 0),
                  'attempts', len(runs['frontier'].get('attempts', [])), flush=True)
    target = Path(__file__).resolve().parents[1]/'results'/'core_exclusion_mixed.json'
    source = Path(__file__).with_name('core_exclusion.py')
    target.write_text(json.dumps(dict(seed=0xE7C10D,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), rows=rows), indent=2)+'\n')


def main():
    sys.setrecursionlimit(20000)
    checks, rescue = exhaustive()
    print('exhaustive', checks, flush=True)
    checks['arbitrary_selected_checks'] = arbitrary_selected()
    print('arbitrary selection', checks['arbitrary_selected_checks'], flush=True)
    rng = random.Random(0xE7C105E)
    full = selection = 0
    for n in range(41):
        for trial in range(40):
            if n and trial < len(FAMILIES):
                p, q = weights(n, FAMILIES[trial], rng)
            else:
                p = [rng.randrange(9) if trial % 2 else 1 << rng.randrange(12) for _ in range(n)]
                q = [rng.randrange(9) if trial % 3 else 1 << rng.randrange(12) for _ in range(n+1)]
            expected = cubic(p, q)[0]
            for kernel in ('frontier', 'knuth'):
                for refine in (False, True):
                    value, tree, _ = solve(p, q, kernel, refine)
                    assert value == expected == cost(tree, p, q)
                    full += 1
            stats = Counter()
            plans = choose_plans(p, q, stats)
            cap = stats.get('protected_core_cap', 0)
            cheapest, highest = {}, {}
            for theta in sorted(set(p+q)-{0}):
                a = anchors_at(p, q, theta)
                if len(a) <= cap:
                    proxy = tri(len(a))+sum(tri(j-i) for i, j in intervals(n, a))
                    if proxy < tri(n):
                        band = len(a).bit_length()-1
                        if band not in cheapest or proxy < cheapest[band][0]:
                            cheapest[band] = (proxy, theta)
                        highest[band] = (proxy, theta)
            expected_plans = sorted(set(cheapest.values()) | set(highest.values()))
            assert [(x['knuth_proxy'], x['threshold']) for x in plans] == expected_plans
            selection += 1
    checks.update(full_solves=full, selection_checks=selection)
    print('full', full, 'selection', selection, flush=True)
    rows = []
    for n in (128, 512, 2048):
        for family, p, q in fixtures(n, rng):
            expected, _, scans = knuth(p, q)
            old, _, old_counts = old_solve(p, q)
            assert old == expected
            runs = {}
            for kernel in ('frontier', 'knuth'):
                for refine in (False, True):
                    value, tree, stats = solve(p, q, kernel, refine)
                    assert value == expected == cost(tree, p, q)
                    runs[kernel+('_refined' if refine else '')] = stats
            rows.append(dict(n=n, family=family, optimum=expected,
                             previous=old_counts, counts=runs, knuth_root_candidates=scans))
            print(n, family, 'witness', runs['frontier'].get('witness_certificate'),
                  'refined', runs['frontier_refined'].get('certified_core', 0), flush=True)
    target = Path(__file__).resolve().parents[1]/'results'/'core_exclusion.json'
    source = Path(__file__).with_name('core_exclusion.py')
    target.write_text(json.dumps(dict(checks=checks, first_refinement_rescue=rescue,
                                     source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                                     rows=rows), indent=2)+'\n')


if __name__ == '__main__':
    if sys.argv[1:] == ['--mixed-only']:
        check_mixed()
    else:
        main()
