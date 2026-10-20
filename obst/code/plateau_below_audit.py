#!/usr/bin/env python3
"""Independent all-root and literal top-sum audits for the below-plateau core."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib,json,random
from aggregate_core_audit import layers,partition
from plateau_below import below_plateau_core

def nu(x):return (x&-x).bit_length()-1

def top(p,k):return sum(sorted(p,reverse=True)[:k])

def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(522019);large=[]
 # Literal arbitrary templates first check the threshold expansion used in the proof.
 for length in range(3,10):
  for _ in range(12):
   v=[rng.randrange(7) for _ in range(length)]
   for m in range(1,length-1):
    f=top(v,m);literal=max(sum(v[i] for i in ss) for ss in combinations(range(length),m));assert f==literal
    delta=top(v[:-1],m)+top(v[1:],m)-f-top(v[1:-1],m)
    predicted=sum(v[0]>=r and v[-1]>=r and sum(x>=r for x in v[1:-1])==m-1 for r in range(1,8))
    assert delta==predicted;stats['literal_top_sum_controls']+=1
 # Every block in small inputs, with independent original all-root layers.
 fixtures=[(n,z,m) for n in range(1,18) for z in range(n) for m in range(1,n-z+1)]
 for n in (23,32,47,64):
  for _ in range(14):
   z=rng.randrange(n);fixtures.append((n,z,rng.randrange(1,n-z+1)))
 for n,z,m in fixtures:
  alpha=Fraction(3,2) if stats['inputs']%17==0 else 1
  p=[alpha if z<=i<z+m else 0 for i in range(n)];q=[0]*(n+1);H=2*n.bit_length();M=(H+1)*sum(p)+1
  for h,A in enumerate(layers(p,q,H,M,stats)):
   if h==0:continue
   c=2**h-1;core,kinds=below_plateau_core(n,h,z,m,alpha,stats,True);expected={}
   for i in range(n):
    for j in range(i+1,min(n,i+c)):
     d=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1];assert d>=0;stats['original_density_controls']+=1
     if d:expected[i,j]=d
   assert core==expected,(n,z,m,h,core,expected);stats['complete_core_controls']+=1
   # Full-block values are checked against literal top-m ruler windows at modest c.
   if c<=63:
    for i in range(z+1):
     for j in range(z+m,n+1):
      if j-i>c:continue
      a=z-i+1;b=c-j+z+m
      score=top([nu(t) for t in range(a,b+1)],m)
      assert A[i][j]==alpha*(h*m-score);stats['window_value_controls']+=1
   uniform=sum(max(0,m-2**r+1) for r in range(1,h))
   assert sum(k=='uniform' for k in kinds.values())==uniform
   assert len(core)<=2*(n-m)+uniform;stats['global_bound_controls']+=1
   N=1<<(n-1).bit_length()
   for s,tiles in partition(N,c)[0].items():
    for a,b in tiles:
     if b-a+s-1>=c:continue
     count=sum(a<=i<a+s and b<=j<b+s for i,j in core)
     assert count<=8*s;stats['local_tile_controls']+=1
  stats['inputs']+=1
 print('small',dict(stats),flush=True)
 # Larger sparse constructions: complete output checked by direct four top-sums for samples.
 for n in (1024,4096,16384,65536):
  for z,m in ((n//4,n//2),(n//2,1),(n//3,n//16),(0,n)):
   counts=Counter();total=0
   for h in range(1,2*n.bit_length()+1):
    core,kinds=below_plateau_core(n,h,z,m,1,counts,True);total+=len(core)
    uniform=sum(max(0,m-2**r+1) for r in range(1,h))
    assert len(core)<=2*(n-m)+uniform
    assert counts['below_full_candidates']<=z*h
    # Recheck each emitted coordinate's explicit divisibility identity, independently.
    c=2**h-1;e=z+m
    for (i,j),kind in core.items():
     if i<z and j>=e:
      U=z-i;V=c-j+e;d=(V-U)//m
      assert V-U==m*d and d>=2 and d&(d-1)==0 and U%d==V%d==0
     elif z<=i<j<e:assert (j-i+1)&(j-i)==0
     elif z<=i<e<=j:
      b=c+e-j;k=e-i;d=b//k;assert b==k*d and d>=2 and d&(d-1)==0
     elif i<z<=j<e:
      ii=n-1-j;jj=n-1-i;ee=n-z;b=c+ee-jj;k=ee-ii;d=b//k;assert b==k*d and d>=2 and d&(d-1)==0
     else:raise AssertionError((i,j,kind))
     counts['large_identity_controls']+=1
   large.append(dict(n=n,start=z,length=m,core_sum=total,counts=counts,verification='Sparse construction and explicit coordinate identities; no large original all-root reference'))
   print('large',n,z,m,total,flush=True)
 files=['plateau_below.py','plateau_below_audit.py','aggregate_core_audit.py']
 (root/'results/plateau_below_audit.json').write_text(json.dumps(dict(scope='Entire below-capacity core for a single equal key block, zero gaps. Proofs supply asymptotic bounds; controls distinguish independent recurrences from formula checks.',seed=522019,counts=stats,large=large,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files}),indent=2)+'\n')
if __name__=='__main__':main()
