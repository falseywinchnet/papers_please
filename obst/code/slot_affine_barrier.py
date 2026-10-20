#!/usr/bin/env python3
"""Actual-prefix witnesses distinct even under positive affine rescaling."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib
import json

from slot_punctured import solve
from slot_punctured_barrier import greedy, witnesses, parameters, lower, history_lower
from slot_record_barrier import dense_prefixes
from slot_records_audit import check_tree
from trimmed_height import knuth_fallback


def family(n):
    base = 16*n*n+1
    exponents = [t+2*n*t*t for t in range(n, 0, -1)]
    w = [base**e for e in exponents]
    return [v-1 for v in w], [1]*(n+1), w, exponents


def main():
    root = Path(__file__).resolve().parents[1]
    counts = Counter()
    for n in (2, 3, 8, 16, 32, 64, 128, 256):
        exponents = [t+2*n*t*t for t in range(1, n+1)]
        seen = set()
        for i in range(n):
            for j in range(i, n):
                exponent = exponents[i]+exponents[j]
                assert exponent not in seen
                seen.add(exponent)
                counts['distinct_quadratic_monomials'] += 1
        assert 4*(n-1)**2 < 16*n*n
    for n in range(2, 11):
        _, _, w, _ = family(n)
        for k, dense, _, _ in dense_prefixes(w, n, counts):
            for b in range(k, 1 << n):
                assert sum(x*y for x,y in zip(w,greedy(k,b))) == dense[b]
                counts['dense_greedy_entries'] += 1
    rows = []
    for n in (8, 12, 13, 16, 17):
        p, q, w, exponents = family(n)
        for i in range(n):
            assert w[i] > n*sum(w[i+1:])
            counts['strict_suffix_certificates'] += 1
        stats = Counter(); signatures = set(); stages = []
        def observe(k, manager, ref):
            local = set()
            for d,s,r,b,positions in witnesses(n,k):
                vectors = [greedy(k,b+t) for t in positions]
                u = [y-x for x,y in zip(vectors[1],vectors[2])]
                v = [x-y for x,y in zip(vectors[0],vectors[1])]
                assert next(i for i,x in enumerate(u) if x) == r and u[r] == 1
                assert v[r] == s-d and u[-1] == 0 and v[-1] != 0
                values = [-sum(x*y for x,y in zip(w,z)) for z in vectors]
                for t,value in zip(positions,values):
                    assert manager.value(ref,b+t) == value
                    stats['witness_entry_checks'] += 1
                denominator = values[2]-values[1]
                assert denominator < 0
                signature = d,Fraction(values[0]-values[1],denominator)
                assert signature not in signatures
                signatures.add(signature);local.add(signature)
                # Exact invariance under several nontrivial affine maps.
                for scale,offset in ((Fraction(3,7),Fraction(-5,2)),(17,31)):
                    transformed = [scale*x+offset for x in values]
                    assert Fraction(transformed[0]-transformed[1],transformed[2]-transformed[1]) == signature[1]
                    stats['affine_invariance_checks'] += 1
                stats['distinct_affine_witnesses'] += 1
            assert len(local) == lower(n,k)
            stages.append(dict(k=k,affine_lower=len(local),additive_nodes=manager.reachable([ref])))
        answer = solve(p,q,n,stats,observe)
        expected = n+sum((i+1)*x for i,x in enumerate(w))
        reference,_ = knuth_fallback(p,q,stats)
        assert answer['cost'] == expected == reference == check_tree(answer['tree'],p,q,n,stats)
        assert len(signatures) == history_lower(n)
        rows.append(dict(n=n,base=16*n*n+1,exponents=exponents,
                         largest_weight_bits=w[0].bit_length(),
                         total_weight_bits=sum(x.bit_length() for x in w),
                         final_lower=lower(n,n),history_lower=history_lower(n),
                         stages=stages,counts=stats))
        print(n,w[0].bit_length(),lower(n,n),history_lower(n),flush=True)
    files = ['slot_affine_barrier.py','slot_punctured_barrier.py','slot_punctured.py',
             'slot_record_barrier.py','slot_records.py','slot_records_audit.py',
             'slot_vector.py','trimmed_height.py']
    result = dict(scope='Distinct three-entry affine invariants in actual mixed prefixes; no full affine-diagram solver or OBST lower bound claimed',
                  checks=counts,rows=rows,
                  source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_affine_barrier.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__ == '__main__':main()
