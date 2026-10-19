#!/usr/bin/env python3
"""Exact full mixed penalty layers restricted to a capacity band."""
from collections import Counter


def solve(p,q,width,H=None,counts=None):
 n=len(p)
 if n<1 or len(q)!=n+1 or width<0 or any(not isinstance(x,int) or x<0 for x in [*p,*q]):raise ValueError('nonnegative integer weights and nonempty key array required')
 if H is None:H=n.bit_length()
 if H<1:raise ValueError('positive height required')
 if counts is None:counts=Counter()
 W=sum(p)+sum(q);M=(H+1)*W+1;prefix=[0]
 for a,b in zip(p,q[1:]):prefix.append(prefix[-1]+a+b)
 counts['prefix_steps']+=n
 base=dict(h=0,c=0,lo=0,hi=min(n,width),cost=[],root=[])
 for k in range(base['hi']+1):base['cost'].append([M*k]*(n-k+1));counts['base_entries']+=n-k+1
 result=[base]
 def get(level,i,k):
  if k==0:return 0
  assert level['lo']<=k<=level['hi'],(level['h'],i,k,width)
  return level['cost'][k-level['lo']][i]
 for h in range(1,H+1):
  c=(1<<h)-1;half=(c-1)//2;lo=max(1,c-width);hi=min(n,c+width)
  if lo>hi:break
  prev=result[-1];cur=dict(h=h,c=c,lo=lo,hi=hi,cost=[],root=[]);start=counts['root_candidates']
  for k in range(lo,hi+1):
   values=[];roots=[]
   for i in range(n-k+1):
    j=i+k
    leftlo=max(0,k-1-half) if k<=c else half
    lefthi=min(half,k-1) if k<=c else k-1-half
    rl=i+leftlo;rr=i+lefthi
    if k>lo:
     lower=cur['root'][-1];rl=max(rl,lower[i]);rr=min(rr,lower[i+1])
    assert rl<=rr
    best=None;arg=None
    for r in range(rl,rr+1):
     v=get(prev,i,r-i)+get(prev,r+1,j-r-1);counts['root_candidates']+=1
     if best is None or v<best:best=v;arg=r
    values.append(best+prefix[j]-prefix[i]+q[i]);roots.append(arg);counts['band_states']+=1
   cur['cost'].append(values);cur['root'].append(roots)
  used=counts['root_candidates']-start
  assert used<=n*(width+1)+2*n*(hi-lo)
  counts['layer_bound_checks']+=1;result.append(cur)
 return dict(n=n,width=width,H=H,penalty=M,layers=result)


def reconstruct(result,i=0,j=None,h=None):
 if j is None:j=result['n']
 if h is None:h=len(result['layers'])-1
 if i==j:return None
 if h==0:raise ValueError('state is not fully exposed')
 level=result['layers'][h];k=j-i
 if k>level['c']:raise ValueError('state is not fully exposed')
 if not level['lo']<=k<=level['hi']:raise ValueError('interval is outside the stored band')
 r=level['root'][k-level['lo']][i]
 return (r,reconstruct(result,i,r,h-1),reconstruct(result,r+1,j,h-1))
