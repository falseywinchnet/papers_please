#!/usr/bin/env python3
"""All-root audit of every above-capacity density for two positive blocks."""
from pathlib import Path
from collections import Counter
from itertools import combinations
import hashlib,json,random
from aggregate_core_audit import layers
from band_dominance import two_block_above_core

def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(43219);stats=Counter();rows=[]
 fixtures=[]
 for n in range(3,11):
  for z,end,second,last in combinations(range(n+1),4):fixtures.append((n,z,end-z,second-end,last-second,1))
 for n in (12,16,24,32,64):
  for _ in range(32):
   m=rng.randrange(1,max(2,n//3));k=rng.randrange(1,max(2,n//3));g=rng.randrange(n-m-k+1);z=rng.randrange(n-m-k-g+1)
   fixtures.append((n,z,m,g,k,3))
 for n,z,m,g,k,alpha in fixtures:
  p=[alpha*int(z<=i<z+m or z+m+g<=i<z+m+g+k) for i in range(n)]
  q=[rng.randrange(4) for _ in range(n+1)];H=n.bit_length();M=(H+1)*(sum(p)+sum(q))+1
  for h,A in enumerate(layers(p,q,H,M,stats)):
   if not h or 2**h-1>=n:continue
   c=2**h-1;reference={}
   for i in range(n):
    for j in range(i+c+1,n):
     D=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
     if D:reference[i,j]=D
     stats['original_above_density_controls']+=1
   got=two_block_above_core(n,h,z,m,g,k,alpha,stats)
   assert got==reference,(n,h,z,m,g,k,got,reference)
   assert len(got)<=28*n;stats['full_above_support_set_controls']+=1
  stats['mixed_inputs']+=1
 print('original controls complete',dict(stats),flush=True)
 for h in range(5,12):
  C=2**h;n=4*C;z=C
  for m,k,g in ((1,1,C//2),(C//8,C//4,C//2)):
   counts=Counter();out=two_block_above_core(n,h,z,m,g,k,1,counts)
   for s in (64,128,256,512):
    if 2*s+C-1>n:continue
    for _ in range(24):
     a=rng.randrange(n-(C-1)-2*s+1);b=rng.randrange(a+s+C-1,n-s+1)
     assert sum(a<=i<a+s and b<=j<b+s for i,j in out)<=40*s
     counts['large_local_square_controls']+=1
   rows.append(dict(h=h,n=n,z=z,m=m,k=k,g=g,core=len(out),bound=28*n,counts=dict(counts),verification='full sparse constructor; independent original all-root controls are restricted to n<=64'))
  print('full scale',h,flush=True)
 files=('two_block_core_audit.py','band_dominance.py','core_monge.py','plateau_core.py','aggregate_core_audit.py')
 out=dict(scope='Exact complete above-capacity core for two equal positive blocks, including all endpoint cuts and arbitrary nonzero gaps. No below-capacity or unrestricted-OBST shortcut is asserted.',checks=stats,scale_rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/two_block_core_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
