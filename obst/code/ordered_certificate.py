#!/usr/bin/env python3
"""Research experiment: order-sensitive residual shape exclusion.

This is deliberately separate from the production fallback. Every bound
is valid; the fixed-budget multiplier optimizer need not attain its dual
optimum. No order-free profile rejection is applied to the ordered bound.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import random

from complete import attempt, best_complete, minimum_ipl
from depth_dual import optimize, SCALE
from research import cost, cubic, knuth, label, shapes


def evaluate(p, q, candidate, iterations=32, delta=0, unique_root=False):
    n = len(p)
    assert n and iterations > 0
    a0, b0 = min(p), min(q)
    assert 0 <= 2*delta <= a0+b0
    a, b = a0-delta, b0-delta
    pp, qq = [w-a for w in p], [w-b for w in q]
    baseline = (a+b)*minimum_ipl(n)+(a+2*b)*n
    residual_upper = candidate-baseline
    lower, counts = optimize(pp, qq, residual_upper, iterations=iterations,
                             unique_root=unique_root)
    exclusion = SCALE*(baseline+a+b)+lower
    counts.update(delta=delta, residual_upper=residual_upper,
                  residual_lower_scaled=lower, exclusion_scaled=exclusion,
                  candidate_scaled=candidate*SCALE,
                  certified=candidate*SCALE <= exclusion)
    # A dimension-based work proxy, counting both passes for unique-root.
    counts['key_depth_cells'] = (n*counts['oracle_height']*
                                 counts['oracle_calls']*(2 if unique_root else 1))
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-n', type=int, default=512)
    parser.add_argument('--iterations', type=int, default=32)
    parser.add_argument('--checks', type=int, default=240)
    args = parser.parse_args()
    rng = random.Random(0x0D3E2026)
    checks = 0
    for trial in range(args.checks):
        n = 1+trial % 8
        baseline = (0, 10, 1000)[trial % 3]
        p = [baseline+rng.randrange(20) for _ in range(n)]
        q = [baseline+rng.randrange(20) for _ in range(n+1)]
        candidate, tree, _ = best_complete(p,q)
        true, _ = cubic(p,q)
        outside = [cost(t,p,q) for t in (label(s)[0] for s in shapes(n))
                   if cost(t,[1]*n,[0]*(n+1))-n > minimum_ipl(n)]
        for unique in (False, True):
            delta = rng.randrange((min(p)+min(q))//2+1)
            stats = evaluate(p,q,candidate,iterations=8,delta=delta,
                             unique_root=unique)
            if outside:
                assert stats['exclusion_scaled'] <= min(outside)*SCALE
            if stats['certified']:
                assert candidate == true == cost(tree,p,q)
            checks += 1
    print('Verified',checks,'ordered exclusion bounds against tree enumeration',flush=True)
    rows = []
    rng = random.Random(0x0D3EBA5E)
    for n in (64,128,256,512,1024,2048):
        if n > args.max_n:
            continue
        for epsilon in (1,2,4,8,16,32):
            p = [1000+rng.randrange(-epsilon,epsilon+1) for _ in range(n)]
            q = [1000+rng.randrange(-epsilon,epsilon+1) for _ in range(n+1)]
            candidate, tree, shape_counts = best_complete(p,q)
            old, _, old_counts = attempt(p,q,optimize_baseline=True)
            true, _, scans = knuth(p,q)
            trials = []
            for unique in (False, True):
                for delta in (0,(min(p)+min(q))//4):
                    stats = evaluate(p,q,candidate,args.iterations,delta,unique)
                    stats['unique_root'] = unique
                    if stats['certified']:
                        assert candidate == true == cost(tree,p,q)
                    trials.append(stats)
            row = dict(n=n,epsilon=epsilon,optimum=true,candidate=candidate,
                       old_certified=old is not None,old_counts=dict(old_counts),
                       shape_counts=dict(shape_counts),trials=trials,
                       knuth_root_candidates=scans,knuth_states=n*(n+1)//2)
            rows.append(row)
            print(n,epsilon,'old',old is not None,'ordered',
                  [x['certified'] for x in trials], 'deficits',
                  [x['candidate_scaled']-x['exclusion_scaled'] for x in trials],
                  flush=True)
    output = Path(__file__).resolve().parents[1]/'results'/'ordered_certificate.json'
    output.write_text(json.dumps(dict(checks=checks,iterations=args.iterations,
                                      scale=SCALE,rows=rows),indent=2)+'\n')


if __name__ == '__main__':
    main()
