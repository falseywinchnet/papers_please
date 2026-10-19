#!/usr/bin/env python3
"""Exact unit-gap densities and the union of all unit-outcome supports."""
from pathlib import Path
from collections import Counter
import hashlib,json
from aggregate_core_audit import layers,partition
from one_key_square import support


def power(z):return z>0 and z&(z-1)==0

def envelope(i,j,h):
 c=2**h-1;k=j-i
 if k==c:return False
 g=abs(k-c)
 return power(g+1) or (k<c and power(g+2))

def gap_density(i,j,x,h):
 c=2**h-1;g=c-(j-i)
 assert g!=0
 if g<0:return 0
 if x in (i,j+1):return int(power(g+1))
 if i<x<=j and power(g+2):
  D=g+2
  return int((x-i-1)%D==D//2)
 return 0

def diagonal_count(a,b,s,k):
 # j-i=k in [a,a+s) x [b,b+s).
 return max(0,min(a+s,b+s-k)-max(a,b-k))

def envelope_count(a,b,s,h):
 c=2**h-1
 ks=set()
 for r in range(1,max(h,(b+s-a).bit_length())+2):
  D=2**r
  ks.update((c-D+1,c+D-1,c-D+2))
 return sum(diagonal_count(a,b,s,k) for k in ks if k>0 and k!=c)

def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rows=[];largest=[0,1]
 for n in (1,2,3,4,5,7,8,9,15,16,17,24,31,32):
  H=n.bit_length()+1
  for x in range(n+1):
   p=[0]*n;q=[int(t==x) for t in range(n+1)]
   for h,A in enumerate(layers(p,q,H,H+2,stats)):
    if not h:continue
    c=2**h-1
    for i in range(n):
     for j in range(i+1,n):
      if j-i==c:continue
      D=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
      assert D==gap_density(i,j,x,h),(n,h,x,i,j,D,gap_density(i,j,x,h))
      assert not D or envelope(i,j,h);stats['unit_gap_density_controls']+=1
  rows.append(dict(n=n,H=H,gap_positions=n+1))
 for n in (8,16,32,64,128,256,512,1024):
  for h in range(1,n.bit_length()):
   ts,_=partition(n,2**h-1)
   for s,anchors in ts.items():
    for a,b in anchors:
     K=envelope_count(a,b,s,h)
     assert K<=2*s;stats['maximal_envelope_controls']+=1
     if K*largest[1]>largest[0]*s:largest=[K,s]
     if n<=32:
      literal=sum(envelope(i,j,h) for i in range(a,a+s) for j in range(b,b+s))
      assert literal==K;stats['literal_envelope_counts']+=1
   if n<=32:
    for x in range(n):
     assert all(envelope(i,j,h) for i,j in support(n,h,x));stats['unit_key_support_controls']+=1
   if n<=16:
    for s in range(1,n+1):
     for a in range(n-s+1):
      for b in range(a+s,n-s+1):
       c=2**h-1
       if b-a-s+1<=c<=b-a+s-1:continue
       K=envelope_count(a,b,s,h);assert K<=8*s;stats['arbitrary_square_controls']+=1
 files=('unit_support_envelope.py','one_key_square.py','aggregate_core_audit.py')
 out=dict(scope='Exact all-root unit-gap density classification and geometric envelope counts. No bound on interaction support is assumed.',checks=stats,rows=rows,largest_observed_envelope_to_side=largest,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/unit_support_envelope.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(stats),largest,flush=True)
if __name__=='__main__':main()
