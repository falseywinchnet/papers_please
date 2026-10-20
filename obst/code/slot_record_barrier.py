#!/usr/bin/env python3
"""Exact binomial record witnesses on strictly positive mixed-weight inputs.

Dense subsequence recurrence and literal controls precede compressed-kernel
comparisons. Large binomial rows are formula evaluations, not enumerations.
"""
from collections import Counter
from itertools import combinations
from fractions import Fraction
from math import comb
from pathlib import Path
import hashlib, json, random
from research import shapes, label, cost
from slot_records import Records, gap_pass, solve as record_solve
from slot_records_audit import check_tree
from slot_vector import normalize, solve as dense_mixed_solve
from trimmed_height import height_bound, knuth_fallback
from affine_period_obst import solve as affine_solve
from periodic_obst_audit import tree_check


def family(n):
    base = n+1
    w = [base**(n-i) for i in range(n)]
    return [x-1 for x in w], [1]*(n+1), w


def dense_prefixes(w, h, stats):
    """Direct zero-gap subsequence recurrence, keeping every ending slot."""
    c = 2**h-1
    valuations = [0]+[(x & -x).bit_length()-1 for x in range(1, c+1)]
    old = [None]*(c+1); old[0] = 0
    for k, weight in enumerate(w, 1):
        new = [None]*(c+1); best = None
        for b in range(k, c+1):
            a = b-1
            if old[a] is not None and (best is None or old[a] > best): best = old[a]
            assert best is not None
            new[b] = best+weight*valuations[b]
            stats['barrier_dense_candidates'] += 1
        last = [None]*h; records = []
        for b in range(k, c+1):
            d = valuations[b]
            assert last[d] is None or new[b] >= last[d]
            if last[d] is None or new[b] > last[d]: records.append((b, -new[b]))
            last[d] = new[b]
            stats['barrier_dense_record_scans'] += 1
        yield k, new, records, valuations
        old = new


def literal(w, k, c, valuations, stats):
    result = [None]*(c+1)
    for ss in combinations(range(1, c+1), k):
        value = sum(w[i]*valuations[t] for i, t in enumerate(ss))
        b = ss[-1]
        if result[b] is None or value > result[b]: result[b] = value
        stats['barrier_literal_selections'] += 1
    return result


