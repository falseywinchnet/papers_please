"""Exact below-capacity ordinary core for one positive key plateau, zero gaps.

Uses ruler divisibility events, not a dense interval table. All returned
nonzero densities equal the common plateau weight. This is a layer-core
constructor, not a new solver for general mixed-weight optimal BSTs.
"""
from collections import Counter

def below_plateau_core(n,h,start,length,weight=1,stats=None,regions=False):
 if stats is None:stats=Counter()
 assert n>=1 and h>=1 and 0<=start<n and 1<=length<=n-start and weight>=0
 z=start;m=length;e=z+m;c=2**h-1;out={};kinds={}
 if not weight:return (out,kinds) if regions else out
 def emit(i,j,kind):
  assert 0<=i<j<n and j-i<c
  assert (i,j) not in out,(i,j,kind,kinds.get((i,j)))
  out[i,j]=weight;kinds[i,j]=kind;stats['below_'+kind+'_outputs']+=1
 # Four intervals contain the whole plateau. Ruler endpoints U,V differ by m*2^r.
 d=2
 while d<=z and d<=c:
  lo=max(1,c+e-n+1-m*d);hi=min(z,c-m*d)
  first=((lo+d-1)//d)*d
  stats['below_full_scales']+=1
  for U in range(first,hi+1,d):
   V=U+m*d;i=z-U;j=c+e-V;stats['below_full_candidates']+=1
   if 0<=i<j<n and i<z and j>=e and j-i<c:emit(i,j,'full')
  d*=2
 # A positive left endpoint and a zero right endpoint, then its reflection.
 for reflected in (False,True):
  stop=(n-z) if reflected else e
  limit=min(n-stop,c)
  vals=[0]*(limit+1)
  for t in range(1,limit+1):
   vals[t]=0 if t%2 else vals[t//2]+1;stats['below_ruler_updates']+=1
   j=stop+t-1;b=c-t+1;local=b
   for r in range(1,vals[t]+1):
    assert local%2==0;local//=2;stats['below_partial_candidates']+=1
    if 1<=local<=m:
     i=stop-local
     if reflected:emit(n-1-j,n-1-i,'right')
     else:emit(i,j,'left')
 # Both changed endpoint keys are positive: ordinary uniform-tree density.
 d=2
 while d<=m and d<=c:
  k=d-1;stats['below_uniform_scales']+=1
  for i in range(z,e-k):emit(i,i+k,'uniform')
  d*=2
 stats['below_total_outputs']+=len(out)
 return (out,kinds) if regions else out
