#!/usr/bin/env python3
"""Independent all-root checks of the full mixed boundary-mass identity."""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib,json,random
from aggregate_core_audit import layers


def val(t):return (t&-t).bit_length()-1


def audit(p,q,stats,family=False):
 n=len(p);P=sum(p);Q=sum(q);L=n.bit_length();M=(L+2)*(P+Q)+1;rows=[]
 for h,A in enumerate(layers(p,q,L,M,stats)):
  if not h:continue
  c=2**h-1
  if c>n:continue
  total=0
  for i in range(n-c):
   walk=0;gain=q[i+1]
   for r in range(1,(c+1)//2):
    walk+=val(2*r)*(p[i+2*r]-p[i+2*r-1]);gain=max(gain,walk+q[i+2*r+1])
   reward=sum(p[i+r-1]*val(r) for r in range(1,c+1))
   expected=h*(sum(p[i+1:i+c])+sum(q[i+1:i+c+1]))-reward-gain
   assert A[i+1][i+c]==expected;stats['one_slot_checks']+=1;total+=gain
  tail=sum(p[n-c+r-1]*val(r) for r in range(1,c+1))
  expected=(h-1)*P+(h-2)*Q+q[0]+q[-1]+total-tail
  mass=support=near=above=0
  for i in range(n):
   for j in range(i+1,n):
    d=A[i][j+1]+A[i+1][j]-A[i][j]-A[i+1][j+1]
    assert d>=0;stats['density_checks']+=1
    if j-i<c:mass+=d;support+=d>0
    if family and h>=2:
     if j-i==c-1:
      assert d==(c+1-h if i%2==0 else 0);near+=d;stats['near_boundary_checks']+=1
     elif j-i>c:
      assert d==(c-h if j-i==c+1 and i%2 else 0);above+=d>0;stats['above_boundary_checks']+=1
  assert mass==expected;stats['mass_identity_checks']+=1
  row=dict(h=h,c=c,below_mass=mass,below_support=support,near_boundary_mass=near,above_support=above)
  if family and h>=2:
   a=p[1];b=q[0]
   closed=(h-1)*n//2+(c-h)*(n-c-1)//2+(a+b)*((h-1)*n+h-c)
   assert mass==closed;stats['family_mass_checks']+=1
   if n==2**(h+1):
    assert near==(n//4+1)*(n//2-h)
    remainder=n*(2*h-5)//4+h+(a+b)*((h-1)*n+h-c)
    assert mass-near==remainder
    row['off_near_mass']=remainder;row['quadratic_layer']=True
  rows.append(row)
 stats['inputs']+=1
 return dict(n=n,p=p,q=q,rows=rows)


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(30219)
 for n in range(1,4):
  for w in product((0,1),repeat=2*n+1):audit(list(w[:n]),list(w[n:]),stats)
 for n in (4,5,7,8,15,16):
  for _ in range(20):audit([rng.randrange(16) for _ in range(n)],[rng.randrange(16) for _ in range(n+1)],stats)
 family=[]
 for n in (8,16,32,64,128):
  for a,b in ((0,0),(0,1),(1,1),(3,2)):
   family.append(audit([a+int(i%2==0) for i in range(n)],[b]*(n+1),stats,True))
 files=['mixed_boundary_mass.py','aggregate_core_audit.py']
 result=dict(scope='Exact mixed-weight mass identity and explicit bounded positive family; no generic tail-bound claim.',checks=stats,family=family,
 source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/mixed_boundary_mass.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
