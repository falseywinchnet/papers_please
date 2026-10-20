#!/usr/bin/env python3
"""Three-entry witnesses for cubic actual-prefix and quartic history size.

Exact counts only. Dense subsequence controls precede implicit full trees.
The mathematical lower bounds do not depend on this finite audit.
"""
from collections import Counter
from math import comb
from pathlib import Path
import hashlib
import json

from slot_punctured import solve
from slot_record_barrier import dense_prefixes
from slot_records_audit import check_tree
from slot_vector import normalize
from trimmed_height import knuth_fallback


def family(n):
    a = 4*n+1
    w = [a**(n-i) for i in range(n)]
    return [x-1 for x in w], [1]*(n+1), w


def greedy(k, b):
    """Valuations of the greedy k-1 predecessors, then the forced slot b."""
    assert b >= k
    out = []
    previous = 0
    for i in range(k-1):
        lo, hi = previous+1, b-(k-1-i)
        d = ((lo-1)^hi).bit_length()-1
        previous = (hi >> d) << d
        assert lo <= previous <= hi and previous & -previous == 1 << d
        out.append(d)
    return out+[(b & -b).bit_length()-1]


def parameters(n):
    q = 2*((n+1)//2)
    d0 = q.bit_length()+2
    return q, d0, max(0, n-d0)


def witnesses(n, k):
    q, d0, _ = parameters(n)
    for d in range(d0, n):
        for s in range(d, n):
            for r in range(1, min(n-s, k-3)+1):
                b = ((1 << (r-1))-1) << (n-r+1)
                b += 1 << s
                yield d, s, r, b, (1, (1 << (d-2))+q, (1 << (d-1))+q)


def lower(n, k):
    _, _, nn = parameters(n)
    return sum((nn-t+1)*min(t, max(0, k-3)) for t in range(1, nn+1))


def history_lower(n):
    _, _, nn = parameters(n)
    return (n-2)*comb(nn+2, 3)-comb(nn+3, 4) if nn else 0


def block_ref(manager, root, boundary, depth):
    ref = root
    for d in range(manager.h-1, depth-1, -1):
        left, _, right = manager.children(ref)
        ref = right if boundary >> d & 1 else left
    return ref


def main():
    root = Path(__file__).resolve().parents[1]
    counts = Counter()
    # Independent dense recurrence checks every greedy reward, including
    # pre-boundary choices, before any use of the compressed constructor.
    for n in range(2, 13):
        p, q, w = family(n)
        for k, dense, _, _ in dense_prefixes(w, n, counts):
            for b in range(k, 1 << n):
                assert sum(x*y for x, y in zip(w, greedy(k, b))) == dense[b]
                counts['dense_greedy_entries'] += 1
    rows = []
    for n in (12, 13, 16, 17, 24, 25, 32, 48):
        p, q, w = family(n)
        assert normalize(p, q) == (w, [0]*(n+1), n)
        for i in range(n):
            assert w[i] > n*sum(w[i+1:])
            counts['strict_suffix_certificates'] += 1
        stats = Counter()
        global_ids = set()
        signatures = set()
        stages = []

        def observe(k, manager, ref):
            ids = set()
            for d, s, r, b, positions in witnesses(n, k):
                vectors = [greedy(k, b+t) for t in positions]
                diff = [y-x for x, y in zip(vectors[1], vectors[2])]
                assert next(i for i, x in enumerate(diff) if x) == r
                assert diff[r] == 1
                assert vectors[0][r]-vectors[1][r] == s-d
                small = [x-y for x, y in zip(vectors[0], vectors[1])]
                assert small[-1] == -((parameters(n)[0] & -parameters(n)[0]).bit_length()-1) < 0
                values = [-sum(x*y for x, y in zip(w, v)) for v in vectors]
                node = block_ref(manager, ref, b, d)
                assert node is not None and manager.nodes[node[1]][0] == d
                for t, value in zip(positions, values):
                    assert manager.value(ref, b+t) == value
                    stats['witness_entry_checks'] += 1
                signature = d, values[2]-values[1], values[0]-values[1]
                assert signature not in signatures
                signatures.add(signature)
                assert node[1] not in global_ids
                global_ids.add(node[1]); ids.add(node[1])
                stats['distinct_witness_nodes'] += 1
            assert len(ids) == lower(n, k)
            actual = manager.reachable([ref])
            assert actual >= len(ids)
            stages.append(dict(k=k, nodes=actual, lower_bound=len(ids)))

        answer = solve(p, q, n, stats, observe)
        expected = n+sum((i+1)*x for i, x in enumerate(w))
        reference, _ = knuth_fallback(p, q, stats)
        assert answer['cost'] == expected == reference == check_tree(answer['tree'], p, q, n, stats)
        tree = answer['tree']
        for i in range(n):
            assert tree[0] == i and tree[1] is None
            tree = tree[2]
        assert tree is None
        assert len(global_ids) == history_lower(n) == sum(lower(n, k) for k in range(1, n+1))
        assert stats['punctured_history_nodes'] >= len(global_ids)
        assert lower(n, n) == comb(parameters(n)[2]+2, 3)
        rows.append(dict(n=n, height=n, base=4*n+1, d0=parameters(n)[1],
                         final_lower=lower(n, n), history_lower=history_lower(n),
                         stages=stages, counts=stats))
        print(n, stages[-1]['nodes'], lower(n, n), stats['punctured_history_nodes'], history_lower(n), flush=True)
    formula_rows = [dict(n=n, d0=parameters(n)[1], final_lower=lower(n,n), history_lower=history_lower(n))
                    for n in (64, 128, 256, 512, 1024, 4096)]
    files = ['slot_punctured_barrier.py', 'slot_punctured.py', 'slot_record_barrier.py',
             'slot_records.py', 'slot_records_audit.py', 'slot_vector.py', 'trimmed_height.py']
    result = dict(scope='Exact actual-prefix and shared-history witnesses on a positive mixed family; representation lower bounds, not a full OBST lower bound',
                  dense_counts=counts, rows=rows, formula_only_rows=formula_rows,
                  source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_punctured_barrier.json').write_text(json.dumps(result, indent=2)+'\n')


if __name__ == '__main__':
    main()
