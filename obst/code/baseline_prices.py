#!/usr/bin/env python3
"""Concave baseline-price search for the full-OBST shape certificate.

The production search is capped by bit_length(n) extra linear oracle calls.
Every sampled price is a valid certificate; exhausting the cap is not a
claim to have found the best price. Integer arithmetic throughout.
"""
from collections import Counter


def priced_huffman(ps, qs, a, b, delta, stats):
    """Lexicographically minimize (residual cost, unweighted path length).

    Each original outcome has secondary weight1. A merged leaf retains
    its number of original outcomes. Summing secondary merge costs gives
    2*IPL+3*n, so tie-breaking also returns a valid supergradient.
    ps and qs are original weights sorted in descending order.
    """
    original = [(w-b+delta, 1) for w in reversed(qs)]
    merged = []
    i = j = 0

    def pop():
        nonlocal i, j
        if i < len(original) and j < len(merged):
            stats['price_merge_comparisons'] += 1
        if i < len(original) and (j == len(merged) or original[i] <= merged[j]):
            v = original[i]
            i += 1
        else:
            v = merged[j]
            j += 1
        return v

    value = secondary = 0
    for w in reversed(ps):
        x, xc = pop()
        y, yc = pop()
        pair = (w-a+delta+x+y, 1+xc+yc)
        assert not merged or pair >= merged[-1]
        merged.append(pair)
        value += pair[0]
        secondary += pair[1]
        stats['price_contractions'] += 1
    n = len(ps)
    assert (secondary-3*n) % 2 == 0
    return value, (secondary-3*n)//2


def exclusion_bound(ps, qs, a, b, imin, delta, stats):
    n = len(ps)
    assert 0 <= 2*delta <= a+b
    residual, ipl = priced_huffman(ps, qs, a, b, delta, stats)
    value = (a+b-2*delta)*(imin+1)+(a+2*b-3*delta)*n+residual
    return value, 2*(ipl-imin-1)


def search_prices(ps, qs, a, b, imin, initial_bound, stats,
                  candidate=None, max_calls=None):
    """Binary supergradient search, retaining the best sampled bound.

    initial_bound is the already-computed bound at delta0. With no cap and
    no early certificate stop, returns the maximum over all integer prices.
    """
    best, chosen = initial_bound, 0
    low, high = 1, (a+b)//2
    calls = 0
    exact = low > high
    while low <= high and (max_calls is None or calls < max_calls):
        delta = (low+high)//2
        value, slope = exclusion_bound(ps, qs, a, b, imin, delta, stats)
        calls += 1
        if value > best:
            best, chosen = value, delta
        if slope == 0:
            exact = True
        if candidate is not None and best >= candidate:
            break
        if slope > 0:
            low = delta+1
        elif slope < 0:
            high = delta-1
        else:
            break
    exact = exact or low > high
    stats['price_oracle_calls'] = calls
    stats['price_search_exact'] = int(exact)
    stats['price_chosen_delta'] = chosen
    stats['price_bound_improvement'] = best-initial_bound
    return best


def main():
    import json
    from pathlib import Path
    import random
    import sys
    from complete import attempt, solve, hybrid_solve, minimum_ipl
    from research import cost, cubic, knuth, profiles
    from sparse import FAMILIES, weights

    sys.setrecursionlimit(20000)
    rng = random.Random(0xBA5E11AE)
    lex_checks = 0
    for n in range(1, 9):
        for _ in range(50):
            p = sorted([rng.randrange(12) for _ in range(n)], reverse=True)
            q = sorted([rng.randrange(12) for _ in range(n+1)], reverse=True)
            a, b = min(p), min(q)
            delta = rng.randrange((a+b)//2+1)
            pp, qq = [w-a+delta for w in p], [w-b+delta for w in q]
            brute = min((sum(w*d for w, d in zip(pp, dp))+
                         sum(w*d for w, d in zip(qq, dq)), sum(dp)-n)
                        for dp, dq in profiles(n))
            assert priced_huffman(p, q, a, b, delta, Counter()) == brute
            lex_checks += 1
    price_checks = 0
    for n in range(1, 21):
        for _ in range(60):
            p = sorted([rng.randrange(20)+10 for _ in range(n)], reverse=True)
            q = sorted([rng.randrange(20)+10 for _ in range(n+1)], reverse=True)
            a, b, imin = min(p), min(q), minimum_ipl(n)
            sampled = [exclusion_bound(p,q,a,b,imin,d,Counter())[0]
                       for d in range((a+b)//2+1)]
            got = search_prices(p,q,a,b,imin,sampled[0],Counter())
            assert got == max(sampled), (p,q,sampled,got)
            price_checks += 1
    full_checks = rescued = 0
    for n in range(1, 31):
        for trial in range(100):
            base = (0, 5, 20, 1000)[trial % 4]
            spread = (3, 10, 100)[trial % 3]
            p = [base+rng.randrange(spread) for _ in range(n)]
            q = [base+rng.randrange(spread) for _ in range(n+1)]
            reference, _ = cubic(p,q)
            old, _, _ = attempt(p,q,unrestricted=True)
            value, tree, stats = attempt(p,q,unrestricted=True,optimize_baseline=True)
            assert old is None or value == old
            if value is not None:
                assert value == reference == cost(tree,p,q)
                rescued += old is None
            got, tree, _ = hybrid_solve(p,q,optimize_baseline=True)
            assert got == reference == cost(tree,p,q)
            got, tree, _ = solve(p,q,optimize_baseline=True)
            assert got == reference == cost(tree,p,q)
            full_checks += 1
    print('Verified',lex_checks,'lexicographic oracles,',price_checks,
          'integer maxima,',full_checks,'full inputs; rescues',rescued,flush=True)
    rows = []
    bench_rng = random.Random(0xBA5E2026)
    fixtures = []
    for n in (128,256,512,1024,2048):
        for epsilon in (1,2,4,8,16,32):
            p = [1000+bench_rng.randrange(-epsilon,epsilon+1) for _ in range(n)]
            q = [1000+bench_rng.randrange(-epsilon,epsilon+1) for _ in range(n+1)]
            fixtures.append((n,'perturbation_'+str(epsilon),p,q))
    for n in (64,128,256):
        fixtures.extend((n,f,*weights(n,f,bench_rng)) for f in FAMILIES)
    for n,f,p,q in fixtures:
        old, _, old_stats = attempt(p,q)
        value, tree, stats = attempt(p,q,optimize_baseline=True)
        reference, _, scans = knuth(p,q)
        if value is not None:
            assert value == reference == cost(tree,p,q)
        assert old is None or value == old
        rows.append(dict(n=n,family=f,optimum=reference,old_certified=old is not None,
                         priced_certified=value is not None,old_counts=dict(old_stats),
                         priced_counts=dict(stats),knuth_root_candidates=scans))
        print(n,f,'old',old is not None,'priced',value is not None,
              'calls',stats.get('price_oracle_calls',0),flush=True)
    target = Path(__file__).resolve().parents[1]/'results'/'baseline_prices.json'
    target.write_text(json.dumps(dict(lex_checks=lex_checks,price_checks=price_checks,
                                     full_checks=full_checks,rescued=rescued,rows=rows),
                                indent=2)+'\n')


if __name__ == '__main__':
    main()
