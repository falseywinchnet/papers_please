#!/usr/bin/env python3
"""Independent checks of ordering in full-OBST depth representations.

The all-interval unique-minimum condition is reverse vertex ranking on a
path. This harness checks its conjunction with level flow against actual
binary-tree shapes, and supplies an arbitrary-window obstruction with
strictly positive weights. No fast exact optimizer is claimed.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from research import cost, cubic, knuth, label, shapes


def gap_lengths(ls):
    return (ls[0],) + tuple(max(a, b) for a, b in zip(ls, ls[1:])) + (ls[-1],)


def flow(ls):
    k, g = Counter(ls), Counter(gap_lengths(ls))
    return [k[1]-1] + [g[d]+k[d+1]-2*k[d] for d in range(1, max(ls)+1)]


def ranked(ls, window=None):
    """Independent interval scan; window is number of keys, not edges."""
    n = len(ls)
    for i in range(n):
        best, count = n+1, 0
        for j in range(i, min(n, i+(n if window is None else window))):
            if ls[j] < best:
                best, count = ls[j], 1
            elif ls[j] == best:
                count += 1
            if count > 1:
                return False
    return True


def stack_ranked(ls):
    """Linear reverse-ranking recognizer, independent of the interval scan."""
    stack = []
    for b in ls:
        while stack and stack[-1] > b:
            stack.pop()
        if stack and stack[-1] == b:
            return False
        stack.append(b)
    return True


def tree_lengths(t, n):
    out = [None]*n
    pending = [(t, 1)]
    while pending:
        node, d = pending.pop()
        if node is not None:
            r, left, right = node
            out[r] = d
            pending.extend(((left, d+1), (right, d+1)))
    return tuple(out)


def obstruction(window, weight_multiple=16):
    assert window >= 2
    assert weight_multiple >= 2
    # The only interval with a repeated minimum has width window+1.
    ls = (3, 1, 2) + tuple(range(3, window+2)) + (2,)
    n = len(ls)
    gs = gap_lengths(ls)
    # E is exactly the contribution of all unit-weight outcomes.
    e = sum(ls[i] for i in range(n) if i not in (1, 2, n-1)) + sum(gs)
    assert e == window*window+4*window+10
    b = weight_multiple*e
    m = 3*b
    p, q = [1]*n, [1]*(n+1)
    p[1], p[2], p[-1] = m, b, b
    candidate = m+4*b+e
    return ls, p, q, dict(window=window, n=n, E=e, B=b, M=m,
                          weight_multiple=weight_multiple,
                          inadmissible_cost=candidate,
                          universal_tree_lower_bound=8*b)


def bury(ls, p, q, levels):
    """Force a valid right-chain prefix above an inadmissible sequence.

    The forcing weight uses only the cost of a feasible right chain, not
    an optimal cost. The exact optimum shift is independently tested below.
    """
    n = len(p)
    upper = sum(a*(i+1) for i, a in enumerate(p))
    upper += sum(a*min(i+1, n) for i, a in enumerate(q))
    offset = 0
    for _ in range(levels):
        mass = sum(p)+sum(q)
        a = mass+upper+2
        offset += a+1+mass
        p, q = [a]+p, [1]+q
        ls = (1,)+tuple(b+1 for b in ls)
        upper = 2*a-1
    return ls, p, q, offset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--enumerate-n', type=int, default=7)
    parser.add_argument('--max-window', type=int, default=128)
    args = parser.parse_args()
    rows = []
    for n in range(1, args.enumerate_n+1):
        actual = {tree_lengths(label(s)[0], n) for s in shapes(n)}
        accepted = set()
        counts = Counter()
        for ls in itertools.product(range(1, n+1), repeat=n):
            counts['sequences'] += 1
            is_ranked = ranked(ls)
            assert stack_ranked(ls) == is_ranked, ls
            counts['ranked'] += is_ranked
            zero_flow = not any(flow(ls))
            counts['zero_flow'] += zero_flow
            if is_ranked and zero_flow:
                accepted.add(ls)
            if zero_flow and ranked(ls, 3):
                counts['window3_zero_flow'] += 1
                counts['window3_invalid'] += ls not in actual
        assert accepted == actual, (n, accepted-actual, actual-accepted)
        row = dict(n=n, valid_trees=len(actual), **counts)
        rows.append(row)
        print(row, flush=True)

    witnesses = []
    for window in range(2, args.max_window+1):
        ls, p, q, row = obstruction(window)
        assert ls.count(1) == 1 and not any(flow(ls))
        assert ranked(ls, window) and not ranked(ls)
        direct = sum(a*b for a, b in zip(p, ls))
        direct += sum(a*b for a, b in zip(q, gap_lengths(ls)))
        assert direct == row['inadmissible_cost']
        opt, tree, root_checks = knuth(p, q)
        assert cost(tree, p, q) == opt >= row['universal_tree_lower_bound'] > direct
        assert direct*128 == row['universal_tree_lower_bound']*113
        if window <= 24:
            brute, bt = cubic(p, q)
            assert brute == opt == cost(bt, p, q)
        row.update(optimum=opt, gap=opt-direct, knuth_root_checks=root_checks)
        if window <= 5:
            row.update(lengths=ls, p=p, q=q)
        witnesses.append(row)
    buried = []
    for window in range(2, 17):
        original, p, q, row = obstruction(window)
        base_opt, _ = cubic(p, q)
        for levels in range(1, 9):
            ls, pp, qq, offset = bury(original, p, q, levels)
            assert ranked(ls, window) and not any(flow(ls)) and not ranked(ls)
            assert ls[:levels] == tuple(range(1, levels+1))
            assert all(b > levels for b in ls[levels:])
            candidate = sum(a*b for a, b in zip(pp, ls))
            candidate += sum(a*b for a, b in zip(qq, gap_lengths(ls)))
            assert candidate == row['inadmissible_cost']+offset
            opt, tree = cubic(pp, qq)
            assert opt == base_opt+offset == cost(tree, pp, qq)
            assert knuth(pp, qq)[0] == opt
            current = tree
            for r in range(levels):
                assert current[0] == r and current[1] is None
                current = current[2]
            assert opt > candidate
            buried.append(dict(window=window, forced_top_levels=levels,
                               n=len(pp), optimum=opt, inadmissible_cost=candidate,
                               preserved_gap=opt-candidate))
    target = Path(__file__).resolve().parents[1]/'results'/'depth_order.json'
    target.write_text(json.dumps(dict(enumeration=rows, witnesses=witnesses,
                                     buried_witnesses=buried), indent=2)+'\n')
    print('Verified', sum(r['sequences'] for r in rows), 'sequences and',
          len(witnesses), 'positive-weight window obstructions and',
          len(buried), 'forced-prefix obstructions.', flush=True)


if __name__ == '__main__':
    main()
