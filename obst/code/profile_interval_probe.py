#!/usr/bin/env python3
"""Independent reachability audit for a two-level key profile; no OBST solver.

A high key must be retained. A low key can be retained only at odd skeleton
rank. Removed keys cannot be adjacent. Exact bit sets merge equivalent
prefix histories; literal word enumeration independently checks short cases.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


def step(state, high, even):
    removed, retained = state
    if high:
        return 0, (removed | retained) << 1
    return retained, ((removed | retained) & even) << 1


def literal(pattern):
    result = [0, 0]
    for word in itertools.product((0, 1), repeat=len(pattern)):
        rank = 0
        previous = 1
        for high, keep in zip(pattern, word):
            if not keep:
                if high or not previous:
                    break
            else:
                rank += 1
                if not high and rank % 2 == 0:
                    break
            previous = keep
        else:
            result[previous] |= 1 << rank
    return tuple(result)


def indices(bits, parity, n):
    return [r // 2 for r in range(parity, n + 1, 2) if (bits >> r) & 1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-n', type=int, default=40)
    parser.add_argument('--literal-n', type=int, default=9)
    args = parser.parse_args()
    checks = Counter()
    for n in range(args.literal_n + 1):
        even = sum(1 << r for r in range(0, n + 2, 2))
        for pattern in itertools.product((0, 1), repeat=n):
            state = (0, 1)
            for high in pattern:
                state = step(state, high, even)
            assert state == literal(pattern), (pattern, state)
            checks['literal_pattern_checks'] += 1
    # Independent real-tree check of the proposed profile connection.
    from check_ramp_complete import enumerate_class
    from research import cost
    for n in range(1, args.literal_n + 1):
        h = (n + 1).bit_length() - 1
        S = 1 << h
        m = S - 1
        s = n - m
        trees = [tree for _, tree in enumerate_class(n)]
        q = [3 if i % 2 == 0 else 11 for i in range(n + 1)]
        for pattern in itertools.product((0, 1), repeat=n):
            if not S // 2 - 1 <= sum(pattern) <= m:
                continue
            p = [17 if high else 2 for high in pattern]
            lower = sum(v * (i + 1).bit_length() for i, v in enumerate(sorted(p, reverse=True)))
            lower += h * sum(q) + 14 * s
            actual = min(cost(tree, p, q) for tree in trees)
            state = literal(pattern)
            attainable = bool(((state[0] | state[1]) >> m) & 1)
            assert (actual == lower) == attainable, (pattern, actual, lower)
            assert actual >= lower
            checks['independent_tree_profile_checks'] += 1
            checks['profile_attained' if attainable else 'profile_unattained'] += 1
    # Each exact state stores the number of binary prefixes yielding it.
    # Dead prefixes stay dead; no pattern is silently dropped.
    states = {(0, 1): 1}
    rows = []
    hole = None
    for n in range(1, args.max_n + 1):
        even = sum(1 << r for r in range(0, n + 2, 2))
        following = Counter()
        for state, multiplicity in states.items():
            for high in (0, 1):
                observed = step(state, high, even)
                following[observed] += multiplicity
                checks['distinct_state_transitions'] += 1
                for bits in observed:
                    for parity in (0, 1):
                        values = indices(bits, parity, n)
                        assert not values or values == list(range(values[0], values[-1] + 1))
                        checks['parity_interval_checks'] += 1
                if high and observed != (0, 0):
                    a = indices(observed[1], 0, n)
                    b = indices(observed[1], 1, n)
                    if a and b:
                        assert a[0] - b[0] in (0, 1)
                        assert a[-1] - b[-1] in (0, 1)
                        checks['interlaced_endpoint_checks'] += 1
        assert sum(following.values()) == 1 << n
        states = following
        rows.append(dict(n=n, distinct_states=len(states), live_states=len(states) - ((0, 0) in states),
                         represented_patterns=sum(states.values()), dead_patterns=states.get((0, 0), 0)))
    pattern = (0, 1, 0, 1, 0, 0)
    result = literal(pattern)
    ranks = [r for r in range(len(pattern) + 1) if ((result[0] | result[1]) >> r) & 1]
    assert ranks == [3, 5]
    report = dict(scope='Reachability only: no full OBST constructor, certificate, or speed claim',
                  checks=dict(checks), rows=rows,
                  ordinary_interval_counterexample=dict(high_key_pattern=pattern, reachable_ranks=ranks),
                  source_sha256={name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in (Path(__file__).name, 'check_ramp_complete.py', 'research.py')})
    destination = Path(__file__).resolve().parents[1] / 'results' / 'profile_interval_probe.json'
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(checks=checks, final=rows[-1], counterexample=ranks), indent=2))


if __name__ == '__main__':
    main()
