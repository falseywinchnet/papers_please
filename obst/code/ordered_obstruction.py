#!/usr/bin/env python3
"""A preserved failed obstruction search and periodic excess fixtures.

Compose seven-key invalid depth gadgets with the perfect-tree profile.
Every level-flow price vanishes. The bound ceiling is analytic; optimality
of the weighted candidate is measured independently for each saved fixture.
The attempted claim that it remained optimal failed, exposing a limitation
of the minimum-IPL candidate class instead.
"""
from collections import Counter
import json
from pathlib import Path

from complete import best_complete, minimum_ipl
from depth_order import flow, gap_lengths, stack_ranked, tree_lengths
from research import cost, cubic, knuth


def witness(h, base=16, epsilon=1):
    assert h >= 3 and base > 0 and epsilon > 0
    n = (1 << h)-1
    copies = 1 << (h-3)
    valid = tuple(h-((i+1 & -(i+1)).bit_length()-1) for i in range(n))
    invalid = list(valid)
    p, q = [base]*n, [base]*(n+1)
    for j in range(copies):
        start = 8*j
        invalid[start:start+7] = [h-3+x for x in (3,1,3,2,3,2,3)]
        p[start+1] += epsilon
    return valid, tuple(invalid), p, q


def main():
    rows = []
    for base in (1,16,128):
        for h in range(3,12):
            valid, invalid, p, q = witness(h,base)
            n, copies = len(p), 1 << (h-3)
            assert stack_ranked(valid) and not stack_ranked(invalid)
            assert all(a != b for a,b in zip(invalid,invalid[1:]))
            assert invalid.count(1) == 1 and not any(flow(invalid))
            assert Counter(valid) == Counter(invalid)
            assert gap_lengths(valid) == gap_lengths(invalid) == (h,)*(n+1)
            assert sum(invalid)-n == minimum_ipl(n)
            candidate, tree, _ = best_complete(p,q)
            assert tree_lengths(tree,n) == valid
            bad_cost = sum(a*b for a,b in zip(p,invalid))+h*sum(q)
            assert candidate-bad_cost == copies
            optimum, opt_tree, scans = knuth(p,q)
            assert optimum == cost(opt_tree,p,q) <= candidate
            if n <= 63:
                assert cubic(p,q)[0] == optimum
            ceiling = bad_cost+2*base
            row = dict(n=n,h=h,base=base,epsilon=1,copies=copies,
                       candidate=candidate,optimum=optimum,
                       candidate_optimal=candidate == optimum,
                       optimal_ipl=sum(tree_lengths(opt_tree,n))-n,
                       invalid_cost=bad_cost,all_price_ceiling=ceiling,
                       certificate_impossible=ceiling<candidate,
                       knuth_root_candidates=scans)
            rows.append(row)
            print(row,flush=True)
    target = Path(__file__).resolve().parents[1]/'results'/'ordered_obstruction.json'
    target.write_text(json.dumps(dict(rows=rows),indent=2)+'\n')


if __name__ == '__main__':
    main()
