#!/usr/bin/env python3
"""Independent one-sided tail diagnostics; no inferred general upper bound."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random
from aggregate_core_audit import layers


def profile(p,stats):
 n=len(p);q=[0]*(n+1);W=sum(p);L=n.bit_length();M=(L+2)*W+1;out=[]
 for h,A in enumerate(layers(p,q,L-1,M,stats)):
  if h==0:continue
  c=2**h-1;lower=[0]*(n+1);upper=[0]*(n+1)
  for i in range(n):
   for j in range(i+1,n):
    value=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1];assert value>=0
    distance=j-i-c
    if distance>0:upper[distance]+=value
    elif distance<0:lower[-distance]+=value
    stats['densities']+=1
  for d in range(n-1,0,-1):lower[d]+=lower[d+1];upper[d]+=upper[d+1]
  out.append(dict(lower=lower,upper=upper,reward=h*W-(A[0][n]-M*(n-c))))
 stats['vectors']+=1;return out


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(33219)
 first=None;maximum=Fraction(0);winner=None;rows=[]
 for n in (4,5,6,7,8,9,10,16,32,64):
  basis=[]
  for x in range(n):
   p=[0]*n;p[x]=1;basis.append(profile(p,stats))
  fixtures=list(product((0,1),repeat=n)) if n<=10 else []
  fixtures += [[rng.randrange(16) for _ in range(n)] for _ in range(80 if n<=32 else 20)]
  fixtures += [[1]*n,[int(i%2==0) for i in range(n)],[i+1 for i in range(n)]]
  for p in fixtures:
   P=sum(p)
   if not P:continue
   for h,a in enumerate(profile(p,stats),1):
    independent=sum(v*basis[x][h-1]['reward'] for x,v in enumerate(p));loss=independent-a['reward'];assert loss>=0
    for d in range(1,n+1):
     upperunit=sum(v*basis[x][h-1]['upper'][d] for x,v in enumerate(p))
     excess=a['upper'][d]-upperunit
     stats['inequalities']+=1
     if excess>loss:
      r=Fraction(excess-loss,P)
      if first is None:first=dict(n=n,h=h,d=d,p=p,mass=a['upper'][d],unit_mass=upperunit,reward_loss=loss)
      if r>maximum:maximum=r;winner=dict(n=n,h=h,d=d,p=p,mass=a['upper'][d],unit_mass=upperunit,reward_loss=loss,ratio=[r.numerator,r.denominator])
  print(n,'max violation/P',str(maximum),flush=True)
 result=dict(scope='Falsification of above-tail interaction <= full skeleton reward loss; all-root recurrence only.',checks=stats,
 first_counterexample=first,maximum_ratio=[maximum.numerator,maximum.denominator],winner=winner,
 source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in ('one_sided_interaction.py','aggregate_core_audit.py')})
 (root/'results/one_sided_interaction.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
