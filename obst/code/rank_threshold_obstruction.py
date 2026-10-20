#!/usr/bin/env python3
"""Literal controls of incompatible binary ruler-threshold optimizers."""
from pathlib import Path
from collections import Counter
from itertools import combinations
import hashlib,json
from rank_reward_tail import scores
from aggregate_core_audit import layers

def nu(x):return (x&-x).bit_length()-1

def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rows=[]
 raw=json.loads((root/'results/rank_threshold_probe_raw.json').read_text())
 p=raw['p'];c=2**raw['h']-1;v=[nu(r) for r in range(1,c+1)]
 best=[0]*raw['h']
 for ts in combinations(range(len(p)),c):
  vals=[sum(p[k]*int(v[r]>=a) for r,k in enumerate(ts)) for a in range(1,raw['h'])]
  best[0]=max(best[0],sum(vals))
  for a,x in enumerate(vals,1):best[a]=max(best[a],x)
  stats['literal_search_winner_subsequences']+=1
 assert best==[raw['full'],*raw['levels']]
 fixtures=[(4,16,[9,12,14],3,4)]
 for h in range(5,15):
  C=2**h;m=h-1;pos=[C//2+1]+[C//2+4*r+2 for r in range(m)]
  assert max(pos)<=C
  fixtures.append((h,C,pos,h-1,2*h-3))
 for h,n,pos,expected,upper in fixtures:
  c=n-1;v=[nu(r) for r in range(1,n)];profiles=[]
  for deleted in range(1,n+1):
   retained=[x-int(x>deleted) for x in pos if x!=deleted]
   values=[nu(r) for r in retained]
   profile=[sum(x>=a for x in values) for a in range(1,h)]
   stats['threshold_comparisons']+=len(values)*(h-1)
   profiles.append(profile);stats['literal_deletions']+=1;stats['positive_rank_evaluations']+=len(retained)
  full=max(map(sum,profiles));levels=[max(row[a] for row in profiles) for a in range(h-1)]
  assert full==expected and sum(levels)==upper
  if h>=5:assert levels==[h-1]+[1]*(h-2)
  if n<=128:
   p=[int(i+1 in pos) for i in range(n)]
   for w,exp in [(v,full)]+[([int(x>=a) for x in v],levels[a-1]) for a in range(1,h)]:
    S,_=scores(p,w,stats);assert S[0][n]==exp;stats['generic_score_controls']+=1
   q=[i%3 for i in range(n+1)];M=(h+1)*(sum(p)+sum(q))+1
   A=list(layers(p,q,h,M,stats))[-1]
   assert A[0][n]==M+h*(sum(p)+sum(q))-full;stats['original_full_interval_controls']+=1
  rows.append(dict(h=h,n=n,positive_positions=pos,full_score=full,threshold_optima=levels,sum_threshold_optima=sum(levels),all_root=n<=128))
 files=('rank_threshold_obstruction.py','rank_threshold_probe.cpp','rank_reward_tail.py','aggregate_core_audit.py')
 out=dict(scope='Exact failure of equality between the full ruler optimum and the sum of separately optimized rank thresholds, already for binary keys. The explicit family gives a ratio tending to two; no universal factor-two upper bound is asserted.',checks=stats,rows=rows,search=raw,search_artifact_sha256=hashlib.sha256((root/'results/rank_threshold_probe_raw.json').read_bytes()).hexdigest(),source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/rank_threshold_obstruction.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