def main():
    root = Path(__file__).resolve().parents[1]; stats = Counter(); rows = []
    # Structural envelope: earliest embeddings preserve *every* valuation.
    for h in range(1, 5):
        c = 2**h-1
        for mask in range(1, 1 << c):
            slots = [b for b in range(1, c+1) if mask >> (b-1) & 1]
            a = 0
            for k, b in enumerate(slots, 1):
                d = (b & -b).bit_length()-1; base = 2**d; step = 2*base
                a = base+step*max(0, (a-base)//step+1)
                assert a <= b and (a & -a).bit_length()-1 == d
                assert bin(a).count('1') <= k
                stats['barrier_earliest_embedding_slots'] += 1
            stats['barrier_earliest_embedding_subsets'] += 1
    rng = random.Random(571019)
    for n in (2, 3, 5, 8, 12, 16):
        for trial in range(12):
            p = [Fraction(rng.randrange(9), 3) for _ in range(n)]
            q = [Fraction(rng.randrange(9), 2) for _ in range(n+1)]
            if trial % 3 == 0: p[rng.randrange(n)] += 2**(n+16)
            h = n.bit_length()+1; expected = []
            def dense_observer(k, m, old, new, back, w, g, v, penalty):
                expected.append((k+m, new))
            dense = dense_mixed_solve(p, q, h, Counter(), dense_observer)
            def record_observer(k, m, old, new):
                end, values = expected.pop(0); assert end == k+m
                assert len(new.records) <= sum(comb(h, j) for j in range(min(end, h)+1))-end
                for b, value, pred in new.records:
                    assert bin(b).count('1') <= end
                    stats['barrier_mixed_envelope_records'] += 1
                for b in range(end, 2**h):
                    assert new.lookup(b)[0] == values[b]
                    stats['barrier_mixed_prefix_controls'] += 1
            result = record_solve(p, q, h, stats, record_observer)
            assert not expected and result['cost'] == dense['cost']
            assert check_tree(result['tree'], p, q, h, stats) == result['cost']
            stats['barrier_mixed_envelope_inputs'] += 1
    # Sharpness for independently varied height and key count, including k>h.
    for h in range(1, 7):
        c = 2**h-1
        for n in range(1, c+1):
            w = [(h+1)**(n-i) for i in range(n)]
            for k, dense, records, valuations in dense_prefixes(w, h, stats):
                assert [b for b, value in records] == [b for b in range(k, c+1) if bin(b).count('1') <= k]
                assert len(records) == sum(comb(h, j) for j in range(min(k, h)+1))-k
                stats['barrier_arbitrary_height_stage_controls'] += 1
    # Literal full shapes establish uniqueness separately from the slot model.
    for n in range(1, 9):
        p, q, w = family(n); reference = sum((i+1)*x for i, x in enumerate(w))+n
        values = [cost(label(shape)[0], p, q) for shape in shapes(n)]
        assert min(values) == reference and values.count(reference) == 1
        stats['barrier_literal_shapes'] += len(values)
        stats['barrier_unique_shape_inputs'] += 1
    for n in range(2, 17):
        p, q, w = family(n); h = n; counts = Counter()
        assert normalize(p, q) == (w, [0]*(n+1), n)
        assert height_bound(w, [0]*(n+1))['height'] == n
        # The dominance inequality applies in every suffix, using the same N.
        for i, x in enumerate(w):
            assert x > n*sum(w[i+1:])
            counts['barrier_dominant_suffixes'] += 1
        popcount = [0]*(2**h)
        for b in range(1, 2**h): popcount[b] = popcount[b//2]+b%2
        old = Records([(0, 0, -1)], h); stage_counts = []; odd_counts = []
        for k, dense, expected_records, valuations in dense_prefixes(w, h, counts):
            actual = gap_pass(old, w[k-1], 0, h, counts)
            assert [(a, value) for a, value, pred in actual.records] == expected_records
            counts['barrier_exact_stage_sets'] += 1
            for b in range(k, 2**h):
                value, a = actual.lookup(b)
                assert value == -dense[b]
                if k == 1: assert a == 0
                else:
                    old_value, _ = old.lookup(a)
                    assert value == old_value-w[k-1]*valuations[b]
                counts['barrier_prefix_controls'] += 1
            if n <= 5: assert literal(w, k, 2**h-1, valuations, counts) == dense
            positions = {a for a, value, pred in actual.records}
            assert len(positions) == sum(comb(h, j) for j in range(k+1))-k
            running = None
            for b in range(k, 2**h):
                assert (b in positions) == (popcount[b] <= k)
                changed = running is None or dense[b] > running
                assert changed == (popcount[b] <= k)
                if changed: running = dense[b]
                counts['barrier_popcount_support_controls'] += 1
                counts['barrier_prefix_max_jump_controls'] += 1
            if k >= 2:
                m = k-1; witnesses = 0
                for ds in combinations(range(1, h), m):
                    ds = sorted(ds, reverse=True); b = 1+sum(2**d for d in ds)
                    expected = sum(w[i]*d for i, d in enumerate(ds))
                    assert b in positions and dense[b] == expected
                    if b-2 >= k: assert dense[b-2] < expected
                    counts['barrier_binomial_witnesses'] += 1; witnesses += 1
                assert witnesses == comb(h-1, m)
            stage_counts.append(len(actual.records))
            odd_counts.append(sum(a%2 for a, value, pred in actual.records))
            old = actual
        k = (n-1)//2+1
        assert odd_counts[k-1] >= comb(n-1, k-1)
        assert stage_counts[-1] == 2**n-n
        rows.append(dict(n=n, height=h, prefix=k, binomial_lower=comb(n-1, k-1),
                         stage_records=stage_counts, odd_records=odd_counts, counts=counts,
                         verification='Every dense prefix value, every compressed record set and every subset witness; literal subsequences for n<=5'))
        if n <= 10:
            result = record_solve(p, q, h, stats)
            expected = sum((i+1)*x for i, x in enumerate(w))+n
            assert result['cost'] == expected == check_tree(result['tree'], p, q, h, stats)
            node = result['tree']
            for i in range(n): assert node[0] == i and node[1] is None; node = node[2]
            assert node is None
            stats['barrier_full_record_trees'] += 1
        print('records', n, k, rows[-1]['binomial_lower'], stage_counts[k-1], flush=True)
    # Other magnitude orders are diagnostics; no upper bound is inferred.
    rng = random.Random(571020); diagnostics = []
    for n in (8, 10, 12):
        _, _, weights = family(n)
        for trial in range(10):
            w = sorted(weights) if trial == 0 else weights[:]
            if trial > 1: rng.shuffle(w)
            counts = Counter(); sizes = []
            for k, dense, records, vals in dense_prefixes(w, n, counts): sizes.append(len(records))
            diagnostics.append(dict(n=n, trial=trial, exponent_order=[weights.index(x) for x in w],
                                    stage_records=sizes, counts=counts))
    # Full existing affine constructor on the same difficult record family.
    # This explicitly distinguishes a representation barrier from OBST hardness.
    full = []
    for n in (16, 32, 64, 128, 256, 1024):
        p, q, w = family(n); counts = Counter()
        value, tree, solver = affine_solve(p, q, counts)
        base = n+1
        numerator = base*(base**(n+1)-(n+1)*base+n)
        assert numerator % (base-1)**2 == 0
        expected = numerator//(base-1)**2+n
        assert value == expected == tree_check(tree, p, q, counts)
        assert tree['key_depth'] == list(range(1, n+1)) and solver.b == 1
        assert counts['affine_phase_candidates'] == 2*n-1
        if n <= 256:
            reference, _ = knuth_fallback(p, q, counts); assert reference == value
        assert height_bound(w, [0]*(n+1))['height'] == n
        full.append(dict(n=n, cost=int(value), max_weight_bits=max(p).bit_length(), counts=counts,
                         verification='Full prior affine constructor and closed unique-chain optimum; independent Knuth only for n<=256'))
        print('affine', n, counts['affine_phase_candidates'], flush=True)
    formula_rows = [dict(n=n, prefix=(n-1)//2+1,
                         record_lower_bound=comb(n-1, (n-1)//2),
                         exact_middle_records=sum(comb(n, j) for j in range((n-1)//2+2))-((n-1)//2+1),
                         exact_final_records=2**n-n,
                         verification='Exact binomial formulas only; no prefix-vector enumeration')
                    for n in (32, 64, 128, 256, 1024)]
    files = ['slot_record_barrier.py', 'slot_records.py', 'slot_vector.py', 'slot_records_audit.py',
             'trimmed_height.py', 'affine_period_obst.py', 'periodic_obst_audit.py', 'research.py']
    out = dict(scope='Sharp universal binary envelope for arbitrary mixed prefix records, attained exponentially at necessary optimal height on strictly positive mixed weights; not an OBST lower bound',
               seed=571019, magnitude_order_seed=571020, counts=stats, exact_prefix_rows=rows, magnitude_order_diagnostics=diagnostics,
               full_affine_controls=full, binomial_formula_only=formula_rows,
               source_sha256={f: hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_record_barrier.json').write_text(json.dumps(out, indent=2)+'\n')


if __name__ == '__main__': main()
