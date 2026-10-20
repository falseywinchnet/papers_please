#!/usr/bin/env python3
"""All-interval sufficient-height check using original all-root optima."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib, json, random
from trimmed_height import height_bound
from slot_vector import normalize


def check(p, q, counts):
    n = len(p)
    bound = height_bound(p, q)['height']
    C = [[0]*(n+1) for _ in range(n+1)]
    H = [[0]*(n+1) for _ in range(n+1)]
    for size in range(1, n+1):
        for i in range(n-size+1):
            j = i+size
            value, h = min((C[i][r]+C[r+1][j], 1+max(H[i][r], H[r+1][j]))
                           for r in range(i, j))
            C[i][j] = value+sum(p[i:j])+sum(q[i:j+1])
            H[i][j] = h
            assert h <= min(size, bound)
            counts['interval_height_controls'] += 1
            counts['interval_all_root_candidates'] += size
    counts['interval_inputs'] += 1


def main():
    root = Path(__file__).resolve().parents[1]
    counts = Counter(); rng = random.Random(551020)
    for n in range(1, 5):
        for ww in product((0, 1), repeat=2*n+1):
            p, q = list(ww[:n]), list(ww[n:])
            check(p, q, counts)
            w, g, _ = normalize(p, q); check(w, g, counts)
    for n in (8, 16, 32, 64):
        for trial in range(24):
            p = [rng.choice((0, 0, 1, 2, 7, 2**80)) for _ in range(n)]
            q = [rng.choice((0, 0, 1, 2, 7, 2**120)) for _ in range(n+1)]
            if trial % 3 == 0:
                p = [Fraction(x, 3) for x in p]
                q = [Fraction(x, 3) for x in q]
            check(p, q, counts)
            w, g, _ = normalize(p, q); check(w, g, counts)
    files = ['trimmed_interval_audit.py', 'trimmed_height.py', 'slot_vector.py']
    out = dict(seed=551020, counts=counts,
               scope='Every original and globally normalized interval has an optimum within the single globally selected height; independent all-root recurrence minimizes height among tied optimal costs.',
               source_sha256={f: hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
    (root/'results/trimmed_interval_audit.json').write_text(json.dumps(out, indent=2)+'\n')
    print(dict(counts), flush=True)


if __name__ == '__main__': main()
