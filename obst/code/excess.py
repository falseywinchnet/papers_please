#!/usr/bin/env python3
"""Exact bounded-excess full-OBST construction with dyadic tilings.

Optimize every tree with IPL <= minimum_ipl(n)+budget.
The gap-depth sequence is an aligned dyadic tiling. A nonnegative leaf
potential bounds drift by the excess and the optional bottom-level width.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import random

from complete import from_lengths, minimum_ipl, residual_huffman
from research import cost, cubic, knuth, label, shapes, unordered_huffman
from sparse import Counted, FAMILIES, weights


def bounded_excess(p,q,budget):
    n, leaves = len(p), len(q)
    assert leaves == n+1
    assert n >= 1 and isinstance(budget,int) and budget >= 0
    h = leaves.bit_length()-1
    slots = 1 << h
    r = leaves-slots
    perfect = r == 0
    unit = 1 << (budget+1 if perfect else budget+2)
    height = h+budget+(1 if perfect else 2)
    scale = (2 if perfect else 1)*unit
    cap = scale*budget
    endpoint = slots*unit
    options = []
    for d in range(1,height+1):
        width = 1 << (height-d)
        penalty = (2*unit*(d-h)+3*(width-unit) if perfect else
                   unit*(d-h)+2*(width-unit))
        assert penalty >= 0
        if penalty <= cap:
            options.append((d,width,penalty))
    previous = {(0,0):0}
    parents = []
    stats = Counter(excess_states=1,excess_max_width=1)
    for i in range(leaves):
        current, pred = {}, {}
        for (drift,spent),value in previous.items():
            position = i*unit+drift
            assert position >= 0
            key_cost = 0
            if i:
                assert position > 0
                key_depth = height-((position & -position).bit_length()-1)
                key_cost = p[i-1]*key_depth
            for d,width,penalty in options:
                stats['excess_transition_checks'] += 1
                after = drift+width-unit
                used = spent+penalty
                next_position = position+width
                count = i+1
                outside_band = (abs(after)>budget*unit if perfect else
                    (2*next_position < (count-budget)*unit or
                     next_position < (count-r-budget)*unit or
                     next_position > (count+budget)*unit or
                     2*next_position > (slots-r+count+budget)*unit))
                if (position % width or used > cap or outside_band or
                    next_position > endpoint or
                    (count == leaves and next_position != endpoint)):
                    continue
                stats['excess_feasible_transitions'] += 1
                state = after,used
                score = value+key_cost+q[i]*d
                if state not in current or score < current[state]:
                    current[state] = score
                    pred[state] = (drift,spent),d
        stats['excess_states'] += len(current)
        stats['excess_max_width'] = max(stats['excess_max_width'],len(current))
        previous = current
        parents.append(pred)
    result,state = min((v,k) for k,v in previous.items() if k[0] == -r*unit)
    chosen_excess = state[1]//scale
    assert state[1] == chosen_excess*scale
    depths = []
    for pred in reversed(parents):
        state,d = pred[state]
        depths.append(d)
    depths.reverse()
    position = 0
    lengths = []
    for d in depths[:-1]:
        position += 1 << (height-d)
        lengths.append(height-((position & -position).bit_length()-1))
    tree = from_lengths(lengths)
    assert sum(lengths)-n == minimum_ipl(n)+chosen_excess
    assert cost(tree,p,q) == result
    stats.update(excess_budget=budget,chosen_excess=chosen_excess,
                 reconstructed_keys=n,rare_choices=min(r,slots-r))
    return result,tree,stats


def attempt(p,q,budget=2):
    candidate,tree,stats = bounded_excess(p,q,budget)
    a,b = min(p),min(q)
    comparisons = Counter()
    ps = [x.value for x in sorted((Counted(w,comparisons) for w in p),reverse=True)]
    qs = [x.value for x in sorted((Counted(w,comparisons) for w in q),reverse=True)]
    stats['bound_sort_comparisons'] = comparisons['bound_weight_comparisons']
    stats['bound_sorted_items'] = len(p)+len(q)
    residual = residual_huffman(ps,qs,a,b,stats)
    threshold = ((a+b)*(minimum_ipl(len(p))+budget+1)+
                 (a+2*b)*len(p)+residual)
    stats.update(candidate=candidate,exclusion_bound=threshold,
                 certified=int(candidate<=threshold))
    return candidate if candidate<=threshold else None,tree,stats


def solve(p,q,budget=2):
    n=len(p)
    slots=1<<((n+1).bit_length()-1)
    r=n+1-slots
    if n and min(r,slots-r)<=n.bit_length():
        value,tree,stats=attempt(p,q,budget)
    else:
        value,tree,stats=None,None,Counter(skipped_wide_shape_space=1)
    if value is None:
        value,tree,scans=knuth(p,q)
        stats.update(fallback_states=n*(n+1)//2,fallback_root_candidates=scans)
    return value,tree,dict(stats)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-n',type=int,default=1024)
    args = parser.parse_args()
    rng = random.Random(0xEACE55)
    shape_checks = 0
    for n in range(1,9):
        trees = [label(s)[0] for s in shapes(n)]
        ipls = [cost(t,[1]*n,[0]*(n+1))-n for t in trees]
        for trial in range(30):
            p=[rng.randrange(30) for _ in range(n)]
            q=[rng.randrange(30) for _ in range(n+1)]
            for budget in range(5):
                value,tree,_ = bounded_excess(p,q,budget)
                expected=min(cost(t,p,q) for t,ipl in zip(trees,ipls)
                             if ipl<=minimum_ipl(n)+budget)
                assert value==expected==cost(tree,p,q)
                shape_checks += 1
    checks=certified=0
    for n in range(1,31):
        for trial in range(100):
            base=(0,10,1000)[trial%3]
            p=[base+rng.randrange(20) for _ in range(n)]
            q=[base+rng.randrange(20) for _ in range(n+1)]
            value,tree,stats=attempt(p,q,budget=2)
            true,_=cubic(p,q)
            a,b=min(p),min(q)
            heap=unordered_huffman([w-a for w in p],[w-b for w in q])
            assert stats['exclusion_bound']==((a+b)*(minimum_ipl(n)+3)+
                                               (a+2*b)*n+heap)
            assert stats['candidate']>=true
            if value is not None:
                assert value==true==cost(tree,p,q)
                certified+=1
            got,tree,_=solve(p,q)
            assert got==true==cost(tree,p,q)
            checks+=1
    family_checks=0
    for n in (0,1,2,3,7,15,31,63):
        for family in FAMILIES:
            p,q=weights(n,family,rng) if n else ([],[rng.randrange(20)])
            got,tree,_=solve(p,q)
            assert got==cubic(p,q)[0]==cost(tree,p,q)
            family_checks+=1
    print('Verified',shape_checks,'bounded shape optima and',checks,
          'full mixed inputs;',certified,'certificates',flush=True)
    from ordered_obstruction import witness
    rows=[]
    for n in (63,64,127,128,255,256,511,512,1023,1024,2047):
        if n>args.max_n: continue
        fixtures=[]
        for epsilon in (1,2,4,8,16):
            p=[1000+rng.randrange(-epsilon,epsilon+1) for _ in range(n)]
            q=[1000+rng.randrange(-epsilon,epsilon+1) for _ in range(n+1)]
            fixtures.append(('perturbation_'+str(epsilon),p,q))
        if (n+1)&n == 0:
            for base in (1,16,128):
                _,_,p,q=witness((n+1).bit_length()-1,base)
                fixtures.append(('periodic_'+str(base),p,q))
        for family,p,q in fixtures:
            true,_,scans=knuth(p,q)
            trials=[]
            for budget in (0,1,2,3):
                value,tree,stats=attempt(p,q,budget)
                assert stats['candidate']>=true
                if value is not None: assert value==true==cost(tree,p,q)
                trials.append(dict(stats))
            row=dict(n=n,family=family,optimum=true,trials=trials,
                     knuth_root_candidates=scans,knuth_states=n*(n+1)//2)
            rows.append(row)
            print(n,family,'certificates',[x['certified'] for x in trials],
                  'gaps',[x['candidate']-true for x in trials],
                  'states',[x['excess_states'] for x in trials],flush=True)
    output=Path(__file__).resolve().parents[1]/'results'/'excess.json'
    output.write_text(json.dumps(dict(shape_checks=shape_checks,full_checks=checks,
                                      certified_checks=certified,family_checks=family_checks,
                                      rows=rows),indent=2)+'\n')


if __name__=='__main__': main()
