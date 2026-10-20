#!/usr/bin/env python3
"""Audit the logarithmic-side single-key square support bound."""
from collections import Counter
from pathlib import Path
import hashlib,json
from aggregate_core_audit import partition,layers


def support(n,h,x):
 C=2**h;c=C-1;out=set()
 for r in range(1,h):
  step=2**r
  for a in range(0,C,step):
   b=a+step;i=x-a;j=c+x+1-b
   if 0<=i<j<n:out.add((i,j))
   if a>0 and b<C:
    i=x+1-b;j=c+x-a
    if 0<=i<j<n:out.add((i,j))
 return out


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();maxima={};rows=[]
 for n in (4,7,8,15,16,31,32,63,64,127,128):
  N=1<<(n-1).bit_length();L=n.bit_length()
  maps={}
  for h in range(1,L):
   ts,_=partition(N,2**h-1);flat=[(a,b,s) for s,ab in ts.items() for a,b in ab];owner={}
   for idx,(a,b,s) in enumerate(flat):
    for i in range(a,a+s):
     for j in range(b,b+s):owner[i,j]=idx
   maps[h]=flat,owner
  for x in range(n):
   actual=list(layers([int(i==x) for i in range(N)],[0]*(N+1),L-1,N+2,stats)) if n<=16 else None
   for h in range(1,L):
    c=2**h-1;cells=support(N,h,x);flat,owner=maps[h];counts=Counter(owner[z] for z in cells)
    if actual:
     A=actual[h]
     observed={(i,j) for i in range(N) for j in range(i+1,N) if j-i!=c and A[i][j+1]+A[i+1][j]>A[i][j]+A[i+1][j+1]}
     assert observed==cells;stats['all_root_support_controls']+=1
    for idx,(a,b,s) in enumerate(flat):
     K=counts[idx];assert K<=s.bit_length() and K<=s;stats['maximal_square_checks']+=1
     if K>maxima.get(s,0):maxima[s]=K
    if n<=8:
     for s in range(1,N+1):
      for a in range(N-s+1):
       for b in range(a+s,N-s+1):
        if b-a-s+1<=c<=b-a+s-1:continue
        K=sum(a<=i<a+s and b<=j<b+s for i,j in cells)
        assert K<=s.bit_length();stats['arbitrary_square_checks']+=1
  rows.append(dict(n=n,all_key_positions=n,independent_all_root=n<=16))
 files=('one_key_square.py','aggregate_core_audit.py')
 out=dict(scope='Closed-form ruler-pair square counts, independent all-root support sets on small inputs, and literal non-dyadic square controls. The general boundary-plus-mass bound is not assumed.',checks=stats,maxima_by_side=maxima,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/one_key_square.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(stats),maxima,flush=True)
if __name__=='__main__':main()
