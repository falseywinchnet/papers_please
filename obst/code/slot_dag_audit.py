#!/usr/bin/env python3
"""Independent dense-prefix, all-root, and complete-tree DAG controls."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib, json, random
from slot_dag import Diagram, solve
from slot_vector import normalize
from slot_records_audit import check_tree
from aggregate_core_audit import layers
from trimmed_height import knuth_fallback


def main():
    root = Path(__file__).resolve().parents[1]
    stats = Counter(); rng = random.Random(581019)

    def check(p, q, h, full_reference=True):
        w, g, _ = normalize(p, q); c = 2**h
        v = [0]+[(b & -b).bit_length()-1 for b in range(1, c)]
        old = [None]*c; old[0] = 0
        def observer(k, manager, ref):
            nonlocal old
            new = [None]*c
            for b in range(k, c):
                choices = []
                for a in range(b):
                    if old[a] is not None:
                        choices.append(old[a]-w[k-1]*v[b]-g[k-1]*min(v[a], v[b]))
                        stats['dag_direct_predecessor_candidates'] += 1
                new[b] = min(choices)
            for b in range(c):
                assert manager.value(ref, b) == new[b], (p,q,h,k,b)
                stats['dag_dense_prefix_controls'] += 1
            old = new
        result = solve(p, q, h, stats, observer)
        assert check_tree(result['tree'], p, q, h, stats) == result['cost']
        if full_reference:
            expected = list(layers(p, q, h, (h+1)*(sum(p)+sum(q))+1, stats))[-1][0][len(p)]
            assert result['cost'] == expected
            stats['dag_all_root_controls'] += 1
        stats['dag_full_small_trees'] += 1

    # No representation size assumptions enter these exhaustive controls.
    for n in range(1, 5):
        for values in product((0, 1), repeat=2*n+1):
            for h in range(n.bit_length(), n.bit_length()+2):
                check(list(values[:n]), list(values[n:]), h)
            stats['dag_binary_inputs'] += 1
    print('binary', dict(stats), flush=True)
    for n in (5, 8, 13, 24):
        for trial in range(8):
            p = [Fraction(rng.randrange(13), 3) for _ in range(n)]
            q = [Fraction(rng.randrange(13), 2) for _ in range(n+1)]
            if trial < 2:
                p = [(n+1)**(n-i)-1 for i in range(n)]
                q = [1]*(n+1)
                if trial: p.reverse()
            check(p, q, n.bit_length()+1)
    print('mixed', dict(stats), flush=True)
    large = []
    for n in (8, 16, 24, 32, 48):
        a = n+1; p = [a**(n-i)-1 for i in range(n)]; q = [1]*(n+1)
        counts = Counter(); result = solve(p, q, n, counts)
        expected = n+sum((i+1)*a**(n-i) for i in range(n))
        assert result['cost'] == expected == check_tree(result['tree'], p, q, n, counts)
        knuth, _ = knuth_fallback(p, q, stats); assert knuth == expected
        large.append(dict(n=n, height=n, family='geometric_chain',
                          final_explicit_records=2**n-n,
                          stage_nodes=result['stage_nodes'], counts=counts,
                          verification='Full arbitrary-weight DAG solver, closed unique-chain optimum, independent Knuth and complete tree'))
        print('geometric', n, result['stage_nodes'][-1], counts['dag_all_nodes'], flush=True)
    files = ['slot_dag.py','slot_dag_audit.py','slot_vector.py','slot_records.py',
             'slot_records_audit.py','aggregate_core_audit.py','trimmed_height.py']
    out = dict(scope='Exact implicit mixed-weight prefix recurrence and full trees; measured DAG sizes do not establish a universal bound',
               seed=581019, counts=stats, large=large,
               source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_dag_audit.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__ == '__main__': main()
