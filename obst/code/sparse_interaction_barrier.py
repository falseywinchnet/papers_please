#!/usr/bin/env python3
"""All-root and exact slot checks of the explicit two-key tail barrier."""
from collections import Counter
from pathlib import Path
import hashlib,json
from aggregate_core_audit import layers


def val(t):return (t&-t).bit_length()-1


def defect(C,a,r,above,stats):
 c=C-1
 if above:
  one=[(u,r-u) for u in range(a+1) if 1<=r-u<=c]
  two=[(u,r+5-u) for u in range(a+1) if 1<=r+5-u<=c]
 else:
  one=[(u,r+u) for u in range(a+1)]
  two=[(u,r+5+u) for u in range(a+1)]
 independent=max(val(t) for u,t in one)+max(val(t) for u,t in two)
 best=-1
 for u,s in one:
  for z,t in two:
   if u<=z and s<t:best=max(best,val(s)+val(t));stats['slot_pairs']+=1
 assert best>=0;stats['slot_defects']+=1
 return independent-best


def table(C,h,a,r,above):
 if not above:
  pattern=(1,1,2,0,2,1,1,0) if a==3 else (1,1,1,1,1,1,0,0,1,1,2,2,1,1,0,0)
  return pattern[(r-1)%len(pattern)]
 if a==3:
  value=3 if r%8==3 else 2 if r%8==7 else 0
  return value-2*int(r in (3,C-5))
 k=r//8;res=r%8
 if res not in (3,4):return 0
 A=h if k==0 else val(8*k);B=h if 8*k+8==C else val(8*k+8)
 value=min(A,B-2) if res==3 else min(A-2,B)
 return value-3*int(r in (4,C-5))


def full_layer(p,h,stats):
 n=len(p);M=(h+2)*sum(p)+1
 A=list(layers(p,[0]*(n+1),h,M,stats))[-1]
 return A,M


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rows=[]
 for h in range(5,13):
  C=2**h;n=2*C;c=C-1;x=C-5;y=C;sums=[]
  for above,a in ((False,3),(False,4),(True,3),(True,4)):
   total=0;limit=C-4 if above else C-6-a
   for r in range(1,limit+1):
    actual=defect(C,a,r,above,stats);assert actual==table(C,h,a,r,above),(h,a,r,above,actual)
    total+=actual;stats['table_checks']+=1
   sums.append(total)
  expected=[C-8,7*C//8-8,5*C//8-6,7*C//16-6]
  assert sums==expected;excess=h-3+sums[0]-sums[1]+sums[2]-sums[3]
  assert excess==5*C//16+h-3;stats['summation_checks']+=1
  unit=C-4*h+4;pair=21*C//16-3*h+1
  if h<=7:
   ps=[]
   for support in ((x,y),(x,),(y,)):
    p=[0]*n
    for z in support:p[z]=1
    ps.append(full_layer(p,h,stats))
   def E(i,j):return sum(sign*(A[i][j]-M*max(0,j-i-c)) for sign,(A,M) in zip((1,-1,-1),ps))
   assert E(0,n)==h-3
   tails=[];sides=[]
   for A,M in ps:
    total=0;lower=0;upper=0
    for i in range(n):
     for j in range(i+1,n):
      if abs(j-i-c)<4:continue
      d=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1];assert d>=0;total+=d;stats['density_checks']+=1
      if j-i<c:lower+=d
      else:upper+=d
    tails.append(total);sides.append((lower,upper))
   assert sides[0][0]-sides[1][0]-sides[2][0]==C//8
   assert sides[0][1]-sides[1][1]-sides[2][1]==3*C//16+h-3
   stats['one_sided_family_checks']+=2
   assert tails[0]==pair and sum(tails[1:])==unit and tails[0]-sum(tails[1:])==excess
   for above,a in ((False,3),(False,4),(True,3),(True,4)):
    length=c+a if above else c-a
    for i in range(n-length+1):
     want=defect(C,a,x-i+1,above,stats) if i<=x and i+length>y else 0
     assert E(i,i+length)==want;stats['independent_band_entries']+=1
   stats['independent_family_checks']+=1
  rows.append(dict(h=h,n=n,W=2,positions=[x,y],d=4,band_sums=sums,full_interaction=h-3,
                   pair_tail=pair,unit_tail=unit,interaction=excess,lower_interaction=C//8,upper_interaction=3*C//16+h-3,proposed_allowance=2*h,
                   verification='independent all-root layers and literal slot choices' if h<=7 else 'literal slot choices and closed-form summation'))
  print(h,'interaction',excess,'allowance',2*h,flush=True)
 for h in (16,32,64,128):
  C=2**h;rows.append(dict(h=h,n=2*C,W=2,positions=[C-5,C],d=4,pair_tail=21*C//16-3*h+1,
   unit_tail=C-4*h+4,interaction=5*C//16+h-3,proposed_allowance=2*h,verification='closed-form evaluation only'))
 files=('sparse_interaction_barrier.py','aggregate_core_audit.py')
 result=dict(scope='Proved two-key obstruction to every O(hW) additive unit-tail allowance; the broader O(W(L+c/d)) target is not contradicted.',
 checks=stats,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/sparse_interaction_barrier.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
