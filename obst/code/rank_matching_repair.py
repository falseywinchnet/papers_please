#!/usr/bin/env python3
"""Exact retained-rank accounting for endpoint augmentations of ruler matchings."""
from collections import Counter
from fractions import Fraction
from itertools import combinations,product
from pathlib import Path
import hashlib,json,random,sys
from rank_reward_tail import scores,tails


def matching(p,u,stats,rightmost=False):
 n=len(p);m=len(u);c=2*m+1;S=[[None]*(n+1) for _ in range(n+1)];R={}
 for i in range(n-c+1):
  prev=[None]*(m+1);prev[0]=0;older=prev.copy();paths=[None]*(m+1);paths[0]=();oldpaths=paths.copy()
  for j in range(i+3,n+1):
   cur=prev.copy();newpaths=paths.copy();x=j-2
   for r in range(1,m+1):
    stats['rank_matching_transitions']+=1
    if older[r-1] is None:continue
    value=older[r-1]+p[x]*u[r-1];path=oldpaths[r-1]+(x,)
    if cur[r] is None or value>cur[r] or (value==cur[r] and ((path>newpaths[r]) if rightmost else (path<newpaths[r]))):cur[r]=value;newpaths[r]=path
   older,prev=prev,cur;oldpaths,paths=paths,newpaths
   if j-i>=c:S[i][j]=prev[m];R[i,j]=paths[m];stats['matching_scores']+=1
 return S,R


def repair(p,u,i,j,chosen,stats):
 score=lambda q:sum(p[x]*u[r] for r,x in enumerate(q))
 old=score(chosen);m=len(u);c=2*m+1;d=j-i-c
 if i+1 not in chosen:return old,[],dict(first=0,retained=0,removed=0,added=0)
 remaining=set(chosen)-{i+1};covered={v for x in remaining for v in (x,x+1)};free=[x for x in range(i+2,j) if x not in covered];assert len(free)==d+1
 best=-1;winning=None;rows=[]
 oldr={x:r for r,x in enumerate(chosen)}
 for a,b in zip(free,free[1:]):
  gone=set(range(a+1,b,2));added=set(range(a,b,2));assert gone<=remaining
  candidate=tuple(sorted((remaining-gone)|added));assert len(candidate)==m and all(y-x>=2 for x,y in zip(candidate,candidate[1:]))
  newr={x:r for r,x in enumerate(candidate)}
  parts=dict(first=p[i+1]*u[0],retained=sum(p[x]*(u[oldr[x]]-u[newr[x]]) for x in remaining-gone),removed=sum(p[x]*u[oldr[x]] for x in gone),added=sum(p[x]*u[newr[x]] for x in added))
  value=score(candidate);assert old-value==parts['first']+parts['retained']+parts['removed']-parts['added'];assert value<=old
  rows.append(dict(a=a,b=b,matching=candidate,score=value,parts=parts));stats['rank_repair_paths']+=1
  if value>best:best=value;winning=parts
 return best,rows,winning


