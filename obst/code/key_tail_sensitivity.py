#!/usr/bin/env python3
"""Probe exact one-sided input-key sensitivity of the true upper tail."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random
from rank_matching_repair import matching
from rank_reward_tail import scores,tails


def directional(p,v,x,stats):
 # The factor exceeds every possible slope difference in one interval.
 scale=max(v)+1
 S,_=scores(p,v,stats);T=tails(S,len(v),stats)
 q=[scale*a for a in p];q[x]+=1
 Q,_=scores(q,v,stats);V=tails(Q,len(v),stats)
 stats['directional_vectors']+=1
 return [b-scale*a for a,b in zip(T,V)]


def coefficients(p,h,stats):
 C=2**h;c=C-1;n=len(p);u=[(r&-r).bit_length() for r in range(1,C//2)]
 S,R=matching(p,u,stats,True);T=tails(S,c,stats);best=None
 for d in range(1,n-c):
  k=c+d;b=n-k;coef=[0]*n
  def add(a,sgn):
   for x,v in zip(a,u):coef[x]+=sgn*v;stats['coefficient_updates']+=1
  for i in range(b):add(R[i,i+k],1);add(R[i+1,i+k],-1)
  add(R[b,n],1);add(R[0,n],-1)
  assert sum(a*b for a,b in zip(p,coef))==T[d];stats['euler_identities']+=1
  x=max(range(n),key=coef.__getitem__);ratio=Fraction(coef[x]*d,(h-1)*d+C)
  if best is None or ratio>Fraction(*best['ratio']):best=dict(n=n,h=h,d=d,x=x,coefficient=coef[x],ratio=[ratio.numerator,ratio.denominator],p=p)
 stats['canonical_vectors']+=1
 return best


def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(37021);stats=Counter();best=None;canonical=None;rows=[]
 for n,h in [(10,3),(16,3),(32,4),(64,5)]:
  fixtures=[]
  if n==10:fixtures += [[0]+list(q)+[0] for q in product((0,1),repeat=8)]
  fixtures += [[1]*n,list(range(1,n+1)),list(range(n,0,-1))]
  for step in (2,3,4,5,7):fixtures.append([int(i%step==0) for i in range(n)])
  for _ in range(40):fixtures.append([rng.randrange(2**20) for i in range(n)])
  for _ in range(40):
   p=[0]*n
   for _ in range(rng.randrange(1,8)):p[rng.randrange(n)]+=rng.randrange(1,17)
   fixtures.append(p)
  for p in fixtures:
   row=coefficients(p,h,stats)
   if canonical is None or Fraction(*row['ratio'])>Fraction(*canonical['ratio']):
    canonical=row
    v=[(r&-r).bit_length()-1 for r in range(1,2**h)]
    ds=directional(p,v,row['x'],stats)
    for d in range(1,n-len(v)):
     ratio=Fraction(ds[d]*d,(h-1)*d+2**h)
     if best is None or ratio>Fraction(*best['ratio']):best=dict(n=n,h=h,d=d,x=row['x'],derivative=ds[d],ratio=[ratio.numerator,ratio.denominator],p=p.copy())
    print('new canonical',row['n'],row['h'],row['d'],row['x'],row['coefficient'],row['ratio'],'directional best',best['ratio'],flush=True)
  rows.append(dict(n=n,h=h,inputs=len(fixtures),canonical=canonical,directional=best))
 files=('key_tail_sensitivity.py','rank_matching_repair.py','rank_reward_tail.py','aggregate_core_audit.py')
 out=dict(scope='Canonical Euler coefficients and exact right directional derivatives; a falsification diagnostic for uniform per-key upper-tail sensitivity, not a proved upper bound.',seed=37021,checks=stats,canonical=canonical,directional=best,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/key_tail_sensitivity.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
