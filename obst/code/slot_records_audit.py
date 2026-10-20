#!/usr/bin/env python3
"""Independent state, traceback, repair and full mixed-OBST controls."""
from collections import Counter
from fractions import Fraction
from itertools import product, combinations
from pathlib import Path
import hashlib, json, random
from aggregate_core_audit import layers
from slot_vector import solve as dense_solve, normalize
from trimmed_height import height_bound, knuth_fallback
from slot_records import solve, nu, select_run, sparse_repair


def check_tree(tree, p, q, h, stats):
    n = len(p); total = 0; order = []; stack = [(tree, 0, n, 0)]
    while stack:
        node, lo, hi, depth = stack.pop()
        if node is None:
            assert lo == hi and depth <= h
            total += q[lo]*depth
            continue
        key, left, right = node
        assert lo <= key < hi and depth < h
        order.append(key); total += p[key]*(depth+1)
        stack.extend(((right, key+1, hi, depth+1), (left, lo, key, depth+1)))
        stats['record_verified_nodes'] += 1
    assert sorted(order) == list(range(n))
    return total


def main():
    root = Path(__file__).resolve().parents[1]
    stats = Counter(); rng = random.Random(561019)
    # Literal perfect-slot subsets check repair without using either optimizer.
    for h in range(1, 4):
        c = 2**h-1
        for mask in range(1, 1 << c):
            slots = [t for t in range(1, c+1) if mask >> (t-1) & 1]
            tree = sparse_repair(slots, h, stats)
            stack = [(tree, 1)]
            while stack:
                node, length = stack.pop()
                if node is None: continue
                key, left, right = node
                assert length <= h-nu(slots[key])
                stack.extend(((left, length+1), (right, length+1)))
                stats['record_repair_depth_controls'] += 1
            check_tree(tree, [1]*len(slots), [1]*(len(slots)+1), h, stats)
            stats['record_repair_subsets'] += 1
    for h in range(1, 6):
        c = 2**h-1
        for a in range(c):
            for b in range(a+1, c+1):
                for m in range(1, b-a+1):
                    actual = select_run(a, b, m, h, stats)
                    ref = sorted(sorted(range(a+1, b), key=lambda t: (-nu(t), t))[:m-1])+[b]
                    assert actual == ref
                    stats['record_selection_controls'] += 1

    # Dense vectors supply *every state*, not merely the optimum value.
    def check(p, q, h, literal=False):
        stages = []
        def observe_dense(k, m, old, new, back, w, g, v, K):
            stages.append((k, m, old, new, w, g, v))
        dense = dense_solve(p, q, h, Counter(), observe_dense)
        def observe_records(k, m, old, new):
            kk, mm, dense_old, dense_new, w, g, v = stages.pop(0)
            assert (k, m) == (kk, mm)
            for b in range(k+m, 2**h):
                value, a = new.lookup(b)
                assert value == dense_new[b]
                if m == 1:
                    candidate = dense_old[a]-w[k]*v[b]-g[k]*min(v[a], v[b])
                else:
                    reward = sum(sorted(v[a+1:b], reverse=True)[:m-1])+v[b]
                    candidate = dense_old[a]-w[k]*reward
                assert candidate == value
                if literal:
                    values = []
                    for prefix in combinations(range(1, b), k+m-1):
                        ss = prefix+(b,)
                        values.append(-sum(w[i]*v[t] for i, t in enumerate(ss))
                                      -sum(g[i]*min(v[ss[i-1]], v[ss[i]]) for i in range(1, len(ss))))
                        stats['record_literal_selections'] += 1
                    assert value == min(values)
                stats['record_prefix_controls'] += 1
            expected = []
            for e in range(h):
                last = None
                for b in range(2**e, 2**h, 2**(e+1)):
                    if b < k+m: continue
                    value = dense_new[b]
                    assert last is None or value <= last
                    if last is None or value < last: expected.append((b, value))
                    last = value
            assert [(a, v) for a, v, pred in new.records] == sorted(expected)
            if all(isinstance(x, int) for x in (*w, *g)):
                assert len(new.records) <= h*(1+(h-1)*(sum(w)+sum(g)))
            stats['record_exact_breakpoint_controls'] += 1
        result = solve(p, q, h, stats, observe_records)
        assert not stages and result['cost'] == dense['cost']
        assert check_tree(result['tree'], p, q, h, stats) == result['cost']
        stats['record_dense_constructor_controls'] += 1
        return result

    for n in range(1, 5):
        for weights in product((0, 1), repeat=2*n+1):
            p = list(weights[:n]); q = list(weights[n:]); H = n.bit_length()+1
            original = list(layers(p, q, H, (H+1)*sum(weights)+1, stats))
            for h in range(n.bit_length(), H+1):
                result = check(p, q, h, h <= 3)
                assert result['cost'] == original[h][0][n]
                stats['record_original_height_controls'] += 1
            stats['record_binary_inputs'] += 1
    print('binary', dict(stats), flush=True)
    for n in (5, 8, 13, 24, 32):
        for trial in range(12):
            if trial == 0: p = [2**i for i in range(n)]; q = [2**(n-i) for i in range(n+1)]
            elif trial < 4:
                p = [rng.randrange(4) for _ in range(3)]
                p = [p[min(2, 3*i//n)] for i in range(n)]
                q = [2]*(n+1); q[n//2] += 7; q[0] = 0; q[-1] = 5
            else:
                p = [Fraction(rng.randrange(7), 3) for _ in range(n)]
                q = [Fraction(rng.randrange(7), 2) for _ in range(n+1)]
            H = n.bit_length()+2
            original = list(layers(p, q, H, (H+1)*(sum(p)+sum(q))+1, stats))
            for h in range(n.bit_length(), H+1):
                result = check(p, q, h)
                assert result['cost'] == original[h][0][n]
                stats['record_original_height_controls'] += 1
            stats['record_mixed_inputs'] += 1
    print('mixed', dict(stats), flush=True)
    large = []
    for n in (64, 192, 512, 1024):
        for kind in ('zero_middle', 'mixed_runs'):
            p = [1 if i < n//3 else 0 if i < 2*n//3 else 2 for i in range(n)]
            q = [0]*(n+1)
            if kind == 'mixed_runs':
                q = [2]*(n+1); q[n//2] += 3; q[n//4] += 1
            w, g, _ = normalize(p, q); h = height_bound(w, g)['height']
            counts = Counter(); result = solve(p, q, h, counts)
            reference, _ = knuth_fallback(p, q, stats)
            assert result['cost'] == reference == check_tree(result['tree'], p, q, h, counts)
            large.append(dict(n=n, height=h, capacity=2**h-1, kind=kind,
                              cost=result['cost'], stage_records=result['stage_records'], counts=counts,
                              verification='Complete output and independent ordinary Knuth optimum'))
            print('large', n, kind, h, sum(result['stage_records']), flush=True)
    # Capacity can be enormous even when the exact full construction is small.
    for h in (16, 32, 64):
        n = 16; p = [1]*n; q = [0]*(n+1); counts = Counter()
        result = solve(p, q, h, counts)
        expected = sum(i.bit_length() for i in range(1, n+1))
        assert result['cost'] == expected == check_tree(result['tree'], p, q, h, counts)
        large.append(dict(n=n, height=h, capacity=2**h-1, kind='enormous_capacity',
                          cost=expected, stage_records=result['stage_records'], counts=counts,
                          verification='Complete output and closed minimum-internal-path-length optimum'))
        print('capacity', h, result['stage_records'], flush=True)
    files = ['slot_records.py', 'slot_records_audit.py', 'slot_vector.py', 'concave_lws.py',
             'mixed_slots.py', 'trimmed_height.py', 'aggregate_core_audit.py']
    out = dict(scope='All prefix records, attaining traceback, sparse repair, height-constrained mixed optima, and certified unrestricted full trees; no timing claims',
               seed=561019, counts=stats, large=large,
               source_sha256={f: hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_records_audit.json').write_text(json.dumps(out, indent=2)+'\n')


if __name__ == '__main__': main()
