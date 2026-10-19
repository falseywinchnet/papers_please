#!/usr/bin/env python3
"""Independent matching representation, augmentation proof, and sharp-scale audit."""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib,json,random
from rank_reward_tail import scores,tails


def matching_scores(p,m,stats,witness=False):
 n=len(p);c=2*m+1;S=[[None]*(n+1) for _ in range(n+1)];R={}
 for i in range(n-c+1):
  prev=[None]*(m+1);prev[0]=0;older=prev.copy();paths=[None]*(m+1);paths[0]=();oldpaths=paths.copy()
  for j in range(i+3,n+1):
   cur=prev.copy();curpaths=paths.copy();x=j-2
   for r in range(1,m+1):
    stats['matching_transitions']+=1
    if older[r-1] is None:continue
    value=older[r-1]+p[x];path=oldpaths[r-1]+(x,) if witness else None
    if cur[r] is None or value>cur[r] or (witness and value==cur[r] and path<curpaths[r]):cur[r]=value;curpaths[r]=path
   older,prev=prev,cur;oldpaths,paths=paths,curpaths
   if j-i>=c:
    S[i][j]=prev[m];stats['matching_scores']+=1
    if witness:R[i,j]=paths[m]
 return S,R


def audit(p,c,stats,repair=True):
 n=len(p);m=(c-1)//2;v=[int(r%2==0) for r in range(1,c+1)];P=sum(p)
 S,_=scores(p,v,stats);Q,R=matching_scores(p,m,stats,repair)
 assert S==Q;stats['representation_inputs']+=1
 T=tails(S,c,stats)
 for d in range(1,n+1):
  assert d*T[d]<=P*(2*d+c-3),(p,c,d,T[d]);assert T[d]<=m*P;stats['tail_bound_checks']+=2
 for i in range(n):
  for j in range(i+c+1,n+1):
   d=j-i-c;delta=S[i][j]-S[i+1][j]
   assert 0<=d*delta<=(d-1)*p[i+1]+S[i][j];stats['endpoint_bounds']+=1
   if not repair:continue
   chosen=R[i,j]
   if i+1 not in chosen:assert delta==0;continue
   remaining=set(chosen)-{i+1};covered={z for e in remaining for z in (e,e+1)}
   free=[z for z in range(i+2,j) if z not in covered];assert len(free)==d+1
   losses=[];used=set()
   for a,b in zip(free,free[1:]):
    assert (b-a)%2==1
    removed=set(range(a+1,b,2));added=set(range(a,b,2));assert removed<=remaining;assert not used&removed;used|=removed
    new=sorted((remaining-removed)|added);assert len(new)==m and all(y-x>=2 for x,y in zip(new,new[1:]));assert new[0]>=i+2 and new[-1]<=j-2
    value=sum(p[x] for x in new);lost=sum(p[x] for x in removed)
    assert value>=S[i][j]-p[i+1]-lost and S[i+1][j]>=value
    losses.append(lost);stats['augmentation_paths']+=1
   assert d*min(losses)<=sum(p[x] for x in remaining);stats['augmentation_packings']+=1
 return T


def main():
 root=Path(__file__).resolve().parents[1];rng=random.Random(35214);stats=Counter();families=[]
 for n in range(4,10):
  for p in product((0,1),repeat=n):
   for c in range(3,n,2):audit(list(p),c,stats)
 for n in (10,12,16,24):
  for _ in range(25):
   c=rng.choice(list(range(3,n,2)));audit([rng.randrange(10) for _ in range(n)],c,stats)
 for n in (32,64,128):
  for _ in range(8):
   c=rng.choice(list(range(3,n,2)));audit([rng.randrange(20) for _ in range(n)],c,stats,False)
 for h in range(4,8):
  C=2**h;c=C-1;n=2*C
  for K in (3,4,5,8,12):
   if C<4*K:continue
   x=C-3*(K-1);p=[int(i>=x and i<=C and (i-x)%3==0) for i in range(n)]
   T=audit(p,c,stats,False);expected=(x+1)//2-1;assert T[K]==expected,(C,K,T[K],expected);stats['cluster_formulas']+=1
   S,_=matching_scores(p,(c-1)//2,stats);k=c+K;stop=n-k
   for i in range(stop):
    expected_delta=int((x-i)%2==1) if i<x else int(i+1 in range(x+3,C+1,3))
    assert S[i][i+k]-S[i+1][i+k]==expected_delta,(C,K,i);stats['cluster_endpoint_formulas']+=1
   assert S[stop][n]==sum(p[stop+1:]);assert S[0][n]==K;stats['cluster_end_formulas']+=2
   families.append(dict(h=h,C=C,K=K,n=n,P=sum(p),d=K,tail=T[K],verification='independent subsequence and matching DP'))
  print('height',h,'families verified',flush=True)
 for K in range(2,13):
  spacing=K+2;n=(K-1)*spacing+3;p=[int(i>=1 and (i-1)%spacing==0 and (i-1)//spacing<K) for i in range(n)]
  T=audit(p,3,stats,False);assert T[spacing-1]==K-1;stats['spaced_maximum_formulas']+=1
 p=[0]*10;p[3]=1;S,_=scores(p,[0,1,0,2,0,1,0],stats)
 assert (S[0][10],S[1][10])==(2,1)
 assert 3*(S[0][10]-S[1][10])>2*p[1]+S[0][10]
 stats['retained_rank_counterexamples']+=1
 for h in (8,16,32,64,128):
  C=2**h;K=2**(h//2);x=C-3*(K-1)
  families.append(dict(h=h,C=C,K=K,n=2*C,P=K,d=K,tail=(x+1)//2-1,verification='proved closed form only'))
 files=('alternating_tail_bound.py','rank_reward_tail.py','aggregate_core_audit.py')
 result=dict(scope='Audit of alternating-template matching representation, explicit augmentations, upper bound U_d<=P min((c-1)/2,2+(c-3)/d), and two necessary scales. Does not prove the full clipped-ruler or mixed tail estimate.',seed=35214,checks=stats,cluster_family=families,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/alternating_tail_bound.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
