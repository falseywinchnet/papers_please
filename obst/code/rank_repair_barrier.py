#!/usr/bin/env python3
"""Audit rightmost zero-loss compatibility and exact augmentation barriers."""
from collections import Counter
from itertools import combinations,product
from pathlib import Path
import hashlib,json,random
from rank_matching_repair import matching,repair
from rank_reward_tail import scores,tails


def scalar(p,u,i,j,stats):
 m=len(u);prev=[None]*(m+1);prev[0]=0;older=prev.copy();paths=[None]*(m+1);paths[0]=();oldpaths=paths.copy()
 for x in range(i+1,j-1):
  cur=prev.copy();newpaths=paths.copy()
  for r in range(1,m+1):
   stats['scalar_transitions']+=1
   if older[r-1] is None:continue
   value=older[r-1]+p[x]*u[r-1];path=oldpaths[r-1]+(x,)
   if cur[r] is None or value>cur[r] or (value==cur[r] and path>newpaths[r]):cur[r]=value;newpaths[r]=path
  older,prev=prev,cur;oldpaths,paths=paths,newpaths
 return prev[m],paths[m]


def main():
 root=Path(__file__).resolve().parents[1];stats=Counter();rng=random.Random(36219);rows=[]
 fixtures=[[0]+list(q)+[0] for q in product((0,1),repeat=8)]
 fixtures += [[rng.randrange(6) for _ in range(16)] for _ in range(50)]
 for p in fixtures:
  S,R=matching(p,[1,2,1],stats,True);n=len(p)
  for i in range(n-7):
   for j in range(i+8,n+1):
    zero=S[i][j]==S[i+1][j]
    assert zero==(R[i,j][0]>i+1);stats['zero_loss_equivalences']+=1
 for B in list(range(1,13))+[2**r for r in (8,16,32,64)]:
  p=[0]*10;p[2]=p[3]=2*B;p[4]=B;p[6]=2*B-1;u=[1,2,1]
  options=[a for a in combinations(range(2,9),3) if all(y-x>=2 for x,y in zip(a,a[1:]))]
  values=[sum(p[x]*u[r] for r,x in enumerate(a)) for a in options];assert len(options)==10
  top=max(values);assert [a for a,v in zip(options,values) if v==top]==[(2,4,6)];assert top==6*B-1
  short,path=scalar(p,u,2,10,stats);assert short==6*B-2 and path==(3,6,8)
  best,paths,_=repair(p,u,1,10,(2,4,6),stats);assert best==5*B-2 and sorted(a['score'] for a in paths)==[2*B,5*B-2]
  S,_=scores(p,[0,1,0,2,0,1,0],stats);assert (S[1][10],S[2][10])==(top,short)
  stats['unique_optimum_families']+=1;stats['literal_matchings']+=len(options)
 for h in range(3,11):
  C=2**h;c=C-1;m=(c-1)//2;n=4*C;d=C;k=c+d;b=n-k;x=C//2+1;t=h-1
  p=[0]*n;p[x]=1;u=[(r&-r).bit_length() for r in range(1,m+1)]
  total=0;active=[]
  for i in range(b):
   j=i+k
   if i<x:
    upper=min(m,(x-i+1)//2);r=1<<(upper.bit_length()-1)
    chosen=tuple([x-2*(r-s) for s in range(1,r+1)]+[j-2-2*(m-s) for s in range(r+1,m+1)])
    value=u[r-1]
   else:
    chosen=tuple(j-2-2*(m-s) for s in range(1,m+1));value=0;r=None
   assert len(chosen)==m and all(z-y>=2 for y,z in zip(chosen,chosen[1:]));assert chosen[0]>=i+1 and chosen[-1]<=j-2
   assert sum(p[z]*u[q] for q,z in enumerate(chosen))==value;stats['formula_witnesses']+=1
   check=h<=5 or i in {0,b-1} or any(abs(i-(x-2**s+1))<=1 for s in range(1,h))
   if check:
    got,path=scalar(p,u,i,j,stats);assert (got,path)==(value,chosen);stats['scalar_witness_controls']+=1
   best,paths,_=repair(p,u,i,j,chosen,stats);loss=value-best;total+=loss
   expected=0 if chosen[0]>i+1 else (1 if r==1 else value-1)
   assert loss==expected;stats['repair_loss_formulas']+=1
   if loss:
    active.append(dict(i=i,rank=r,score=value,repair_loss=loss))
    if h==3 or (h==4 and r==C//4):
     prefix=chosen[:r];opts=[]
     for suffix in combinations(range(x+2,j-1),m-r):
      if any(z-y<2 for y,z in zip(suffix,suffix[1:])):continue
      alternative=prefix+suffix;assert sum(p[z]*u[q] for q,z in enumerate(alternative))==value
      got,_,_=repair(p,u,i,j,alternative,stats);assert value-got==loss
      opts.append(alternative);stats['all_optimal_repair_checks']+=1
     if h==3:
      literal=[a for a in combinations(range(i+1,j-1),m) if all(z-y>=2 for y,z in zip(a,a[1:])) and sum(p[z]*u[q] for q,z in enumerate(a))==value]
      assert set(literal)==set(opts);stats['literal_optimal_matching_sets']+=1

  # Root threshold: an optimum needs exactly C/8 augmenting components.
  i=2;j=i+k;r=C//4
  chosen=tuple([x-2*(r-s) for s in range(1,r+1)]+[j-2-2*(m-s) for s in range(r+1,m+1)])
  remaining=set(chosen[1:])
  new=tuple(sorted(chosen[r//2:r]+chosen[r:]+tuple(range(x+2,x+r+1,2))))
  assert len(new)==m and all(z-y>=2 for y,z in zip(new,new[1:]))
  assert new[0]>=i+2 and new[-1]<=j-2 and new.index(x)+1==r//2
  assert sum(p[z]*u[q] for q,z in enumerate(new))==h-2
  added=set(new)-remaining;removed=remaining-set(new)
  assert len(added)==C//8 and len(removed)==C//8-1
  symmetric=sorted(added|removed)
  assert all(z-y>=2 for y,z in zip(symmetric,symmetric[1:]))
  assert len([z for z in remaining if z<x])-len([z for z in new if z<x])==C//8-1
  stats['many_component_constructions']+=1
  full,fullpath=scalar(p,u,0,n,stats);end,endpath=scalar(p,u,b,n,stats)
  assert (full,end)==(h-1,0);certificate=total+end-full;assert certificate==(h-2)*(h-3)//2;stats['global_certificate_formulas']+=1
  if h<=5:
   S,_=scores(p,[(r&-r).bit_length()-1 for r in range(1,C)],stats);T=tails(S,c,stats);assert T[d]==0;stats['independent_zero_tails']+=1
  rows.append(dict(h=h,C=C,n=n,x=x,d=d,P=1,t=t,repair_certificate=certificate,actual_tail=0,minimum_augmenting_components=C//8,minimum_deaugmenting_components=C//8-1,active=active,verification='explicit witnesses and repairs; scalar DP controls; full generic tail through h=5'))
  print('height',h,'certificate',certificate,'actual tail 0',flush=True)
 for h in (16,32,64,128):rows.append(dict(h=h,C=2**h,n=2**(h+2),d=2**h,repair_certificate=(h-2)*(h-3)//2,actual_tail=0,minimum_augmenting_components=2**(h-3),minimum_deaugmenting_components=2**(h-3)-1,verification='proved formula only'))
 files=('rank_repair_barrier.py','rank_matching_repair.py','rank_reward_tail.py','aggregate_core_audit.py')
 result=dict(scope='Rightmost zero-loss equivalence, unique-optimum local repair gap, and a single-key quadratic-in-height best one-augmentation certificate despite zero true tail, attained by rightmost starts; an optimal root-threshold repair needs exactly C/8 augmenting and C/8-1 deaugmenting components. These obstruct the one-augmentation certificate, not the actual tail bound or general OBST algorithms.',seed=36219,checks=stats,one_key_family=rows,source_sha256={f:hashlib.sha256((root/'code'/f).read_bytes()).hexdigest() for f in files})
 (root/'results/rank_repair_barrier.json').write_text(json.dumps(result,indent=2)+'\n');print(dict(stats),flush=True)
if __name__=='__main__':main()
