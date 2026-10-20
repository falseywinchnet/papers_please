#!/usr/bin/env python3
"""Exact mixed-weight OBST contraction research; see CONTRACTION.md."""
import argparse
from collections import deque
import itertools
import json
from pathlib import Path
import random
import sys

from research import check_weights, cost, cubic, knuth
from sparse import FAMILIES, weights


def reduce_instance(p, q):
    check_weights(p, q)
    n = len(p)
    prev = [i - 1 for i in range(n)]
    nxt = [i + 1 for i in range(n)]
    alive = [True] * n
    gap = list(q)
    payload = [None] * (n + 1)
    todo = deque(range(n))
    offset = checks = pops = contractions = 0
    while todo:
        k = todo.popleft()
        pops += 1
        if not alive[k]:
            continue
        a, b = prev[k], nxt[k]
        checks += 1
        if a == -1 and b == n:
            safe = True
        elif a == -1:
            safe = p[b] >= p[k] + gap[k]
        elif b == n:
            safe = p[a] >= p[k] + gap[b]
        else:
            threshold = 2 * p[k] + gap[k] + gap[b]
            safe = min(p[a], p[b]) >= threshold
        if not safe:
            continue
        s = p[k] + gap[k] + gap[b]
        offset += s
        contractions += 1
        payload[b] = (k, payload[k], payload[b])
        gap[b] = s
        alive[k] = False
        if a != -1:
            nxt[a] = b
            todo.append(a)
        if b != n:
            prev[b] = a
            todo.append(b)
    keys = [k for k in range(n) if alive[k]]
    leaves = keys + [n]
    return ([p[k] for k in keys], [gap[k] for k in leaves],
            keys, [payload[k] for k in leaves], offset,
            dict(input_keys=n, core_keys=len(keys), contractions=contractions,
                 predicate_checks=checks, queue_pops=pops))


def solve(p, q):
    cp, cq, keys, leaves, offset, counts = reduce_instance(p, q)
    value, core, candidates = knuth(cp, cq)

    def expand(t, lo=0):
        if t is None:
            return leaves[lo]
        r, left, right = t
        return keys[r], expand(left, lo), expand(right, r + 1)

    m = len(cp)
    counts.update(dp_states=m*(m+1)//2, root_candidates=candidates)
    return value + offset, expand(core), counts


def verify():
    checked = 0
    for n in range(5):
        for weights in itertools.product(range(3), repeat=2*n+1):
            p, q = weights[:n], weights[n:]
            value, tree, counts = solve(p, q)
            ref, _ = cubic(p, q)
            assert value == ref == cost(tree, p, q), (p, q, value, ref)
            assert counts['queue_pops'] <= 3*n
            checked += 1
    rng = random.Random(0xC017AC7)
    random_count = 0
    for n in range(1, 21):
        for trial in range(300):
            if trial % 3 == 0:
                p = [1 << rng.randrange(20) for _ in range(n)]
                q = [1 << rng.randrange(20) for _ in range(n+1)]
            elif trial % 3 == 1:
                p = [rng.randrange(100) for _ in range(n)]
                q = [rng.randrange(100) for _ in range(n+1)]
            else:
                p = [rng.randrange(100) for _ in range(n)]
                q = [rng.randrange(3) for _ in range(n+1)]
            value, tree, counts = solve(p, q)
            ref, _ = cubic(p, q)
            assert value == ref == cost(tree, p, q), (p, q, value, ref)
            assert counts['queue_pops'] <= 3*n
            random_count += 1
    return dict(exhaustive=checked, random=random_count)


def survey(max_n):
    rng = random.Random(0xC017AC8)
    rows = []
    for n in (16, 32, 64, 128, 256, 512):
        if n > max_n:
            break
        inputs = [(name, *weights(n, name, rng)) for name in FAMILIES]
        inputs += [('geometric4', [4**i for i in range(n)],
                    [4**i for i in range(n+1)]),
                   ('keys_heavy', [rng.randrange(1000) for _ in range(n)],
                    [rng.randrange(10) for _ in range(n+1)])]
        for name, p, q in inputs:
            value, tree, counts = solve(p, q)
            ref, _, candidates = knuth(p, q)
            assert value == ref == cost(tree, p, q), (name, n)
            rows.append(dict(family=name, n=n, cost=value, **counts,
                             baseline_states=n*(n+1)//2,
                             baseline_candidates=candidates))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-n', type=int, default=512)
    args = parser.parse_args()
    sys.setrecursionlimit(10000)
    result = dict(verification=verify(), survey=survey(args.max_n))
    path = Path(__file__).resolve().parents[1] / 'results' / 'contraction.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result['verification']))
    print(path)


if __name__ == '__main__':
    main()
