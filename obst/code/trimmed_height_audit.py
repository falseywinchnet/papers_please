#!/usr/bin/env python3
"""Independent optimal-shape and full-constructor audit; no timing results."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib, json, random
from trimmed_height import height_bound, solve
from slot_vector import normalize
from research import shapes, label, cost, cubic, knuth
from slot_run_audit import verify_tree


def threshold(mu, light, n):
    a, b, t = 1, 1, 0
    while a*mu <= light and t < n:
        a, b, t = b, a+b, t+1
    return t


def tree_data(tree, p, q):
    positive = []
    def visit(node, lo, hi, depth):
        if node is None: return q[lo], depth
        r, left, right = node
        lm, lh = visit(left, lo, r, depth+1)
        rm, rh = visit(right, r+1, hi, depth+1)
        mass = p[r]+lm+rm
        if mass: positive.append((depth, mass))
        return mass, max(lh, rh)
    _, h = visit(tree, 0, len(p), 0)
    return positive, h


def shape_check(p, q, stats, subsets=False):
    n = len(p)
    entries = [(sum(p[i:j])+sum(q[i:j+1]), j-i)
               for i in range(n) for j in range(i+1, n+1)]
    mu = min((a for a, length in entries if a), default=None)
    z = max((length for a, length in entries if not a), default=0)
    candidates = [(cost(t, p, q), t) for t in (label(s)[0] for s in shapes(n))]
    optimum = min(v for v, t in candidates)
    optimal = [tree_data(t, p, q) for v, t in candidates if v == optimum]
    stats['height_literal_shapes'] += len(candidates)
    stats['height_optimal_shapes'] += len(optimal)
    W = sum(p)+sum(q)
    weights = sorted(p+q, reverse=True)
    cuts = []
    def observe(k, light, t, h):
        ref_t = threshold(mu, light, n)
        assert ref_t == t
        raw = t if not k else t+k+1
        assert h == min(n, raw+z.bit_length())
        for nodes, tree_h in optimal:
            assert all(d < raw for d, mass in nodes)
            stats['height_positive_node_controls'] += len(nodes)
        assert min(tree_h for nodes, tree_h in optimal) <= h
        cuts.append(h)
        stats['height_sorted_cut_controls'] += 1
    result = height_bound(p, q, stats, observe if mu else None)
    assert result['mu'] == mu and result['zero_run'] == z
    assert min(h for nodes, h in optimal) <= result['height']
    if cuts: assert result['height'] == min(cuts)
    stats['height_shape_inputs'] += 1
    # Arbitrary marked sets, not merely prefixes in weight order.
    if subsets and mu:
        for mask in range(1 << (2*n+1)):
            k = bin(mask).count('1')
            light = sum(w for i, w in enumerate(p+q) if not mask >> i & 1)
            t = threshold(mu, light, n)
            raw = t if not k else t+k+1
            for nodes, h in optimal:
                assert all(d < raw for d, mass in nodes)
            stats['height_arbitrary_subset_controls'] += 1
    return optimum


def main():
    root = Path(__file__).resolve().parents[1]
    stats = Counter(); rng = random.Random(551019)
    for n in range(1, 5):
        for index, ww in enumerate(product((0, 1, 9), repeat=2*n+1)):
            p, q = list(ww[:n]), list(ww[n:])
            ref = shape_check(p, q, stats, subsets=n <= 3)
            if n <= 3 or index % 31 == 0:
                for forced in (False, True):
                    result = solve(p, q, stats, force_vector=forced)
                    assert result['cost'] == ref
                    assert verify_tree(result['tree'], p, q, n, stats) == ref
                    stats['height_full_constructor_controls'] += 1
        print('exhaustive', n, dict(stats), flush=True)
    for q in ([0], [7], [Fraction(2, 3)]):
        result = solve([], q, stats)
        assert result['cost'] == 0 and result['tree'] is None
        stats['height_empty_controls'] += 1
    for n in (5, 6, 7, 8, 12, 16, 24, 32, 48, 64):
        for trial in range(18):
            if trial == 0:
                p = [2**i for i in range(n)]; q = [0]*(n+1)
            elif trial == 1:
                p = [0]*n; q = [0]*(n+1); q[n//2] = 2**100
            elif trial == 2:
                p = [0]*n; p[n//2] = 2**80; q = [0]*(n+1)
            elif trial == 3:
                p = [1]*n; q = [0]*(n+1); q[n//2] = 2**100
            else:
                p = [rng.choice((0, 1, 2, 7, 2**32)) for _ in range(n)]
                q = [rng.choice((0, 1, 2, 7, 2**48)) for _ in range(n+1)]
            ref, _ = cubic(p, q)
            stats['height_cubic_reference_candidates'] += n*(n+1)*(n+2)//6
            if n <= 8: assert shape_check(p, q, stats) == ref
            # Rational scaling changes neither optima nor height decisions.
            if trial % 3 == 0:
                p = [Fraction(x, 3) for x in p]
                q = [Fraction(x, 3) for x in q]
                ref = Fraction(ref, 3)
            result = solve(p, q, stats)
            assert result['cost'] == ref
            assert verify_tree(result['tree'], p, q, n, stats) == ref
            stats['height_full_constructor_controls'] += 1
            if n <= 12:
                result = solve(p, q, stats, force_vector=True)
                assert result['cost'] == ref
                assert verify_tree(result['tree'], p, q, result['plan']['height'], stats) == ref
                stats['height_full_constructor_controls'] += 1
    print('mixed', dict(stats), flush=True)
    large = []
    for n in (32, 96, 192, 384):
        for kind in ('moderate_gap', 'huge_gap', 'huge_key_and_gap'):
            p = [1 if i < n//3 else 3 if i < 2*n//3 else 2 for i in range(n)]
            q = [0]*(n+1)
            q[n//2] = n if kind == 'moderate_gap' else 2**128
            if kind.endswith('and_gap'): p[n//5] = 2**192
            counts = Counter(); result = solve(p, q, counts, force_vector=True)
            ref, _, scans = knuth(p, q)
            assert result['cost'] == ref
            assert verify_tree(result['tree'], p, q, result['plan']['height'], counts) == ref
            large.append(dict(n=n, kind=kind, cost=ref, plan=result['plan'],
                              counts=counts, reference_candidates=scans,
                              reference_states=n*(n+1)//2,
                              verification='Full forced vector kernel, independent ordinary Knuth optimum, and original output-tree order/height/cost'))
            print('full', n, kind, result['plan']['height'], flush=True)
    # A full optimum can exceed the default Python recursion depth.
    # For p_i=2^i and zero gaps, the endpoint dominance inequality holds
    # on every remaining prefix, proving the rightmost-root chain optimum.
    n = 1024; p = [2**i for i in range(n)]; q = [0]*(n+1)
    counts = Counter(); result = solve(p, q, counts)
    assert result['method'] == 'knuth'
    assert result['cost'] == 2**(n+1)-n-2
    node = result['tree']
    for i in range(n-1, -1, -1):
        assert node[0] == i and node[2] is None
        node = node[1]
    assert node is None
    deep_chain = dict(n=n, verification='Complete rightmost-root chain and closed-form optimum from endpoint dominance',
                      plan=result['plan'], counts=counts)
    plans = []
    for n in (1024, 4096, 16384, 65536):
        for bits in (64, 256, 4096):
            p = [1 if i < n//3 else 3 if i < 2*n//3 else 2 for i in range(n)]
            q = [0]*(n+1); q[n//2] = 2**bits
            p[n//5] = 2**(bits+16)
            w, g, _ = normalize(p, q)
            counts = Counter(); plan = height_bound(w, g, counts)
            assert plan['marked'] == 2
            plans.append(dict(n=n, exceptional_bits=bits, plan=plan, counts=counts,
                              verification='Height selection only; no full tree or optimum reference at this size'))
    files = ['trimmed_height.py', 'trimmed_height_audit.py', 'slot_vector.py',
             'concave_lws.py', 'mixed_slots.py', 'research.py', 'slot_run_audit.py']
    out = dict(seed=551019, scope='Sufficient unrestricted height and exact mixed constructor; heavy-outcome magnitudes are unrestricted. Operation types remain separate.',
               counts=stats, full_constructions=large, deep_chain=deep_chain, plans_only=plans,
               source_sha256={f: hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/trimmed_height_audit.json').write_text(json.dumps(out, indent=2, default=str)+'\n')
    print('complete', dict(stats), flush=True)


if __name__ == '__main__': main()
