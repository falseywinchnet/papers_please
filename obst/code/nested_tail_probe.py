#!/usr/bin/env python3
"""Falsify a nested-threshold upper bound for exact upper tails."""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib,json,random
from rank_reward_tail import scores,tails


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(38011);cache={};first={};zero={};worst=None;rows=[]
 def tail(p,v):
  key=(tuple(p),tuple(v))
  if key not in cache:
   S,_=scores(p,v,stats);cache[key]=tails(S,len(v),stats)
  return cache[key]
 def check(p,h,t):
  nonlocal worst
  C=2**h;v=[min((r&-r).bit_length()-1,t) for r in range(1,C)];n=len(p)
  actual=tail(p,v);nested=[0]*(n+1);previous=0;thresholds=[]
  for a in sorted(set(p)-{0}):
   q=[int(z>=a) for z in p];T=tail(q,v);thresholds.append(dict(level=a,increment=a-previous,p=q,tail=T))
   for d in range(n+1):nested[d]+=(a-previous)*T[d]
   previous=a
  stats['inputs']+=1
  for d in range(1,n-C+1):
   stats['width_comparisons']+=1;gap=actual[d]-nested[d]
   if gap>0:
    stats['upper_violations']+=1
    row=dict(n=n,h=h,t=t,d=d,p=p,actual=actual[d],nested=nested[d],gap=gap,thresholds=thresholds)
    key='alternating' if t==1 else 'full'
    if key not in first:first[key]=row;print('first violation',key,json.dumps(row),flush=True)
    if nested[d]==0 and key not in zero:zero[key]=row;print('zero threshold tail',key,json.dumps(row),flush=True)
    if worst is None or gap>worst['gap']:worst=row
   if gap<0:stats['lower_violations']+=1
 for n,h in [(6,2),(8,2),(10,3)]:
  for t in range(1,h):
   for q in product(range(3),repeat=n-2):check([0]+list(q)+[0],h,t)
   rows.append(dict(n=n,h=h,t=t,mode='exhaustive ternary interior'))
  print('completed exhaustive',n,flush=True)
 for n,h in [(16,3),(32,4)]:
  for _ in range(100):
   p=[rng.randrange(5) for i in range(n)]
   for t in range(1,h):check(p,h,t)
  rows.append(dict(n=n,h=h,mode='seeded integer vectors'))
  cache.clear();print('completed random',n,flush=True)
 files=('nested_tail_probe.py','rank_reward_tail.py','aggregate_core_audit.py')
 out=dict(scope='Exact diagnostic for U(p)<=sum threshold increments times U(binary threshold sets). No asymptotic upper-bound inference.',seed=38011,checks=stats,first_violations=first,zero_threshold_tails=zero,worst_gap=worst,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/nested_tail_probe.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
