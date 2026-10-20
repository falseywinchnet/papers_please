#!/usr/bin/env python3
"""Marked reward spectra and full trees with unbounded exceptional weights."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib, json, random
from slot_records import solve, nu
from slot_vector import normalize
from slot_records_audit import check_tree
from trimmed_height import height_bound, knuth_fallback


def main():
    root = Path(__file__).resolve().parents[1]; stats = Counter(); rng = random.Random(561020)
    for n in range(1, 6):
        for trial in range(12):
            p = [rng.randrange(4) for _ in range(n)]; q = [0]*(n+1)
            # Leave one internal gap zero, so normalization is literal.
            eligible = [('p', i) for i in range(n)]+[('q', i) for i in range(2, n)]
            marks = rng.sample(eligible, min(2, len(eligible)))
            for j, (kind, i) in enumerate(marks):
                value = Fraction(5, 3) if (trial+j)%2 else 2**(64+trial)
                (p if kind == 'p' else q)[i] = value
            V = sum(p[i] for i in range(n) if ('p', i) not in marks)
            assert normalize(p, q) == (p, q, 0)
            h = 3; profiles = set(); values = set()
            for ss in combinations(range(1, 2**h), n):
                rewards = {('p', i): nu(t) for i, t in enumerate(ss)}
                rewards.update({('q', i): min(nu(ss[i-1]), nu(ss[i])) for i in range(1, n)})
                signature = tuple(rewards[x] for x in marks)
                light = sum(p[i]*rewards['p', i] for i in range(n) if ('p', i) not in marks)
                value = light+sum((p if kind == 'p' else q)[i]*rewards[kind, i] for kind, i in marks)
                assert light.denominator == 1 if isinstance(light, Fraction) else isinstance(light, int)
                assert 0 <= light <= (h-1)*V
                profiles.add(signature); values.add(value); stats['marked_literal_selections'] += 1
            assert len(profiles) <= h**len(marks)
            assert len(values) <= h**len(marks)*(1+(h-1)*V)
            result = solve(p, q, h, stats)
            assert result['cost'] == h*(sum(p)+sum(q))-max(values)
            assert max(result['stage_records']) <= h**(len(marks)+1)*(1+(h-1)*V)
            assert check_tree(result['tree'], p, q, h, stats) == result['cost']
            stats['marked_spectrum_inputs'] += 1
    large = []
    for n in (32, 96, 192):
        for bits in (64, 512):
            p = [1 if i < n//3 else 2 if i < 2*n//3 else 3 for i in range(n)]
            q = [0]*(n+1); p[n//3] = 2**(bits+16); q[2*n//3] = 2**bits
            w, g, _ = normalize(p, q); h = height_bound(w, g)['height']; counts = Counter()
            result = solve(p, q, h, counts); ref, _ = knuth_fallback(p, q, stats)
            assert result['cost'] == ref == check_tree(result['tree'], p, q, h, counts)
            V = sum(p)-p[n//3]
            assert max(result['stage_records']) <= h**3*(1+(h-1)*V)
            large.append(dict(n=n, bits=bits, marked=2, light_mass=V, height=h,
                              stage_records=result['stage_records'], cost=result['cost'], counts=counts,
                              verification='Complete unrestricted tree and independent ordinary Knuth optimum'))
            print('marked', n, bits, h, sum(result['stage_records']), flush=True)
    for a, b in zip(large[::2], large[1::2]):
        assert a['height'] == b['height'] and a['stage_records'] == b['stage_records']
    files = ['slot_marked_records_audit.py', 'slot_records.py', 'slot_records_audit.py',
             'slot_vector.py', 'trimmed_height.py', 'concave_lws.py']
    out = dict(scope='Finite reward spectra with rational marked weights; full unrestricted mixed trees with two large integer outcomes. Combinatorial bound proved separately.',
               seed=561020, counts=stats, large=large,
               source_sha256={f: hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/slot_marked_records_audit.json').write_text(json.dumps(out, indent=2)+'\n')


if __name__ == '__main__': main()
