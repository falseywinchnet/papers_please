#!/usr/bin/env python3
"""All-root audit of capacity maxima and the width-one interaction theorem."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random
from aggregate_core_audit import layers


def profile(w,stats,check=True):
 n=(len(w)-1)//2;p=w[:n];q=w[n:];W=sum(w);L=n.bit_length();M=(L+2)*W+1;rows=[]
 for h,A in enumerate(layers(p,q,L-1,M,stats)):
  if not h:continue
  c=2**h-1;tail=[0]*(n+1);potentials=0
  for i in range(n-c):
   walk=0;F=0;G=q[i+1]
   for r in range(1,(c+1)//2):
    walk+=((2*r&-2*r).bit_length()-1)*(p[i+2*r]-p[i+2*r-1])
    F=max(F,-walk);G=max(G,walk+q[i+2*r+1])
   delta=A[i][i+c+1]+A[i+1][i+c]-A[i][i+c]-A[i+1][i+c+1]
   assert delta==M-F-G;stats['capacity_identities']+=1;potentials+=F+G
  for i in range(n):
   for j in range(i+1,n):
    delta=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1];assert delta>=0
    distance=abs(j-i-c)
    if distance:tail[distance]+=delta
    stats['density_checks']+=1
  for d in range(n-1,0,-1):tail[d]+=tail[d+1]
  full=A[0][n]-M*(n-c);singles=sum(p)+2*sum(q)-q[0]-q[-1]
  assert tail[1]==full-singles+potentials;stats['total_identities']+=1
  rows.append(dict(tail=tail,full=full,potentials=potentials))
 stats['vectors']+=1;return rows


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(32219)
 counterexample=None;largest=Fraction(0);winner=None
 for n in (2,3,4,5,8,16,32):
  basis=[]
  for x in range(2*n+1):
   w=[0]*(2*n+1);w[x]=1;basis.append(profile(w,stats))
  fixtures=list(product((0,1),repeat=2*n+1)) if n<=5 else []
  fixtures += [[rng.randrange(16) for _ in range(2*n+1)] for _ in range(30)]
  fixtures += [[1]*(2*n+1),[1+int(i%2==0) for i in range(n)]+[1]*(n+1)]
  for w in fixtures:
   W=sum(w);P=sum(w[:n]);a=profile(w,stats)
   for h,row in enumerate(a,1):
    unitfull=sum(v*basis[x][h-1]['full'] for x,v in enumerate(w))
    unitpotential=sum(v*basis[x][h-1]['potentials'] for x,v in enumerate(w))
    fullgain=row['full']-unitfull
    assert 0<=fullgain<=(h-1)*P
    assert row['potentials']<=unitpotential;stats['subadditivity_checks']+=1
    for d in range(1,n+1):
     unit=sum(v*basis[x][h-1]['tail'][d] for x,v in enumerate(w))
     excess=row['tail'][d]-unit;stats['interaction_checks']+=1
     if d==1:
      assert excess<=fullgain;stats['width_one_checks']+=1
      if P and h>1 and Fraction(excess,(h-1)*P)>largest:
       largest=Fraction(excess,(h-1)*P);winner=dict(n=n,h=h,weights=w,excess=excess,full_gain=fullgain)
     elif excess>fullgain and counterexample is None:
      counterexample=dict(n=n,h=h,d=d,weights=w,tail=row['tail'][d],unit_tail=unit,
                          full_gain=fullgain,excess=excess,band_interaction=fullgain-excess)
  print(n,'checks complete',flush=True)
 result=dict(scope='Exact capacity identity and proved width-one interaction bound; wider-band superadditivity is tested separately.',
 checks=stats,maximum_width_one_ratio=[largest.numerator,largest.denominator],winner=winner,
 wider_band_counterexample=counterexample,
 source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in ('capacity_interaction.py','aggregate_core_audit.py')})
 (root/'results/capacity_interaction.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result),flush=True)
if __name__=='__main__':main()
