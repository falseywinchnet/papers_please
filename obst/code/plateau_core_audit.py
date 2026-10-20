#!/usr/bin/env python3
"""Exact controls for linear above-capacity support of one positive plateau."""
from pathlib import Path
from collections import Counter
import hashlib,json,random
from aggregate_core_audit import layers
from plateau_core import above_plateau_core,range_max_core

def nu(x):return (x&-x).bit_length()-1

def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(42203);stats=Counter();rows=[]
 for n in (*range(1,13),16,24,32,64):
  blocks=[(z,m) for m in range(1,n+1) for z in range(n-m+1)]
  if n==64:blocks=rng.sample(blocks,30)
  for z,m in blocks:
   alpha=1 if n<=16 else 3;p=[alpha*int(z<=i<z+m) for i in range(n)];q=[rng.randrange(4) for _ in range(n+1)]
   H=n.bit_length();M=(H+1)*(sum(p)+sum(q))+1
   for h,A in enumerate(layers(p,q,H,M,stats)):
    if not h:continue
    c=2**h-1
    if c>=n:continue
    v=[m+bin(r).count('1')-bin(r+m).count('1') for r in range(c-m+1)] if m<=c else []
    for r,x in enumerate(v):
     assert x==sum(nu(k) for k in range(r+1,r+m+1));stats['block_reward_controls']+=1
    edges=range_max_core(v,stats);assert len(edges)<=max(0,len(v)-2)
    literal=[]
    for a in range(len(v)):
     interior=-1
     for b in range(a+1,len(v)):
      if b-a>=2:
       D=min(v[a],v[b])-interior
       if D>0:literal.append((a,b,D))
      interior=max(interior,v[b]);stats['literal_visibility_pairs']+=1
    assert sorted(edges)==literal;stats['visibility_set_controls']+=1
    predicted={(z-b,c+z-1-a):alpha*D for a,b,D in edges if 0<=z-b<c+z-1-a<n}
    assert above_plateau_core(n,h,z,m,alpha,stats)==predicted;stats['linear_constructor_controls']+=1
    got={}
    for i in range(n):
     for j in range(i+c+1,n):
      D=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
      if D:got[i,j]=D
      if p[i] or p[j]:assert D==0;stats['positive_endpoint_zero_controls']+=1
      stats['original_density_controls']+=1
    assert got==predicted and len(got)<=max(0,c-m-1)
    stats['original_support_set_controls']+=1
    if n<=12:
     squares=[(a,b,s) for s in range(1,(n-c)//2+1) for a in range(n-c-2*s+1) for b in range(a+s+c,n-s+1)]
    else:
     squares=[]
     for _ in range(3):
      if n-c<2:continue
      s=rng.randrange(1,(n-c)//2+1);a=rng.randrange(n-c-2*s+1);b=rng.randrange(a+s+c,n-s+1)
      squares.append((a,b,s))
    for a,b,s in squares:
     assert sum(a<=i<a+s and b<=j<b+s for i,j in got)<=2*s-1
     stats['local_square_support_controls']+=1
  rows.append(dict(n=n,blocks=len(blocks)));print(n,len(blocks),flush=True)
 sharp=[]
 for h in range(3,15):
  C=2**h;c=C-1;v=[nu(r) for r in range(1,C)];edges=range_max_core(v,stats)
  assert len(edges)==C-2*h
  separate=Counter();constructed=above_plateau_core(2*C,h,C+1,1,1,separate)
  assert len(constructed)==C-2*h
  assert separate['stack_pushes']==c and separate['stack_pops']<=c and separate['visibility_candidates']<=2*c
  sharp.append(dict(h=h,n=2*C,m=1,above_core=len(edges),bound=c-2,constructor_counts=dict(separate),verification='linear core constructor; original all-root controls are in the smaller mixed cases'))
 files=('plateau_core_audit.py','plateau_core.py','aggregate_core_audit.py')
 out=dict(scope='Exact one-plateau above-capacity density support, including arbitrary nonnegative gap weights and positive endpoint cuts. No below-capacity support claim is made.',checks=stats,rows=rows,sharp_rows=sharp,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/plateau_core_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
