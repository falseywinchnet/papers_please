#!/usr/bin/env python3
"""Independent dense, literal, and original-layer controls for band dominance."""
from pathlib import Path
from collections import Counter
from itertools import product,combinations
import hashlib,json,random
from band_dominance import dominance,two_block_interior,band_matrix,prefix_matrix
from core_monge import Monge,multiply
from aggregate_core_audit import layers

def dense_core(A):
 p=len(A);q=len(A[0]);out={}
 for i in range(p-1):
  for j in range(q-1):
   d=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
   assert d>=0
   if d:out[i,j]=d
 return out

def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(43117);stats=Counter();rows=[]
 fixtures=[]
 for n in range(1,5):
  for F in product((0,1),repeat=n):
   for G in product((0,1),repeat=n):
    for g in range(n):fixtures.append((list(F),list(G),g))
 for n in (5,8,12,16):
  for _ in range(20):fixtures.append(([rng.randrange(-9,10) for _ in range(n)],[rng.randrange(-9,10) for _ in range(n)],rng.randrange(n+2)))
 for F,G,g in fixtures:
  n=len(F);T=dominance(F,G,g,stats);Q,K=band_matrix(F,G,g,stats)
  dense=[[K*(max(u-v,0)+max(v-u-g,0))-F[u]-G[v] for v in range(n)] for u in range(n)]
  assert dense_core(dense)=={(i,j):v for i,j,v in Q.entries}
  for A in range(n):
   for B in range(n):
    best=min(K*max(u-A,0)+dense[u][v]+K*max(B-v,0) for u in range(n) for v in range(n))
    stats['literal_product_candidates']+=n*n
    assert T.value_reference(A,B)==best;stats['finite_product_entry_controls']+=1
    if B<=A+g:
     reward=max(F[u]+G[v] for u in range(A+1) for v in range(B,n) if 0<=v-u<=g)
     assert best==-reward;stats['feasible_score_controls']+=1
  for _ in range(3):
   a=rng.randrange(n);aa=rng.randrange(a,n);b=rng.randrange(n);bb=rng.randrange(b,n)
   rg=[list(range(a+1))]+[[x] for x in range(a+1,aa+1)]
   cg=[[x] for x in range(b,bb)]+[list(range(bb,n))]
   small=[[min(dense[u][v] for u in rr for v in cc) for cc in cg] for rr in rg]
   core=dense_core(small)
   assert len(core)<=2*max(0,min(len(rg)-2,len(cg)-2))+max(0,len(rg)-1)+max(0,len(cg)-1)
   Qsmall=Monge(small[0],[row[0] for row in small],[(i,j,v) for (i,j),v in core.items()],stats)
   left,_=multiply(prefix_matrix(len(rg),K,stats),Qsmall)
   local,_=multiply(left,prefix_matrix(len(cg),K,stats))
   for x in range(len(rg)):
    for y in range(len(cg)):
     if b+y<=a+x+g:
      assert local.value_reference(x,y)==T.value_reference(a+x,b+y)
      stats['coarsened_product_entry_controls']+=1
   stats['coarsened_band_core_controls']+=1
  stats['generic_band_inputs']+=1
 print('generic band',stats['generic_band_inputs'],flush=True)
 for n in (7,8,10,12,16,24,32):
  for _ in range(24):
   m=rng.randrange(1,max(2,n//4));k=rng.randrange(1,max(2,n//4));g=rng.randrange(n-m-k+1);z=rng.randrange(n-m-k-g+1)
   p=[int(z<=i<z+m or z+m+g<=i<z+m+g+k) for i in range(n)]
   q=[rng.randrange(4) for _ in range(n+1)];H=n.bit_length();M=(H+1)*(sum(p)+sum(q))+1
   for h,A in enumerate(layers(p,q,H,M,stats)):
    if not h or 2**h-1>=n:continue
    c=2**h-1;got={}
    for i in range(z):
     for j in range(max(i+c+1,z+m+g+k),n):
      D=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
      if D:got[i,j]=D
      stats['original_interior_density_controls']+=1
    predicted=two_block_interior(n,h,z,m,g,k,stats)
    assert predicted==got;stats['original_interior_support_sets']+=1
    if n<=10 and m+k<=c:
     for i in range(z+1):
      for j in range(max(i+c,z+m+g+k),n+1):
       best=max(sum(p[x]*((r&-r).bit_length()-1) for r,x in enumerate(ts,1)) for ts in combinations(range(i,j),c))
       assert A[i][j]==M*(j-i-c)+h*(sum(p[i:j])+sum(q[i:j+1]))-best
       stats['literal_subsequence_intervals']+=1
       from math import comb
       stats['literal_subsequence_choices']+=comb(j-i,c)
    for side in range(1,n//2+1):
     if z<side or n-(z+m+g+k)<side:continue
     for _ in range(2):
      a=rng.randrange(z-side+1);b=rng.randrange(z+m+g+k,n-side+1)
      if b-a-side+1<=c:continue
      assert sum(a<=i<a+side and b<=j<b+side for i,j in got)<=22*side
      stats['local_square_controls']+=1
   stats['mixed_two_block_inputs']+=1
  print('mixed',n,flush=True)
 for h in range(5,13):
  C=2**h;n=4*C;z=C
  for m,k,g in ((1,1,C//2),(3,5,C//3),(C//8,C//4,C//2)):
   separate=Counter();out=two_block_interior(n,h,z,m,g,k,separate)
   for side in (32,64,128,256,512):
    if side>z or side>n-(z+m+g+k):continue
    for _ in range(8):
     a=rng.randrange(z-side+1);b=rng.randrange(z+m+g+k,n-side+1)
     if b-a-side+1<=C-1:continue
     assert sum(a<=i<a+side and b<=j<b+side for i,j in out)<=22*side
     separate['large_constructed_square_controls']+=1
   rows.append(dict(h=h,n=n,m=m,k=k,g=g,core=len(out),bound=14*(C-m-k-1),counts=dict(separate),verification='condensed product construction; original-layer controls are the smaller mixed cases'))
  print('scale',h,flush=True)
 files=('band_dominance.py','band_dominance_audit.py','core_monge.py','plateau_core.py','aggregate_core_audit.py')
 result=dict(scope='Two-block interior density construction, finite band factorization, and local boundary bound; partial positive-block endpoints are outside the theorem.',checks=stats,scale_rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/band_dominance_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
