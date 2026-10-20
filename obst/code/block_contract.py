#!/usr/bin/env python3
"""Exact certified block contraction, with a capped Cartesian-tree scan."""
import argparse
import json
import math
from pathlib import Path
import random
import sys
from research import check_weights, cost, cubic, knuth
from sparse import FAMILIES, weights


def candidate_blocks(p, q, cap=None):
    n = len(p)
    if not n:
        return [], dict(predicate_checks=0, selection_events=0, cap=0)
    left, right = [-1]*n, [-1]*n
    stack = []
    for i in range(n):
        last = -1
        while stack and p[stack[-1]] < p[i]:
            last = stack.pop()
        if stack:
            right[stack[-1]] = i
        left[i] = last
        stack.append(i)
    root = stack[0]
    order, stack = [], [root]
    while stack:
        r = stack.pop()
        order.append(r)
        stack.extend(c for c in (left[r], right[r]) if c != -1)
    lo, hi = list(range(n)), [i+1 for i in range(n)]
    prefix = [0]
    for i in range(n):
        prefix.append(prefix[-1]+p[i]+q[i+1])
    safe = [False]*n
    checks = 0
    # The summaries describe maximal safe descendants, regardless of cap.
    covered, states = [0]*n, [0]*n
    events = [[] for _ in range(n+1)]
    for r in reversed(order):
        if left[r] != -1:
            lo[r] = lo[left[r]]
        if right[r] != -1:
            hi[r] = hi[right[r]]
        i, j = lo[r], hi[r]
        k = j-i
        child_covered = sum(covered[c] for c in (left[r],right[r]) if c!=-1)
        child_states = sum(states[c] for c in (left[r],right[r]) if c!=-1)
        if k != n:
            checks += 1
            mass = prefix[j]-prefix[i]+q[i]
            # A balanced k-key tree has height ceil(log2(k+1)).
            threshold = mass*(k.bit_length() + (i != 0 and j != n))
            safe[r] = ((i == 0 or p[i-1] >= threshold)
                       and (j == n or p[j] >= threshold))
        if safe[r]:
            covered[r], states[r] = k, k*(k+1)//2
            events[k].append((k-child_covered,states[r]-child_states))
        else:
            covered[r],states[r] = child_covered,child_states
    event_count = 0
    if cap is None:
        m, block_states, best, cap = n, 0, n*(n+1)//2, 0
        for k,bucket in enumerate(events):
            for removed, added_states in bucket:
                m -= removed
                block_states += added_states
                event_count += 1
            objective = block_states + m*(m+1)//2
            if objective < best:
                best,cap = objective,k
    chosen, stack = [], [root]
    while stack:
        r = stack.pop()
        if safe[r] and hi[r]-lo[r] <= cap:
            chosen.append((lo[r],hi[r]))
        else:
            stack.extend(c for c in (left[r],right[r]) if c != -1)
    # Right-first traversal lists disjoint intervals in decreasing order.
    return list(reversed(chosen)), dict(predicate_checks=checks,
                                       selection_events=event_count,cap=cap)


def solve(p, q, cap=None):
    check_weights(p, q)
    n = len(p)
    blocks, selection = candidate_blocks(p,q,cap)
    alive = [True]*n
    gap = list(q)
    payload = [None]*(n+1)
    offset = block_states = root_candidates = 0

    def relabel(t, shift):
        if t is None:
            return None
        r,a,b=t
        return r+shift,relabel(a,shift),relabel(b,shift)

    for i,j in blocks:
        c,t,scans = knuth(p[i:j],q[i:j+1])
        payload[j] = relabel(t,i)
        gap[j] = sum(p[i:j])+sum(q[i:j+1])
        offset += c
        root_candidates += scans
        k=j-i
        block_states += k*(k+1)//2
        alive[i:j] = [False]*k
    keys = [i for i in range(n) if alive[i]]
    leaves = keys+[n]
    c,t,scans=knuth([p[i] for i in keys],[gap[i] for i in leaves])

    def expand(t,lo=0):
        if t is None:
            return payload[leaves[lo]]
        r,a,b=t
        return keys[r],expand(a,lo),expand(b,r+1)

    m=len(keys)
    return c+offset,expand(t),dict(
        input_keys=n,core_keys=m,block_count=len(blocks),**selection,
        cartesian_nodes=n,block_states=block_states,
        core_states=m*(m+1)//2,total_states=block_states+m*(m+1)//2,
        root_candidates=root_candidates+scans)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-n',type=int,default=512)
    args=parser.parse_args()
    sys.setrecursionlimit(10000)
    rng=random.Random(0xB10C0)
    tested=0
    for n in range(1,21):
        for trial in range(150):
            p=[1<<rng.randrange(20) for _ in range(n)]
            q=[rng.randrange(10) if trial%2 else 1<<rng.randrange(20)
               for _ in range(n+1)]
            c,t,_=solve(p,q,None if trial%3 else 1+trial%n)
            ref,_=cubic(p,q)
            assert c==ref==cost(t,p,q),(p,q,c,ref)
            if n<=10 and trial<30:
                _,_,adaptive=solve(p,q)
                proxies=[]
                for limit in range(n+1):
                    blocks,_=candidate_blocks(p,q,limit)
                    sizes=[j-i for i,j in blocks]
                    m=n-sum(sizes)
                    proxies.append(m*(m+1)//2+sum(k*(k+1)//2 for k in sizes))
                assert adaptive['total_states']==min(proxies)
            tested+=1
    rows=[]
    for n in (16,32,64,128,256,512):
        if n>args.max_n:
            break
        inputs=[(f,*weights(n,f,rng)) for f in FAMILIES]
        # Dense tiny runs bounded by sparse heavy keys; all weights positive.
        # Random placement is independent of the contraction scan.
        p=[rng.randrange(1,4) for _ in range(n)]
        q=[rng.randrange(1,4) for _ in range(n+1)]
        for k in rng.sample(range(n),max(1,math.isqrt(n))):
            p[k]=1000000
        inputs.append(('heavy_separators',p,q))
        for f,p,q in inputs:
            c,t,counts=solve(p,q)
            ref,_,scans=knuth(p,q)
            assert c==ref==cost(t,p,q),(n,f,c,ref)
            rows.append(dict(family=f,n=n,**counts,
                             baseline_states=n*(n+1)//2,
                             baseline_candidates=scans))
    out=Path(__file__).resolve().parents[1]/'results/block_contraction_adaptive.json'
    out.write_text(json.dumps(dict(random_verification=tested,rows=rows),indent=2)+'\n')
    print(tested,'random instances verified')
    for row in rows:
        if row['n']==args.max_n:
            print(row['family'],row['core_keys'],row['total_states'])


if __name__=='__main__':
    main()
