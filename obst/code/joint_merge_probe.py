#!/usr/bin/env python3
"""Harness-first audit of free-key/fixed-gap compatible merging.

This is a research probe, not a certified bound implementation. The oracle
enumerates every tree and independently rearranges only the internal weights.
"""
from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import random
from research import shapes,label,cubic,cost
from threshold_probe import depth_vectors,key_bound,threshold_bound


@lru_cache(None)
def enumerated(n):
    out=[]
    for shape in shapes(n):
        tree=label(shape)[0];pd,qd=depth_vectors(tree,n)
        out.append((tree,pd,qd))
    return out


def oracle(p,q):
    ps=sorted(p,reverse=True);n=len(p);best=None;witness=None
    for tree,pd,qd in enumerated(n):
        value=sum(a*b for a,b in zip(ps,sorted(pd)))+sum(a*b for a,b in zip(q,qd))
        if best is None or value<best:best=value;witness=dict(tree=tree,pd=pd,qd=qd)
    return best,witness


def from_gap_depths(lengths):
    stack=[]
    for d in lengths:
        stack.append((d,None))
        while len(stack)>1 and stack[-1][0]==stack[-2][0]:
            d,right=stack.pop();_,left=stack.pop()
            stack.append((d-1,(left,right)))
    if len(stack)!=1 or stack[0][0]!=0:return None,False
    return label(stack[0][1])[0],True


def candidate(p,q):
    # A pair is compatible when no original leaf lies strictly between it.
    # Infinitesimal leaf weights 2^i make all competing pair sums distinct.
    items=[(w,1<<i,True,i) for i,w in enumerate(q)]
    trace=[];charges=0;pair_evaluations=0
    for key in sorted(p):
        best=second=None
        for i in range(len(items)-1):
            for j in range(i+1,len(items)):
                pair_evaluations+=1
                pair=(items[i][0]+items[j][0],items[i][1]+items[j][1],i,j)
                if best is None or pair<best:second=best;best=pair
                elif second is None or pair<second:second=pair
                if items[j][2]:break
        mass,secondary,i,j=best;a=items[i];b=items[j]
        trace.append(dict(key=key,left_mass=a[0],right_mass=b[0],positions=[i,j],
                          pair_margin=None if second is None else second[0]-mass))
        charges+=mass+key
        items[i]=(mass+key,secondary,False,(a[3],b[3]));del items[j]
    qd=[0]*len(q);stack=[(items[0][3],0)]
    while stack:
        node,d=stack.pop()
        if isinstance(node,int):qd[node]=d
        else:stack.extend([(node[0],d+1),(node[1],d+1)])
    tree,valid=from_gap_depths(qd)
    if not valid:return dict(valid=False,qd=qd,trace=trace,charges=charges,pair_evaluations=pair_evaluations)
    pd,_=depth_vectors(tree,len(p))
    value=sum(a*b for a,b in zip(sorted(p,reverse=True),sorted(pd)))+sum(a*b for a,b in zip(q,qd))
    return dict(valid=True,value=value,qd=qd,pd=pd,tree=tree,trace=trace,charges=charges,pair_evaluations=pair_evaluations)


def main():
    checks=Counter();failures=[];rng=random.Random(317206)
    for n in range(6):
        for q in itertools.product(range(3),repeat=n+1):
            p=[0]*n;c=candidate(p,q);value=cubic(p,q)[0]
            assert c['valid'] and c['value']==c['charges']==value,(p,q,c,value)
            checks['ordinary_alphabetic_controls']+=1
    for n in range(1,9):
        for trial in range(300):
            p=[rng.randrange(10) for _ in range(n)];q=[rng.randrange(10) for _ in range(n+1)]
            expected,witness=oracle(p,q);actual=candidate(p,q)
            lower=key_bound(p)+threshold_bound(q)
            assert lower<=expected<=cubic(p,q)[0]
            checks['joint_oracle_controls']+=1
            checks['literal_tree_evaluations']+=len(enumerated(n))
            checks['candidate_pair_evaluations']+=actual['pair_evaluations']
            if not actual['valid'] or actual['value']!=expected:
                checks['invalid_levels' if not actual['valid'] else 'suboptimal_candidate']+=1
                if len(failures)<12:failures.append(dict(p=p,q=q,expected=expected,oracle=witness,candidate=actual,separate_lower=lower))
            else:checks['exact_candidate']+=1
    result=dict(seed=317206,checks=dict(checks),failures=failures,
                source_sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in ('joint_merge_probe.py','threshold_probe.py','research.py')})
    (Path(__file__).resolve().parents[1]/'results'/'joint_merge_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