def evaluate(p,h,t,stats,controls=False,rightmost=False):
 n=len(p);c=2**h-1;m=(c-1)//2;u=[min(1+(r&-r).bit_length()-1,t) for r in range(1,m+1)];v=[min((r&-r).bit_length()-1,t) for r in range(1,c+1)]
 S,R=matching(p,u,stats,rightmost)
 if controls:
  Q,_=scores(p,v,stats);assert S==Q;stats['independent_vectors']+=1
 T=tails(S,c,stats);loss={};firstfailure=None;maxlocal=None
 for i in range(n-c):
  for j in range(i+c+1,n+1):
   value,paths,parts=repair(p,u,i,j,R[i,j],stats);L=S[i][j]-value;delta=S[i][j]-S[i+1][j];assert L>=delta>=0;stats['endpoint_checks']+=1;loss[i,j]=L
   if L>delta:
    stats['strict_repair_losses']+=1
    row=dict(n=n,h=h,t=t,p=p.copy(),i=i,j=j,d=j-i-c,old=S[i][j],short=S[i+1][j],chosen=R[i,j],short_chosen=R[i+1,j],repair_best=value,paths=paths)
    if firstfailure is None:firstfailure=row
    if maxlocal is None or L-delta>maxlocal['old']-maxlocal['repair_best']-(maxlocal['old']-maxlocal['short']):maxlocal=row
 P=sum(p);best=None;gapbest=None
 for d in range(1,n-c):
  k=c+d;b=n-k;B=sum(loss[i,i+k] for i in range(b))+S[b][n]-S[0][n];assert B>=T[d];stats['global_repair_bounds']+=1
  if P:
   ratio=Fraction(B*d,P*(t*d+c+1));gapratio=Fraction((B-T[d])*d,P*(t*d+c+1));row=dict(n=n,h=h,t=t,d=d,P=P,p=p.copy(),repair_bound=B,actual_tail=T[d],ratio=[ratio.numerator,ratio.denominator],gap_ratio=[gapratio.numerator,gapratio.denominator])
   if best is None or ratio>Fraction(*best['ratio']):best=row
   if gapbest is None or gapratio>Fraction(*gapbest['gap_ratio']):gapbest=row
 stats['inputs']+=1
 return best,gapbest,firstfailure,maxlocal


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(36021);first=None;worst=None;best=None;gapbest=None;rows=[];rightmost='--rightmost' in sys.argv
 def consider(p,h,t,controls=False):
  nonlocal first,worst,best,gapbest
  a,b,f,g=evaluate(p,h,t,stats,controls,rightmost)
  if f is not None and first is None:first=f;print('first strict repair',json.dumps(f),flush=True)
  if g is not None and (worst is None or g['short']-g['repair_best']>worst['short']-worst['repair_best']):worst=g
  if a and (best is None or Fraction(*a['ratio'])>Fraction(*best['ratio'])):best=a
  if b and (gapbest is None or Fraction(*b['gap_ratio'])>Fraction(*gapbest['gap_ratio'])):gapbest=b
 for q in product(range(3),repeat=8):consider([0]+list(q)+[0],3,2,True)
 for n in (16,32,64):
  h=n.bit_length()-2;c=2**h-1
  fixtures=[[1]*n,[i+1 for i in range(n)],[n-i for i in range(n)],[int(i%2==0) for i in range(n)]]
  for step in (3,4,5,7,8,9):fixtures.append([int(i%step==0) for i in range(n)])
  for block in (2,4,8):fixtures.append([int((i+i//block)%2==0) for i in range(n)])
  for _ in range(35):fixtures.append([rng.randrange(9) for _ in range(n)])
  for _ in range(35):
   p=[0]*n
   for z in range(rng.randint(1,8)):p[rng.randrange(n)]+=rng.randint(1,9)
   fixtures.append(p)
  for t in sorted({1,2,h-1}):
   if t>h-1:continue
   for p in fixtures:consider(p,h,t,n<=32)
  rows.append(dict(n=n,best=best,gapbest=gapbest));print('size',n,'best',best['ratio'],'gap',gapbest['gap_ratio'],flush=True)
 files=('rank_matching_repair.py','rank_reward_tail.py','aggregate_core_audit.py')
 result=dict(scope='Exact accounting diagnostic for canonical endpoint augmentations; repair bounds are upper certificates, not assumed optimal or asymptotically bounded.',seed=36021,canonical='rightmost' if rightmost else 'leftmost',checks=stats,first_failure=first,worst_local=worst,best_global=best,best_excess=gapbest,rows=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results'/('rightmost_rank_repair.json' if rightmost else 'rank_matching_repair.json')).write_text(json.dumps(result,indent=2)+'\n');print('complete',dict(stats),flush=True)
if __name__=='__main__':main()
