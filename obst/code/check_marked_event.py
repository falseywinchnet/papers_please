#!/usr/bin/env python3
"""Independent oracles for an unproved marked-boundary event search."""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
from marked_event_probe import candidate, greedy
from joint_merge_probe import enumerated
from research import cubic, knuth, cost


def main():
    rng = random.Random(317217)
    checks = Counter()
    examples = {}
    totals = Counter()
    def check(q, r, weight, exhaustive=False, all_crossings=False):
        n = len(q) - 1
        p = [0] * n
        p[r] = weight
        expected, tree = cubic(p, q)
        assert expected == knuth(p, q)[0] == cost(tree, p, q)
        if exhaustive:
            assert expected == min(sum(v*d for v, d in zip(q, qd)) + weight*pd[r]
                                   for _, pd, qd in enumerated(n))
            checks['literal_oracles'] += 1
        result = candidate(q, r, weight, all_crossings=False)
        totals.update(result['stats'])
        checks['cases'] += 1
        if result['cost'] != expected:
            checks['event_failures'] += 1
            examples.setdefault('event_failure', dict(q=q, r=r, weight=weight, expected=expected, result=result))
        else:
            assert cost(result['witness'][2][1], p, q) == expected
        if all_crossings:
            full = candidate(q, r, weight)
            checks['all_crossing_controls'] += 1
            if full['cost'] != expected:
                checks['all_crossing_failures'] += 1
                examples.setdefault('all_crossing_failure',dict(q=q,r=r,weight=weight,expected=expected,result=full))
            if full['cost'] != result['cost']:
                checks['crossing_choice_differences'] += 1
        g = greedy(q, r, weight)
        if g['cost'] != expected:
            checks['greedy_failures'] += 1
            examples.setdefault('greedy_failure', dict(q=q,r=r,weight=weight,expected=expected,greedy=g))
        if g['charge'] != g['cost']:
            checks['charge_mismatches'] += 1
            examples.setdefault('charge_mismatch',dict(q=q,r=r,weight=weight,expected=expected,greedy=g))
        seq = [level[0][1] for level in result['levels']]
        finite = [v if v is not None else float('inf') for v in seq]
        up = False
        for a,b in zip(finite,finite[1:]):
            if b > a: up = True
            if b < a and up:
                checks['nonunimodal'] += 1
                examples.setdefault('nonunimodal',dict(q=q,r=r,weight=weight,expected=expected,cost_sequence=seq))
                break
    for n in range(1,6):
        for qt in itertools.product(range(3),repeat=n+1):
            for r in range(n):
                for weight in range(1,4):
                    check(list(qt),r,weight,exhaustive=True,all_crossings=n<=4)
        print('exhaustive n',n,dict(checks),flush=True)
    for n in (6,8,12,16,24,32):
        for trial in range(500):
            kind=trial%5
            if kind==0:q=[rng.randrange(101) for _ in range(n+1)];weight=rng.randrange(201)
            elif kind==1:q=[1<<rng.randrange(15) for _ in range(n+1)];weight=1<<rng.randrange(17)
            elif kind==2:q=[100+rng.randrange(3) for _ in range(n+1)];weight=rng.randrange(401)
            elif kind==3:q=[rng.randrange(2) for _ in range(n+1)];weight=rng.randrange(3)
            else:q=[rng.randrange(1,100) for _ in range(n+1)];weight=sum(q)*rng.randrange(1,5)
            r=rng.randrange(n)
            check(q,r,weight,exhaustive=n<=8,all_crossings=trial<50)
        print('random n',n,dict(checks),flush=True)
    result=dict(seed=317217,checks=dict(checks),totals=dict(totals),examples=examples,
      source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest()
      for f in ('check_marked_event.py','marked_event_probe.py','joint_merge_probe.py','research.py','threshold_probe.py')})
    dest=Path(__file__).resolve().parents[1]/'results'/'marked_event.json'
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print('written',dest,dict(checks),flush=True)


if __name__=='__main__':main()
