#!/usr/bin/env python3
"""Falsify a proposed additive interaction allowance; all-root arithmetic only."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random
from aggregate_core_audit import layers


def tails(w,stats):
 n=(len(w)-1)//2;L=n.bit_length();W=sum(w);M=(L+2)*W+1;out=[]
 for h,A in enumerate(layers(w[:n],w[n:],L-1,M,stats)):
  if not h:continue
  c=2**h-1;mass=[0]*(n+1)
  for i in range(n):
   for j in range(i+1,n):
    delta=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1];assert delta>=0
    d=abs(j-i-c)
    if d:mass[d]+=delta
  for d in range(n-1,0,-1):mass[d]+=mass[d+1]
  out.append(mass)
 stats['vectors']+=1;return out


def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(31219);stats=Counter();best=Fraction(0);winner=None
 for n in (4,5,8,16,32):
  basis=[]
  for i in range(2*n+1):
   w=[0]*(2*n+1);w[i]=1;basis.append(tails(w,stats))
  fixtures=list(product((0,1),repeat=2*n+1)) if n<=5 else []
  fixtures += [[rng.randrange(8) for _ in range(2*n+1)] for _ in range(80)]
  fixtures += [[1]*(2*n+1),[1+int(i%2==0) for i in range(n)]+[1]*(n+1)]
  for w in fixtures:
   W=sum(w)
   if not W:continue
   tt=tails(w,stats)
   for h,a in enumerate(tt,1):
    for d in range(1,n+1):
     unit=sum(v*basis[i][h-1][d] for i,v in enumerate(w));excess=a[d]-unit;ratio=Fraction(excess,h*W)
     stats['interaction_checks']+=1
     if ratio>best:best=ratio;winner=dict(n=n,h=h,d=d,W=W,mass=a[d],unit_mass=unit,ratio=[ratio.numerator,ratio.denominator],weights=w)
  print(n,'maximum interaction / hW',str(best),flush=True)
 result=dict(scope='Diagnostic of T(w)<=sum_x w_x*T(e_x)+hW; this inequality is unproved.',checks=stats,
 maximum_ratio=[best.numerator,best.denominator],winner=winner,
 source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in ('core_tail_interaction.py','aggregate_core_audit.py')})
 (root/'results/core_tail_interaction.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
