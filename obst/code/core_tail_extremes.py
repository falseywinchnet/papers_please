#!/usr/bin/env python3
"""Exact lower families for both terms of the unproved global tail estimate."""
from collections import Counter
from pathlib import Path
from fractions import Fraction
import hashlib,json
from aggregate_core_audit import layers


def single_tail(h,d):
 r=(d+1-1).bit_length()  # ceil(log2(d+1)) = bit_length(d)
 if r>=h:return 0
 return (1<<(h-r+2))-2*(h-r)-4


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rows=[]
 for h in range(2,7):
  n=1<<(h+1);c=(1<<h)-1;L=n.bit_length()
  for mode in ('single_key','uniform_mixed'):
   p=[1]*n if mode=='uniform_mixed' else [0]*n;q=[1]*(n+1) if mode=='uniform_mixed' else [0]*(n+1)
   if mode=='single_key':p[(1<<h)+1]=1
   W=sum(p)+sum(q);M=(h+2)*W+1
   for A in layers(p,q,h,M,stats):pass
   tail=[0]*(n+1);support=[0]*(n+1)
   for i in range(n):
    for j in range(i+1,n):
     v=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1];assert v>=0;stats['density_checks']+=1
     d=abs(j-i-c)
     if d:tail[d]+=v;support[d]+=v>0
   for d in range(n-1,0,-1):tail[d]+=tail[d+1];support[d]+=support[d+1]
   for d in range(1,n+1):
    if mode=='single_key':
     expected=single_tail(h,d);assert tail[d]==expected==support[d]
     assert tail[d]*(d+1)<=4*(c+1)
    else:
     expected=2*sum(n-((1<<r)-1) for r in range(1,h) if c-((1<<r)-1)>=d)
     assert tail[d]==expected
    stats['tail_formula_checks']+=1
   d=(1<<(h//2))-1 if mode=='single_key' else 1<<(h-1)
   rows.append(dict(h=h,n=n,c=c,d=d,W=W,mass=tail[d],verification='independent all-root recurrence'))
 for r in (4,8,12,16,24,32,48,64):
  h=2*r;n=1<<(h+1);c=(1<<h)-1;d=(1<<r)-1;L=h+2
  mass=single_tail(h,d);assert mass==4*(1<<r)-2*r-4
  ratio=Fraction(mass*d,L*d+c);assert ratio==Fraction(4*(1<<r)-2*r-4,(1<<r)+2*r+3)
  rows.append(dict(family='single_key_limit',h=h,n=n,c=c,d=d,W=1,mass=mass,ratio=[ratio.numerator,ratio.denominator],verification='closed-form evaluation only'))
  d=1<<(h-1);mass=2*((h-1)*n+h-c);W=2*n+1
  rows.append(dict(family='uniform_mixed_limit',h=h,n=n,c=c,d=d,W=W,mass=mass,ratio_to_WL=[mass,W*L],verification='closed-form evaluation only'))
 files=['core_tail_extremes.py','aggregate_core_audit.py']
 result=dict(scope='Proved lower families and one-key upper bound; not a universal mixed tail upper bound.',checks=stats,rows=rows,
 source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/core_tail_extremes.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
