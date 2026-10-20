#!/usr/bin/env python3
"""Independent subsequence audit of an exact periodic-template obstruction."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib,json
from rank_reward_tail import scores,tails


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rows=[]
 for h in range(3,8):
  C=2**h;c=C-1;n=2*C;p=[int(i in (C-5,C)) for i in range(n)];v=[int(r%2==0) for r in range(1,C)]
  S,_=scores(p,v,stats);T=tails(S,c,stats)
  left=sum(S[i][i+C+1] for i in range(C));right=sum(S[j][j+C] for j in range(1,C))
  assert (left,right,S[0][n],T[2])==(2*C-6,3*C//2-4,2,C//2-4);stats['family_identities']+=4
  for i in range(C):
   expected=2 if 1<=i<=C-6 else 1
   assert S[i][i+C+1]==expected;stats['boundary_entries']+=1
  for j in range(1,C):
   r=C-4-j;expected=1+int(j<=C-5 and r%2==0)
   assert S[j][j+C]==expected;stats['boundary_entries']+=1
  if h==3:
   for i in range(n-c+1):
    for j in range(i+c,n+1):
     best=0
     for seq in combinations(range(i,j),c):
      best=max(best,sum(p[x]*v[r] for r,x in enumerate(seq)));stats['literal_subsets']+=1
     assert S[i][j]==best;stats['literal_intervals']+=1
  rows.append(dict(h=h,n=n,boundary_long=left,boundary_short=right,full_reward=S[0][n],tail=T[2],verification='exact subsequence dynamic program'))
  print(h,T[2],flush=True)
 for h in (8,16,32,64,128):
  C=2**h;rows.append(dict(h=h,n=2*C,tail=C//2-4,verification='proved closed form only'))
 files=('periodic_tail_barrier.py','rank_reward_tail.py','aggregate_core_audit.py')
 result=dict(scope='Exact family proof audit; periodic reward template is an auxiliary clipping template, not a claim about the original ruler layer.',checks=stats,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/periodic_tail_barrier.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
