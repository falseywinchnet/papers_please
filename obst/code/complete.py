#!/usr/bin/env python3
"""Exact near-complete-shape optimizer plus a full-OBST certificate.

The shortcut either proves its tree globally optimal or falls back to
Knuth. It never treats minimum unweighted path length as a weight-based
assumption. Both key and gap weights remain in the objective.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import random
import sys

from research import cost, cubic, knuth, label, shapes, unordered_huffman
from sparse import Counted, FAMILIES, weights


def parameters(n):
    h = (n+1).bit_length()-1
    slots = 1 << h
    r = n-(slots-1)
    return h, slots, r


def minimum_ipl(n):
    h, slots, r = parameters(n)
    return (h-2)*slots+2+h*r


def from_lengths(ls):
    """Linear Cartesian construction; the caller supplies valid lengths."""
    if not ls:
        return None
    left, right = [None]*len(ls), [None]*len(ls)
    stack = []
    for i, b in enumerate(ls):
        previous = None
        while stack and ls[stack[-1]] > b:
            previous = stack.pop()
        if stack:
            right[stack[-1]] = i
        left[i] = previous
        stack.append(i)

    def build(i):
        return None if i is None else (i, build(left[i]), build(right[i]))
    return build(stack[0])


def best_complete(p, q):
    """Optimize all minimum-IPL trees in O(n*(1+min(r,2^h-r)))."""
    n = len(p)
    h, slots, r = parameters(n)
    previous = {0: 0}
    parents = []
    stats = Counter(complete_states=1)
    for j in range(slots):
        current, pred = {}, {}
        # Depth of the j-th key of the complete upper skeleton.
        d = h-((j+1 & -(j+1)).bit_length()-1)
        for e, value in previous.items():
            i = j+e
            for x in (0, 1):
                after = e+x
                if not 0 <= r-after <= slots-j-1:
                    continue
                stats['complete_transitions'] += 1
                if x:
                    v = value+(p[i]+q[i]+q[i+1])*(h+1)
                else:
                    v = value+q[i]*h
                if j < slots-1:
                    v += p[i+x]*d
                if after not in current or v < current[after]:
                    current[after] = v
                    pred[after] = (e, x)
        stats['complete_states'] += len(current)
        previous = current
        parents.append(pred)
    e, choices = r, []
    for pred in reversed(parents):
        e, x = pred[e]
        choices.append(x)
    choices.reverse()
    ls = []
    for j, x in enumerate(choices):
        if x:
            ls.append(h+1)
        if j < slots-1:
            ls.append(h-((j+1 & -(j+1)).bit_length()-1))
    tree = from_lengths(ls)
    stats['complete_reconstructed_keys'] = len(ls)
    assert len(ls) == n and sum(ls)-n == minimum_ipl(n)
    assert cost(tree, p, q) == previous[r]
    return previous[r], tree, stats


def residual_huffman(ps, qs, a, b, stats):
    """Two sorted queues implement the same nonnegative mixed-node bound."""
    original = [w-b for w in reversed(qs)]
    merged = []
    i = j = 0

    def pop():
        nonlocal i, j
        if i < len(original) and j < len(merged):
            stats['bound_merge_comparisons'] += 1
        if i < len(original) and (j == len(merged) or original[i] <= merged[j]):
            v = original[i]
            i += 1
        else:
            v = merged[j]
            j += 1
        return v

    answer = 0
    for w in reversed(ps):
        total = w-a+pop()+pop()
        assert not merged or total >= merged[-1]
        merged.append(total)
        answer += total
        stats['bound_contractions'] += 1
    return answer


def attempt(p, q, unrestricted=False, optimize_baseline=False):
    n = len(p)
    h, slots, r = parameters(n)
    rare = min(r, slots-r)
    stats = Counter(input_keys=n, bottom_optional_slots=slots,
                    bottom_expansions=r, rare_choices=rare)
    if not unrestricted and rare > max(1, n.bit_length()):
        stats['skipped_wide_shape_space'] = 1
        return None, None, stats
    candidate, tree, counts = best_complete(p, q)
    stats.update(counts)
    if not n:
        stats['certified'] = 1
        return candidate, tree, stats
    a, b = min(p), min(q)
    comparisons = Counter()
    ps = [x.value for x in sorted((Counted(w, comparisons) for w in p), reverse=True)]
    qs = [x.value for x in sorted((Counted(w, comparisons) for w in q), reverse=True)]
    stats['profile_sort_comparisons'] = comparisons['bound_weight_comparisons']
    stats['profile_sorted_items'] = 2*n+1
    profile_cost = sum(w*(i+1).bit_length() for i, w in enumerate(ps))
    profile_cost += h*sum(qs)+(sum(qs[-2*r:]) if r else 0)
    stats.update(candidate_cost=candidate, profile_certificate_ceiling=profile_cost+a+b)
    if candidate > profile_cost+a+b:
        # A fixed minimum-I shape with freely permuted residual weights is
        # feasible for the order-free bound, so this upper bound on the
        # certificate threshold proves the certificate cannot succeed.
        stats['profile_rejected'] = stats['certificate_failed'] = 1
        return None, None, stats
    residual_bound = residual_huffman(ps, qs, a, b, stats)
    base = (a+b)*minimum_ipl(n)+(a+2*b)*n
    lower_nonminimal = base+a+b+residual_bound
    stats.update(nonminimal_lower_bound=lower_nonminimal,
                 residual_lower_bound=residual_bound)
    if candidate <= lower_nonminimal:
        stats['certified'] = 1
        return candidate, tree, stats
    if optimize_baseline:
        from baseline_prices import search_prices
        improved = search_prices(ps,qs,a,b,minimum_ipl(n),lower_nonminimal,stats,
                                 candidate=candidate,max_calls=n.bit_length())
        stats['priced_nonminimal_lower_bound'] = improved
        if candidate <= improved:
            stats['certified'] = stats['price_rescued'] = 1
            return candidate, tree, stats
    stats['certificate_failed'] = 1
    return None, None, stats


def solve(p, q, optimize_baseline=False):
    value, tree, stats = attempt(p, q, optimize_baseline=optimize_baseline)
    if value is None:
        value, tree, scans = knuth(p, q)
        stats['fallback_dp_states'] = len(p)*(len(p)+1)//2
        stats['fallback_root_candidates'] = scans
    return value, tree, dict(stats)


def hybrid_solve(p, q, optimize_baseline=False):
    """Keep the earlier recursive contraction algorithm as the fallback."""
    from recursive_contract import solve as recursive_solve
    value, tree, stats = attempt(p, q, optimize_baseline=optimize_baseline)
    if value is None:
        value, tree, counts = recursive_solve(p, q)
        for name, count in counts.items():
            stats['recursive_'+name] += count
    return value, tree, dict(stats)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-n', type=int, default=1024)
    args = parser.parse_args()
    sys.setrecursionlimit(20000)
    rng = random.Random(0xC0A91E7E)
    shape_checks = 0
    for n in range(9):
        ts = [label(s)[0] for s in shapes(n)]
        ipls = [cost(t, [1]*n, [0]*(n+1))-n for t in ts]
        assert min(ipls) == minimum_ipl(n)
        minimal = [t for t, ipl in zip(ts, ipls) if ipl == min(ipls)]
        for _ in range(40):
            p = [rng.randrange(20) for _ in range(n)]
            q = [rng.randrange(20) for _ in range(n+1)]
            value, tree, _ = best_complete(p, q)
            assert value == min(cost(t, p, q) for t in minimal)
            assert cost(tree, p, q) == value
            shape_checks += 1
    full_checks = certified_checks = 0
    for n in range(1, 31):
        for trial in range(100):
            if trial % 3 == 0:
                base = (0, 10, 1000)[trial % 9 // 3]
                p = [base+rng.randrange(3) for _ in range(n)]
                q = [base+rng.randrange(3) for _ in range(n+1)]
            elif trial % 3 == 1:
                p = [rng.randrange(100) for _ in range(n)]
                q = [rng.randrange(100) for _ in range(n+1)]
            else:
                p = [1 << rng.randrange(16) for _ in range(n)]
                q = [1 << rng.randrange(16) for _ in range(n+1)]
            expected, _ = cubic(p, q)
            candidate, tree, stats = attempt(p, q, unrestricted=True)
            a, b = min(p), min(q)
            heap_bound = unordered_huffman([w-a for w in p], [w-b for w in q])
            threshold = (a+b)*(minimum_ipl(n)+1)+(a+2*b)*n+heap_bound
            assert (candidate is not None) == (stats['candidate_cost'] <= threshold), (p,q,stats,threshold)
            if 'residual_lower_bound' in stats:
                assert stats['residual_lower_bound'] == heap_bound
            if candidate is not None:
                assert candidate == expected == cost(tree, p, q)
                certified_checks += 1
            value, tree, _ = solve(p, q)
            assert value == expected == cost(tree, p, q)
            value, tree, _ = hybrid_solve(p, q)
            assert value == expected == cost(tree, p, q)
            full_checks += 1
    print('Validated', shape_checks, 'shape optima and', full_checks,
          'full inputs;', certified_checks, 'unrestricted certificates.', flush=True)
    rows = []
    fixtures = []
    bench_rng = random.Random(0xC0A91E)
    for n in (32, 64, 128, 256, 512, 1024):
        if n <= args.max_n:
            fixtures.extend((n, family, *weights(n, family, bench_rng))
                            for family in FAMILIES)
    for h in range(5, 11):
        for delta in (-5, -2, -1, 0, 1, 2, 5):
            n = (1 << h)+delta
            if n <= args.max_n:
                fixtures.append((n, 'near_uniform_offset',
                                 *weights(n, 'near_uniform', bench_rng)))
    for n in (256, 512, 1024):
        if n <= args.max_n:
            for epsilon in (0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512):
                p = [1000+bench_rng.randrange(-epsilon, epsilon+1) for _ in range(n)]
                q = [1000+bench_rng.randrange(-epsilon, epsilon+1) for _ in range(n+1)]
                fixtures.append((n, 'perturbation_'+str(epsilon), p, q))
    for n in (384, 768, 1000):
        if n <= args.max_n:
            fixtures.append((n, 'near_uniform_interior',
                             *weights(n, 'near_uniform', bench_rng)))
    for n, family, p, q in fixtures:
        value, tree, stats = solve(p, q)
        expected, _, scans = knuth(p, q)
        assert value == expected == cost(tree, p, q)
        row = dict(n=n, family=family, optimum=value,
                   knuth_dp_states=n*(n+1)//2, knuth_root_candidates=scans, **stats)
        rows.append(row)
        print(n, family, 'cert' if stats.get('certified') else 'fallback',
              stats.get('complete_states', 0), stats.get('fallback_dp_states', 0), flush=True)
    target = Path(__file__).resolve().parents[1]/'results'/'complete.json'
    target.write_text(json.dumps(dict(shape_checks=shape_checks,
                                     full_checks=full_checks,
                                     certified_checks=certified_checks,
                                     rows=rows), indent=2)+'\n')


if __name__ == '__main__':
    main()
